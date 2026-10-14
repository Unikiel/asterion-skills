# 多语言调用示例

下列示例等效。**输入语言不限**，输出默认中文；默认 DOCX + PDF、老版式、真实页码目录、中英双语地点＋日本原名/假名/罗马字。

## 简体中文

```text
$periplus 京都，2026-11-05 至 2026-11-11，去程从上海浦东到关西机场 MU123，返程从关西机场到北京首都 MU124。重点：建筑、铁路、摄影。
```

## English

```text
$periplus Prepare Kyoto, Japan for November 5–11, 2026. Outbound flight MU123 Shanghai Pudong to Kansai; return MU124 Kansai to Beijing Capital. Focus on architecture, museums, trains, photography, minimal walking.
```

## 日本語

```text
$periplus 2026年11月5日〜11日、京都。往路 上海浦東発・関西空港着 MU123、復路 関西空港発・北京首都着 MU124。建築、美術館、鉄道、写真を重視。
```

## Español

```text
$periplus Kyoto, del 5 al 11 de noviembre de 2026. Vuelo de ida MU123 de Shanghái Pudong a Kansai; regreso MU124 de Kansai a Pekín. Prefiero museos y arquitectura.
```

若想改变**攻略正文语言**，明确加“输出语言：English”等指令；没有指定则保持中文。

航班号仅为格式示范，非已确认的航班资料。


## 自然语言样例（入参无语言限制）

`$periplus
目的地：京都；日期：2026-11-05 至 2026-11-11；去程：JR新干线，东京→京都；返程：JR新干线，京都→东京；住宿：我已订XXX酒店，地址XXX；偏好：现代建筑和铁路。`

`$periplus For Kyoto Nov 5-11: outbound by ferry+rail, return by train. Hotel: XXX, address XXX. Museums and photography.`

交通/酒店/真实图文、地图、标题分页等固定规范不需要在输入中重复。
**出发点/终点不是可省略的默认参数：** 去程明确起点，返程明确最终目的地，不默认返程到最初出发城市。西文字体无需在每次调用时重复声明，默认 Oswald。
