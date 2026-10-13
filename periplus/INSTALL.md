# Periplus v2.3 — Installation and execution

Periplus is the `periplus/` skill in the Asterion Skills repository. The
collection install is to copy that complete folder into a supported skills
directory. See the repository [README](../README.md). The ZIP installers below
are an optional path when you already have a packaged archive.

## Codex installation on your own computer

This conversation runs in a separate container and cannot write into your Windows/macOS machine. Run the installer on that machine after downloading the ZIP.

- Windows: `powershell -ExecutionPolicy Bypass -File .\install_codex.ps1 -Zip .\periplus-skill-v2.3.0.zip`
- macOS/Linux: `bash install_codex.sh ./periplus-skill-v2.3.0.zip`

The scripts install into `%USERPROFILE%\.codex\skills\periplus\` (Windows) or `~/.codex/skills/periplus/` (macOS/Linux), then check `SKILL.md` exists. Restart Codex to refresh available skills.

You may also unzip manually into that directory. Local generator requires an authenticated Codex CLI, website research access, Python `python-docx` and `markdown-it-py`, `pymupdf` and LibreOffice installed for PDF export.

## ChatGPT

There is **no tool in this conversation that can install a custom Skill into your ChatGPT account**. If your ChatGPT client presents a skill import/upload feature, use it to import `periplus-skill-v2.3.0.zip` or the extracted `periplus/` folder as appropriate. Do not mistake a local Codex skill install for ChatGPT account installation. If your client does not offer skill upload, attach `SKILL.md` and the bundled references in a ChatGPT Project / compatible custom GPT as instructions and reference material; a normal chat cannot permanently register a skill by claiming it was installed.

## Quick execution example (replace flight numbers)

```text
$periplus
目的地：京都，日本
日期：2026-11-05 至 2026-11-11
去程：MU123（示例，非实际航班）
回程：MU124（示例，非实际航班）
偏好：建筑、博物馆、摄影、铁路、少走路、雨天备选
```

The expected final files are `exports/Seven_Ninths_Travel_Brochure.docx` and `.pdf`; the `.md` file is an internal manuscript unless explicitly requested.

### Runtime status and boundaries

If required research or conversion tools are not available, Periplus must raise a visible blocker and preserve intermediate work. The local installer makes the skill discoverable; it does **not** silently install LibreOffice or configure external AI/model credentials, and it does not run the multi-hour research task until invoked.

默认输出中文 DOCX 与 PDF，中文+英文地点名，日本再附日文原名、假名读音、罗马字；完整页码目录与旧手册版式均为内置规则。用户可用任意语言调用。
