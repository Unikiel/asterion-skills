# Phase 5 — Concrete date-aware itinerary with validated logistics

Read request.json, every research/*.md completed so far and all source guidance. Write `research/05_day_by_day_itinerary.md` using actual outward/return travel legs in `journey`, regardless of mode, as first/last-day anchors.

Build:
1. An overview with primary base/hotel proposal vs booked hotel status, map-area legend, daily timeline and ranked must-sees from user customization.
2. Detailed daily plan for **every inclusive travel date**, with times or transparent estimates, travel mode and transfers, stops with meaningful onsite durations, meal and coffee anchors, rest/walking buffers, and return to lodging. Distinguish optional stops. Avoid stacking physically remote areas or excessive walking if user limits it.
3. Respect real closed weekdays, seasonal operating windows and reservation lead times. Do not make a hard-time claim unsupported by source. For attractions requiring entry reservations, provide booking site and mark unbooked.
4. Include bad-weather alternative per day, avoiding long walks when user requests short walking. Recommend qualified Around Area excursions if feasible but keep them optional unless user specified.
5. For arrival and departure, explicitly budget the ACTUAL journey: immigration/security and airport lead time only for relevant international flight segments; railway interchange/platform time for trains, boarding deadlines for ferries/buses, driving or road delays where relevant, plus luggage and hotel check-in. If terminal details are unclear, say exactly what requires reconfirmation.
6. Provide a transit cost comparison where sourced; list useful route/official timetable URLs. Check that no service/route or date conflict exists.

Append any new sources to ledger. End with a practical prioritized reservation/verification checklist—not blank planning questions.


## 必须遵守：输入语言无关＋多语言目的地标签＋老攻略版式

允许用户用任何语言调用，不可要求英文 Prompt。输出正文按 `request.json` 的 `customization.language`（默认 zh-CN）；对所有重要地名/景点/车站/线路/酒店/餐厅逐条提供中文/英文名称，日本目的地额外提供日文原名、可靠的假名及 Hepburn 罗马字，并制作供问路时展示的名称卡。执行 `references/multilingual_names_and_pronunciation.md`。封面、页眉、页脚及三级页码目录以三份历史攻略的出版版式为准，但严禁引用原攻略的旧事实、旧景点清单和旧票价代替本次独立研究；执行 `references/legacy_layout_contract.md`。正文与路线必须含这些名称而不能只放附录。


Honor the explicitly supplied hotel address/name if present. Do not invent a new hotel base. Include cross-checked real area map images; photo-ready timetables, transit diagrams and physical documents are not replaceable with URLs.