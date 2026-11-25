"""Make the demo scripts importable. Their names start with a digit, so load them by path."""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = ROOT / "demo"
sys.path.insert(0, str(DEMO_DIR))  # demos do `from common import ...`


def load_demo(filename: str):
    spec = importlib.util.spec_from_file_location(filename.removesuffix(".py"), DEMO_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def agent(tmp_path, monkeypatch):
    """Demo-3 module with its workspace redirected to a temp copy of the real one."""
    module = load_demo("03_agent_loop.py")
    for src in (DEMO_DIR / "workspace").iterdir():
        if src.is_file() and src.name != "report.md":
            (tmp_path / src.name).write_bytes(src.read_bytes())
    monkeypatch.setattr(module, "WORKSPACE", tmp_path.resolve())
    return module
