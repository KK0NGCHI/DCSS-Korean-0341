#pragma once

#include "tag-version.h"

/*
 * This file is auto-generated. See util/form-gen.py and dat/forms.
 */

struct form_entry
{
    // Row 1:
    transformation tran;
    monster_type equivalent_mons;
    const char *short_name;
    const char *long_name;
    const char *wiz_name;

    // Row 2:
    const char *description;

    // Row 3:
    int min_skill;
    int max_skill;
    int hp_skill_penalty_mult;
    talisman_type talisman;

    // Row 4:
    int blocked_slots;
    int resists;

    // Row 5:
    int str_mod;
    int dex_mod;
    size_type size;
    int hp_mod;
    int move_speed;

    // Row 6:
    FormScaling ac;
    FormScaling ev;
    FormScaling body_ac_mult;
    bool can_cast;
    FormScaling unarmed_bonus_dam;

    // Row 7:
    brand_type uc_brand;
    int uc_colour;
    const char *uc_attack;
    FormAttackVerbs uc_attack_verbs;

    // Row 8:
    form_capability can_fly;
    form_capability can_swim;
    form_capability offhand_punch;
    bool changes_anatomy;
    bool changes_substance;
    mon_holy_type holiness;

    // Row 9:
    bool is_badform;
    form_capability has_blood;
    form_capability has_hair;
    form_capability has_bones;
    form_capability has_feet;
    form_capability has_ears;

    // Row 10:
    const char *shout_verb;
    int shout_volume_modifier;
    const char *hand_name;
    const char *foot_name;
    const char *prayer_action;
    const char *flesh_equivalent;

    // Row 11:
    const dam_deducer* special_dice;
    const char* special_dice_name;

    // pairs of the form {terse_description, full_description} for display in
    // `A` and `%`. Either can be empty.
    // Resistances (except rTorm), flight, amphibious, no grasping,
    // melded equipment are added separately in mutation.cc:_get_form_badmuts
    vector<pair<string,string>> fakemuts;
    vector<pair<string,string>> badmuts;
};

static const form_entry formdata[] =
{

{
    transformation::none, MONS_PLAYER, "", "", "none",
    "",
    0, 0, 1, NUM_TALISMANS,
    0, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {},
    {}
},


{
    transformation::spider, MONS_SPIDER, "Spider", "spider-form", "spider",
    "an agile web-spinner.",
    12, 20, 1, TALISMAN_SPIDER,
    4606, mrd(MR_RES_POISON, -1),
    0, 5, SIZE_TINY, 100, 10,
    FormScaling().Base(3), FormScaling().Base(5).Scaling(10), {}, true, FormScaling().Base(3),
    SPWPN_NORMAL, LIGHTGREEN, "Fangs", { "hit", "bite", "pounce on", "eviscerate" },
    FC_DEFAULT, FC_FORBID, FC_DEFAULT, true, false, MH_NONE,
    false, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID,
    "hiss", -4, "front pincers", "", "crawl onto", "flesh",
    nullptr, "",
    {{"ensnaring attack", "You sometimes web enemies you hit."},
     {"rampage", "You can move swiftly towards enemies."},
     {"jumping", "You can leap distances in the blink of an eye."},
     {"stealth", "You are stealthy and inflict bonus damage to unaware enemies."},
     {"", "You are tiny and dextrous."}},
    {{"poison vulnerability", "You are susceptible to poisons. (rPois-)"}}
},


{
    transformation::blade, MONS_PLAYER, "Blade", "blade-form", "blade",
    "",
    17, 25, 1, TALISMAN_BLADE,
    0, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, FormScaling().Base(-50).Scaling(30), true, {},
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {{"blade aux", "You can perform multiple auxiliary attacks with your blades."},
     {"blade parry", "You gain SH while attacking, based on your slaying."}},
    {}
},


{
    transformation::statue, MONS_STATUE, "Statue", "statue-form", "statue",
    "a stone statue.",
    17, 25, 1, TALISMAN_STATUE,
    232, MR_RES_ELEC | MR_RES_NEG | MR_RES_PETRIFY,
    7, 0, SIZE_CHARACTER, 130, 10,
    FormScaling().Base(27).Scaling(11), {}, {}, true, FormScaling().Base(5),
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, true, MH_NONLIVING,
    false, FC_FORBID, FC_FORBID, FC_FORBID, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "place yourself before", "stone",
    nullptr, "",
    {{"powerful", "Your melee attacks are powerful."},
     {"torment resistance 1", "You are resistant to unholy torment."}},
    {{"slow", "All of your actions are slow."},
     {"reduced EV", "Your evasion is reduced."}}
},


{
    transformation::serpent, MONS_ANACONDA, "Serpent", "amphisbaena-form", "amphisbaena",
    "an enormous two-headed serpent.",
    12, 20, 1, TALISMAN_SERPENT,
    4590, MR_RES_POISON,
    5, 0, SIZE_LARGE, 120, 10,
    FormScaling().Base(10).Scaling(6), {}, {}, true, FormScaling().Base(7),
    SPWPN_NORMAL, LIGHTGREY, "", { "hit", "lash", "body-slam", "crush" },
    FC_DEFAULT, FC_ENABLE, FC_DEFAULT, true, false, MH_NONE,
    false, FC_DEFAULT, FC_FORBID, FC_ENABLE, FC_FORBID, FC_FORBID,
    "hiss", -2, "coils", "", "coil in front of", "flesh",
    nullptr, "",
    {{"constrict", "You have a powerful constriction melee attack."},
     {"two hats", "You can wear a hat or helmet on each head."}},
    {}
},


{
    transformation::dragon, MONS_PROGRAM_BUG, "Dragon", "dragon-form", "dragon",
    "a fearsome dragon!",
    17, 25, 1, TALISMAN_DRAGON,
    4606, MR_RES_FIRE | MR_RES_COLD | MR_RES_POISON,
    10, 0, SIZE_GIANT, 150, 10,
    FormScaling().Base(12).Scaling(6), {}, {}, true, FormScaling().Base(8).Scaling(10),
    SPWPN_NORMAL, GREEN, "Teeth and claws", { "hit", "claw", "bite", "maul" },
    FC_ENABLE, FC_FORBID, FC_ENABLE, true, false, MH_NONE,
    false, FC_DEFAULT, FC_FORBID, FC_ENABLE, FC_ENABLE, FC_ENABLE,
    "roar", 6, "foreclaw", "", "bow your head before", "flesh",
    nullptr, "Breath Dmg",
    {{"dragon claw", "You have a powerful clawing attack."},
     {"dragon scales", "Your giant scaled body is strong and resilient, but less evasive."}},
    {}
},


{
    transformation::death, MONS_ANCIENT_CHAMPION, "Death", "death-form", "death",
    "an undying horror.",
    26, 27, 1, TALISMAN_DEATH,
    0, MR_RES_COLD | mrd(MR_RES_NEG, 3),
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, FormScaling().Base(6),
    SPWPN_DRAINING, MAGENTA, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_UNDEAD,
    false, FC_FORBID, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "fossilised flesh",
    nullptr, "",
    {{"vile attack", "Your melee attacks drain, slow and weaken victims."},
     {"siphon essence", "You can torment nearby foes to heal from their wounds."},
     {"torment immunity", "You are immune to unholy pain and torment."}},
    {{"no potions", "You cannot drink."},
     {"accursed", "You recover more slowly from Doom and Banes."}}
},


{
    transformation::bat, MONS_BAT, "Bat", "bat-form", "bat",
    "a bat.",
    0, 0, 1, NUM_TALISMANS,
    5118, MR_NO_FLAGS,
    0, 5, SIZE_TINY, 100, 5,
    {}, {}, {}, false, FormScaling().XLBased(),
    SPWPN_NORMAL, LIGHTGREY, "Teeth", ANIMAL_VERBS,
    FC_ENABLE, FC_FORBID, FC_DEFAULT, true, false, MH_NONE,
    true, FC_DEFAULT, FC_ENABLE, FC_ENABLE, FC_ENABLE, FC_ENABLE,
    "squeak", -8, "foreclaw", "", "perch on", "flesh",
    nullptr, "",
    {{"extremely fast", "You cover ground extremely quickly."},
     {"", "You are tiny, dextrous, and very evasive."}},
    {{"weak attacks", "Your unarmed attacks are very weak."}}
},


{
    transformation::pig, MONS_HOG, "Pig", "pig-form", "pig",
    "a filthy swine.",
    0, 0, 1, NUM_TALISMANS,
    5118, MR_NO_FLAGS,
    0, 0, SIZE_SMALL, 100, 7,
    {}, {}, {}, false, FormScaling().XLBased(),
    SPWPN_NORMAL, LIGHTGREY, "Teeth", ANIMAL_VERBS,
    FC_DEFAULT, FC_FORBID, FC_DEFAULT, true, false, MH_NONE,
    true, FC_DEFAULT, FC_ENABLE, FC_ENABLE, FC_ENABLE, FC_ENABLE,
    "squeal", 0, "front trotter", "trotter", "bow your head before", "flesh",
    nullptr, "",
    {{"very fast", "You cover ground very quickly."},
     {"weak attacks", "Your unarmed attacks are very weak."}},
    {}
},


#if TAG_MAJOR_VERSION == 34
{
    transformation::appendage, MONS_PLAYER, "App", "appendages", "appendages",
    "",
    0, 0, 1, NUM_TALISMANS,
    80, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {},
    {}
},
#endif


{
    transformation::tree, MONS_ANIMATED_TREE, "Tree", "tree-form", "tree",
    "a tree.",
    0, 0, 1, NUM_TALISMANS,
    504, MR_RES_POISON,
    0, 0, SIZE_CHARACTER, 150, 10,
    FormScaling().Base(20).Scaling(14).XLBased(), {}, {}, true, FormScaling().Base(9),
    SPWPN_NORMAL, BROWN, "Branches", { "hit", "smack", "pummel", "thrash" },
    FC_FORBID, FC_FORBID, FC_DEFAULT, true, true, MH_PLANT,
    true, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID,
    "creak", 0, "branch", "root", "sway towards", "wood",
    nullptr, "",
    {{"resilient", "Your bark is very hard, but your evasion is minimal."},
     {"branches", "Your unarmed attacks smack enemies forcefully with your branches."},
     {"torment immunity", "You are immune to unholy torment."}},
    {{"stationary", "Your roots penetrate the ground, keeping you stationary."},
     {"-Tele", "You cannot be teleported."}}
},


#if TAG_MAJOR_VERSION == 34
{
    transformation::porcupine, MONS_PORCUPINE, "Porc", "porc-form", "porcupine",
    "a spiny porcupine.",
    0, 0, 1, NUM_TALISMANS,
    6142, MR_NO_FLAGS,
    0, 0, SIZE_TINY, 100, 10,
    {}, {}, {}, false, FormScaling().XLBased(),
    SPWPN_NORMAL, LIGHTGREY, "Teeth", ANIMAL_VERBS,
    FC_DEFAULT, FC_FORBID, FC_DEFAULT, true, false, MH_NONE,
    false, FC_DEFAULT, FC_ENABLE, FC_ENABLE, FC_ENABLE, FC_ENABLE,
    "squeak", -8, "front leg", "", "curl into a sanctuary of spikes before", "flesh",
    nullptr, "",
    {},
    {}
},
#endif


{
    transformation::wisp, MONS_TWISTER, "Wisp", "wisp-form", "wisp",
    "an insubstantial wisp.",
    0, 0, 1, NUM_TALISMANS,
    6142, mrd(MR_RES_FIRE, 2) | mrd(MR_RES_COLD, 2) | MR_RES_ELEC | mrd(MR_RES_NEG, 3) | MR_RES_CORR,
    0, 0, SIZE_TINY, 100, 10,
    FormScaling().Base(5).Scaling(14).XLBased(), {}, {}, false, FormScaling().Base(2).XLBased(),
    SPWPN_NORMAL, LIGHTGREY, "Misty tendrils", { "touch", "touch", "engulf", "engulf" },
    FC_ENABLE, FC_FORBID, FC_DEFAULT, true, true, MH_NONLIVING,
    true, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID,
    "whoosh", -8, "misty tendril", "strand", "swirl around", "vapour",
    nullptr, "",
    {{"", "You are tiny and evasive."},
     {"insubstantial", "You are insubstantial and cannot be petrified, ensnared, or set on fire."},
     {"torment immunity", "You are immune to unholy pain and torment."},
     {"highly resistant", "You are highly resistant to most damage types. (rF++, rC++, rN+++, rElec, rCorr)"}},
    {}
},


{
    transformation::jelly, MONS_JELLY, "Jelly", "jelly-form", "jelly",
    "a lump of jelly.",
    0, 0, 1, NUM_TALISMANS,
    4606, MR_RES_POISON | mrd(MR_RES_CORR, 3),
    0, 0, SIZE_CHARACTER, 125, 10,
    FormScaling().Base(1).Scaling(7).XLBased(), {}, {}, true, FormScaling().Base(9).Scaling(14).XLBased(),
    SPWPN_ACID, LIGHTGREY, "Pseudopod", { "slap", "smack", "body-slam", "engulf" },
    FC_DEFAULT, FC_ENABLE, FC_DEFAULT, true, true, MH_NATURAL,
    true, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID,
    "gurgle", 0, "pseudopod", "pseudopod", "squish down before", "jelly",
    nullptr, "",
    {{"acid body", "You are resistant to acid and immune to corrosive walls."},
     {"amorphous state", "Your amorphous body is immune to blinding, drowning, and ensnarement."},
     {"acidic touch", "Your melee attacks splash acid on your foes."}},
    {{"heavily diminished spells", "You cast all spells with heavily decreased power."}}
},


{
    transformation::fungus, MONS_WANDERING_MUSHROOM, "Fungus", "fungus-form", "fungus",
    "a sentient fungus.",
    0, 0, 1, NUM_TALISMANS,
    4606, MR_NO_FLAGS,
    0, 0, SIZE_TINY, 100, 10,
    FormScaling().Base(12), {}, {}, false, FormScaling().Base(9).XLBased(),
    SPWPN_CONFUSE, BROWN, "Spores", { "release spores at", "release spores at", "release spores at", "release spores at" },
    FC_DEFAULT, FC_FORBID, FC_DEFAULT, true, true, MH_PLANT,
    true, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID,
    "sporulate", -8, "hypha", "", "release spores on", "flesh",
    nullptr, "",
    {{"", "You are tiny and evasive."},
     {"spores", "Your melee attacks release spores that confuse breathing creatures."},
     {"torment immunity", "You are immune to unholy pain and torment."}},
    {{"terrified", "You become terrified and freeze when enemies are visible."}}
},


#if TAG_MAJOR_VERSION == 34
{
    transformation::shadow, MONS_PLAYER_SHADOW, "Shadow", "shadow-form", "shadow",
    "a swirling mass of dark shadows.",
    0, 0, 1, NUM_TALISMANS,
    0, mrd(MR_RES_POISON, 3) | mrd(MR_RES_NEG, 3) | MR_RES_MIASMA | MR_RES_PETRIFY,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, MAGENTA, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_FORBID, FC_DEFAULT, false, true, MH_NONLIVING,
    false, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID,
    "", 0, "", "", "", "shadow",
    nullptr, "",
    {{"half damage", "Damage taken is halved, but you are drained when taking damage."},
     {"bleed smoke", "You bleed smoke when taking damage."},
     {"invisible", "You are invisible."},
     {"unshakeable will", "Your willpower is unshakeable."},
     {"torment immunity", "You are immune to unholy pain and torment."}},
    {{"weak attacks", "Your attacks do half damage."},
     {"weak spells", "Your spells are much less powerful."}}
},
#endif


#if TAG_MAJOR_VERSION == 34
{
    transformation::hydra, MONS_HYDRA, "Hydra", "hydra-form", "hydra",
    "",
    0, 0, 1, NUM_TALISMANS,
    4606, MR_RES_POISON,
    0, 0, SIZE_GIANT, 130, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, GREEN, "", { "nip at", "bite", "gouge", "chomp" },
    FC_DEFAULT, FC_ENABLE, FC_DEFAULT, true, false, MH_NONE,
    false, FC_DEFAULT, FC_FORBID, FC_ENABLE, FC_ENABLE, FC_FORBID,
    "roar", 4, "foreclaw", "", "bow your heads before", "flesh",
    nullptr, "",
    {{"fast swimmer", "You swim very quickly."},
     {"devour", "You can devour living enemies to heal."}},
    {}
},
#endif


{
    transformation::storm, MONS_TWISTER, "Storm", "storm-form", "storm",
    "a lightning-filled tempest!",
    23, 27, 1, TALISMAN_STORM,
    4606, MR_RES_ELEC,
    0, 0, SIZE_CHARACTER, 100, 10,
    FormScaling().Base(12).Scaling(3), FormScaling().Base(20).Scaling(7), {}, true, FormScaling().Base(24).Scaling(6),
    SPWPN_ELECTROCUTION, LIGHTCYAN, "", { "hit", "buffet", "batter", "blast" },
    FC_ENABLE, FC_DEFAULT, FC_ENABLE, true, true, MH_NONLIVING,
    false, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID, FC_FORBID,
    "bellow", 0, "", "", "place yourself before", "air",
    new dicedef_calculator<1,11,600,135>, "Blinkbolt Dmg",
    {{"electrical cleaving", "Your electrical attacks strike out in all directions at once."},
     {"evasive", "You are incredibly evasive."},
     {"blinkbolt", "You can turn into living lightning."},
     {"insubstantial", "You are insubstantial and cannot be petrified, ensnared, or set on fire."}},
    {}
},


{
    transformation::quill, MONS_PLAYER, "Quill", "quill-form", "quill",
    "covered in sharp quills.",
    0, 7, 1, TALISMAN_QUILL,
    496, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    new dicedef_calculator<1,2,6,7>, "Quill Dmg",
    {{"quills", "Your quills sometimes injure those who attack you in melee."}},
    {}
},


{
    transformation::maw, MONS_PUTRID_MOUTH, "Maw", "maw-form", "maw",
    "a creature with a mouth for a stomach.",
    12, 20, 1, TALISMAN_MAW,
    0, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, FormScaling().Base(-75), true, {},
    SPWPN_NORMAL, GREEN, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "shout twice", 0, "", "", "", "",
    nullptr, "",
    {{"maw attack", "Your maw can bite with vicious strength."},
     {"devouring maw", "You can devour enemies to increase your regeneration."}},
    {{"growling stomach", "Your maw sometimes becomes mesmerised by tasty morsels."},
     {"low body AC", "Your maw has eaten a hole through body armour, reducing its AC."}}
},


{
    transformation::flux, MONS_SHAPESHIFTER, "Flux", "flux-form", "flux",
    "something dangerously unstable.",
    5, 14, 2, NUM_TALISMANS,
    4142, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, FormScaling().Base(6).Scaling(10), {}, true, {},
    SPWPN_NORMAL, CYAN, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    new dicedef_calculator<2,5,30,15>, "Contam Dmg",
    {{"contaminating", "Foes you strike become dangerously contaminated with transmutational energy."},
     {"glow", "You glow with energy, making you easy to see."}},
    {{"weak attacks", "Your attacks are very weak."}}
},


{
    transformation::slaughter, MONS_BRIMSTONE_FIEND, "Slaughter", "slaughter-form", "slaughter",
    "a vessel of demonic slaughter.",
    0, 0, 1, NUM_TALISMANS,
    0, MR_RES_POISON | mrd(MR_RES_NEG, 3) | MR_RES_MIASMA,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTRED, "", DEFAULT_VERBS,
    FC_ENABLE, FC_FORBID, FC_DEFAULT, false, false, MH_DEMONIC,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {{"damage resistance", "Damage taken is decreased by 1/3."},
     {"doubled heal-on-kills", "Healing from kills is doubled."},
     {"unshakeable will", "Your willpower is unshakeable."},
     {"torment immunity", "You are immune to unholy pain and torment."}},
    {{"demonic bargain", "You will endure the Crucible once your slaughter is complete."}}
},


{
    transformation::vampire, MONS_VAMPIRE, "Vampire", "vampire-form", "vampire",
    "a living vampire.",
    17, 25, 1, TALISMAN_VAMPIRE,
    0, MR_RES_COLD | mrd(MR_RES_NEG, 2),
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTMAGENTA, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {{"vampire fangs", "Your fangs allow you to drain the lifeblood from your enemies."},
     {"bloodcurse", "When you kill a living creature with a stab, you may create a vampiric thrall."},
     {"torment resistance 1", "You are resistant to unholy torment."},
     {"bat form", "You can occasionally transform into a swarm of bats."},
     {"hypnotic gaze", "You often daze monsters when they first notice you."},
     {"very stealthy", "You are very stealthy."}},
    {{"inhibited regeneration", "You do not regenerate when monsters are visible."},
     {"accursed", "You recover more slowly from Doom and Banes."}}
},


{
    transformation::bat_swarm, MONS_VAMPIRE_BAT, "Bat Swarm", "batswarm-form", "bat swarm",
    "a swarm of vampire bats.",
    17, 25, 1, NUM_TALISMANS,
    4606, MR_RES_COLD | mrd(MR_RES_NEG, 2),
    0, 5, SIZE_TINY, 100, 5,
    {}, FormScaling().Base(15).Scaling(20), {}, false, FormScaling().XLBased(),
    SPWPN_NORMAL, LIGHTGREY, "Teeth", ANIMAL_VERBS,
    FC_ENABLE, FC_FORBID, FC_DEFAULT, true, false, MH_NONE,
    false, FC_DEFAULT, FC_ENABLE, FC_ENABLE, FC_ENABLE, FC_ENABLE,
    "squeak", -8, "foreclaw", "", "perch on", "flesh",
    nullptr, "",
    {{"extremely fast", "You cover ground extremely quickly."},
     {"", "You are tiny, dextrous, and very evasive."},
     {"vampire fangs", "Your fangs allow you to drain the lifeblood from your enemies."},
     {"bloodcurse", "When you kill a living creature with a stab, you may create a vampiric thrall."},
     {"torment resistance 1", "You are resistant to unholy torment."},
     {"very stealthy", "You are very stealthy."}},
    {{"weak attacks", "Your unarmed attacks are very weak."},
     {"inhibited regeneration", "You do not regenerate when monsters are visible."},
     {"accursed", "You recover more slowly from Doom and Banes."}}
},


{
    transformation::rime_yak, MONS_YAK, "Yak", "yak-form", "rime yak",
    "an ice-encrusted yak.",
    8, 14, 1, TALISMAN_RIMEHORN,
    4606, mrd(MR_RES_COLD, 2) | mrd(MR_RES_FIRE, -1),
    0, 0, SIZE_LARGE, 115, 10,
    FormScaling().Base(6).Scaling(6), {}, {}, true, FormScaling().Base(4),
    SPWPN_NORMAL, LIGHTBLUE, "Horns", { "hit", "headbutt", "gore", "skewer" },
    FC_DEFAULT, FC_ENABLE, FC_DEFAULT, true, false, MH_NONE,
    false, FC_DEFAULT, FC_ENABLE, FC_ENABLE, FC_ENABLE, FC_ENABLE,
    "bellow", 0, "front hooves", "hooves", "bow your head before", "icy fur",
    new dicedef_calculator<2,1,3,5>, "Frigid Wall Dmg",
    {{"frigid aura", "You freeze nearby walls in an area that expands as you fight."},
     {"ice wizardry", "You can cast Ice magic more easily."}},
    {}
},


{
    transformation::hive, MONS_SPIDER, "Hive", "hive-form", "hive",
    "a living hive.",
    17, 25, 1, TALISMAN_HIVE,
    24, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    FormScaling().Base(5), {}, {}, true, {},
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {{"hive swarm", "When at low health, angry bees swarm out to defend you."},
     {"hive regen", "You regenerate HP and MP more quickly."}},
    {}
},


{
    transformation::aqua, MONS_PROGRAM_BUG, "Aqua", "aqua-form", "aqua",
    "",
    12, 20, 1, TALISMAN_AQUA,
    8, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, FormScaling().Base(6).Scaling(7), {}, true, {},
    SPWPN_NORMAL, BLUE, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_ENABLE, FC_DEFAULT, false, true, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    new dicedef_calculator<4,1,6,5>, "Watery Grave Dmg",
    {{"water reaching", "Your aqueous body allows to you attack from a distance."},
     {"water splatter", "When injured, pools of shallow water form around you."},
     {"watery grave", "You can command nearby water to drown your enemies."}},
    {{"steam response", "When hit by fire damage, your body sometimes produces steam."},
     {"freeze response", "When hit by cold damage, your body sometimes freezes."}}
},


{
    transformation::sphinx, MONS_SPHINX, "Sphinx", "sphinx-form", "sphinx",
    "a cunning sphinx.",
    17, 25, 1, TALISMAN_SPHINX,
    4222, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 115, 10,
    FormScaling().Base(7), {}, {}, true, {},
    SPWPN_NORMAL, LIGHTCYAN, "Paws", { "hit", "swat", "pounce on", "maul" },
    FC_ENABLE, FC_DEFAULT, FC_DEFAULT, true, false, MH_NONE,
    false, FC_DEFAULT, FC_ENABLE, FC_ENABLE, FC_ENABLE, FC_ENABLE,
    "roar", 0, "forepaw", "", "curl up before", "flesh",
    nullptr, "",
    {{"airstrike attack", "You unleash cutting winds upon enemies you strike."},
     {"hex mastery", "Hexes are much easier for you to cast and harder to resist."}},
    {{"riddle compulsion", "You often pose riddles to enemies when you first see then."}}
},


{
    transformation::werewolf, MONS_WOLF, "Werewolf", "werewolf-form", "werewolf",
    "a ferocious werewolf.",
    12, 20, 1, TALISMAN_WEREWOLF,
    224, MR_RES_COLD,
    3, 3, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {{"werefury", "You gain temporary slaying when you kill enemies in melee."},
     {"werehowl", "You sometimes unleash a terrifying howl when you kill enemies in melee."},
     {"bestial takedown", "You can leap to fearful enemies and eviscerate them."}},
    {}
},


{
    transformation::walking_scroll, MONS_WALKING_TOME, "Scroll", "scroll-form", "walking scroll",
    "a walking scroll.",
    0, 7, 1, TALISMAN_INKWELL,
    4606, mrd(MR_RES_FIRE, -1),
    0, 0, SIZE_TINY, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTGREY, "Magic Parchment", { "flutter at", "slap", "unfurl around", "read the riot act to" },
    FC_DEFAULT, FC_FORBID, FC_DEFAULT, true, true, MH_NONLIVING,
    false, FC_FORBID, FC_FORBID, FC_DEFAULT, FC_ENABLE, FC_FORBID,
    "flutter", -2, "parchment", "", "unroll yourself before", "parchment",
    nullptr, "",
    {{"scribal knowledge", "You have increased skill with all magical schools."},
     {"magic absorption", "Your melee attacks sometimes restore your MP."}},
    {{"novice magic", "You cannot cast spells above level 4."},
     {"weak attacks", "Your melee attacks are very weak."}}
},


{
    transformation::fortress_crab, MONS_CRAB, "Crab", "crab-form", "fortress crab",
    "a heavily-armoured crab.",
    12, 20, 1, TALISMAN_FORTRESS,
    4596, mrd(MR_RES_POISON, -1) | MR_RES_CORR,
    0, 0, SIZE_CHARACTER, 100, 10,
    FormScaling().Base(3), {}, FormScaling().Base(70).Scaling(80), true, FormScaling().Base(5).Scaling(5),
    SPWPN_NORMAL, GREEN, "pincers", { "nip", "snap", "crush", "mangle" },
    FC_DEFAULT, FC_ENABLE, FC_DEFAULT, true, false, MH_NONE,
    false, FC_DEFAULT, FC_FORBID, FC_FORBID, FC_ENABLE, FC_ENABLE,
    "clack", 0, "pincers", "", "scuttle before", "shell",
    nullptr, "",
    {{"armoured shell", "Your body armour is fused into your shell, improving its AC and properties."},
     {"rust breath", "You can exhale clouds of rust."}},
    {{"slow movement", "You cover ground slowly."}}
},


{
    transformation::sun_scarab, MONS_BOMBARDIER_BEETLE, "Scarab", "scarab-form", "sun scarab",
    "a gleaming scarab beetle.",
    8, 14, 1, TALISMAN_SCARAB,
    4606, mrd(MR_RES_FIRE, 2) | mrd(MR_RES_POISON, -1),
    0, 0, SIZE_SMALL, 100, 10,
    FormScaling().Base(5).Scaling(4), {}, {}, true, {},
    SPWPN_NORMAL, LIGHTRED, "Mandibles", ANIMAL_VERBS,
    FC_DEFAULT, FC_FORBID, FC_DEFAULT, true, false, MH_NONE,
    false, FC_FORBID, FC_FORBID, FC_FORBID, FC_ENABLE, FC_FORBID,
    "hiss", -4, "mandibles", "", "crawl onto", "carapace",
    new dicedef_calculator<2,2,8,5>, "Flare Dmg",
    {{"sun companion", "You manifest a globe of solar heat that you carry with you."},
     {"", "Your solar ember damages enemies next to it every second time you attack."},
     {"", "You heal your solar ember whenever you swap places with it."},
     {"searing attack", "Your melee attacks sometimes make enemies vulnerable to fire."},
     {"fire wizardry", "You can cast Fire magic much more easily."}},
    {{"poison vulnerability", "You are susceptible to poisons. (rPois-)"}}
},


{
    transformation::medusa, MONS_FORMLESS_JELLYFISH, "Medusa", "medusa-form", "medusa",
    "",
    8, 14, 1, TALISMAN_MEDUSA,
    272, MR_RES_POISON,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, {},
    SPWPN_NORMAL, LIGHTGREY, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    nullptr, "",
    {{"stinger hair", "Your tendrils poison nearby enemies when you attack."},
     {"lithotoxin", "When significantly injured, you may petrify poisoned enemies."}},
    {}
},


{
    transformation::eel_hands, MONS_PLAYER, "Eel", "", "eel hands",
    "",
    12, 20, 1, TALISMAN_EEL,
    4134, MR_RES_ELEC,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, FormScaling().Base(3).Scaling(4),
    SPWPN_NORMAL, LIGHTCYAN, "", { "hit", "punch", "bite", "thrash" },
    FC_DEFAULT, FC_DEFAULT, FC_ENABLE, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    new dicedef_calculator<1,-2,23,10>, "Jolt damage",
    {{"eel punch", "Electricity sometimes discharges through enemies you attack."},
     {"eeljolt", "When badly injured, your eels discharge electricity violently."}},
    {}
},


{
    transformation::spore, MONS_PLAYER, "Spore", "spore-form", "spore",
    "",
    8, 14, 1, TALISMAN_SPORE,
    4164, MR_NO_FLAGS,
    0, 0, SIZE_CHARACTER, 100, 10,
    {}, {}, {}, true, FormScaling().Base(4),
    SPWPN_NORMAL, BROWN, "", DEFAULT_VERBS,
    FC_DEFAULT, FC_DEFAULT, FC_ENABLE, false, false, MH_NONE,
    false, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT, FC_DEFAULT,
    "", 0, "", "", "", "",
    new dicedef_calculator<2,1,4,5>, "Burstshroom damage",
    {{"weakening spores", "Your melee attacks may weaken breathing enemies."},
     {"sporulate", "Your melee attacks cause explosive burstshrooms to grow."}},
    {}
},


};
COMPILE_CHECK(ARRAYSZ(formdata) == NUM_TRANSFORMS);
