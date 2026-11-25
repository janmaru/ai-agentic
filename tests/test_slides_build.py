"""The deck must build cleanly - catches a broken mkslides.yml or a library upgrade."""

import subprocess
import sys
from pathlib import Path

from conftest import ROOT


def test_slides_build(tmp_path):
    mkslides = Path(sys.executable).with_name("mkslides")
    subprocess.run(
        [mkslides, "build", "slides", "-f", "mkslides.yml", "-d", tmp_path / "site"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    html = (tmp_path / "site" / "index.html").read_text(encoding="utf-8")
    assert "RevealMermaid" in html
    assert "theme.css" in html
