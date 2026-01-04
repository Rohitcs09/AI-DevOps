# run_agent.py

with open("logs.txt") as f:
    logs = f.read()

from ai_agent import ai_agent
ai_agent(logs)

