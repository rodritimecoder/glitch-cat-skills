#!/usr/bin/env python3
import json
import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))
from notes_index_core import NotesIndex, apply_rule, mask_secrets, plan  # noqa: E402


class TestNotesIndex(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp(prefix="test_notes_index_")
        self.folder = Path(self.td)
        self.index = NotesIndex(self.folder)

    def tearDown(self):
        self.index.close()
        shutil.rmtree(self.td, ignore_errors=True)

    def write(self, name: str, body: str) -> Path:
        path = self.folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return path

    def test_01_update_indexes_notes(self):
        self.write("2026-01-01-alpha.md", "# Alpha\n\nThe retrieval pipeline uses bm25 ranking.\n")
        self.write("2026-02-02-beta.md", "# Beta\n\nSwarm contracts enforce a budget ceiling.\n")
        report = self.index.update(use_summarizer=False)
        self.assertEqual(report.files_total, 2)
        self.assertEqual(report.new_files, 2)
        self.assertEqual(self.index.status()["rows"], 2)
        print("  ✓ first pass indexes every note")

    def test_02_unchanged_files_are_skipped(self):
        self.write("note.md", "# Note\n\nstable content about orchestration\n")
        self.index.update(use_summarizer=False)
        second = self.index.update(use_summarizer=False)
        self.assertEqual(second.unchanged_files, 1)
        self.assertEqual(second.new_files, 0)
        print("  ✓ unchanged notes are skipped")

    def test_03_changed_file_is_reindexed(self):
        path = self.write("note.md", "# Note\n\nfirst version\n")
        self.index.update(use_summarizer=False)
        path.write_text("# Note\n\nsecond version with different words\n", encoding="utf-8")
        report = self.index.update(use_summarizer=False)
        self.assertEqual(report.changed_files, 1)
        hits = self.index.search("different words")
        self.assertTrue(any(hit.path == "note.md" for hit in hits))
        print("  ✓ changed notes are re-indexed")

    def test_04_removed_file_rows_are_deleted(self):
        path = self.write("gone.md", "# Gone\n\ntemporary content\n")
        self.index.update(use_summarizer=False)
        self.assertEqual(self.index.status()["rows"], 1)
        path.unlink()
        report = self.index.update(use_summarizer=False)
        self.assertEqual(report.removed_files, 1)
        self.assertEqual(self.index.status()["rows"], 0)
        print("  ✓ removed notes leave no rows behind")

    def test_05_search_returns_ranked_hits(self):
        self.write("2026-03-03-graph.md", "# Graph\n\nKnowledge graph traversal with sqlite k-hop walks.\n")
        self.write("2026-03-04-cache.md", "# Cache\n\nSemantic cache bypass with vector cosine similarity.\n")
        self.index.update(use_summarizer=False)
        hits = self.index.search("graph traversal")
        self.assertTrue(hits)
        self.assertIn("graph", hits[0].path)
        self.assertTrue(hits[0].full_path.endswith(".md"))
        print("  ✓ search ranks the right note first")

    def test_06_search_respects_after_filter(self):
        self.write("2020-01-01-old.md", "# Old\n\nhistorical decision about indexing\n")
        self.write("2026-05-05-new.md", "# New\n\nrecent decision about indexing\n")
        self.index.update(use_summarizer=False)
        hits = self.index.search("indexing", after="2025-01-01")
        self.assertTrue(hits)
        self.assertTrue(all(hit.path.startswith("2026") for hit in hits))
        print("  ✓ --after filters out old notes")

    def test_07_health_line_shape(self):
        self.write("note.md", "# Note\n\ncontent\n")
        self.index.update(use_summarizer=False)
        health = self.index.health_line()
        self.assertIn("rows |", health)
        self.assertIn("last refreshed", health)
        self.assertIn("last error: none", health)
        print("  ✓ health line carries rows, freshness and error")

    def test_08_long_file_is_chunked_into_raw_rows(self):
        self.write("long.md", "# Long\n\n" + ("x" * 9000))
        report = self.index.update(use_summarizer=False)
        kinds = self.index.status()["rows_by_kind"]
        self.assertEqual(kinds.get("raw"), 3)
        print("  ✓ long notes become 4000-char raw rows")

    def test_09_secrets_are_masked_before_storage(self):
        fake_key = "sk-" + "abcdefghijklmnop1234"
        fake_aws = "AKIA" + "IOSFODNN7EXAMPLE"
        self.write("secret.md", f"# Secret\n\napi_key = {fake_key} and {fake_aws}\n")
        self.index.update(use_summarizer=False)
        conn = sqlite3.connect(str(self.index.db_path))
        stored = " ".join(row[0] for row in conn.execute("SELECT text FROM rows"))
        conn.close()
        self.assertNotIn(fake_key, stored)
        self.assertNotIn(fake_aws, stored)
        self.assertIn("sk-***", stored)
        print("  ✓ secrets are masked before they hit the database")

    def test_10_stale_lock_does_not_block(self):
        lock = self.folder / ".notes-index.lock"
        lock.write_text("999999", encoding="utf-8")
        self.write("note.md", "# Note\n\ncontent\n")
        report = self.index.update(use_summarizer=False)
        self.assertEqual(report.files_total, 1)
        print("  ✓ a dead lock is ignored, not a blocker")

    def test_11_rule_block_is_idempotent(self):
        script = self.folder / "index.py"
        script.write_text("#\n", encoding="utf-8")
        apply_rule(self.folder, script, "full")
        apply_rule(self.folder, script, "lean")
        text = (self.folder / "AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(text.count("notes-index:start"), 1)
        self.assertIn("don't also grep", text)
        print("  ✓ the AGENTS.md rule is rewritten, never duplicated")

    def test_14_rule_target_agents_by_default(self):
        script = self.folder / "index.py"
        script.write_text("#\n", encoding="utf-8")
        path = apply_rule(self.folder, script, "full")
        self.assertEqual(path.name, "AGENTS.md")
        self.assertTrue(path.exists())
        self.assertFalse((self.folder / "CLAUDE.md").exists())
        print("  ✓ the rule lands in AGENTS.md by default")

    def test_15_rule_target_claude_on_request(self):
        script = self.folder / "index.py"
        script.write_text("#\n", encoding="utf-8")
        path = apply_rule(self.folder, script, "full", "claude")
        self.assertEqual(path.name, "CLAUDE.md")
        print("  ✓ CLAUDE.md is still available on request")

    def test_12_plan_counts_long_files(self):
        self.write("short.md", "short\n")
        self.write("long.md", "y" * 9000)
        result = plan(self.folder)
        self.assertEqual(result["files"], 2)
        self.assertEqual(result["long_files"], 1)
        print("  ✓ the first-pass plan counts notes and summaries")

    def test_13_mask_secrets_helper(self):
        masked = mask_secrets("token: ghp_abcdefghijklmnopqrstuvwxyz012345")
        self.assertNotIn("ghp_abcdefghijklmnopqrstuvwxyz012345", masked)
        print("  ✓ secret masking covers the common key shapes")


if __name__ == "__main__":
    unittest.main(verbosity=2)
