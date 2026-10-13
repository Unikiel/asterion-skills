# Phase 2 — Build encyclopedic Brief Sketch

Read request, research/01_operations.md, all coverage and content specifications in the installed skill. Search authoritative sources; no filler or skeletal bullet-only text.

Write `research/02_destination_compendium.md` as a real substantial chapter of the finished guide. Keep meaningful hierarchy:
- Brief Sketch with city orientation and destination boundaries;
- History (organized by meaningful eras and dated inflection points);
- Geography / Administrative Region / Climate / Population / Religion / Politics;
- Economy (primary/secondary/tertiary industries) / Education;
- Culture, Language & Dialect, Localism, Travel, Literature & Art, Art & Craft, Architecture, Museum, Events & Festivals, Delicacy & Diet & Cuisine, Media, Sports, Subculture;
- Transportation: national and local rail, metro, buses, roads/highway, ports/ferries, airports and international exchange when pertinent.

Use actual names, substantive history/background, meaningful context, contemporary corrections, relevant photo/architecture/museum knowledge. Organize on the template taxonomy and make cross references. Look beyond the user's chosen short itinerary—the brochure doubles as a reference encyclopedia. Avoid stale political incumbents and unsupported rankings. Every time-sensitive statistic is dated and sourced. Append source URLs + retrieval dates to `research/EVIDENCE_LEDGER.md`. Target high detail (several thousand Chinese characters). Preserve all relevant categories; for nonexistent facilities say why.

Required output: `research/02_destination_compendium.md`; not a table of contents.


## 必须遵守：输入语言无关＋多语言目的地标签＋老攻略版式

允许用户用任何语言调用，不可要求英文 Prompt。输出正文按 `request.json` 的 `customization.language`（默认 zh-CN）；对所有重要地名/景点/车站/线路/酒店/餐厅逐条提供中文/英文名称，日本目的地额外提供日文原名、可靠的假名及 Hepburn 罗马字，并制作供问路时展示的名称卡。执行 `references/multilingual_names_and_pronunciation.md`。封面、页眉、页脚及三级页码目录以三份历史攻略的出版版式为准，但严禁引用原攻略的旧事实、旧景点清单和旧票价代替本次独立研究；执行 `references/legacy_layout_contract.md`。正文与路线必须含这些名称而不能只放附录。
