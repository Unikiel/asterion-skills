# Periplus v2.4.1 — 任意语言输入 · 中文默认输出 · 中英日地名与读音 · 老攻略版式

**输入目的地、日期、去程起点、返程终点及去程/返程交通方式（飞机/火车/巴士/轮船/自驾/组合均可）及可选住宿酒店、偏好。** 不用重复研究、排版、目录、校验等规则。输入可用中文、英语、日语或其他语言；正文默认简体中文，明确要求可改为其他语言。

**必备产物：DOCX + PDF**，保留旧版 Nagoya/Kobe/Tokyo 三份攻略的 A4 封面风格、`Content` 真正的三级带页码目录、`Seven Ninths Travel Brochure` 每页页眉、`N / Total` 页脚。仅参照它们的**版式**，绝不复用当年的景点事实和时刻表。

**地点标注永久规则：** 中文 + English；日本还显示日文原名、核实的假名及罗马字，方便向站务人员展示和发音。机场、铁路线路、车站、景点、餐厅、酒店、Around Area 同样适用。

## 一句话使用

```text
$periplus
目的地：京都，日本
日期：2026-11-05 到 2026-11-11
去程：新干线，东京站 → 京都站
回程：新干线，京都站 → 大阪站（返程终点可以不同）
住宿：已预订酒店名称及地址（可选）
偏好：现代建筑、铁路、博物馆、摄影、少走路
```

也可用英语、日语等任意自然语言提供相同参数。车次只是语法示例，并非已确认时刻、车票或预订。

## 安装到本地 Codex

本目录是 Asterion Skills 仓库中的 Periplus 2.4.1。集合级说明见仓库根目录 [README](../README.md)。把完整的 `periplus/` 目录复制到 Windows `%USERPROFILE%\.codex\skills\periplus\`，macOS/Linux `~/.codex/skills/periplus/`。若已有包含 `periplus/SKILL.md` 的 ZIP，也可用同目录的 `install_codex.ps1` 或 `install_codex.sh`；见 `INSTALL.md`。ChatGPT 账户的安装需通过其支持的 Skill 导入操作执行。

## 本地一键执行（可选）

```powershell
python scripts/generate.py --destination Kyoto --country Japan --start 2026-11-05 --end 2026-11-11 --outbound-mode rail --outbound-origin "Tokyo Station" --outbound-destination "Kyoto Station" --outbound "Nozomi 123" --return-mode rail --return-origin "Kyoto Station" --return-destination "Osaka Station" --return-service "Nozomi 456" --hotel "Booked Hotel" --custom "铁路、博物馆、摄影、少走路" --out .\trips
```

需要已经配置联网研究权限的 Codex CLI，以及 `python-docx`、`markdown-it-py`、`pymupdf`、`Pillow`、LibreOffice 才能导出并验收真实 DOCX/PDF。

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
  references/media_acquisition_and_maps.md
  scripts/generate.py
  scripts/export_brochure.py
  scripts/fetch_media.py
  scripts/map_from_geojson.py
  scripts/media_utils.py
  scripts/validate.py
  scripts/test_skill.py
```

这是可安装的 Skill 代码包，不会从本对话自动写入你电脑或账号。联网端到端真实目的地攻略需要在用户的 Codex 环境进行测试。



## 出版交付强制条件

- **必须内嵌实际真实照片 + 真实地图**（包括每个 Map A/B 等区域），不能把网页图片链接当插图。媒体来源、作者与版权条件写入 `research/MEDIA_MANIFEST.json`，每张图有标注。
- **一级、二级标题各自都从新页面开始**；三级标题不断页。
- 使用酒店入参作为主要住宿与换乘基点；无酒店时仅推荐未预订的酒店。
- `Arrival & Departure` 接受各类交通，而非必须飞机。
- 发行前执行真实媒体与DOCX/PDF页码、页眉、目录及换页 QA。
媒体辅助脚本：`scripts/fetch_media.py` 可下载已确认许可的真实照片/官方地图；`scripts/map_from_geojson.py` 可用经过核实的真实地理 GeoJSON 数据制作区域地图。缺乏真实素材时不会用地图 URL 或虚构插图冒充成品。

## 英文字体与端点默认规范

西文英文字体固定使用 **Oswald**（封面、页眉、目录、标题、正文与数字）；中文使用 Noto Sans CJK SC 等可读 CJK 字体。PDF 导出前请在执行机器上安装 Oswald，导出程序会核验 PDF 字体，未安装则报错阻止 FINAL（Skill ZIP 不包含任何字体文件）。**去程起点** `journey.outbound.origin` 与**返程最终目的地** `journey.return.destination` 必填，不假设相同。
