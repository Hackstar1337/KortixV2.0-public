#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MANAGE = ROOT / "selfhost" / "manage.py"
TEMPLATE = ROOT / "selfhost" / "compose.template.yml"


class ManageContractTests(unittest.TestCase):
    def run_manager(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(MANAGE), *args],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
        )

    def init(self, directory: Path, callback: str = "https://api.example.com", extra: list[str] | None = None) -> tuple[subprocess.CompletedProcess[str], Path]:
        directory.mkdir(parents=True, exist_ok=True)
        credentials = directory / "docker-cloud-input.env"
        credentials.write_text("DOCKER_CLOUD_USERNAME=synthetic-docker-id\nDOCKER_CLOUD_PAT=synthetic-cloud-pat\n", encoding="utf-8")
        command = [
            "init", "--instance-dir", str(directory),
            "--callback-url", callback,
            "--frontend-url", "https://app.example.com",
            "--docker-cloud-credentials", str(credentials),
        ]
        if extra:
            command.extend(extra)
        return self.run_manager(*command), credentials

    def test_init_is_private_and_reuses_source_compose_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw) / "instance"
            result, _ = self.init(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((directory / "config.json").is_file())
            self.assertTrue((directory / ".env").is_file())
            self.assertTrue((directory / "docker-compose.docker-cloud.yml").is_file())
            self.assertIn("migrate.ts", (directory / "docker-compose.yml").read_text(encoding="utf-8"))
            self.assertIn("bootstrap", (directory / "docker-compose.yml").read_text(encoding="utf-8"))
            self.assertNotIn("synthetic-cloud-pat", (directory / ".env").read_text(encoding="utf-8"))
            overlay = json.loads((directory / "docker-compose.docker-cloud.yml").read_text(encoding="utf-8"))
            self.assertEqual(list(overlay["services"]), ["kortix-api"])
            self.assertEqual(overlay["services"]["kortix-api"]["env_file"], [".env", ".docker-cloud.env"])
            if os.name != "nt":
                self.assertEqual((directory / ".env").stat().st_mode & 0o077, 0)
                self.assertEqual((directory / "config.json").stat().st_mode & 0o077, 0)
                self.assertEqual((directory / ".docker-cloud.env").stat().st_mode & 0o077, 0)

    def test_production_rejects_localhost_and_quick_tunnel(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            for index, callback in enumerate(("http://localhost:8008", "https://api.trycloudflare.com")):
                result, _ = self.init(base / f"invalid-{index}", callback)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("production callback", result.stderr)

    def test_development_can_use_localhost_but_reports_warning(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw) / "instance"
            result, _ = self.init(directory, "http://localhost:8008", ["--mode", "development"])
            self.assertEqual(result.returncode, 0, result.stderr)
            doctor = self.run_manager("doctor", "--instance-dir", str(directory))
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            report = json.loads(doctor.stdout)
            self.assertTrue(any("development mode" in item for item in report["warnings"]))

    def test_start_is_plan_first_and_exposes_validated_resources(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw) / "instance"
            result, _ = self.init(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = self.run_manager("start", "--instance-dir", str(directory))
            self.assertEqual(plan.returncode, 0, plan.stderr)
            report = json.loads(plan.stdout)
            self.assertFalse(report["apply"])
            self.assertEqual(report["docker_cloud_resources"], {"cpu_cores": 2, "memory_gib": 4})
            self.assertFalse(report["deletes_data"])

    def test_named_tunnel_token_is_a_file_reference_not_an_argument_value(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            directory = base / "instance"
            token_file = base / "cloudflared-token.txt"
            token_file.write_text("synthetic-named-tunnel-token\n", encoding="utf-8")
            result, _ = self.init(directory, "https://api.example.com", ["--named-tunnel-token-file", str(token_file)])
            self.assertEqual(result.returncode, 0, result.stderr)
            config = json.loads((directory / "config.json").read_text(encoding="utf-8"))
            self.assertEqual(config["tunnel_token_file"], str(token_file.resolve()))
            self.assertNotIn("synthetic-named-tunnel-token", result.stdout)
            env = (directory / ".env").read_text(encoding="utf-8")
            self.assertNotIn("synthetic-named-tunnel-token", env)

    def test_stop_plan_does_not_delete(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw) / "instance"
            result, _ = self.init(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = self.run_manager("stop", "--instance-dir", str(directory))
            self.assertEqual(plan.returncode, 0, plan.stderr)
            report = json.loads(plan.stdout)
            self.assertFalse(report["apply"])
            self.assertFalse(report["deletes_data"])
            self.assertTrue((directory / ".env").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
