import os

LOG_FILE = "ai-devops-maven/build.log"
JAVA_FILE = "ai-devops-maven/src/main/java/com/example/Test.java"

print("🔍 AI Agent analyzing logs...")

if not os.path.exists(LOG_FILE):
    print("❌ Log file not found")
    exit(1)

with open(LOG_FILE, "r") as f:
    logs = f.read()

if "COMPILATION ERROR" in logs or "BUILD FAILURE" in logs:
    print("❌ Issue Detected by AI")

    # 🔥 AUTO FIX (your known issue)
    fixed_code = '''
package com.example;

public class Test {
    public static void main(String[] args) {
        System.out.println("Hello");

        int a = 10;
    }
}
'''

    with open(JAVA_FILE, "w") as f:
        f.write(fixed_code)

    print("💡 AI Fixed the issue in Test.java ✅")

    # 🔥 GIT PUSH
    os.system("git add .")
    os.system('git commit -m "🤖 AI auto-fixed build error"')
    os.system("git push")

else:
    print("✅ Build looks fine")
