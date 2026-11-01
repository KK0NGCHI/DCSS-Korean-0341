# Bulk P0 translation batch — 2026-11-01

Base: `main` at `4923edc852d7bd2f91cede82643e39dfd9006a97`.
Working branch: `ko/bulk-p0-runtime-20261101`.

## Integrated PRs

- #172 (`54fbea974025faabece7e557236a9604633e02bc`): exceptional game messages; Linux console KO runtime and inventory checks passed.
- #173 (`4923edc852d7bd2f91cede82643e39dfd9006a97`): item identification, draining, Xom effects and manual completion messages; Linux console KO runtime and inventory checks passed.

## Batch policy

Accumulate multiple commits on this branch. Do not open a PR after a single
message or a handful of translated strings. Target 200–500 verified,
player-visible P0 output sites per PR, unless risk or semantic cohesion
requires a smaller isolated change. Track changed output sites separately from
unique translated strings and from changed source lines.

Prioritize remaining combat, damage, status, inventory, item-use, spells,
abilities and skills. Classify before editing: Korean already present,
English player-visible, internal diagnostics, format-only, or dynamic/needs QA.
Never translate internal identifiers, database keys, printf placeholders, Lua
directives, or markup as prose. Preserve English fallback.

Run translation inventory and Linux KO runtime smoke on the final accumulated
patch. Compile all changed C++ files, not just a historical allowlist.
Verify Windows Tiles and dynamic grammar separately before claiming runtime
completeness.

## Outstanding verification

- Refresh the full current-main P0 output-site inventory; old 2026-10-24
  counts are not a remaining untranslated count.
- Deduplicate already translated C++ outputs and Korean DB overlays.
- Confirm output contexts for dynamic name, particle, number and plural forms.
- Use dedicated large batches for `help.txt`, `insult.txt`, and database
  prose only after comparing existing KO overlays with their source keys.
- Report every subsequent batch with translated sites, files, CI status,
  remaining confirmed untranslated sites, and any unresolved cases.

## Accumulated translations (first commit set)

- `source/god-passive.cc`: 5 fixed messages for Qazlal resistance expiration and supernatural speed ending.
- `source/spl-transloc.cc`: 1 controlled teleport interruption diagnostic.
- `source/god-wrath.cc`: 2 further divine warning outputs localized.
- `source/god-prayer.cc`: 1 ambiguous altar conversion prompt.
- `source/monster.cc`: 3 monster effect outputs.
- `source/spl-damage.cc`: 1 lightning arc output.
- 13 output sites translated in total; English fallback preserved.
- No PR opened yet: continue accumulating translations until a coherent large batch is ready.
- CI status for this cumulative branch has not been confirmed; do not claim successful build or runtime verification.

**Status:** 13 translated output sites in this batch, awaiting additional translations and verification. The 200–500 target has not been reached.
