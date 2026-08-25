# Pure Python Agent

A 40-line ReAct agent built with zero frameworks. Just Python + `httpx`.

&gt; Built by a 4th-sem student learning AI infrastructure from scratch.

## Run It

```bash
git clone https://github.com/sa82912045-blip/python-agent-from-scratch.git
cd python-agent-from-scratch
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
python agent.py

---

## Read the Article
📖 [I Was Told I Need LangChain to Build an AI Agent. I Did It in 40 Lines of Pure Python.](LINK_COMING_AFTER_PUBLISH)

*Article published 25 Aug 2026. Link updating soon.*

---

## What It Does
| Part | Lines | What Happens |
|------|-------|--------------|
| `Agent.__init__` | 3 | Sets up memory and tool registry |
| `register_tool` | 10 | Attaches a Python function as an LLM-callable tool |
| `_chat` | 12 | Raw API call to OpenAI with optional tool schemas |
| `run` | 15 | The ReAct loop: ask LLM → check for tool calls → execute → respond |

**Total agent logic: 40 lines.** No hidden files. No 200-line abstraction.

---

## What's Next
- [ ] MCP client integration (v2.0.0) — connect to Claude Desktop
- [ ] Ollama support for local LLMs — run offline
- [ ] Multi-agent routing — delegate tasks to specialized agents

**Follow the build:** [github.com/sa82912045-blip/python-agent-from-scratch](https://github.com/sa82912045-blip/python-agent-from-scratch)
