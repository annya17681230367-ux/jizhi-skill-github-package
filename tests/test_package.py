import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = os.environ.get("TEST_PYTHON", sys.executable)
FIXTURES = ROOT / "tests/fixtures"


def run(*args, check=True, env=None):
    return subprocess.run([str(x) for x in args], cwd=ROOT, text=True, capture_output=True, check=check, env=env)


class PackageTests(unittest.TestCase):
    def test_route_matrix(self):
        cases = {
            "做全年学业规划陪跑方案": ("jizhi-academic-year-plan-proposal", "single"),
            "做纯DP安心包方案": ("dp-proposal-designer", "single"),
            "做DP产品价格": ("dp-product-new-customer-quote", "single"),
            "做安心包报价": ("dp-product-new-customer-quote", "single"),
            "做DP全包作业方案并报价": ("dp-proposal-designer", "dp_proposal_with_quote"),
            "两门DP，一门陪跑并报价": ("jizhi-academic-year-plan-proposal", "mixed")
        }
        for text, expected in cases.items():
            result = json.loads(run(PYTHON, "scripts/route_request.py", text).stdout)
            self.assertEqual((result["owner"], result["mode"]), expected, text)

    def test_annual_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp)/"a.html", Path(tmp)/"b.html"
            script = "skills/jizhi-academic-year-plan-proposal/scripts/build_planning_proposal.py"
            run(PYTHON, script, FIXTURES/"annual.json", a)
            run(PYTHON, script, FIXTURES/"annual.json", b)
            self.assertEqual(hashlib.sha256(a.read_bytes()).digest(), hashlib.sha256(b.read_bytes()).digest())
            text = a.read_text(encoding="utf-8")
            for label in ("六大学业规划模块", "AI智慧学习系统", "每日 / 每周 / 每月执行"):
                self.assertIn(label, text)

    def test_dp_proposal_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp)/"a.html", Path(tmp)/"b.html"
            script = "skills/dp-proposal-designer/scripts/build_dp_proposal.py"
            run(PYTHON, script, FIXTURES/"dp_proposal.json", a)
            run(PYTHON, script, FIXTURES/"dp_proposal.json", b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            text = a.read_text(encoding="utf-8")
            self.assertIn("v2 官网检索版", text)
            self.assertIn("DP安心包核心价值", text)

    def test_quote_workbook(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/"quote.xlsx"
            run(PYTHON, "skills/dp-product-new-customer-quote/scripts/build_quote_workbook.py", FIXTURES/"dp_assessment.json", output, "--quote-json", FIXTURES/"dp_quote.json")
            from openpyxl import load_workbook
            wb = load_workbook(output, data_only=False)
            ws = wb["课程考核与DP报价"]
            values = [cell.value for row in ws.iter_rows() for cell in row]
            self.assertIn(12000, values)
            self.assertIn("折后价", values)
            self.assertEqual(ws["M10"].hyperlink.target, "https://example.edu/module")

    def test_install_quarantines_retired_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            retired = home/"skills/dp-customer-visual-proposal"
            retired.mkdir(parents=True)
            (retired/"SKILL.md").write_text("old", encoding="utf-8")
            env = os.environ.copy(); env["CODEX_HOME"] = str(home)
            result = run("bash", "install.sh", env=env)
            self.assertIn("Quarantined retired competing skill", result.stdout)
            self.assertEqual(len(list((home/"skills").glob("*/SKILL.md"))), 3)

            output = home / "smoke"
            output.mkdir()
            run(PYTHON, home/"skills/jizhi-academic-year-plan-proposal/scripts/build_planning_proposal.py", FIXTURES/"annual.json", output/"annual.html")
            run(PYTHON, home/"skills/dp-proposal-designer/scripts/build_dp_proposal.py", FIXTURES/"dp_proposal.json", output/"dp.html")
            run(
                PYTHON,
                home/"skills/dp-product-new-customer-quote/scripts/build_quote_workbook.py",
                FIXTURES/"dp_assessment.json",
                output/"quote.xlsx",
                "--quote-json",
                FIXTURES/"dp_quote.json",
            )
            for artifact in (output/"annual.html", output/"dp.html", output/"quote.xlsx"):
                self.assertGreater(artifact.stat().st_size, 0, artifact.name)

    def test_audit(self):
        result = run(PYTHON, "scripts/audit_boundaries.py")
        self.assertIn("PASS", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
