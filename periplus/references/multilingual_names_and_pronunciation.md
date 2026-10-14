# Periplus — Multilingual Place Names, Signage and Pronunciation (Mandatory)

## Core principles

- Users may submit requests in **any language**, including Chinese, English, Japanese, Korean, French or mixed-language text. Interpret free text and place names faithfully; the prompt language must not change the request's meaning.
- **The default guide narrative language is Simplified Chinese (zh-CN)**. If the user specifies another output language, use it throughout the narrative, chapter explanations, lists and schedules. The language of skill instructions, README files and examples does not change this default. Skill documentation and bundled examples are written in English; generated guides still support Chinese input and output.
- **All important locatable entities must have Chinese and English names**: attractions, shrines/temples, museums, art galleries, districts, shopping centres, restaurants, hotels, stations, airports, platforms/exits, lines and nearby excursion destinations. Label nonofficial translations as descriptive translations or transliterations, in the guide's narrative language; never present them as official English names.
- **Japanese destinations also retain the original Japanese name, verified kana pronunciation and Hepburn romanization**, allowing identification on site. If pronunciation cannot be reliably verified, mark it as pronunciation pending in the guide's language; never guess readings of personal or place-name kanji. Do not arbitrarily rewrite established official readings.
- Outside Japan, retain **local script and the applicable standard transliteration/phonetic notation** when reliably sourced. Never invent pronunciation notation.

## Standard record format (recommended minimum)

The following English documentation examples use descriptive placeholders for non-English script. Replace placeholders with researched names and readings in the generated guide; never print placeholders in final output.

**[Chinese name] / Kyoto Station**\
Japanese: [official Japanese name] ([verified kana], *Kyoto-eki in verified Hepburn spelling*)\
Show staff: **[official Japanese name]**\
Category: railway hub | Location: Kyoto City | Available lines: independently verified

**[Chinese name] / Kiyomizu-dera Temple**\
Japanese: [official Japanese name] ([verified kana], *Kiyomizu-dera*)\
Show a local resident: **[official Japanese name]** (include the actual address to distinguish similarly named destinations)

> These examples illustrate naming format only. Dates, services, addresses and routes require independent verification when executing a travel task.

## Mandatory output layout

1. Attraction H3 headings: `### [Chinese name] / English Name`, followed immediately by a separate `**Original Japanese name:** [official script] ([verified kana] / [Hepburn romanization])` line. Render field labels in the requested narrative language. For non-Japanese places, use local official script and verified pronunciation instead.
2. Tables show Chinese + English for stations, bus stops, lines, hotels and restaurants; never use Chinese alone.
3. Routes list official station/line names in sequence, particularly entrances, platforms, direction, interchange locations and exits. Show Chinese beside local script; include official English signage when needed.
4. Supply small **ask-for-directions cards** for key attractions and complex transfer hubs: Chinese meaning, local-script text that can be shown on site, verified romanized pronunciation, and address or nearest station. Example card structure:
   - Chinese: [Chinese translation of "How do I get to Kyoto Station?"]
   - Japanese: [verified natural Japanese question asking directions to Kyoto Station]
   - Romaji: [verified Hepburn rendering of that same Japanese question]
   - Show staff: **[official Japanese station name]**
5. Image/map labels include at least Chinese/English; retain original Japanese signage for Japanese destinations. Text must be clearly legible.
6. Provide full pronunciation at first mention; subsequent short paragraphs may use Chinese/English shortened names. **An appendix alone is insufficient: the body, schedule and routes also require multilingual labels.**
7. Resolve ambiguous translated names, Japanese readings or romanization using the official attraction, rail operator, municipality or authoritative map, and record the source.

## Research evidence

Prioritize official attractions, transport operators, government tourism sites and official English pages for name records. Not every entity has an official English translation. Where needed, identify an English name derived from the Chinese meaning as a descriptive translation rather than an official name. Prefer displaying Japanese kanji, kana and romanization over retaining only an uncommon English semantic translation.

## Audit

- Check at least the first 10 core attractions, or all if fewer than 10: Chinese + English + Japanese/local name + reliably sourced pronunciation must be complete.
- Check at least one entity in each Airport, Hotel, Railway, Attraction, Around Area, Restaurant & Cafe and Shopping section against the same multilingual rules.
- PDF fonts must support Chinese, English, Japanese, kana and long-vowel marks. Visually inspect for corruption, overlapping text and missing glyphs.
