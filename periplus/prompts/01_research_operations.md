# Phase 1 — Research actual outbound/return transportation, lodging and arrival/departure logistics

Read `request.json`, `PROJECT.md`, installed Periplus SKILL and source rules. Automatically search fresh, primary sources, do not merely restate request.

1. Preserve `journey.outbound.origin` as the true journey START and `journey.return.destination` as the true journey END. They need not match, and may be different countries; never replace the final return endpoint with the outbound origin. Resolve the user’s actual `journey.outbound` and `journey.return` mode(s) FOR THE APPLICABLE DATE: flight numbers/airport terminals when flying; railway/train/platforms when by rail; bus stops, ferry ports, road routing or multimodal transfer details as appropriate. Validate service/route numbers where given and respect user-supplied reservation status; never assume flying. Handle arrival-date shifts and local timezones.
2. Research actual arrival terminal/station/port/parking → main-destination hotel/base (and reverse), with actual operators, fare bands, boarding stations, likely transfer, earliest/last service, walking/exits, and weather/luggage contingencies. Do not assert live timetables based solely on general route articles.
3. If `request.hotel` is supplied, research and honor its actual location, check-in/check-out, local spelling and access. Only if there is no supplied hotel, compare 2–3 logical neighborhoods and 2–3 accommodation choices without invented prices or availability; choose tentative best base for day-trip planning. Do not claim any reservation.
4. Research relevant travel restrictions, holiday and seasonal factors for the date window, and record operational sources and access dates.
5. Save detailed evidence-backed prose to `research/01_operations.md` (minimum 1200 meaningful Chinese characters or equivalent, unless actual destination is extremely constrained). Write timestamped URL entries into `research/EVIDENCE_LEDGER.md`. Keep source links near claims in notes.
6. If online research capability is unavailable, write `research/RESEARCH_BLOCKER.md` specifying which capability must be enabled and DO NOT invent facts. Do not mark phase complete when blocked.

Required deliverable this phase: `research/01_operations.md` containing actual outbound/return mode and service facts, reservation status, door-to-door options, supplied hotel details or clearly unbooked alternatives, and citations.


## 必须遵守：输入语言无关＋多语言目的地标签＋老攻略版式

允许用户用任何语言调用，不可要求英文 Prompt。输出正文按 `request.json` 的 `customization.language`（默认 zh-CN）；对所有重要地名/景点/车站/线路/酒店/餐厅逐条提供中文/英文名称，日本目的地额外提供日文原名、可靠的假名及 Hepburn 罗马字，并制作供问路时展示的名称卡。执行 `references/multilingual_names_and_pronunciation.md`。封面、页眉、页脚及三级页码目录以三份历史攻略的出版版式为准，但严禁引用原攻略的旧事实、旧景点清单和旧票价代替本次独立研究；执行 `references/legacy_layout_contract.md`。正文与路线必须含这些名称而不能只放附录。


### Permanent v2.4 travel and visuals requirements

Read `request.journey.outbound/return` (modes may be flight, rail, bus, ferry, drive, mixed, other) and `request.hotel` when supplied. Do not assume flights or airports. Identify arrival/departure terminals/vehicles/road nodes appropriate to the actual modes; include accurate hotel transfer instructions. Open `references/media_acquisition_and_maps.md`; research legally reusable real photographic sources and real map assets, with provenance and image rights. Start `research/MEDIA_MANIFEST.json`, downloads into `photos/` / `maps/` during normal execution.