#!/usr/bin/env python3
"""Narrow editorial regression checks and date-aware connection arithmetic.
Facts, inventory completeness and buffer adequacy still require source/visual review.
"""
import json
import re
from datetime import datetime, timedelta, date
from pathlib import Path


def section(text, title):
    match = re.search(r'^#{1,6}\s+' + re.escape(title) + r'[^\n]*\n', text, re.M | re.I)
    if not match:
        return ''
    level = len(match.group(0)) - len(match.group(0).lstrip('#'))
    tail = text[match.end():]
    end = re.search(r'^#{1,' + str(level) + r'}\s+', tail, re.M)
    return tail[:end.start()] if end else tail


def audit_reader_text(text, request):
    errors = []
    # Only narrow policy/process phrases; legitimate logistical explanations remain allowed.
    patterns = [r'(?:\u672c\u624b\u518c|\u672c\u653b\u7565|\u672c\u518c|\u6280\u80fd|skill)\s*(?:\u8981\u6c42|\u89c4\u5b9a|\u5fc5\u987b)[^。\n]*(?:Around Area|\u4e00\u65e5\u5f80\u8fd4|\u540c\u65e5\u5f80\u8fd4|\u56fe\u7247|\u7167\u7247|\u76ee\u5f55)',
                r'\u4e3a(?:\u4e86)?\u6ee1\u8db3(?:\u672c\u624b\u518c|\u672c\u653b\u7565|\u6280\u80fd|skill)', r'\u672c(?:\u518c|\u624b\u518c)\u53ea(?:\u8003\u8651|\u6536\u5f55)[^。\n]*(?:\u5f80\u8fd4|\u5468\u8fb9)',
                r'(?<!\w)(?:DRAFT_REVIEW|RESEARCH-COMPLETE|Day-trip qualification)\b']
    for pattern in patterns:
        if re.search(pattern, text, re.I):
            errors.append('Internal planning/policy narration appears in reader prose: ' + pattern)
    around = section(text, 'Around Area')
    if re.search(r'^###\s+[^\n]*(?:\u4e00\u65e5\u5f80\u8fd4|\u5f53\u65e5\u5f80\u8fd4|\u540c\u65e5\u5f80\u8fd4|one.day round.trip|same.day round.trip)', around, re.M | re.I):
        errors.append('Around Area titles repeat round-trip labels; use destination names')
    tickets = section(text, 'Tickets & Prices')
    if re.search(r'(?:\u9884\u7b97|\u4eba\u5747\u603b(?:\u4ef7|\u8d39\u7528)|\u603b\u5f00\u9500|\u6bcf\u65e5\u5f00\u652f|trip budget|daily spending|estimated total)', tickets, re.I):
        errors.append('Tickets & Prices contains a budget; use passes, combination tickets and discounts')
    return errors


def aware_datetime(value):
    if not isinstance(value, str):
        raise ValueError('ISO datetime with UTC offset required')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.utcoffset() is None:
        raise ValueError('UTC offset required')
    return result


def audit_transport_plan(project, text, request):
    path = Path(project) / 'research/TRANSPORT_PLAN.json'
    try:
        data = json.loads(path.read_text(encoding='utf8'))
    except (OSError, ValueError) as ex:
        return [f'Missing/invalid research/TRANSPORT_PLAN.json: {ex}']
    if not isinstance(data, dict) or not isinstance(data.get('legs'), list) or not data['legs']:
        return ['TRANSPORT_PLAN requires nonempty legs']
    errors = []; roles = set(); ids = set()
    for leg in data['legs']:
        if not isinstance(leg, dict):
            errors.append('Transport leg must be an object'); continue
        tag = str(leg.get('id', '?'))
        for k in ('id', 'role', 'mode', 'origin', 'destination', 'operator', 'status', 'checked_on'):
            if not isinstance(leg.get(k), str) or not leg[k].strip():
                errors.append(f'Transport {tag} missing {k}')
        if tag in ids: errors.append(f'Duplicate transport id: {tag}')
        ids.add(tag); roles.add(leg.get('role'))
        if leg.get('role') not in ('outbound', 'return', 'transfer'):
            errors.append(f'Transport {tag} invalid role')
        if leg.get('mode') not in ('flight', 'rail', 'bus', 'ferry', 'drive', 'taxi', 'walk', 'other'):
            errors.append(f'Transport {tag} invalid physical mode')
        try: date.fromisoformat(leg.get('checked_on', ''))
        except (ValueError, TypeError): errors.append(f'Transport {tag} invalid checked_on')
        urls = leg.get('source_urls')
        if not isinstance(urls, list) or not urls or any(not isinstance(u, str) or not (re.match(r'https?://', u) or (leg.get('status') == 'booked' and u == 'user-provided booking')) for u in urls):
            errors.append(f'Transport {tag} missing evidence sources')
        status = leg.get('status')
        if status not in ('booked', 'recommended', 'unreleased', 'historical_unavailable', 'continuous'):
            errors.append(f'Transport {tag} invalid status'); continue
        service = leg.get('service') or leg.get('route')
        if status in ('booked', 'recommended', 'continuous') and (not isinstance(service, str) or not service.strip()):
            errors.append(f'Transport {tag} needs actual service or route')
        if status in ('unreleased', 'historical_unavailable'):
            if not leg.get('limitation'): errors.append(f'Transport {tag} missing precise limitation')
            continue
        if status == 'continuous':
            if leg.get('mode') == 'flight': errors.append(f'Transport {tag} flight cannot be continuous')
            continue
        try:
            dep = aware_datetime(leg.get('departure')); arr = aware_datetime(leg.get('arrival'))
            if arr <= dep: errors.append(f'Transport {tag} arrival must follow departure')
        except (ValueError, TypeError) as ex:
            errors.append(f'Transport {tag} invalid departure/arrival: {ex}'); continue
        if isinstance(service, str) and service.casefold() not in text.casefold():
            errors.append(f'Recommended service absent from guide: {tag} / {service}')
        prior = leg.get('preceding')
        if leg.get('role') == 'transfer' and prior is None:
            errors.append(f'Transport {tag} transfer lacks preceding activity/arrival buffers')
        if prior is not None:
            if not isinstance(prior, dict):
                errors.append(f'Transport {tag} preceding must be an object'); continue
            try:
                end = aware_datetime(prior.get('ends_at'))
                values = prior.get('buffer_minutes')
                if not isinstance(values, dict) or not values or any(isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0 for v in values.values()):
                    raise ValueError('nonnegative process buffer_minutes required')
                if prior.get('type') == 'international_flight':
                    required = {'disembarkation', 'immigration', 'baggage', 'customs', 'terminal_transfer', 'ticketing_boarding', 'delay_reserve'}
                    if required - values.keys(): errors.append(f'Transport {tag} international arrival process buffers incomplete')
                if end + timedelta(minutes=sum(values.values())) > dep:
                    errors.append(f'Transport {tag} departs before preceding activity and connection buffers finish')
            except (ValueError, TypeError, OverflowError) as ex:
                errors.append(f'Transport {tag} invalid predecessor buffer: {ex}')
    for role in ('outbound', 'return'):
        if role not in roles: errors.append(f'Transport plan missing {role} journey')
    modes = data.get('considered_modes')
    if not isinstance(modes, list) or not modes:
        errors.append('Transport plan lacks researched multimodal alternatives')
    else:
        distinct = {option.get('mode') for option in modes if isinstance(option, dict) and isinstance(option.get('mode'), str)}
        if len(distinct) < 3 and not str(data.get('alternatives_limitation') or '').strip():
            errors.append('Fewer than three modes assessed: record a source-grounded alternatives_limitation when geography/user constraints restrict choices')
        for option in modes:
            if not isinstance(option, dict) or option.get('status') not in ('viable', 'excluded') or not all(isinstance(option.get(k), str) and option[k].strip() for k in ('mode', 'route', 'source_url', 'note')):
                errors.append('Multimodal option needs mode, status, route, source_url and note')
            elif not re.match(r'https?://', option['source_url']): errors.append('Multimodal option needs actual source URL')
    return errors
