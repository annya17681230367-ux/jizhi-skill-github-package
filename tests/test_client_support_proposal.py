import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
FIXTURE = ROOT / "tests/fixtures/client_support_sim_dit.json"
SCRIPT = ROOT / "skills/jizhi-academic-year-plan-proposal/scripts/build_client_support_proposal.py"


class ClientSupportProposalTests(unittest.TestCase):
    def test_client_support_proposal_defaults_to_ucl_master(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "client.html"
            subprocess.run([PYTHON, SCRIPT, FIXTURE, output], cwd=ROOT, check=True)
            text = output.read_text(encoding="utf-8")
            for marker in (
                "全年学业规划",
                "课程的服务路径配置",
                "学情判断与全年目标",
                "全年节点推进",
                "执行责任",
                "预期效果与正式执行条件",
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

    def test_client_support_proposal_keeps_sim_variant_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = json.loads(FIXTURE.read_text(encoding="utf-8"))
            data["visual_style"] = "sim_dit"
            source = Path(tmp) / "sim.json"
            output = Path(tmp) / "client.html"
            source.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            subprocess.run([PYTHON, SCRIPT, source, output], cwd=ROOT, check=True)
            text = output.read_text(encoding="utf-8")
            for marker in (
                "新生首年",
                "学业护航方案",
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
