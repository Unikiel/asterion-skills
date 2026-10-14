# Periplus v2.4.1 — Installation and execution

Periplus 2.4.1 is the `periplus/` skill in the Asterion Skills repository. The
collection install is to copy that complete folder into a supported skills
directory. See the repository [README](../README.md). The ZIP installers below
are an optional path when you already have a packaged archive.

## Codex installation on your own computer

This conversation runs in a separate container and cannot write into your Windows/macOS machine. Run the installer on that machine after downloading the ZIP.

- Windows: `powershell -ExecutionPolicy Bypass -File .\install_codex.ps1 -Zip .\periplus-skill-v2.4.1.zip`
- macOS/Linux: `bash install_codex.sh ./periplus-skill-v2.4.1.zip`

The scripts install into `%USERPROFILE%\.codex\skills\periplus\` (Windows) or `~/.codex/skills/periplus/` (macOS/Linux), then check `SKILL.md` exists. Restart Codex to refresh available skills.

You may also unzip manually into that directory. Local generator requires an authenticated Codex CLI, website research access, Python `python-docx` and `markdown-it-py`, `pymupdf`, `Pillow` and LibreOffice installed for PDF export.

## ChatGPT

There is **no tool in this conversation that can install a custom Skill into your ChatGPT account**. If your ChatGPT client presents a skill import/upload feature, use it to import `periplus-skill-v2.4.1.zip` or the extracted `periplus/` folder as appropriate. Do not mistake a local Codex skill install for ChatGPT account installation. If your client does not offer skill upload, attach `SKILL.md` and the bundled references in a ChatGPT Project / compatible custom GPT as instructions and reference material; a normal chat cannot permanently register a skill by claiming it was installed.

## Quick execution example (any transport mode)

```text
$periplus
目的地：京都，日本
日期：2026-11-05 至 2026-11-11
去程：JR新干线 东京→京都（示例）
回程：JR新干线 京都→东京（示例）
住宿：已订酒店名称及地址（可选）
偏好：建筑、博物馆、摄影、铁路、少走路、雨天备选
```

The expected final files are `exports/Seven_Ninths_Travel_Brochure.docx` and `.pdf`; the `.md` file is an internal manuscript unless explicitly requested.

### Runtime status and boundaries

If required research or conversion tools are not available, Periplus must raise a visible blocker and preserve intermediate work. The local installer makes the skill discoverable; it does **not** silently install LibreOffice or configure external AI/model credentials, and it does not run the multi-hour research task until invoked.

默认输出中文 DOCX 与 PDF，中文+英文地点名，日本再附日文原名、假名读音、罗马字；完整页码目录与旧手册版式均为内置规则。用户可用任意语言调用。


**v2.4 输入示例：** 目的地、起止日期、去回程交通方式与已知班次（非飞机亦可）、酒店名称/地址（可选）、个性化需求（可选）。内置真实图像+地图抓取与嵌入要求、Heading 1/2 分页、中文 DOCX/PDF 和三级目录，无须重复输入。
### Typography preflight

English text is set to **Oswald** (Google Fonts). Install Oswald from https://fonts.google.com/specimen/Oswald on the DOCX/PDF rendering computer before publishing, then restart LibreOffice (refresh font cache on Linux). Chinese and Japanese use CJK fonts independently. If PDF actually substitutes Oswald, Periplus stops publication. The ZIP deliberately does not redistribute any font file.

### Required route endpoints

The trip request must include the outbound starting point (`journey.outbound.origin`) and final return destination (`journey.return.destination`). They can be different cities. Natural-language input may supply them inside route statements rather than separate fields.
