# PR #174 pre-merge audit — 2026-11-06

## Source of truth
- Base branch `main`: `1285359c1bc3402095cffadfc41af4f158bf2425` at audit time.
- Draft PR #174 head: `c71a046cd4ed66edf09647d3fab24184ed7d3450`.
- Branch: `ko/bulk-p0-runtime-20261101`.
- PR delta: 196 commits, 42 changed files, +1541/-815 lines.
- Main has 13 commits since PR's merge base `4923edc`; those commits modify only `docs/translation-review/ROADMAP-ACTIVE.md`. GitHub reports PR mergeability `clean`.
- Linux Korean runtime workflow: [PASS on exact PR head](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/42031343493).
- Translation source inventory: [PASS on exact PR head](https://github.com/KK0NGCHI/DCSS-Korean-0341/actions/runs/42031343523).
- No Windows Tiles run for this cumulative PR head has been established. CI successes do not validate visible grammar, line wrapping, item/monster generated names or full game scenarios.

## Review of changes / QA issues
The GitHub PR files list and sample C++ patches were inspected. This is a **partial source review**, not a complete 42-file semantic audit. Concrete review targets:
1. `source/god-wrath.cc`: Korean `simple_god_message` suffixes begin with a mixture of spaces and em dashes; test concatenation with translated/generated god names and the `simple_god_message` prefix.
2. `source/mon-abil.cc` and `source/mon-behv.cc`: em-dash suffixes follow generated monster names; the name may remain English, requiring Windows text inspection.
3. `source/mon-ench.cc`: newly formatted `mprf` branches change source sentence structure; inspect name argument and visibility/friendliness variants.
4. `source/command.cc`: 55 command-help labels and additional diagnostics need Tiles font-width, overflow and keybinding checks.
5. `source/beam.cc`: 22 explosion types × 2 localized data fields; validate the Korean map selection, shared output formatter and all printf specifiers.
6. `source/item-use.cc`, `source/mon-cast.cc`: particle-neutral rephrasings preserve buildability but require in-game grammatical/semantic QA.
7. Ensure `cpp-build-verification.yml` and `korean-runtime-smoke.yml` both overlay all changed C++ files; only the Korean runtime smoke and inventory workflow were confirmed successful on this SHA.

## Decision
**Do not mark PR ready or merge yet** under the existing project's acceptance policy. Passing Linux checks resolves the previously outstanding build gate, but Windows Tiles and dynamic-name grammar acceptance are not demonstrated. The 13-commit divergence is documentation-only and need not be rebased destructively.

## Next actionable tasks
- Review all 42 changed files for placeholder arity, channel retention, English fallback, duplicate KO conditions and semantic changes; record exact file/line and correction for every concrete defect.
- Rebuild Windows Tiles at the audited PR head and check the UI, combat, gods, equipment, spell/monster/beam display, and save/load. Record PASS/FAIL.
- Update PR head if defects are fixed; re-run both successful workflows on the exact new head, then merge #174.
- Once merged, rebuild the distinct, player-visible callsite inventory against merged `main`, separating translated, English-visible, diagnostic, format-only and dynamic/QA cases. No project-wide translation percentage until denominators are verified.

## Counting discipline
3,778/3,778 translated description keys is data coverage, not total game translation. The historical PR log mixes translated text variants and output positions. The 104 changes on 2026-11-05 are edited literal/conditional text positions, **not** canonical distinct callsites.

## Targeted diff scan (2026-11-06)
- Examined the GitHub-provided patches for all 42 changed PR files, searching newly added lines for literal particle placeholders `이(가)`, `을(를)`, `은(는)`, `와(과)`.
- **0 matches in added C++ lines.** Five matches were found only in the added work-log document, referring to past corrections. This reduces one specific risk but **does not** establish that unchanged source contains no such strings, or that generated Korean grammar is correct.
- Retain the above runtime QA targets; the scan is not a substitute for testing with generated names.
