"""Tests for conservative DCSS monster spell data validators."""
import unittest

from audit_monspell_ko import parse, structural_issues, audit


class MonsterSpellKoreanAuditTests(unittest.TestCase):
    def test_key_lookup_and_preserve_weight_variants(self):
        en = "%%%%\nVv cast\n\nVISUAL:@The_monster@ gestures.\n\nw:3\nVISUAL:@The_monster@ stamps its foot.\n%%%%\n"
        ko = "%%%%\nVv cast\n\nVISUAL:@The_monster@이(가) 손짓한다.\n\nw:3\nVISUAL:@The_monster@이(가) 발을 구른다.\n%%%%\n"
        self.assertEqual(audit(en, ko)["issues"], [])
        missing_weight = ko.replace("w:3\n", "")
        self.assertIn("weight_list", structural_issues(
            parse(en)[0]["Vv cast"], parse(missing_weight)[0]["Vv cast"]))

    def test_required_macros_and_optional_grammar(self):
        source = ["@The_monster@ fires @beam@ @at@ @target@."]
        target = ["@The_monster@이(가) @target@에게 @beam@을(를) 발사한다."]
        self.assertEqual(structural_issues(source, target), [])
        broken = ["@The_monster@이(가) @beam@을(를) 발사한다."]
        self.assertIn("line_1_required_markers", structural_issues(source, broken))

    def test_alternatives_and_unchanged_source_keys(self):
        src = "%%%%\nmonster cast\n\n@The_monster@ [sings|chants].\n%%%%\n"
        translated = "%%%%\nmonster cast\n\n@The_monster@이(가) [노래한다|주문을 외운다].\n%%%%\n"
        self.assertEqual(audit(src, translated)["issues"], [])
        self.assertTrue(audit(src, translated.replace("|주문을 외운다", ""))["issues"])

    def test_unknown_and_duplicate(self):
        src = "%%%%\na cast\n\nCast.\n%%%%\n"
        target = ("%%%%\na cast\n\n시전한다.\n%%%%\n"
                  "%%%%\na cast\n\n또 시전한다.\n%%%%\n")
        result = audit(src, target)
        self.assertTrue(any(e["issue"] == "duplicate_korean_key"
                            for e in result["issues"]))


if __name__ == "__main__":
    unittest.main()
