"""Offline tests for the tools the demos give to Claude. No API key needed."""

import json

import pytest

from conftest import load_demo


def test_list_files_shows_workspace_contents(agent):
    assert agent.list_files.call({}).splitlines() == ["brief.md", "sales.csv"]


def test_aggregate_csv_returns_exact_totals_sorted_descending(agent):
    result = agent.aggregate_csv.call({"name": "sales.csv", "group_by": "regione", "value_column": "ricavi_eur"})
    totals = json.loads(result)
    assert totals == {"Nord": 10950.0, "Sud": 8700.0, "Centro": 4800.0}
    assert list(totals) == ["Nord", "Sud", "Centro"]


@pytest.mark.parametrize("name", ["../secret.txt", "../../.env", "/etc/passwd"])
def test_read_file_refuses_paths_outside_workspace(agent, name):
    with pytest.raises(ValueError, match="outside the workspace"):
        agent.safe_path(name)


def test_write_file_saves_when_approved(agent, monkeypatch):
    monkeypatch.setattr(agent.Conferma, "ask", lambda *a, **k: True)
    agent.write_file.call({"name": "report.md", "content": "# Report"})
    assert (agent.WORKSPACE / "report.md").read_text() == "# Report"


def test_write_file_does_nothing_when_declined(agent, monkeypatch):
    monkeypatch.setattr(agent.Conferma, "ask", lambda *a, **k: False)
    result = agent.write_file.call({"name": "report.md", "content": "# Report"})
    assert "rifiutato" in result
    assert not (agent.WORKSPACE / "report.md").exists()


def test_get_order_status_known_and_unknown_orders():
    demo = load_demo("02_tool_use.py")
    assert json.loads(demo.get_order_status("A-1001"))["stato"] == "spedito"
    assert "errore" in json.loads(demo.get_order_status("Z-9999"))
