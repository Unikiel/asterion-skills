# Seven Ninths Travel Brochure — 老攻略版式合同

版式依据用户亲自提供的三份 Word 攻略，而非借用当年旧行程、旧票价或目的地资料：
- `2024.Japan.Nagoya.0323-0328.docx`
- `2025.Japan.Kobe.1002-1007.docx`
- `2026.Japan.Tokyo.0501-0504.docx`

## 必须继承的出版形式

1. **A4、竖向长篇手册**，非 PPT 型旅游海报、单页景点列表，也不能变成博客排版。
2. **独立封面**：上方/中央国名 `JAPAN`、目的地大字、`YYYY.MM.DD – YYYY.MM.DD` 日期范围，使用克制黑白设计＋日系红色强调，正文不复用老攻略图片或内容。
3. **封面后紧接 Content/目录**：**三级章节**（Heading 1–3），左侧层级缩进、点状引导线、右侧**真实页码**，多页目录允许自动延伸。
4. 旧三份 DOCX 内均包含 `TOC \\o "1-3" \\h \\z \\u` 字段，且 TOC1/2/3 均有页码；Periplus 要生成真正可在 Word 更新的 TOC 字段，同时在导出的 DOCX 和 PDF 中预先填入核验过的目录页码，不依赖用户打开 Word 后手工“更新域”。
5. **固定页眉**：`Seven Ninths Travel Brochure`，每一页；加细分隔线。**页脚**中央 `当前页 / 总页数`，各页有效。
6. **正文结构与标题层级**：只继承三份旧攻略中的栏目与层级；目的地事实、航班、时刻表、信息来源都必须重新研究，不能复用旧内容。
7. 景点、交通、酒店支持照片、站台图、地图和表格；实际文件可用时内嵌，来源和图注可查证；无实图时不要生成空的“地图”图框。
8. 内容默认简体中文，实体名称中英双语并附当地官方名字与读音；具体参见 `multilingual_names_and_pronunciation.md`。
9. 文档采用一致段落间距、可读中文字体与正确的字体回退，不能出现方框缺字。
10. **DOCX→PDF 后逐页检查**页眉、目录页码、跳转及页脚。PDF页码应与目录实际页面一致，Word TOC 可再更新。

## 章节架构

- Arrival & Departure
- Accommodation
- Brief Sketch（History / Geography / Climate / Population / Religion / Politics / Economy / Education / Culture / Transportation / ...）
- Attractions & Schedule（Maps A–P ... / Schedule）
- Sightseeing & Adventure（Primary City / Around Area [同日往返的附近目的地] / Tours）
- Delicacy & Shopping（Restaurant & Café & Bar / Supermarket & Store & Market）
- Recommends & Tips（Tourist Travel Pass & Ticket / Tourist Center / Tickets & Prices / Practical Information / Currency / Embassy / Important Numbers / Useful links）

栏目标题可以保留原有英文，内部正文按用户指定语言输出。地名不要因为章节使用英文而丢失中英日三种标注。

## DOCX 输出约束

- 正文由真正的 `Heading 1/2/3` 样式编码，Word 的“导航窗格”和 PDF 书签能够导航。
- 内置`TOC`字段负责 Word 后续更新，**必须同时拥有经过排版稳定性复核的静态缓存页码**供 DOCX/PDF 即时阅读。
- 拒绝未带数字页码的手工目录、带 `000` 的缓存、只有 `Contents` 的空页、以及和正文错位的页码。
- 目录不应包含封面的大字标题本身；目录标题 `Content` 不应重复进入目录。
