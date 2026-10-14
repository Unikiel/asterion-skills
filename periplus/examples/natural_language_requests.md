# Request examples

All examples below are English. They demonstrate the request structure, not a requirement to use English. Equivalent Chinese, Japanese or other-language requests are accepted. Generated guide narration defaults to Simplified Chinese (`zh-CN`), unless explicitly overridden. Do not confuse the skill's documentation language with traveler input or generated-content language.

## Rail with a different final endpoint

```text
$periplus
Destination: Kyoto, Japan
Dates: 2026-11-05 through 2026-11-11
Outbound: Shinkansen, Tokyo Station -> Kyoto Station; recommend a suitable train
Return: Shinkansen, Kyoto Station -> Osaka Station; recommend a suitable train
Preferences: modern architecture, museums, railways, photography, minimal walking
```

## Supplied flights

```text
$periplus Prepare Kyoto, Japan for November 5-11, 2026.
Outbound: supplied flight MU123, Shanghai Pudong -> Kansai.
Return: supplied flight MU124, Kansai -> Beijing Capital.
Preferences: architecture, museums, trains and photography.
```

Service identifiers in this example are illustrative and unverified. Preserve real user bookings and independently research their date/terminal details; never treat example numbers as actual services.

## Optional hotel and mixed transfer modes

```text
$periplus
Destination: Kobe, Japan
Dates: 2026-11-05 through 2026-11-08
Outbound: ferry and rail, Osaka Port -> Kobe
Return: rail, Kobe -> Tokyo Station
Accommodation: supplied hotel name and address
Preferences: port architecture, railway history, seated meals and short walks
```

The user need not repeat default research, publication, image, map, font or QA rules. Outbound origin and final return destination must be specified or unambiguously resolvable; do not assume symmetry.

## Multiple stay periods, any count

```text
$periplus
Destination: Tokyo, Japan
Dates: 2026-07-11 through 2026-07-12; 2026-07-17 through 2026-07-19
Outbound: rail, Ueno Station -> Tokyo
Return: rail, Tokyo -> Osaka Station
Preferences: architecture, photography, minimal walking
```

Default outputs are `2026.Japan.Tokyo.0711-0712.0717-0719.docx` and matching `.pdf`. Append additional periods chronologically without a fixed segment count. Do not schedule July 13-16.

## Explicit output-language override

```text
$periplus
Destination: Aomori, Japan
Dates: 2026-11-05 through 2026-11-08
Outbound: rail, Ueno Station -> Aomori
Return: rail, Aomori -> Hachinohe Station
Output language: English
Preferences: modern architecture, railways, museums, photography, minimal walking
```

This changes generated narration to English. It does not change English-only filenames, required source research, bilingual entity names or the Japanese original-script/reading requirements.
