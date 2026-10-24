"""Tests for Korean speech directive, grammar, macro and weighted variants."""
import unittest
from audit_monspeak_ko import check_variants, audit


class KoreanMonsterSpeechTests(unittest.TestCase):
    def test_omitted_english_grammar_not_identity_tokens(self):
        en = ["@The_monster@ shouts @at_foe@, 'Be gone!'"]
        ko = ["@The_monster@이(가) 외친다. '꺼져!'"]
        self.assertEqual(check_variants(en, ko), [])
        self.assertEqual(check_variants(
            ["VISUAL:@The_monster@ sniffs @surface@."],
            ["VISUAL:@The_monster@이(가) @surface@의 냄새를 맡는다."]), [])
        self.assertIn("line_1_markers", check_variants(
            ["@The_monster@ sees @foe@."],
            ["@The_monster@이(가) 바라본다."]))

    def test_reflexive_grammar_is_optional_but_identity_is_not(self):
        original = ["@The_monster@ hums to @reflexive@."]
        translated = ["@The_monster@이(가) 스스로를 달래며 흥얼거린다."]
        self.assertEqual(check_variants(original, translated), [])
        self.assertIn("line_1_markers", check_variants(
            original, ["스스로를 달래며 흥얼거린다."]))

    def test_directive_and_alternatives_must_survive(self):
        en = ["VISUAL:@The_monster@ [pauses|stops]."]
        ko = ["VISUAL:@The_monster@이(가) [멈칫한다|가만히 선다]."]
        self.assertEqual(check_variants(en, ko), [])
        self.assertIn("line_1_directive_prefix",
                      check_variants(en, [ko[0].replace("VISUAL:", "")]))
        self.assertIn("line_1_random_alternatives",
                      check_variants(en, ["VISUAL:@The_monster@이(가) 멈춘다."]))

    def test_weight_preservation(self):
        en = ["w:3", "VISUAL:@The_monster@ blinks."]
        ko = ["w:3", "VISUAL:@The_monster@이(가) 눈을 깜박인다."]
        self.assertEqual(check_variants(en, ko), [])
        self.assertIn("weight_list", check_variants(en, ko[1:]))

    def test_weapon_noise_markup_and_weighting(self):
        src = ("%%%%\nweapon_noise\n\nw:10\n"
               "@Your_weapon@ [howls|laughs].\n\nw:3\n"
               "SOUND:You hear @weapon_noise@.\n%%%%\n")
        ko = ("%%%%\nweapon_noise\n\nw:10\n"
              "@Your_weapon@이(가) [울부짖는다|웃는다].\n\nw:3\n"
              "SOUND:@weapon_noise@ 소리가 들린다.\n%%%%\n")
        self.assertEqual(audit(src, ko)["problems"], [])
        self.assertTrue(audit(src, ko.replace("w:3", "w:4"))["problems"])
        self.assertTrue(audit(src, ko.replace("SOUND:", ""))["problems"])

    def test_lua_conditionals_are_not_display_text(self):
        src = [
            "{{",
            '  if you.race() == "Felid" then',
            '    return "@_friendly_imp_@"',
            "  else",
            '    return "Hello there!"',
            "  end",
            "}}",
        ]
        translated = [
            "{{",
            '  if you.race() == "Felid" then',
            '    return "@_friendly_imp_@"',
            "  else",
            '    return "반가워!"',
            "  end",
            "}}",
        ]
        self.assertEqual(check_variants(src, translated), [])
        self.assertIn("line_5_no_hangul", check_variants(src, src))
        modified = list(translated)
        modified[1] = '  if you.race() == "Mummy" then'
        self.assertIn("line_2_lua_control_modified",
                      check_variants(src, modified))

    def test_lua_dynamic_return_stays_program_code(self):
        src = ["{{", "return you.genus()", "}}"]
        self.assertEqual(check_variants(src, src), [])
        changed = ["{{", "return you.race()", "}}"]
        # Changing non-displaying Lua expressions must also fail.
        self.assertIn("line_2_no_hangul", check_variants(src, changed))

    def test_counts_and_duplicate_data(self):
        src = "%%%%\nthing\n\n@The_monster@ speaks.\n%%%%\nthing\n\n@The_monster@ shouts.\n%%%%\n"
        ko = "%%%%\nthing\n\n@The_monster@이(가) 말한다.\n%%%%\n"
        result = audit(src, ko)
        self.assertEqual(result["localized_keys"], 1)
        self.assertEqual(result["source_unique_keys"], 1)
        self.assertEqual(result["source_duplicate_key_occurrences"], 1)
        self.assertFalse(result["problems"])


if __name__ == "__main__":
    unittest.main()
