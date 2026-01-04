# ai_model.py

def analyze_logs(logs):
    if logs.count("CPU_HIGH") >= 3:
        return "CPU_OVERLOAD"
    return "NORMAL"

