"""Tests for P0 output-callsite scanning (no game build required)."""
import tempfile
import unittest
from pathlib import Path
from audit_p0_callsites import classify, end_of_call, masked_code, scan_file


class CallsiteAuditTests(unittest.TestCase):
    def test_comments_and_quotes_do_not_appear_as_calls(self):
        source = """// mpr("not live");
const char* txt = "mpr(\\"not a call\\")";
/* yesno("comment"); */
mpr("You feel better.");
mprf(MSGCH_WARN, "Target: %s", foo("anything"));
"""
        mask = masked_code(source)
        self.assertEqual(mask.count("mpr("), 1)
        self.assertEqual(mask.count("mprf("), 1)
        start = mask.index("mprf(")
        end = end_of_call(mask, mask.index("(", start))
        self.assertTrue(source[start:end + 1].endswith('foo("anything"))'))

    def test_languages_and_channels(self):
        self.assertEqual(classify("You feel better.", "mpr(\"You feel better.\")"),
                         "english_output_review")
        self.assertEqual(classify("HP가 줄었다.", "mpr(\"HP가 줄었다.\")"),
                         "contains_hangul")
        self.assertEqual(classify("%s", 'mprf("%s")'), "format_or_symbol_only")
        self.assertEqual(classify("Lua error: %s", 'mprf(MSGCH_ERROR, "Lua error: %s")'),
                         "developer_or_error_review")

    def test_scan_source_and_keep_addresses(self):
        with tempfile.TemporaryDirectory() as base:
            path = Path(base) / "message.cc"
            path.write_text(
                '// mpr("ignored");\n'
                'mpr("You see a monster.");\n'
                'mpr("몬스터가 보인다.");\n'
                'mprf(MSGCH_WARN, "Warning: %s", name.c_str());\n',
                encoding="utf-8")
            entries = scan_file(path, "message.cc")
            self.assertEqual([x["line"] for x in entries], [2, 3, 4])
            self.assertEqual(entries[0]["classification"], "english_output_review")
            self.assertEqual(entries[1]["classification"], "contains_hangul")
            self.assertEqual(entries[2]["format_specifiers"], 1)


if __name__ == "__main__":
    unittest.main()
