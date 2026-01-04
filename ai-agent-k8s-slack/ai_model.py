# ai_model.py

def analyze_logs(logs):
    cpu_errors = logs.count("CPU_HIGH")

    if cpu_errors >= 3:
        return "CRITICAL"
    return "NORMAL"

