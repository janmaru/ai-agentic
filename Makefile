PY := .venv/bin/python
BIN := .venv/bin

.PHONY: setup serve build demo1 demo2 demo3 clean

setup:
	python3 -m venv .venv
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt
	@test -f .env || cp .env.example .env

serve:            ## live-reload slides at http://localhost:8000
	$(BIN)/mkslides serve slides

build:            ## static HTML into ./site
	$(BIN)/mkslides build slides

demo1:
	$(PY) demo/01_simple_llm_call.py

demo2:
	$(PY) demo/02_tool_use.py

demo3:
	$(PY) demo/03_agent_loop.py

clean:
	rm -rf site demo/workspace/report.md
