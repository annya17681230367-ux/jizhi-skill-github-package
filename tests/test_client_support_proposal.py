import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
FIXTURE = ROOT / "tests/fixtures/client_support_sim_dit.json"
SCRIPT = ROOT / "skills/jizhi-academic-year-plan-proposal/scripts/build_client_support_proposal.py"


class ClientSupportProposalTests(unittest.TestCase):
    def test_client_support_proposal_renders_expected_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "client.html"
            subprocess.run([PYTHON, SCRIPT, FIXTURE, output], cwd=ROOT, check=True)
            text = output.read_text(encoding="utf-8")
            for marker in (
                "新生首年",
                "学业护航方案",
                "专业课 51 节 / 75%",
                "陪跑课 17 节 / 25%",
                "课程风险与服务匹配",
                "Programming Foundations",
                "AI 智慧学习系统",
            ):
                self.assertIn(marker, text)
            for forbidden in (
                "我们不会只给家长一句",
                "给学生的价值",
                "客户价值",
                "方案亮点",
                "保证通过",
                "100%通过",
                "内部审核",
                "模型估算",
            ):
                self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
