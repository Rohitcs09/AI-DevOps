# k8s_logs.py

def get_pod_logs(pod_name, namespace="default", mode="DEMO"):
    if mode == "DEMO":
        return """
        INFO Starting payment service
        INFO CPU usage normal
        WARNING Memory usage high
        ERROR CPU_HIGH detected
        ERROR CPU_HIGH detected
        ERROR CPU_HIGH detected
        """
    else:
        # PROD mode placeholder (not used in demo)
        return ""

