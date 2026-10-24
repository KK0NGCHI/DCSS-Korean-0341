"""Unit tests for the conservative translation review queue."""
import csv
import tempfile
import unittest
from pathlib import Path

from triage_visible_v1 import load_queue, normalize, review_kind, tier, write_queue


class TriageTests(unittest.TestCase):
    def test_normalize_and_kind(self):
        self.assertEqual(normalize('"You   feel\nbetter."'), "You feel better.")
        self.assertEqual(review_kind("괴물이 보인다."), "contains_hangul")
        self.assertEqual(review_kind("You feel better."), "review_english_or_identifier")
        self.assertEqual(review_kind("%d / %s"), "review_english_or_identifier")
        self.assertEqual(tier("player.cc"), "P0")
        self.assertEqual(tier("dat/dlua/init.lua"), "P1")

    def test_queue_deduplicates_with_locations_and_keeps_korean_separate(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            inv = base / "strings.csv"
            fields = ["path", "line", "column", "family", "literal", "status"]
            items = [
                ("player.cc", "10", "2", "cc", '"You feel better."', "visible_candidate"),
                ("message.cc", "20", "5", "cc", '"You feel better."', "review_dynamic"),
                ("beam.cc", "30", "2", "cc", '"몸이 나아진다."', "visible_candidate"),
                ("player.cc", "40", "2", "cc", '"Error: %s"', "internal_candidate"),
                ("dat/descript/items.txt", "1", "1", "description", '"Description"', "visible_candidate"),
            ]
            with inv.open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                for item in items:
                    writer.writerow(dict(zip(fields, item)))
            groups, counts, skipped = load_queue(inv)
            self.assertEqual(len(groups), 2)
            self.assertEqual(counts["visible_candidate"], 2)
            self.assertEqual(counts["review_dynamic"], 1)
            self.assertEqual(groups["You feel better."]["occurrences"], 2)
            self.assertEqual(groups["You feel better."]["priority"], "P0")
            self.assertEqual(len(groups["You feel better."]["locations"]), 2)
            self.assertEqual(skipped["other_status"], 1)
            self.assertEqual(skipped["non_code"], 1)
            write_queue(groups, base / "triage")
            with (base / "triage/p0_english_review.csv").open(
                encoding="utf-8-sig", newline=""
            ) as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["literal"], "You feel better.")
            self.assertEqual(rows[0]["occurrences"], "2")


if __name__ == "__main__":
    unittest.main()
