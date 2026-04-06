# run.py

from ai_model import analyze_logs

with open("logs.txt", "r") as file:
    logs = file.read()

result = analyze_logs(logs)
print(result)

