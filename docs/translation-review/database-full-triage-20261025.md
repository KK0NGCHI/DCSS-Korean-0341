# Database inventory and translation triage — 2026-10-25

Source: `main`, `source/dat/database/*.txt` (23 top-level files). This is a **lexical scan** of original top-level databases, **not** a verified count of untranslated on-screen text. Korean `ko/*.txt` overlays provide fallback and must be checked independently.

Counting rules: split on `%%%%`; omit blank/comment (`#`) lines and `w:N` weighting lines; first meaningful line is the key. English candidate: Latin alphabet sequences after stripping `@...@` placeholders and `<...>` markup, excluding Korean-containing lines and pure `@reference@` lines. Lua control may still be in candidates; original English body remains English intentionally when a Korean overlay exists. `keys` counts occurrences and may differ from unique-key totals.

| File | Keys | Body lines | Hangul body | English candidates | Pure refs | Lua-control | Triage | Priority |
|---|---:|---:|---:|---:|---:|---:|---|---|
| FAQ.txt | 39 | 197 | 0 | 197 | 0 | 0 | help/prose | P1 |
| colourname.txt | 9 | 434 | 0 | 428 | 3 | 0 | generated fragments | P2 |
| decorlines.txt | 133 | 263 | 0 | 217 | 36 | 57 | generated lines / Lua | P1 |
| gizmo.txt | 3 | 539 | 0 | 539 | 0 | 0 | generated names | P2 |
| godname.txt | 23 | 50 | 0 | 50 | 0 | 0 | localized overlay complete | QA |
| godspeak.txt | 193 | 560 | 123 | 401 | 29 | 9 | mixed original + KO overlay | P1 |
| graffiti.txt | 58 | 404 | 0 | 351 | 39 | 0 | generated text | P1 |
| help.txt | 13 | 519 | 0 | 517 | 0 | 3 | help/prose | P0 |
| insult.txt | 33 | 557 | 0 | 541 | 14 | 1 | generated speech | P0 |
| miscast.txt | 33 | 193 | 0 | 193 | 0 | 0 | localized overlay complete | QA |
| miscname.txt | 10 | 158 | 0 | 156 | 0 | 7 | generated names | P2 |
| monflee.txt | 1 | 5 | 5 | 0 | 0 | 0 | Korean in original | QA |
| monname.txt | 52 | 842 | 0 | 789 | 52 | 0 | generated names | P2 |
| monspeak.txt | 731 | 3556 | 0 | 3153 | 374 | 115 | localized overlay independent text covered | QA |
| monspell.txt | 260 | 359 | 0 | 345 | 12 | 0 | localized overlay independent text covered | QA |
| montitle.txt | 86 | 86 | 86 | 0 | 0 | 0 | Korean in original | QA |
| rand_all.txt | 18 | 584 | 0 | 577 | 7 | 0 | generated names | P2 |
| rand_arm.txt | 19 | 529 | 0 | 529 | 0 | 0 | generated names | P2 |
| rand_wpn.txt | 45 | 845 | 0 | 816 | 23 | 0 | generated names | P2 |
| randbook.txt | 73 | 1597 | 0 | 1563 | 31 | 0 | generated names | P2 |
| randname.txt | 33 | 483 | 0 | 450 | 25 | 0 | generated names | P2 |
| shout.txt | 93 | 119 | 87 | 2 | 26 | 0 | mixed original + KO overlay | QA |
| wpnnoise.txt | 65 | 733 | 0 | 701 | 30 | 1 | localized overlay complete | QA |

## Actionable queue

1. **P0: `help.txt`, `insult.txt`** — audit the actual renderer/macro substitutions and translate full sentences. Keep original text for English fallback; create KO overlays keyed exactly like existing DB overlays.
2. **P1: `graffiti.txt`, `decorlines.txt`, `FAQ.txt`, `godspeak.txt`** — separate prose, generator references, Lua code and already localized Korean original/overlay before translating.
3. **P2: name/color generators** (`colourname`, `gizmo`, `miscname`, `monname`, `rand_all`, `rand_arm`, `rand_wpn`, `randbook`, `randname`) — require Korean word order, name inflection and combinator validation; do not translate fragments blindly.
4. **QA** `godname`, `monspell`, `monspeak`, `wpnnoise`, `miscast`, `monflee`, `montitle`, `shout` — measure real output and dynamic grammar, not nominal overlay key counts.

## Caveats

- These source totals include 23 files, but localized overlay files were not scanned for their full per-key coverage in this report.
- In particular source `monspeak.txt` has 731 keys by the simplified parsing method; the project's authoritative unique-key audit reported 731 unique keys with one duplicate occurrence. The different rule needs normalization.
- Do not sum `English candidates` into an overall untranslated percentage.
- Original `godspeak` has Korean mixed with English; PR #20 added 139 overlay entries without replacing original. Further English samples may already be covered.
- Lua code, placeholders, grammatical affixes and gender/case inflections must be verified at runtime.
