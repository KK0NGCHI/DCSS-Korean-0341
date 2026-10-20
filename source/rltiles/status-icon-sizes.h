#pragma once

// This file is auto generated, edit rltiles/icon-sizes.txt instead.

#include "tiledef-icons.h"

inline int status_icon_size(tileidx_t icon)
{
    switch (icon)
    {
    case TILEI_BERSERK:
    case TILEI_IDEALISED:
    case TILEI_TOUCH_OF_BEOGH:
    case TILEI_SHADOWLESS:
    case TILEI_SUMMONED:
    case TILEI_MINION:
    case TILEI_UNREWARDING:
    case TILEI_TESSERACT_SPAWN:
    case TILEI_ANIMATED_WEAPON:
    case TILEI_VENGEANCE_TARGET:
    case TILEI_VAMPIRE_THRALL:
    case TILEI_ENKINDLED_1:
    case TILEI_ENKINDLED_2:
    case TILEI_NOBODY_MEMORY_1:
    case TILEI_NOBODY_MEMORY_2:
    case TILEI_NOBODY_MEMORY_3:
    case TILEI_PYRRHIC:
    case TILEI_FRENZIED:
        return 0;
    case TILEI_DRAIN:
    case TILEI_MIGHT:
    case TILEI_SWIFT:
    case TILEI_DAZED:
    case TILEI_HASTED:
    case TILEI_SLOWED:
    case TILEI_CORRODED:
    case TILEI_INFESTED:
    case TILEI_WEAKENED:
    case TILEI_PETRIFIED:
    case TILEI_PETRIFYING:
    case TILEI_BOUND_SOUL:
    case TILEI_POSSESSABLE:
    case TILEI_PARTIALLY_CHARGED:
    case TILEI_FULLY_CHARGED:
    case TILEI_VITRIFIED:
    case TILEI_CONFUSED:
    case TILEI_SENTINEL_MARK:
    case TILEI_DIMMED:
        return 6;
    case TILEI_LACED_WITH_CHAOS:
    case TILEI_CONC_VENOM:
    case TILEI_FIRE_CHAMP:
    case TILEI_INNER_FLAME:
    case TILEI_PAIN_MIRROR:
    case TILEI_STICKY_FLAME:
    case TILEI_STRONG_WILLED:
        return 7;
    case TILEI_ANGUISH:
    case TILEI_FIRE_VULN:
    case TILEI_RESISTANCE:
    case TILEI_GHOSTLY:
    case TILEI_MALMUTATED:
    case TILEI_MAGNETISED:
        return 8;
    case TILEI_RECALL:
    case TILEI_TELEPORTING:
    case TILEI_FIGMENT:
        return 9;
    case TILEI_BLIND:
    case TILEI_BRILLIANCE:
    case TILEI_SLOWLY_DYING:
    case TILEI_WATERLOGGED:
    case TILEI_STILL_WINDS:
    case TILEI_ANTIMAGIC:
    case TILEI_DEFLECT_MISSILES:
    case TILEI_INJURY_BOND:
    case TILEI_GLOW_LIGHT:
    case TILEI_GLOW_HEAVY:
    case TILEI_BULLSEYE:
    case TILEI_CURSE_OF_AGONY:
    case TILEI_REGENERATION:
    case TILEI_RETREAT:
    case TILEI_RIMEBLIGHT:
    case TILEI_UNDYING_ARMS:
    case TILEI_BIND:
    case TILEI_SIGN_OF_RUIN:
    case TILEI_WEAK_WILLED:
    case TILEI_DOUBLED_VIGOUR:
    case TILEI_KINETIC_GRAPNEL:
    case TILEI_TEMPERED:
    case TILEI_HEART:
    case TILEI_UNSTABLE:
    case TILEI_VEXED:
    case TILEI_PARADOX:
    case TILEI_WARDING:
    case TILEI_SUNDERING:
        return 10;
    case TILEI_CONSTRICTED:
    case TILEI_VILE_CLUTCH:
    case TILEI_PAIN_BOND:
        return 11;
    default:
        return -1;
    }
}
