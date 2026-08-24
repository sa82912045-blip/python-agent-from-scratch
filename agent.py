"""
Pure Python ReAct Agent
No frameworks. Just Python, httpx, and OpenAI's API.
Built by a student learning what actually happens under the hood.
"""

import json
import os
import httpx
from typing import Callable


class Agent:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        self.memory = []
        self.tools = {}

    def register_tool(self, name: str, func: Callable, description: str, params: dict):
        self.tools[name] = {
            "func": func,
            "schema": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": params,
                    "required": list(params.keys())
                }
            }
        }

    def _chat(self, messages: list, tools: list = None) -> dict:
        payload = {"model": self.model, "messages": messages}
        if tools:
            payload["tools"] = [{"type": "function", "function": t} for t in tools]
            payload["tool_choice"] = "auto"

        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=30.0
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]

    def run(self, prompt: str) -> str:
        self.memory.append({"role": "user", "content": prompt})

        system_msg = {
            "role": "system",
            "content": "You are a helpful assistant with access to tools. "
                       "Use a tool only when necessary. Be concise."
        }
        tool_schemas = [t["schema"] for t in self.tools.values()]
        msg = self._chat([system_msg] + self.memory, tool_schemas)

        if msg.get("tool_calls"):
            self.memory.append(msg)
            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                result = self.tools.get(name, {}).get("func", lambda **_: "Error")(**args)
                self.memory.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": str(result)
                })
            msg = self._chat([system_msg] + self.memory)

        self.memory.append(msg)
        return msg["content"]


if __name__ == "__main__":
    import sys

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable.")
        sys.exit(1)

    agent = Agent(api_key=api_key)

    # Demo tool: Calculator
    agent.register_tool(
        name="calculate",
        func=lambda expression: eval(expression),
        description="Evaluate a mathematical expression. Use for any math.",
        params={
            "expression": {
                "type": "string",
                "description": "Math expression like '25 * 4' or '(100 + 50) / 3'"
            }
        }
    )

    # Demo tool: Get current date
    from datetime import datetime
    agent.register_tool(
        name="get_date",
        func=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="Get the current date and time.",
        params={}
    )

    print("=" * 50)
    print("Pure Python Agent — Type 'exit' to quit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        response = agent.run(user_input)
        print(f"Agent: {response}")