# Phase 7 — Publication quality gate

Read `research/QUALITY_REPORT.md`, `request.json`, `exports/Seven_Ninths_Travel_Brochure.md`, and original source coverage matrix. Execute `python ABSOLUTE_SKILL_PATH/scripts/validate.py --project . --mode final` (resolve absolute Skill path from invocation). If failing, FIX the actual brochure/research immediately, then rerun. Do not evade validation by weakening requirements or deleting needed categories.

Check full itinerary date coverage, actual outbound/return mode-specific itineraries (not necessarily flights), lodging status, all main headings, real Around Area day-trip status, historical source vs current verified sources, enough genuine and unique named attractions, captions/maps source references, local names and no prompts/placeholders left. Check all departure and same-day-return time windows against verified dates where possible. When legitimate limitations remain (e.g. schedule not yet published), label them precisely and update `research/QUALITY_REPORT.md`.

Finish only after publication quality review. `project.json` may be set to `"release_status":"FINAL"` only if final audit passes. Maintain `TASKS.md` with real completion marks. The wrapper also runs local structural validation and must not print false success.


Release gate: default requested formats are DOCX and PDF, with running header `Seven Ninths Travel Brochure`. The execution wrapper performs the actual conversion after agent phases. Ensure text is complete before conversion.


## 必须遵守：输入语言无关＋多语言目的地标签＋老攻略版式

允许用户用任何语言调用，不可要求英文 Prompt。输出正文按 `request.json` 的 `customization.language`（默认 zh-CN）；对所有重要地名/景点/车站/线路/酒店/餐厅逐条提供中文/英文名称，日本目的地额外提供日文原名、可靠的假名及 Hepburn 罗马字，并制作供问路时展示的名称卡。执行 `references/multilingual_names_and_pronunciation.md`。封面、页眉、页脚及三级页码目录以三份历史攻略的出版版式为准，但严禁引用原攻略的旧事实、旧景点清单和旧票价代替本次独立研究；执行 `references/legacy_layout_contract.md`。正文与路线必须含这些名称而不能只放附录。


**Check localized names:** use `research/NAME_INDEX.md` to verify Chinese+English each major place, with Japanese original+verified kana+romaji in Japan, along with proofread pages and functioning 3-level TOC. Do not pass review if columns are incomplete or main guide does not show the same labels.


### Hard media/pagination gates

Verify all real photo/map files exist in `photos/` / `maps/`, match provenance/rights in `research/MEDIA_MANIFEST.json`, and are actually referenced inline (not URLs) in output. Each `Map A/B/...` has corresponding real map illustration. Verify docx and pdf contain embedded raster media, not only links. Every printed H1 and H2 must start fresh page. Validate supplied hotel and mode-agnostic outbound/return routes. No FINAL unless these pass.