import os

def read_logs():
    try:
        with open("build.log", "r") as f:
            return f.read()
    except:
        return "No logs found"

def analyze_logs(logs):
    print("🔍 AI Agent analyzing logs...\n")

    if "BUILD FAILURE" in logs:
        print("❌ Build Failed Detected")
        print("💡 Suggestion: Check dependency or syntax error")

    elif "COMPILATION ERROR" in logs:
        print("❌ Compilation Error")
        print("💡 Suggestion: Fix Java syntax or missing imports")

    else:
        print("✅ Build looks fine")

if __name__ == "__main__":
    logs = read_logs()
    analyze_logs(logs)
