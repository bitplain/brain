from __future__ import annotations

import os
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "site"


class KnowledgeBaseBuildTests(unittest.TestCase):
    @staticmethod
    def _next_stale_dir(path: Path) -> Path:
        candidate = path.with_name(f"{path.name}.stale-root")
        index = 2
        while candidate.exists():
            candidate = path.with_name(f"{path.name}.stale-root-{index}")
            index += 1
        return candidate

    @classmethod
    def setUpClass(cls) -> None:
        if SITE_DIR.exists():
            for path in SITE_DIR.rglob("*"):
                try:
                    os.chmod(path, 0o755 if path.is_dir() else 0o644)
                except PermissionError:
                    pass
            try:
                os.chmod(SITE_DIR, 0o755)
            except PermissionError:
                pass
            try:
                shutil.rmtree(SITE_DIR)
            except PermissionError:
                stale_dir = cls._next_stale_dir(SITE_DIR)
                SITE_DIR.rename(stale_dir)

        subprocess.run(
            ["python3", "scripts/zensical_cli.py", "build"],
            cwd=REPO_ROOT,
            check=True,
        )

        cls.home = (SITE_DIR / "index.html").read_text(encoding="utf-8")
        cls.instructions = (SITE_DIR / "instructions" / "index.html").read_text(encoding="utf-8")
        cls.rdp = (SITE_DIR / "instructions" / "remote-desktop" / "index.html").read_text(
            encoding="utf-8"
        )
        cls.vipnet = (
            SITE_DIR / "instructions" / "vipnet-client-windows" / "index.html"
        ).read_text(encoding="utf-8")

    def test_home_page_uses_dark_branding_and_explicit_navigation(self) -> None:
        self.assertIn('data-md-color-scheme="slate"', self.home)
        self.assertIn("База знаний Cofi", self.home)
        self.assertIn("Главная", self.home)
        self.assertIn("Инструкции", self.home)

    def test_brand_assets_are_local(self) -> None:
        self.assertIn("assets/branding/cofi-logo", self.home)
        self.assertIn("assets/branding/cofi-favicon", self.home)
        self.assertNotIn("static.tildacdn.com", self.home)
        self.assertNotIn("https://cofi.ru", self.home)

    def test_remote_desktop_page_is_part_of_the_knowledge_base(self) -> None:
        self.assertIn("Подключение к удалённому рабочему столу", self.rdp)
        self.assertIn(r"inf.co.fi\пользователь", self.rdp)
        self.assertIn('../../assets/instructions/rdp-icon.png', self.rdp)
        self.assertIn('../../assets/instructions/rdp-login.png', self.rdp)
        self.assertNotIn('src="../assets/instructions/rdp-icon.png"', self.rdp)
        self.assertNotIn('src="../assets/instructions/rdp-login.png"', self.rdp)
        self.assertIn("Инструкции", self.rdp)

    def test_vipnet_page_is_listed_in_the_instructions_section(self) -> None:
        self.assertIn("Установка ViPNet Client на Windows", self.instructions)
        self.assertIn('href="vipnet-client-windows/"', self.instructions)
        self.assertIn("Установка ViPNet Client на Windows", self.home)

    def test_vipnet_page_uses_local_assets_and_masks_sensitive_data(self) -> None:
        self.assertIn("Установка ViPNet Client на Windows", self.vipnet)
        self.assertIn('../../assets/instructions/vipnet-client-01.png', self.vipnet)
        self.assertIn('../../assets/instructions/vipnet-client-02.png', self.vipnet)
        self.assertIn('../../assets/instructions/vipnet-client-04.png', self.vipnet)
        self.assertIn('../../assets/instructions/vipnet-client-08.png', self.vipnet)
        self.assertIn('../../assets/instructions/vipnet-client-10.png', self.vipnet)
        self.assertNotIn("Alexander", self.vipnet)
        self.assertNotIn("audit", self.vipnet)
        self.assertNotIn("n.mirzoyan", self.vipnet)


if __name__ == "__main__":
    unittest.main()
