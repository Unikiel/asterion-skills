#!/usr/bin/env python3
"""Arbitrary trip-date periods, date coverage and English publication filenames."""
from datetime import date, timedelta
import re


def trip_periods(request):
    periods = request.get('date_ranges')
    if periods is None:
        periods = [{'start_date':request.get('start_date'), 'end_date':request.get('end_date')}]
    if not isinstance(periods, list) or not periods:
        raise ValueError('date_ranges must be a nonempty list of date periods')
    parsed=[]
    for i, item in enumerate(periods):
        if not isinstance(item, dict): raise ValueError(f'date_ranges[{i}] must be an object')
        try:
            start=date.fromisoformat(item['start_date']); end=date.fromisoformat(item['end_date'])
        except (KeyError, TypeError, ValueError) as ex:
            raise ValueError(f'date_ranges[{i}] needs valid start_date and end_date') from ex
        if start>end: raise ValueError(f'date_ranges[{i}] start_date cannot be later than end_date')
        parsed.append((start,end,dict(item)))
    parsed.sort(key=lambda item:(item[0],item[1]))
    for prev, following in zip(parsed,parsed[1:]):
        if following[0]<=prev[1]: raise ValueError('date_ranges cannot overlap or repeat dates')
    # Keep adjacent segments distinct; never bridge gaps or collapse user periods.
    return [{**item,'start_date':start.isoformat(),'end_date':end.isoformat()} for start,end,item in parsed]


def normalize_trip_dates(request):
    periods=trip_periods(request)
    first,last=periods[0]['start_date'],periods[-1]['end_date']
    if request.get('date_ranges') is not None:
        if request.get('start_date') and request['start_date']!=first: raise ValueError('start_date conflicts with date_ranges envelope')
        if request.get('end_date') and request['end_date']!=last: raise ValueError('end_date conflicts with date_ranges envelope')
    request['date_ranges']=periods
    request['start_date']=first;request['end_date']=last
    return request


def trip_days(request):
    for period in trip_periods(request):
        current=date.fromisoformat(period['start_date']);end=date.fromisoformat(period['end_date'])
        while current<=end:
            yield current
            current+=timedelta(days=1)


def display_trip_dates(request):
    return '\n'.join(f"{date.fromisoformat(p['start_date']):%Y.%m.%d} – {date.fromisoformat(p['end_date']):%Y.%m.%d}" for p in trip_periods(request))


def english_component(request, key):
    value=request.get(key+'_en') or request.get(key)
    if not isinstance(value,str) or not value.strip() or not value.isascii() or not re.search(r'[A-Za-z]',value):
        raise ValueError(f'Publication needs verified English {key}_en; enrich request from source research, not a new traveler requirement')
    component=re.sub(r'[^A-Za-z0-9]+','-',value.strip()).strip('-')
    if not component: raise ValueError(f'Invalid English {key} filename component')
    return component


def publication_stem(request):
    periods=trip_periods(request)
    years=sorted({d.year for p in periods for d in (date.fromisoformat(p['start_date']),date.fromisoformat(p['end_date']))})
    country=english_component(request,'country'); city=english_component(request,'destination')
    prefix=str(years[0]) if len(years)==1 else f'{years[0]}-{years[-1]}'
    pattern='%m%d' if len(years)==1 else '%Y%m%d'
    ranges=['-'.join(date.fromisoformat(p[k]).strftime(pattern) for k in ('start_date','end_date')) for p in periods]
    return '.'.join([prefix,country,city,*ranges])


def audit_schedule_periods(text, request):
    """Reject explicitly headed gap-day schedules and duplicate dated day headings."""
    import re
    from reader_qa import section
    block=section(text,'Schedule')
    active={d.isoformat() for d in trip_days(request)}; seen=set(); errors=[]
    for heading in re.findall(r'^#{3,6}\s+([^\n]+)',block,re.M):
        # Period grouping headings may contain two endpoints; those are not day cards.
        dates=re.findall(r'\d{4}-\d{2}-\d{2}',heading)
        if len(dates)!=1 or not re.match(r'^\d{4}-\d{2}-\d{2}(?:\s|$)',heading): continue
        day=dates[0]
        if day not in active: errors.append(f'Schedule contains excluded gap/non-trip day: {day}')
        if day in seen: errors.append(f'Schedule repeats day heading: {day}')
        seen.add(day)
    return errors
