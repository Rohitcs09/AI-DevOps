# ai_agent.py

from ai_model import analyze_logs

def restart_service():
    print("Restarting service...")

def send_alert(msg):
    print(f"Alert sent: {msg}")

def ai_agent(logs):
    decision = analyze_logs(logs)

    if decision == "CPU_OVERLOAD":
        restart_service()
        send_alert("CPU overload detected on server")
    else:
        print("System running normally")

