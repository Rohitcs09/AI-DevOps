# ai_agent.py

from k8s_logs import get_pod_logs
from ai_model import analyze_logs
from config import MODE

def restart_pod(pod_name):
    print(f"Restarting Kubernetes pod: {pod_name}")

def send_alert(message):
    print(f"Slack Alert: {message}")

def ai_agent(pod_name, namespace="default"):
    logs = get_pod_logs(pod_name, namespace, MODE)
    decision = analyze_logs(logs)

    if decision == "CRITICAL":
        restart_pod(pod_name)
        send_alert("High CPU detected on pod")
    else:
        print("Pod is healthy")

