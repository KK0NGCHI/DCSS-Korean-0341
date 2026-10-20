# DCSS 0.34.1 Korean Localization — Extraction Roadmap

## Scope and principles
- Reference source: `C:\DCSS-Dev\stone_soup-0.34.1\source` (unmodified English 0.34.1).
- Integration source: `C:\DCSS-Dev\stone_soup-0.34.1-ko\source` (Korean smoke tests and future runtime changes).
- Local extractor workspace: `C:\DCSS-Dev\dcss-extractor`.
- Preserve original text, source location, call context, placeholders, and parsing errors.
- Never count a parsed string as confirmed player-visible without evidence.
- Track occurrences separately from unique translation units.
- Source files are read-only during extraction.

## Phases
| Phase | Deliverable | Completion criterion | Status |
|---|---|---|---|
| 00 Baseline | Roadmap, rules, progress records, source manifest | Manifest generated locally and validated | in_progress |
| 01 Pilot | C++ extraction on message.cc, invent.cc, describe.cc, newgame.cc | Parse errors and omissions reviewed; report recorded | pending |
| 02 C++ inventory | Full C++ string and callsite catalog | All in-scope files accounted for, errors reviewed | pending |
| 03 Lua and data | Script, game-data, descriptions and documentation catalog | All data families inventoried and sampled | pending |
| 04 Classification | Visible/internal/dynamic categorization, deduplication | Unknowns and manual-review queue reported | pending |
| 05 Legacy alignment | 0.24 Korean translation mapping | Matches and ambiguous cases recorded | pending |
| 06 Translation catalog | Context-aware POT/PO, draft/review workflow | Placeholder and context checks pass | pending |
| 07 Runtime integration | Korean loader, grammar handling, UI regression tests | Build and representative runtime tests pass | pending |

## Extraction priority (not exclusion)
P0: messages, combat, core menus, inventory, names.
P1: descriptions, gods, shops, branches, events, Lua.
P2: help, options, long-form documentation.
P3: rare/debug/developer text.

## Status semantics
pending -> in_progress -> completed. A phase is not completed merely because a script exits successfully.
Translation: untranslated -> draft -> reviewed -> verified; use review flags separately.

## Reporting
For every batch record: batch ID, input source version/hash, files attempted/succeeded/failed, literal occurrences, unique units, visible candidates, internal candidates, dynamic candidates, unknowns, parse errors, manual-review count, output paths, and validation notes.
No percentages before denominators are measured. Keep translation coverage distinct from extraction and runtime verification coverage.

## First batch
CPP-PILOT-001: message.cc, invent.cc, describe.cc, newgame.cc. Compare lexical string counts against extracted AST records; preserve errors and uncertain classifications.
