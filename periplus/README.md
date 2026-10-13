# Periplus v2.3.0 — 任意语言输入 · 中文默认输出 · 中英日地名与读音 · 老攻略版式

本目录是 Asterion Skills 仓库中的 `periplus` 技能。集合级说明、安装和调用示例见仓库根目录 [README](../README.md)。

**只输入目的地、日期、去程/回程航班，偏好可选。** 不用重复研究、排版、目录、校验等规则。输入可用中文、英语、日语或其他语言；正文默认简体中文，明确要求可改为其他语言。

**必备产物：DOCX + PDF**，保留旧版 Nagoya/Kobe/Tokyo 三份攻略的 A4 封面风格、`Content` 真正的三级带页码目录、`Seven Ninths Travel Brochure` 每页页眉、`N / Total` 页脚。仅参照它们的**版式**，绝不复用当年的景点事实和时刻表。

**地点标注永久规则：** 中文 + English；日本还显示日文原名、核实的假名及罗马字，方便向站务人员展示和发音。机场、铁路线路、车站、景点、餐厅、酒店、Around Area 同样适用。

## 一句话使用

```text
$periplus
目的地：京都，日本
日期：2026-11-05 到 2026-11-11
去程航班：MU123
回程航班：MU124
偏好：现代建筑、铁路、博物馆、摄影、少走路
```

也可用英语、日语等任意自然语言提供相同参数。MU123/MU124 是输入格式演示，并非已确认的实际航班。

## 安装到本地 Codex

在 Asterion Skills 仓库中，把完整的 `periplus/` 目录复制到技能目录：Windows `%USERPROFILE%\.codex\skills\periplus\`，macOS/Linux `~/.codex/skills/periplus/`。若已有包含 `periplus/SKILL.md` 的 ZIP，也可用同目录的 `install_codex.ps1` 或 `install_codex.sh`；见 `INSTALL.md`。ChatGPT 账户的安装需通过其支持的 Skill 导入操作执行。

## 本地一键执行（可选）

```powershell
python scripts/generate.py --destination Kyoto --country Japan --start 2026-11-05 --end 2026-11-11 --outbound MU123 --return-flight MU124 --custom "铁路、博物馆、摄影、少走路" --out .\trips
```

需要已经配置联网研究权限的 Codex CLI，以及 `python-docx`、`markdown-it-py`、`pymupdf`、LibreOffice 才能导出并验收真实 DOCX/PDF。

`Around Area` 是离主目的地足够近、能**同日出发、当日返回**的周边一日游，不是主目的地的别名。

## 目录（示意）

```text
periplus/
  SKILL.md
  README.md
  agents/openai.yaml
  references/multilingual_names_and_pronunciation.md
  references/legacy_layout_contract.md
  references/*.md
  prompts/01-07_*.md
  assets/Seven_Ninths_Master_Skeleton.md
  scripts/generate.py
  scripts/export_brochure.py
  scripts/validate.py
  scripts/test_skill.py
```

这是可安装的 Skill 代码包，不会从本对话自动写入你电脑或账号。联网端到端真实目的地攻略需要在用户的 Codex 环境进行测试。

