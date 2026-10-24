"""Minimal regression tests for dat/database Korean overlay audit."""
import tempfile
import unittest
from pathlib import Path
from audit_database_translations import parsed_entries, language_lines, inspect_database


class DatabaseAuditTests(unittest.TestCase):
    def test_comment_directives_and_keys(self):
        source = """# comment
%%%%
# note
Dream sheep flee

w:30
@The_monster@ runs away.

VISUAL:도망친다.
%%%%
Xom lastname

w:20
Xom of Chaos
%%%%
"""
        self.assertEqual([a for a, _ in parsed_entries(source)],
                         ["Dream sheep flee", "Xom lastname"])
        lines = language_lines(source)
        self.assertEqual(lines["korean_lines"], 1)
        self.assertEqual(lines["no_hangul_with_latin"], 2)

    def test_overlay_and_missing_keys(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp) / "source" / "dat" / "database"
            (base / "ko").mkdir(parents=True)
            (base / "godname.txt").write_text(
                "%%%%\nZin lastname\n\nZin the Law-Giver\n%%%%\n"
                "Xom lastname\n\nXom of Chaos\n%%%%\n", encoding="utf-8")
            (base / "ko/godname.txt").write_text(
                "%%%%\nZin lastname\n\n율법의 진\n%%%%\n", encoding="utf-8")
            result = inspect_database(base.parent.parent)
            self.assertEqual(result["original_files"], 1)
            self.assertEqual(result["localized_files"], 1)
            self.assertEqual(result["localized_matched_keys_sum"], 1)
            self.assertEqual(result["files"][0]["missing_localized_keys"], 1)
            self.assertFalse(result["issues"])


    def test_long_separator_is_new_entry(self):
        from audit_database_translations import parsed_entries
        text = "%%%%\nfirst cast\n\nfirst\n%%%%%\nsecond cast\n\nsecond\n%%%%\n"
        self.assertEqual([key for key, _ in parsed_entries(text)],
                         ["first cast", "second cast"])


if __name__ == "__main__":
    unittest.main()
