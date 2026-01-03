# ai_model.py

def analyze_pipeline(logs):
    if "ModuleNotFoundError" in logs:
        return "Prediction: Missing dependency in requirements.txt"

    if "Permission denied" in logs:
        return "Prediction: Permission issue in build environment"

    if "Tests failed" in logs:
        return "Prediction: Unit test failure"

    return "Prediction: Unknown pipeline failure"

