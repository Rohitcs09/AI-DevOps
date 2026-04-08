import os

print("🔍 AI Agent analyzing logs...")

log_path = "ai-devops-project/ai-devops-maven/build.log"

if not os.path.exists(log_path):
    print("❌ Log file not found:", log_path)
    exit(0)

with open(log_path, "r") as f:
    logs = f.read()

if "COMPILATION ERROR" in logs or "BUILD FAILURE" in logs:
    print("❌ Issue Detected by AI")

    for line in logs.splitlines():
        if "error" in line.lower():
            print("👉", line)
            break

    print("💡 Suggested Fix:")
    print("- Fix syntax error in Java file")
    print("- Check missing semicolon or invalid statement")

else:
    print("✅ Build looks fine")
