# Phase 3 — Full individual attraction catalogue + qualified Around Area excursions

Read all prior phases and the Around Area contract and itinerary engine. Use official/local source research and nearby maps. Write a detailed `research/03_attractions_and_around_area.md`.

A. **Primary destination**: research a broad catalogue spanning central areas and outer districts, not just planned day's stops. For each actual named place include localized official name, relevant historical/architectural/cultural reason, location, typical visit duration, opening windows/closed dates where sourceable, fare when sourceable, access via rail/bus + nearby station, reservation notes, seasonal/weather notes and photography. Include sites suitable for user's explicit interests. Mark missing live facts precisely (do not fill placeholders). Do not duplicate major landmarks under multiple categories.
B. **Area maps**: create an annotated geographic grouping Map A / Map B / ... with named neighborhoods, ground locators (station/address), and links to verified map or directions sources; if local tools can render actual maps, generate assets/maps and reference them. Never claim a map exists when it doesn't.
C. **Around Area** is *a different locality visited on a one-day round trip from the principal city/base, returning same calendar day*. Each candidate must include outbound route and realistic departure, on-site visits/time, return service/window, total travel burden and contingency. Classify recommended / possible with constraints / rejected (overnight). Do not use the principal city as Around Area subheading; never imply nearby simply means one-direction journey time is short. Inspect last trains and seasonality.
D. Special Tours (themes, events, festivals, seasonal strolls, accessible photo routes) separately from Around Area city excursions.

Scale catalogue to destination complexity: major Japanese metro often dozens of detailed sites, multiple districts and multiple vetted day trips. Source all practical data with URL+access date in evidence ledger.


## 必须遵守：输入语言无关＋多语言目的地标签＋老攻略版式

允许用户用任何语言调用，不可要求英文 Prompt。输出正文按 `request.json` 的 `customization.language`（默认 zh-CN）；对所有重要地名/景点/车站/线路/酒店/餐厅逐条提供中文/英文名称，日本目的地额外提供日文原名、可靠的假名及 Hepburn 罗马字，并制作供问路时展示的名称卡。执行 `references/multilingual_names_and_pronunciation.md`。封面、页眉、页脚及三级页码目录以三份历史攻略的出版版式为准，但严禁引用原攻略的旧事实、旧景点清单和旧票价代替本次独立研究；执行 `references/legacy_layout_contract.md`。正文与路线必须含这些名称而不能只放附录。


**Additional mandatory index:** write `research/NAME_INDEX.md` as a structured all-major-places index, one row for each venue/destination/station/interchange/route (including the main city and each Around Area). Columns: category; 中文名; English name (official or explanatory); local native name; Japanese kana/other verified phonetic reading; romaji/transliteration; location/short address; source URL; verification status. Every name included in the brochure must be consistently represented, no guessed reading.
