#!/usr/bin/env python3
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(SCRIPTS))
from cache_engine import SemanticCache, cosine_similarity


class TestSemanticCache(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp(prefix="test_cache_")
        self.db_path = Path(self.td) / "cache.db"
        self.cache = SemanticCache(self.db_path)

    def tearDown(self):
        shutil.rmtree(self.td, ignore_errors=True)

    def test_01_cache_hit_identical(self):
        q = "How do I configure git worktrees for parallel agents?"
        ans = "Use 'git worktree add <path> -b <branch>' and pre-claim file lines."
        self.cache.set(q, ans)

        res = self.cache.get(q, threshold=0.90)
        self.assertTrue(res["hit"])
        self.assertEqual(res["answer"], ans)
        self.assertGreaterEqual(res["similarity"], 0.95)
        print("  ✓ identical hit · verified")

    def test_02_cache_hit_paraphrase(self):
        q1 = "How do I configure git worktrees for parallel agents?"
        ans = "Use 'git worktree add <path> -b <branch>' and pre-claim file lines."
        self.cache.set(q1, ans)

        q2 = "How to configure git worktrees for parallel subagents?"
        res = self.cache.get(q2, threshold=0.75)
        if self.cache.embedder.last_source != "endpoint":
            self.skipTest(
                "paraphrase recall is a property of the embedding model on :8087; "
                f"the engine fell back to {self.cache.embedder.last_source} "
                f"and scored {res.get('best_similarity', 0):.3f} against a 0.75 threshold"
            )
        self.assertTrue(res["hit"])
        self.assertEqual(res["answer"], ans)
        print("  ✓ paraphrase hit · verified")

    def test_03_cache_miss_unrelated(self):
        q1 = "How do I configure git worktrees for parallel agents?"
        ans = "Use 'git worktree add <path> -b <branch>' and pre-claim file lines."
        self.cache.set(q1, ans)

        q2 = "What is the capital city of Australia?"
        res = self.cache.get(q2, threshold=0.75)
        self.assertFalse(res["hit"])
        print("  ✓ unrelated miss · verified")

    def test_04_stats_and_purge(self):
        self.cache.set("q1", "a1")
        self.cache.set("q2", "a2")
        self.cache.get("q1")
        st = self.cache.stats()
        self.assertEqual(st["total_entries"], 2)
        self.assertEqual(st["total_cache_hits"], 1)

        purged = self.cache.purge()
        self.assertEqual(purged, 2)
        st2 = self.cache.stats()
        self.assertEqual(st2["total_entries"], 0)
        print("  ✓ stats and purge · verified")

    def test_05_fallback_embedding_survives_a_restart(self):
        code = (
            "import sys; sys.path.insert(0, %r)\n"
            "from cache_engine import LocalEmbedder\n"
            "e = LocalEmbedder(endpoint='http://127.0.0.1:1/v1/embeddings')\n"
            "v = e.embed('git worktrees for parallel agents')\n"
            "print(','.join(f'{x:.6f}' for x in v))\n"
        ) % str(SCRIPTS)
        outs = []
        for _ in range(2):
            proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            outs.append(proc.stdout.strip())
        self.assertEqual(outs[0], outs[1], "the fallback vector changed between processes")
        self.assertEqual(len(outs[0].split(",")), 128)
        print("  ✓ fallback embedding is identical across processes")


if __name__ == "__main__":
    print("\n🧪 Running Semantic Cache Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSemanticCache)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
