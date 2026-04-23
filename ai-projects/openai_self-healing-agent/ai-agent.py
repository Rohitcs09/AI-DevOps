import os
import re

# 📄 Correct log file path (from Jenkins root)
LOG_FILE = os.path.abspath(os.path.join(os.getcwd(), "../../build.log"))

JAVA_FILE = None

# 🔍 Auto-detect Java file
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".java"):
            JAVA_FILE = os.path.join(root, file)


# -----------------------------
# 🔧 FIX 1: Missing Semicolon
# -----------------------------
def fix_semicolon():
    print("🔧 Fix: Checking missing semicolon...")

    if not JAVA_FILE:
        print("❌ Java file not found")
        return False

    with open(JAVA_FILE, "r") as f:
        lines = f.readlines()

    fixed = False
    new_lines = []

    for line in lines:
        if "System.out.println" in line and ";" not in line:
            print("⚡ Fixing missing semicolon...")
            line = line.rstrip() + ";\n"
            fixed = True

        new_lines.append(line)

    if fixed:
        with open(JAVA_FILE, "w") as f:
            f.writelines(new_lines)
        print("✅ Semicolon fixed")
        return True

    print("ℹ️ No syntax issue found")
    return False


# -----------------------------
# 🔧 FIX 2: Upgrade JUnit
# -----------------------------
def fix_junit():
    print("🔧 Fix: Checking JUnit version...")

    pom_path = "ai-devops-maven/pom.xml"

    if not os.path.exists(pom_path):
        print("❌ pom.xml not found")
        return False

    with open(pom_path, "r") as f:
        pom = f.read()

    if "<version>4.10</version>" in pom:
        print("⚡ Upgrading JUnit version...")
        pom = pom.replace("<version>4.10</version>", "<version>4.13.2</version>")

        with open(pom_path, "w") as f:
            f.write(pom)

        print("✅ JUnit upgraded")
        return True

    print("ℹ️ JUnit already correct")
    return False


# -----------------------------
# 🤖 MAIN AI LOGIC
# -----------------------------
def auto_fix():
    print("🤖 AI Agent Started...\n")

    print("📂 Current Dir:", os.getcwd())
    print("📄 Looking for log at:", LOG_FILE)

    if not os.path.exists(LOG_FILE):
        print("❌ build.log not found")
        return

    with open(LOG_FILE, "r") as f:
        log = f.read()

    print("\n📄 Analyzing logs...\n")
    print("🔍 Log Preview:\n", log[:500])

    fixed_any = False

    # 🔥 Robust Syntax Detection
    if re.search(r"; expected", log) or re.search(r"';' expected", log):
        print("\n🚨 Syntax error detected!")
        fixed_any = fix_semicolon()

    # 🔥 JUnit Detection
    if "junit" in log.lower():
        fixed_any = fix_junit() or fixed_any

    if fixed_any:
        print("\n🚀 Fix applied successfully!")
    else:
        print("\n⚠️ No auto-fix applied")


# -----------------------------
if __name__ == "__main__":
    auto_fix()
