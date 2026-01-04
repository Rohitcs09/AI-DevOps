# ai_model.py

def analyze_logs(log_data):
    cpu_errors = log_data.count("CPU_HIGH")
    memory_warnings = log_data.count("Memory usage high")

    if cpu_errors >= 3:
        return "Prediction: CPU bottleneck detected"
    elif memory_warnings >= 2:
        return "Prediction: Possible memory leak"
    else:
        return "Prediction: System looks stable"

