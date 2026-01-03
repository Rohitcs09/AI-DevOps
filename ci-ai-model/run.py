# run.py

from ai_model import analyze_pipeline

with open("pipeline.log", "r") as file:
    logs = file.read()

result = analyze_pipeline(logs)
print(result)

