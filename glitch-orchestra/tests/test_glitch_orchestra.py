#!/usr/bin/env python3
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent / "scripts"))
from orchestra_conductor import OrchestraConductor


class TestGlitchOrchestra(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.mkdtemp(prefix="test_orchestra_")
        self.conductor = OrchestraConductor(Path(self.td))

    def tearDown(self):
        shutil.rmtree(self.td, ignore_errors=True)

    def test_01_session_lifecycle(self):
        s = self.conductor.register_child_session("subagent_01", "Refactor models", "tty_01")
        self.assertEqual(s["status"], "running")

        st1 = self.conductor.status()
        self.assertEqual(st1["active_count"], 1)

        evidence = Path(self.td) / "lifecycle.json"
        evidence.write_text('{"status": "ok"}', encoding="utf-8")
        c = self.conductor.mark_session_complete("subagent_01", "Models refactored cleanly", evidence=str(evidence))
        self.assertEqual(c["status"], "completed")
        self.assertTrue(c["verified"])

        st2 = self.conductor.status()
        self.assertEqual(st2["active_count"], 0)
        self.assertEqual(st2["completed_count"], 1)
        self.assertEqual(st2["verified_count"], 1)
        print("  ✓ session lifecycle · completed with evidence")

    def test_02_completion_alert(self):
        res = self.conductor.trigger_completion_alert("Run complete")
        self.assertEqual(res["alert_message"], "Run complete")
        self.assertTrue(res["bell_emitted"])
        print("  ✓ completion alert · bell emitted")

    def test_03_evidence_gate(self):
        self.conductor.register_child_session("subagent_02", "Ship checkout", "tty_02")
        evidence = Path(self.td) / "verify.json"
        evidence.write_text('{"verdict": "pass"}', encoding="utf-8")
        c = self.conductor.mark_session_complete("subagent_02", "Checkout shipped", evidence=str(evidence))
        self.assertTrue(c["verified"])
        self.assertEqual(c["evidence"], str(evidence.resolve()))
        self.assertEqual(self.conductor.status()["verified_count"], 1)

        self.conductor.register_child_session("subagent_03", "Claim without proof", "tty_03")
        with self.assertRaises(FileNotFoundError):
            self.conductor.mark_session_complete("subagent_03", "Trust me", evidence=str(Path(self.td) / "missing.json"))

        u = self.conductor.mark_session_complete("subagent_03", "Trust me")
        self.assertFalse(u["verified"])
        print("  ✓ evidence gate · missing artifact refused, unverified completion labelled")


if __name__ == "__main__":
    print("\n🧪 Running Glitch Orchestra Test Suite:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGlitchOrchestra)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
