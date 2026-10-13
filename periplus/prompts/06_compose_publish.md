# Phase 6 — Write the ACTUAL finished Seven Ninths Travel Brochure

This is a full-writing phase, not a scaffold phase. Read all existing research files and the full Seven Ninths master structure. Compose `exports/Seven_Ninths_Travel_Brochure.md` as a polished, publication-ready, continuous, comprehensive travel guide in the requested language.

Preserve all top-level sections, in order:
1. Do NOT manually author a cover or Content/TOC in the Markdown manuscript: the DOCX/PDF exporter creates the legacy cover and a real three-level page-numbered clickable Content section;
2. Arrival & Departure (both flights and actual airport access);
3. Accommodation (booked or clearly recommended);
4. Brief Sketch (full researched country/city history, geography, population, politics, economy, education, language, culture, transport, etc);
5. Attractions & Schedule (Area Maps and every travel date schedule);
6. Sightseeing & Adventure (detailed primary destination catalogue, qualified Around Area day trips, Tours);
7. Delicacy & Shopping (restaurants/cafés and markets/stores);
8. Recommends & Tips (Tourist Travel Pass & Ticket, Tourist Center, Tickets & Prices, Practical Information, Currency, Embassy, Important Numbers, Useful links);
9. Source bibliography and any discreet dated verification caveats.

DO NOT just copy the master skeleton into the published output! Remove all bracket placeholders, TODOs, instructional metadata and dummy lists. Write actual factual paragraphs for every applicable chapter, tables only for genuinely tabular material, and complete substantive entries for each recommended attraction, dining/retail venue and excursion. Retain Japanese/local names. Provide source links with time-sensitive claims; do not invent a map or photo, instead link grounded map services if actual assets absent.

This should read like the user's substantial Nagoya/Kobe/Tokyo compendia, not a thin one-page itinerary. For large destinations, draft over multiple writing passes to avoid truncation—preserve and extend existing prose rather than leaving sections empty. Never mark brochure complete simply because the file exists.

After writing, create `research/QUALITY_REPORT.md` with completeness-by-section, source/freshness audit, explicit limitations and outstanding booking checks. Set project status to `DRAFT_REVIEW` until Phase 7 succeeds. DOCX and PDF are mandatory default publication outputs. Finish the substantive Markdown manuscript first; after Phase 7 the runner calls export_brochure.py and checks the brand header on every page. Never treat Markdown as the default deliverable or claim output without rendering.


## 必须遵守：输入语言无关＋多语言目的地标签＋老攻略版式

允许用户用任何语言调用，不可要求英文 Prompt。输出正文按 `request.json` 的 `customization.language`（默认 zh-CN）；对所有重要地名/景点/车站/线路/酒店/餐厅逐条提供中文/英文名称，日本目的地额外提供日文原名、可靠的假名及 Hepburn 罗马字，并制作供问路时展示的名称卡。执行 `references/multilingual_names_and_pronunciation.md`。封面、页眉、页脚及三级页码目录以三份历史攻略的出版版式为准，但严禁引用原攻略的旧事实、旧景点清单和旧票价代替本次独立研究；执行 `references/legacy_layout_contract.md`。正文与路线必须含这些名称而不能只放附录。


**Before publication:** read `research/NAME_INDEX.md`, expand the names within the body itself (not only in an appendix); provide usable local-language show-to-staff names and verified pronunciations.

### 版式交接约定

**Markdown 只写真实正文和章节标题**；不要输出 `# COVER`、`# Content`、手工目录、点引导线或页码，也不要复制 `assets` 里的模板占位符。`scripts/export_brochure.py` 会依据 `request.json` 自动生成封面及带页码的三级目录。正文中保留经过核实的多语言名称和读音，供出版器保持原样。
