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
- `source/monster.cc`: 4 additional item-ownership diagnostic outputs (diagnostic, not ordinary gameplay text).
- `source/misc.cc`: 1 stasis teleport warning.
- `source/player-equip.cc`: 2 equipment/hand interaction messages.
- `source/monster.cc`: 15 further weapon aura, combat effect and sound messages.
- `source/misc.cc`: 2 movement/swap messages.
- `source/god-prayer.cc`: 2 prayer/tithe messages.
- `source/monster.cc`: 2 bloodstain/gold outputs and 2 mount death/fall outcomes.
- `source/mon-act.cc`: 1 visible door interaction output.
- `source/monster.cc`: 2 additional weapon-brand aura output sites (freezing branch covers ranged and melee variants); mount death grammar corrected.
- `source/god-wrath.cc`: 5 divine retribution messages.
- `source/god-passive.cc`: 3 divine passive/protection messages.
- `source/god-passive.cc`: 3 Wu Jian attack announcements (lunge, whirlwind, wall jump).
- Corrected the Korean divine protection output to retain `MSGCH_GOD`.
- `source/spl-damage.cc`: 1 freezing damage/no-damage feedback output.
- `source/mon-death.cc`: an attempted duplicate death message branch was removed; the original Korean death message remains. No additional unique output site counted.
- 58 output sites translated in total; English fallback preserved.
- Draft PR #174 opened for compiler verification; continue accumulating on this same PR rather than making small PRs.
- CI for draft PR #174 was queued on 2026-11-02; no successful build or runtime verification established yet. Both build workflows now copy the modified `monster.cc`, `misc.cc`, `god-passive.cc`, `god-prayer.cc`, and `god-wrath.cc`.
- QA: monster diagnostics now use explicit field labels and plain `%s` formats to avoid ambiguous particles and positional printf portability issues.
- QA: equipment messages still use literal `이(가)`; replace with context-aware output grammar before final language-quality acceptance.
- QA: divine protection channel mismatch fixed; verify compilation and display behavior.
- QA: Wu Jian output retains target and momentum/count semantics but uses label-style Korean; polish after dynamic grammar support.

**Status:** 268 translated output patterns in this batch, awaiting additional translations and verification. The 200–500 target has not been reached.

## CI verification 2026-11-02

Draft PR #174 head `590cc639b1a5c39cf5c246c92a2e1e97ef76898a` passed `linux-console-ko-runtime` and `inventory` checks. Subsequent translations in `spl-damage.cc` and `mon-death.cc` require fresh CI; do not carry the prior pass forward to newer commits. Korean death feedback currently uses field-label phrasing to avoid uninflected particles and requires natural-language QA.

## 2026-11-02 QA fix

- Removed a duplicate KO/else branch in `source/mon-death.cc`, restoring the source blob to its pre-batch state. The previous 59-site tally counted this already-localized site in error; revised cumulative count: **58** (including 4 diagnostic sites).
- Reworded the 3 Wu Jian attack outputs in `source/god-passive.cc` into Korean sentences.
- CI must be rerun after these corrections; no new successful check established for the corrected head yet.

## 2026-11-02 additional monster effects batch

- Latest previously checked head `e1d2d9c0832541a80a01160bbc447f7e181406cd` passed Linux KO runtime and inventory CI.
- `source/mon-ench.cc`: 13 newly localized enchantment, grapnel, portal, merfolk and wind messages.
- `source/spl-clouds.cc`: 1 rot cloud spell message.
- `source/mon-cast.cc`: 1 wizard-only unsupported dummy monster message; an attempted additional chaos message was already localized and immediately reverted (do not count).
- New sites: 15, cumulative **73** sites (including 5 diagnostics/developer messages); latest head still requires CI.
- Next: CI status check, resolve particle grammar in `%s` monster output, translate remaining monster enchantment text, and Windows Tiles QA.

## 2026-11-02 monster detection follow-up

- CI for previous cumulative head `0ab605972ecbb392b1a98a65143e13256c04aa67` passed inventory and Linux Korean runtime smoke.
- `source/mon-ench.cc`: three additional player-facing outputs localized (visibility detection on charm/bribe expiry and soul grip loss).
- New cumulative count: **76** sites, of which **71** are non-diagnostic messages.
- QA: translated detection messages use target-label grammar to avoid unhandled Korean particles. Retain existing charm/bribe state context in later prose polish.
- Next: check the new CI run, inspect remaining genuinely untranslated spell outputs, fix Korean water-attack particle placeholders and review natural wording, then continue translations on draft PR #174.

## 2026-11-02 bulk combat/status update

- `source/mon-ench.cc`: 20 `simple_monster_message` status expiry/impact messages localized; use appended label phrasing pending grammar QA.
- `source/mon-abil.cc`: 8 monster ability and movement messages localized, in addition to the solar-flare hit message.
- `source/fineff.cc`: 1 electrical discharge hit message localized.
- **This batch: 30 distinct output sites. Cumulative: 106 output sites, including 5 diagnostic/developer sites.**
- Previous head `5ec55e542cc229fee3c18961772bb310a1d7bfa8` was pending CI when work began. New head requires fresh Linux runtime compilation CI.
- Next: check CI status; scan the bulk additions for overlapping Korean branches and placeholder mismatches; refine monster-name particle-free phrasing; translate further `simple_monster_message` instances in combat and enchantment subsystems.

## 2026-11-03 bulk monster-message batch

- Pre-batch head `d0030bed8cf3e7f51577b1d60d1ea843cf573eeb`: inventory and Linux Korean runtime smoke CI both passed.
- `source/mon-ench.cc`: 4 additional effect-expiry messages.
- `source/mon-act.cc`: 2 door-breaking/door-eating messages.
- `source/mon-behv.cc`: 1 gate-passing message.
- `source/mon-death.cc`: 16 monster defeat, death, falling, return, and pacification messages.
- 23 new output sites, **129 cumulative** (5 developer/diagnostic sites), pending fresh CI at new head.
- Next: check fresh CI, inspect output formatting and already-present Korean branches, continue scanning monster action/death messages in larger batches, and verify Windows Tiles behavior separately.

## 2026-11-03 monster gameplay message batch II

- Baseline `0160c87634cc6abd80442809ec0219e02e15ea21`: Linux console KO runtime and inventory checks successful.
- `source/monster.cc`: 13 monster frenzy, berserk, banishment, movement, damage/weakening, and recollection messages.
- `source/mon-death.cc`: 3 Beogh rescue, demise and flame-expiry messages.
- `source/mon-cast.cc`: 2 god-protection messages.
- 18 new output sites, cumulative **147** (5 diagnostic/developer sites); post-batch CI required.
- Next: check new CI, review monster-message suffix formatting and dynamic grammar, continue scanning non-`mpr` output paths and translate further batches, then Windows Tiles spot checks.

## 2026-11-03 bulk divine messages

- Previous baseline head `3bb32cd0896ace30bf0a9ebef36834ea38469ef4` passed `inventory` and `linux-console-ko-runtime`.
- `source/god-wrath.cc`: 29 divine wrath, speech, failure, protection and punishment messages.
- `source/god-passive.cc`: 2 audience-related deity passive messages.
- This batch: **31** new output sites; cumulative **178** (5 developer/diagnostic).
- New head requires CI rerun; output suffixes still need natural Korean particle/grammar QA. Do not merge until verified.
- Next: check CI for this head, revise deity speech Korean particles and verbose strings, scan multiline and dynamic `simple_god_message` calls for more messages, and translate to at least 200 sites on this draft PR.

## 2026-11-03 large divine wrath follow-up

- Baseline `3465486d6885a2fa49b6d8dd774bd6744bb31702`: both inventory and Linux Korean runtime checks passed.
- `source/god-wrath.cc`: 25 distinct new localization patterns for conditional punishments, summoning results, divine speeches, Jiyva/Fedhas effects, Ignis anointing and protective fire. The conditional variants may occur at more than one callsite; cumulative site tally remains conservative.
- Fixed English fallback argument handling for the Ignis anointing and fire effects and normalized duplicated spaces in Korean wrath suffixes.
- Cumulative **203** localized patterns/output positions counted, including 5 developer/diagnostic messages. Latest changes require new CI. Next: check compile, verify dynamic format/grammar, then continue translation of conditional god_speaks and monster gameplay messages.

## 2026-11-03 divine speech and equipment attunement

- `source/god-wrath.cc`: five previously unlocalized English speech variants for The Shining One, Kikubaaqudgha, and Jiyva's slime summoning results (three call positions).
- `source/player-reacts.cc`: one equipment-attunement output expanded into Korean status and regeneration/chemistry effect messages, avoiding English grammar suffixes.
- **Six new translated patterns, cumulative 209 patterns (not necessarily 209 distinct source callsites)**. The source-count metric previously mixed alternatives and sites and needs a full audit before PR merge.
- Linux runtime CI was in progress for prior head `9fb51c92c466426fe843549cb3c37c5582ba23fe` when work began; latest head requires separate validation.
- Next: confirm CI, audit formatting and particles, scan other message constructors beyond mpr, and continue large batch translations across unreviewed gameplay modules.

## 2026-11-03 weapon brands, religion and effects bulk batch

- Pre-batch PR head `64f708605c4d71aa5cc2039c796fa2b5fff3bcbc` passed `linux-console-ko-runtime` and `inventory` checks.
- `source/item-use.cc`: 17 new weapon rebranding messages, preserving one `%s` item-name argument.
- `source/religion.cc`: 30 new output positions across 25 single-literal patterns (26 uses) and 4 multiline god messages; covers gifts, conversion, deity refusals, and Slime Pits treasure unlock.
- `source/potion.cc`: 6 outputs (5 patterns), covering god reactions and monster potion effects.
- `source/mutation.cc`: 2 mutation/protection outputs.
- `source/spl-selfench.cc`: 3 outputs, including a separately translated Jinx Bite message with `some/more` semantics intact.
- `source/evoke.cc`: 1 cobweb output.
- **This batch: 59 output positions across 6 C++ files. Previous reported 209 patterns + 59 new output positions = 268 provisional cumulative units.** Previous cumulative units mixed patterns and output sites, so a distinct-callsite inventory still needs to replace this provisional number.
- Fresh CI required for the new head. Next: check compile/smoke results, review religion and item-use grammar/printf placeholders, enumerate untranslated messages in game UI and combat modules, and maintain the existing draft PR #174 without merging.

## 2026-11-04 Korean particle/grammar QA batch

- Corrected **31 existing localized output positions** across `player-equip.cc`, `mon-cast.cc`, `mon-death.cc`, `mon-abil.cc`, `mon-act.cc`, `religion.cc`, `item-use.cc`, and `spl-transloc.cc`. This includes two player-equipment positions in the first commit and 29 more positions in the follow-up batch.
- Removed literal Korean `이(가)`, `을(를)`, and `와(과)` from these selected paths, using sentences without variable-dependent particles while preserving printf argument counts and English-language fallback.
- Removed an unused English-only movement noun in `player-equip.cc` after the Korean message stopped interpolating it.
- **QA changes, not new translated sites**: do not add 31 to the provisional 268 translation-unit tally.
- Selected phrases that use labels or neutral constructions need in-game naturalness review; dynamic grammar infrastructure is still unfinished.
- Compile on the latest PR head. Previous successful CI runs cannot validate these new modifications.

## 2026-11-04 bulk P0 player-facing outputs (19 new positions)

- `source/evoke.cc`: 2 no-target confirmation prompts (tremorstone/cloud condenser).
- `source/spl-clouds.cc`: 1 blastmote cloud warning.
- `source/stairs.cc`: 1 dangerous transition confirmation prompt.
- `source/delay.cc`: 10 equipment/transform/servitor prompts, start/stop/finish and HP recovery outputs.
- `source/travel.cc`: 1 Zot proximity autoexploration prompt.
- `source/mon-abil.cc`: 2 Slymdra metamorphosis/splitting outputs, single and multiple spawn.
- `source/shopping.cc`: 1 shopping list header with quantity and cost.
- `source/potion.cc`: 1 lethal-cloud tree transformation prompt.
- **19 newly localized output sites**, 8 C++ files. All retain English fallback. Diagnostics excluded from count.
- This is separate from the previous 31-site grammar QA batch, which was **not** counted as new translations.
- PR #174 provisional cumulative translation count: **268 prior mixed units + 19 new distinct sites = 287 mixed provisional units**. Do not treat this as precise distinct-site total; comprehensive callsite recount still required.
- All edits committed to the same draft PR. The prior Linux run was still in progress at the start of the batch. The newest code must pass fresh full-overlay compilation and runtime smoke before merge.
- Known QA: neutral equipment-change text loses equip-on/off distinction; improve with safe Korean-specific message variants when practical. Windows Tiles in-game output and dynamic names remain unverified.

### 2026-11-04 follow-up: equip-on/off clarity

- `source/delay.cc`: localized the previously dynamic `EquipOffDelay::try_interrupt` confirmation (1 more new output site); distinguished equip-on from equip-off in 6 Korean start/stop/finish messages while preserving English fallback.
- **Total new output sites for this 2026-11-04 batch: 20** (19 first group + 1 follow-up), across 8 C++ files. Existing Korean text refinements are not additional translations.
- **Provisional cumulative mixed units: 288** (268 prior mixed + 20 new); still not a definitive distinct-callsite total.

### 2026-11-04 further travel, equipment and evocation follow-up

- Seven **additional** newly localized output sites: Zot deadline warning (`stairs.cc`), soundlessness and inert evoker feedback (`evoke.cc`), servitor spell imbuing (`delay.cc`), route-warning confirmation, destination menu title, and blocked auto-travel feedback (`travel.cc`).
- **2026-11-04 new translation total: 27 output sites** over 8 C++ files; existing-message grammar QA remains a separate 31-site count.
- Previous running provisional mixed total **288 + 7 = 295**. This is not yet a canonical unique-output count.
- Outstanding risk: `barrier.second` in blocked auto-travel and `deviant.describe()` in route warnings may still contain English or require Korean particles; inspect their producers. Validate full changed-file compile and Linux KO database runtime on the newest head; Windows Tiles QA pending.

## 2026-11-04 follow-up: 25 further confirmed player-facing outputs

- `shopping.cc`: 3 shopping-list prompts (replace cheaper item, remove entry, insufficient-funds travel confirmation).
- `stairs.cc`: 2 staircase warnings (annotated next level, excluded stairs).
- `player-stats.cc`: 2 attribute increase/stat-zero feedback messages.
- `travel.cc`: 2 pickup failure and level display descriptions.
- `item-use.cc`: 4 scroll-abort and dangerous-item-use confirmation prompts.
- `spl-cast.cc`: 2 spell-casting warnings (god penance, dangerous contamination).
- `god-prayer.cc`: 1 unknown-god conversion confirmation.
- `player-equip.cc`: 9 equipment size, limb, and wings restrictions.
- **New translations this turn: 25 distinct output sites in 8 C++ files**, no diagnostics. Do not mix these with the previous 31 grammar QA corrections or prior 27-site batch.
- Prior provisional mixed tally 295 + 25 = **320 provisional units**; the historical 268 component mixes literal patterns and callsites, so a complete callsite audit is required.
- All changes preserve English fallback and percent-format arguments. `player-equip.cc` English wings/size descriptors remain in the English-only branch.
- Runtime QA still required for Korean item names supplied by `describe_thing()`, `stat_desc()`, level annotations and branch names. No Windows Tiles QA was performed.
- Latest Linux runtime CI must be checked against the **exact newest PR HEAD**. Earlier green inventory jobs do not validate future revisions.

## 2026-11-04 batch: shopping, risk prompts and equipment restrictions (57 new sites)

- Shopping list: 3 prompts (replace an expensive entry, remove an item, travel even when unaffordable).
- Stairs: 2 warnings (annotated next floor, excluded staircase).
- Player attributes: 2 messages (stat gain and stat drained to zero).
- Travel: 2 outputs (uncollected items, branch level title).
- Item use: 4 confirmations (scroll wasted on cancel ×2, invisibility-effect warning, unsafe transformation).
- Spell cast: 2 warnings (penance and magical contamination).
- God prayer: 1 unknown-god conversion warning.
- Player equipment: **41 distinct failure/restriction outputs**, covering sizing, appendages, equipment slots, helmets, amulets, exoframes, and anatomical constraints. The original `NO_SLOT`/`NO_EQUIP` macros still receive `string` or literal English fallbacks.
- **Total: 57 new output sites across 8 C++ files**. Diagnostics not counted. Previous grammar corrections (31 positions) are not new translations.
- Previous provisional mixed units 295 + 57 = **352 provisional units**. The historical figure mixes translated patterns and callsites and must not be presented as a precise completed-string count.
- QA: variable data from `describe_thing`, `stat_desc`, branch names and item-name generators can remain untranslated. Prompt semantics and English fallback preserved; full Linux compilation and Windows Tiles runtime QA must be rerun for latest head.
- Current HEAD before recording this section: `325d648392f2f72059657c7a0c254dfeb118a38b`. Both inventory and Linux KO runtime checks were still in progress when checked. Do not merge draft PR #174 until compiler and runtime validation are confirmed.

## 2026-11-04 batch: transformation, species, spell UI and dream sheep QA (44 changed localization positions)

- `mutation.cc`: **28 new Korean localization points** for transformation/innate ability descriptions, AC/HP modifiers, equipment restrictions, water walking, flight, cold-bloodedness, poison immunity, ancestor essence, ring count, and a bane name/skill impact. Dynamic English descriptions outside this specific set remain to be audited.
- `spl-book.cc`: **7 points** spanning newly learned spell message, search matched terms, Divine Exegesis MP display, hidden spells, action help label, menu search/help, and Esc clear-search hint. Several mode labels are still built as separate dynamic fragments; review in Windows UI.
- `spl-cast.cc`: 1 spell miscast failure-risk and confirmation prompt rewritten to use Korean `failure_rate` and numeric severity (original English fallback retained).
- `ouch.cc`: 1 wizard/test death confirmation.
- `mon-death.cc`: 1 Kirke polymorph expiration message for singular/plural hogs and original/human forms.
- `mon-cast.cc`: 6 localized expressions for dream-sheep sleep effects: **5 standalone message or branch texts and 1 shared drowsiness suffix**. The suffix is *not* counted as a unique output callsite.
- **44 modified translation positions total = 43 potential output/description sites or branches + 1 dynamic suffix**. The number is an edit count, **not** a verified distinct callsite count. This batch introduces no diagnostic translations.
- Earlier provisional mixed tally 352 + 44 = **396 provisional edited translation units**. Do not use this as a precise distinct-callsite count or overall translation percentage.
- Baseline PR head `2f897486d796485b787fc98ab3782544c13e6adb`: inventory and Linux console KO runtime checks both passed. The newly modified HEAD needs an independent CI pass.
- Source-backed editing verified each old snippet was unique before replacing and retained English fallback; Windows Tiles gameplay remains untested and actual in-game phrasing/width needs QA.

### 2026-11-04 spell-library modes follow-up (six further output alternatives)

- `source/spl-book.cc`: all six conditional spell-library mode labels now have Korean text (cast, memorise, imbue, describe, hide, show); the original English switch remains intact.
- **50 localized text positions/variants changed in this turn**, consisting of 49 potential independent UI/output description branches plus one reusable drowsiness suffix. Some are mutually exclusive branches in a single output site; this is not 49 unique callsites.
- Revised **provisional historical mixed count: 352 + 50 = 402**, for tracking editing effort only. A fresh deduplicated callsite audit remains required before any translation-completion percentage can be reported.
- Post-change Linux KO runtime CI and inventory must pass on the exact latest PR HEAD. Windows Tiles QA still pending.

## 2026-11-04 batch: spells, mutation UI, ranged sounds and explosion SFX

**Baseline:** PR #174 head `d26544132b8a4f695407c7fefab8ae6a78cc7c89` passed translation inventory; Linux KO runtime build was still running when the batch started. Do not carry any check conclusion to a newer commit.

### Newly localized direct outputs and descriptions — 34 positions

- `spl-book.cc`: 4 spell memorisation refusal reasons (already known, restricted school, unavailable, unexpected error).
- `throw.cc`: 6 ranged action/sound outputs (confused aim, sling, bow, crossbow, triple crossbow, hand cannon).
- `mon-cast.cc`: 5 monster environmental spell messages (magma, ice, wind, rubble, hostile forest).
- `mutation.cc`: 9 mutation menu and intrinsic-description outputs (header, mundane message in two contexts, suppressed/transient/future-level legend, HP wand cost, tentacle grappling, claws), plus 2 forced equipment-removal outputs from mutations.
- `beam.cc`: 8 direct player-visible tree-burning and generic explosion feedback messages.

### Explosion SFX table — 44 fields, not 44 independent callsites

- `beam.cc`: created a separate Korean `spell_explosions_ko` map parallel to the original `spell_explosions` for **22 spell types × 2 fields** (visible explosion text and audible sound description). The map lookup selects based on `Options.language`, preserving English and identifiers. Generic sound formatting also has a separate Korean branch.
- Fields are **data entries**, not directly invoked message callsites; the actual output paths are shared. Do not add all 44 fields to a callsite count.

### Existing Korean QA — 3 fixes

- `mutation.cc`: revised the forced-unwield/unequip Korean object-particle message to use a label-style structure.
- `terrain.cc`: revised two preexisting ice-damage Korean messages to avoid the literal `을(를)` particle.

**Accounting:** 34 newly localized direct output/description positions, 44 explosion message/sound data fields, one shared sound message formatting change, and 3 revisions to existing Korean outputs. Historical previous provisional mixed total was 402; because table data and direct outputs cannot be added to a single completion denominator, retain **402 as the pre-batch historical tally** until a proper recount. No overall completion percentage is claimed.

**QA and verification:** Validate latest HEAD of draft PR #174 with source inventory and Linux KO runtime compile/smoke. The localized explosion sound values are sound-label fragments and are rendered by a separate Korean sentence. Player-generated names and Windows Tiles output still need in-game validation. Do not merge without passing fresh checks.

## 2026-11-05 follow-up: dynamic item/beam output QA

- Previous batch (documented immediately above): 24 directly localized positions in `spl-book.cc` (4), `throw.cc` (6), `mon-cast.cc` (5), and `mutation.cc` (9).
- `beam.cc`: eight previously untranslated tree/explosion feedback strings and five beam/silver-impact outputs; a Korean branch for the generic localized explosion sound announcement was also added.
- `beam.cc`: full parallel `spell_explosions_ko` map with **22 spell types and 44 translated visual/audio data fields**. The original English map remains selected for non-Korean game language.
- `mutation.cc`: two forced-equipment-loss outputs translated; preexisting Korean grammar corrected at one forced item output.
- `terrain.cc`: two preexisting Korean ice-effect messages revised to avoid literal ambiguous particles.
- `item-use.cc`: seven logical confirmation/scroll-read output positions translated (potion warning, Victory-armour potion prompt, Victory-armour scroll prompt, scroll penance prompt, scroll bad-item confirmation, target-not-visible prompt, and successful scroll read). Some compose conditional appended phrases in the same output position, and their English fallback was retained.
- `beam.cc`: two further hit-on-player and hit-on-monster messages translated, preserving chaos extra effect, zero-damage indication, and punctuation. A temporary wrong count of printf format placeholders in the new player message was fixed in the immediately succeeding source commit.
- **Output accounting:** 46 localized output/description positions as grouped above (24 + 8 + 2 + 7 + 5), 44 translated explosion SFX data fields, and 3 edits of existing Korean grammar, plus one shared explosion-sound formatting variant. These categories must not be added together as 1:1 unique runtime callsites.
- Starting HEAD `a23557cac3ee5b091766f00f49abb59feb8754ea` passed both inventory and Linux console KO runtime. **The latest PR head is newer and requires its own PASS**. Windows Tiles QA remains pending.
- Review note: some dynamically supplied `name`, `verb_object`, and skill labels can still arrive in English. This needs the planned global name/grammar output pass.

## 2026-11-05 large dynamic-message batch — 44 modified output/description positions

Starting PR HEAD: `df7f0fd41cb14b9175364982f5dbe4ba3cbded04`. Translation inventory passed; Linux KO runtime CI was still running when inspected. All below source changes are newer and require a separate compile check.

### New Korean output or explanation branches (42 positions)

- `religion.cc` — 6: good-god wrath warnings (Elyvilon, Shining One, Zin chaotic/evil choice, fallback), god-selection default help and selection prompt.
- `mon-death.cc` — 1: animated forest abruptly stopping.
- `mon-cast.cc` — 1: visible merfolk siren song with a Korean name-compatible suffix, preserving English.
- `beam.cc` — 1: blocked line-of-fire explanatory warning.
- `spl-damage.cc` — 3: Ignite Poison allied-harm prompt, invisible target prompt, self-hit unravelling prompt.
- `spl-transloc.cc` — 7: held/movement restrictions, two mesmerisation/fear charge directions, chaos word target confirmation, self-charge and unseen charge target.
- `mon-util.cc` — 1: Sanctuary preventing a hostile attack.
- `player-reacts.cc` — 1: careful versus berserk barbed-spike removal.
- `spl-damage.cc` — additional 18 localized message/phrase positions including Ozocubu's Refrigeration, Drain Life, Sonic Wave (player, unseen/global, seen-monster suffix, unseen-monster), Ignite Poison cloud warning fragments, and Inner Flame targeting/immunity descriptions.
- `spl-goditem.cc` — 3: pacification impossible for mindless, nonliving and immobile monsters.

### Existing Korean message QA (2 positions)

- `throw.cc` — changed the thrown/shoot projectile statement from a literal `을(를)` particle to an item-label construction.
- `beam.cc` — changed the demonic-will counterattack from a literal `을(를)` to target-dative phrasing.

**Counting:** The above includes **42 new Korean translation text positions** (6+1+1+1+3+7+1+1+18+3 = 42) plus 2 existing Korean grammar fixes. To avoid an inconsistent total, the raw file-level edit count is **44 source edit positions**. Some are conditional components of the same runtime output; this is not a unique-callsites measure. For QA use the per-file breakdown and do not add 44 to a completion denominator.

**Verification:** Latest branch HEAD must pass inventory and Linux KO runtime. Windows Tiles runtime is not yet tested. Remaining focus: generic beam impact conjugation, `resist_margin_phrase` output, dynamic monster/item names, incidental English in spell labels. Draft PR remains unmerged.

## 2026-11-05 bulk output and help translation: 104 newly localized source text positions

**Baseline:** PR #174 head `52a30073682261132c02a13277b965fcff7cde16` passed both Linux KO runtime and inventory. The revised head requires fresh CI.

### Newly added Korean text positions (8 C++ source files)

| Source | Count | Scope |
| --- | ---: | --- |
| `source/spl-transloc.cc` | 5 | charge range / adjacent targets / immovable or terrain obstacles / allied target refusal |
| `source/player.cc` | 6 | draconian scale colour, invisibility denied by light and equipment, flight denied by form |
| `source/mon-death.cc` | 12 | derived-undead gait and habitat descriptions, mist summon success/failure, vampire bat rejoining, moving simulacrum |
| `source/spl-damage.cc` | 4 | airstrike strength explanations, arc blade/static discharge risk prompts |
| `source/spl-other.cc` | 7 | Passwall invalid destinations, thick rock, dangerous water/lava beyond rocks |
| `source/mon-abil.cc` | 5 | starcursed-mass screams varying with chorus size and victim state |
| `source/stairs.cc` | 2 | excluded destination stairs, invalid/fallback Hell environmental effect |
| `source/command.cc` | 63 | console/tiles diagnostics headings and more importantly **55** command-help action strings: gameplay, movement, inventory, saving, character status and notes |
| **Total** | **104** | **edited literal/conditional text positions, NOT canonical unique callsites** |

All translated strings retain the original English fallback except where the source already supplied a partial localized component; command hotkeys, `%s`/numeric format specifiers, style tags, and command identifiers are unchanged. The `command.cc` output may need screen-width wrapping in Windows Tiles; the 55 help entries are not verified with the actual font/viewport.

**Risk review:** `source/player.cc` draconian `species::scale_type` and some item/monster names are generated in other functions and might remain English. Some localized generic movement failures intentionally omit English-only fragment morphology. For further translation work, prioritise `resist_margin_phrase`, dynamic beam hit verbs and god/monster templated output; do not translate English fallback branches as missing strings.

**Verification:** Linux KO runtime and inventory checks need to pass for the *latest* PR HEAD after these edits. Draft PR #174 must remain unmerged until full checks and relevant Windows Tiles runtime QA. A definitive coverage percentage requires a stable deduplicated output-site inventory.
