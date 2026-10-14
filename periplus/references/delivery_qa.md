# QA and Release Gates

Do not label output **FINAL** unless it passes all relevant gates. The scripts enforce structural/procedural checks only; editorial and factual accuracy still require human/agent review and source validation.

## Structural gate

- [ ] `SKILL.md` frontmatter valid; all referenced resources exist.
- [ ] Cover identity, dates/place, real TOC, chapter order.
- [ ] Original main categories covered, including Tokyo-only and Kobe/Nagoya-only categories (or explicitly merged/NA in coverage log).
- [ ] `Sightseeing & Adventure` splits: Main Destination / Around Area / Tours.
- [ ] Canonical Around Area means **same-day out-and-back**; not a main-city alias.
- [ ] Regional maps A… correctly reference corresponding destinations and schedules.
- [ ] Arrival + departure, hotel + transport, food and shopping, passes and tourist offices, important numbers and links accounted for.

## Operational gate

- [ ] Incoming/return transit modes, terminals, station exits, real travel duration, realistic interchange and luggage allowances.
- [ ] `journey.outbound.origin` 明确为旅行起点、`journey.return.destination` 明确为最终返程落点；两者允许不同，不自动取相同值。
- [ ] Each Around Area entry independently has outbound and return route and enough visiting time, with same-day return verified if claimed.
- [ ] Venue hours/closure days and ticket prices are relevant to chosen dates and cited.
- [ ] Weather, disruption and alternative plans.
- [ ] No invented departure times, local maps, reservation links or live availability.

## Evidence gate

- [ ] User plans differentiated from real bookings.
- [ ] Historical sources not treated as up-to-date logistics.
- [ ] Provenance / checked dates stored in evidence ledger.
- [ ] Photographs/maps licensed or user-provided with appropriate attribution.
- [ ] Nothing sensitive copied from ticket/booking paperwork to publicly distributable example.

## Editorial gate

- [ ] No template markers (`[Attraction 1]`, TODO, TBD etc.) remaining in final publication.
- [ ] Proper local-language place names and unambiguous region/station identity.
- [ ] Descriptions informative, not repeated stock boilerplate.
- [ ] Source references functional; clear map/ticket/restaurant data.
- [ ] Date, time, currency symbols and units consistent.
- [ ] 默认 DOCX + PDF 已生成并分别检查。PDF 实际字体为 Oswald（英文字母、数字、封面、目录、页眉），DOCX 对应西文样式声明 Oswald；CJK 字符可读、无乱码。
- [ ] `PROJECT.md`/`TASKS.md` accurately reflect outstanding tasks and verified status.

## Release classification

- `SCAFFOLD`: an initialized file and task structure, NOT a finished guide.
- `DRAFT`: substantive content underway; unverified operational details explicitly labeled.
- `RESEARCH-COMPLETE`: content and ledger populated; must still pass review.
- `FINAL`: editorial and operational gates passed and deliverables verified. 

Never turn scaffold/draft validator success into a claim that train times or tickets are factually confirmed.


## 多语言标注与三级目录（固定要求）

用户请求语言不限，攻略默认简体中文。每个重要地点、景点、交通站和路线必须中文＋英文；日本还须含日文原名、假名发音及罗马字；不能核实的读音不得编造。参照 `multilingual_names_and_pronunciation.md`。最终 DOCX/PDF 的目录需 Heading 1–3、真实页码与可点击链接；参照 `legacy_layout_contract.md`。


## Four permanent operational gates

- [ ] Arrival & Departure reflect ACTUAL outbound + return modes; flight is optional. Rail/coach/ferry/driving/mixed segments must be properly planned.
- [ ] If `hotel` is supplied, brochure contains the exact provided name/address and hotel-to-terminal directions; if missing, recommendations are UNBOOKED.
- [ ] Actual licensed/source-backed photographs and actual geographic map images in both DOCX/PDF, not just hyperlinks. `MEDIA_MANIFEST.json` complete and physical DOCX/PDF image audit passed.
- [ ] Every Heading 1 and Heading 2 starts a new printed page; keep Heading 1 introduction substantial before the next Heading 2.
