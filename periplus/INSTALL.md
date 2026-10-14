# Periplus v2.5.0 — Installation and execution

## Local Codex installation

Download `Periplus_Skill_v2.5.0.zip`. The archive contains a `periplus/` folder. Install that folder into `%USERPROFILE%\.codex\skills\periplus\` on Windows or `~/.codex/skills/periplus/` on macOS/Linux. Restart the local Codex client to refresh skills.

Alternatively, extract the archive and use its bundled installer on your own computer, passing the original ZIP path:

```powershell
powershell -ExecutionPolicy Bypass -File .\periplus\install_codex.ps1 -Zip .\Periplus_Skill_v2.5.0.zip
```

```bash
bash ./periplus/install_codex.sh ./Periplus_Skill_v2.5.0.zip
```

The installers back up an existing local skill before replacing it and verify that SKILL.md exists. They do not install a configured Codex CLI, website-research access, Python dependencies, fonts or LibreOffice, and do not start a travel-research run.

## Other environments

For an environment with a supported skill import feature, import the ZIP or extracted folder according to that environment's interface. A local installer changes only the computer where it is run. In this Work Mode environment, saved skill updates are committed and pushed to the managed Skills repository; exporting a ZIP provides a separate portable copy.

## Invoke

```text
$periplus
Destination: Kyoto, Japan
Dates: 2026-11-05 through 2026-11-11
Outbound: rail, Tokyo Station -> Kyoto Station
Return: rail, Kyoto Station -> Osaka Station
Accommodation: supplied hotel name/address (optional)
Preferences: architecture, museums, photography, railways, minimal walking
```

All documentation and bundled examples are English. Requests written in Chinese or other languages remain accepted without translation by the user. Generated narration defaults to Simplified Chinese, or the user's explicit language choice. The final filenames are English and date-based, such as `2026.Japan.Kyoto.1105-1111.docx` and `.pdf`. Multiple date periods are supported without a fixed count.

## Runtime preflight

Use an authenticated, configured Codex CLI for the optional local generator, with working primary-source web retrieval. Publication requires `python-docx`, `markdown-it-py`, `pymupdf`, `Pillow` and LibreOffice. Install Oswald from its official distribution on the rendering computer and use an appropriate CJK font; refresh the font cache/restart LibreOffice as needed. The ZIP does not redistribute fonts. Missing research or conversion tools must produce a visible blocker, not a false FINAL result.

Check the canonical package version:

```bash
python scripts/generate.py --version
```

The expected result is `Periplus 2.5.0`. Skill release and schema version are recorded in project.json; the Git commit identifies the exact saved source revision separately.
