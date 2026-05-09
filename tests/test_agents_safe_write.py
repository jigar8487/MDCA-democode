"""Tests for agent_write_guard.safe_write path and extension rules."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import agent_write_guard


class TestSafeWrite(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_root = agent_write_guard.REPO_ROOT
        self._orig_gen = agent_write_guard.GENERATED_APP_DIR
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        agent_write_guard.REPO_ROOT = root
        agent_write_guard.GENERATED_APP_DIR = root / "generated_app"

    def tearDown(self) -> None:
        agent_write_guard.REPO_ROOT = self._orig_root
        agent_write_guard.GENERATED_APP_DIR = self._orig_gen

    def test_writes_under_generated_app(self) -> None:
        rel = "generated_app/demo/backend/Program.cs"
        out = agent_write_guard.safe_write(rel, "// ok")
        self.assertIsNotNone(out)
        self.assertTrue(out.is_file())
        self.assertEqual(out.read_text(), "// ok")

    def test_rejects_traversal(self) -> None:
        self.assertIsNone(
            agent_write_guard.safe_write("generated_app/demo/../../evil.txt", "x")
        )

    def test_rejects_outside_generated_app(self) -> None:
        self.assertIsNone(agent_write_guard.safe_write("README.md", "x"))

    def test_rejects_bad_extension(self) -> None:
        self.assertIsNone(
            agent_write_guard.safe_write("generated_app/demo/foo.bin", "x")
        )

    def test_allows_dockerfile(self) -> None:
        rel = "generated_app/demo/Dockerfile"
        out = agent_write_guard.safe_write(rel, "FROM scratch\n")
        self.assertIsNotNone(out)
        self.assertEqual(out.read_text(), "FROM scratch\n")


if __name__ == "__main__":
    unittest.main()
