PY := .venv/bin/python
BIN := .venv/bin

.PHONY: setup serve build test demo1 demo2 demo3 api-demo1 api-demo2 api-demo3 clean

setup:
	python3 -m venv .venv
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt
	@test -f .env || cp .env.example .env

serve:            ## live-reload slides at http://localhost:8000
	$(BIN)/mkslides serve slides

build:            ## static HTML into ./site
	$(BIN)/mkslides build slides

test:             ## offline tests: demo tools + slide build
	$(PY) -m pytest -q tests

# Live demos via Claude Code headless (`claude -p`): uses your Claude Code login
demo1:
	$(PY) demo/cli_01_simple_call.py

demo2:
	$(PY) demo/cli_02_tool_use.py

demo3:
	$(PY) demo/cli_03_agent.py

# Same demos via the Anthropic API (needs ANTHROPIC_API_KEY and API credit)
api-demo1:
	$(PY) demo/01_simple_llm_call.py

api-demo2:
	$(PY) demo/02_tool_use.py

api-demo3:
	$(PY) demo/03_agent_loop.py

clean:
	rm -rf site demo/workspace/report.md
