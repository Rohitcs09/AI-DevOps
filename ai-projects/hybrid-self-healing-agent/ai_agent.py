import os
import subprocess
import re
import time

# -------------------------------
# 📂 Auto-detect files
# -------------------------------
def find_java_file():
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".java"):
                return os.path.join(root, file)
    return None

JAVA_FILE = find_java_file()
POM_FILE = os.path.join(os.getcwd(), "pom.xml")


# -------------------------------
# 📝 LOG FUNCTION
# -------------------------------
def log_action(message):
    with open("build.log", "a") as f:
        f.write(f"\n👉 {message}\n")


# -------------------------------
# 🔧 FIX 1: Java Syntax
# -------------------------------
def fix_java_syntax():
    print("🔍 Checking Java syntax...")

    if not JAVA_FILE:
        print("❌ No Java file found")
        log_action("No Java file found")
        return False

    with open(JAVA_FILE, "r") as f:
        lines = f.readlines()

    fixed = False
    new_lines = []

    for line in lines:
        stripped = line.strip()

        if "System.out.println" in stripped and not stripped.endswith(";"):
            print("⚠️ Missing semicolon detected")
            log_action("Missing semicolon detected")

            line = line.rstrip() + ";\n"
            fixed = True

        new_lines.append(line)

    if fixed:
        with open(JAVA_FILE, "w") as f:
            f.writelines(new_lines)

        print("✅ Fixed: Semicolon added")
        log_action("Fixed Java syntax (semicolon added)")
        return True

    print("✔ No syntax issue")
    log_action("No syntax issue found")
    return False


# -------------------------------
# 🔧 FIX 2: JUnit Upgrade
# -------------------------------
def fix_junit():
    print("🔍 Checking JUnit dependency...")

    if not os.path.exists(POM_FILE):
        print("❌ pom.xml not found")
        log_action("pom.xml not found")
        return False

    with open(POM_FILE, "r") as f:
        pom = f.read()

    updated = pom

    pattern = r'(<dependency>.*?<groupId>junit</groupId>.*?<artifactId>junit</artifactId>.*?<version>)(.*?)(</version>.*?</dependency>)'

    updated = re.sub(
        pattern,
        r'\g<1>4.13.2\g<3>',
        updated,
        flags=re.DOTALL
    )

    # If not present → add
    if "<artifactId>junit</artifactId>" not in updated:
        print("⚠️ JUnit not found, adding dependency")
        log_action("JUnit dependency missing → adding")

        junit_block = """
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
        """

        updated = updated.replace("</dependencies>", junit_block + "\n</dependencies>")

    if updated != pom:
        with open(POM_FILE, "w") as f:
            f.write(updated)

        print("✅ Fixed: JUnit updated to 4.13.2")
        log_action("JUnit dependency set to 4.13.2")
        return True

    print("✔ JUnit already correct")
    log_action("JUnit already correct")
    return False


# -------------------------------
# 🏗️ BUILD FUNCTION
# -------------------------------
def run_build(attempt):
    print("🚀 Running Maven build...")

    result = subprocess.run(
        ["mvn", "clean", "install"],
        capture_output=True,
        text=True
    )

    with open("build.log", "a") as f:
        f.write(f"\n\n===== ATTEMPT {attempt} =====\n")
        f.write(result.stdout)
        f.write("\n--- ERRORS ---\n")
        f.write(result.stderr)

    return result.returncode


# -------------------------------
# 🤖 MAIN AGENT
# -------------------------------
def auto_fix():
    print("🤖 AI Agent Started...\n")

    for i in range(3):
        print(f"\n🔁 Attempt {i+1}")

        status = run_build(i+1)

        if status == 0:
            print("🎉 BUILD SUCCESS")
            log_action("Build succeeded")
            return

        print("❌ Build failed. Running fixes...\n")

        # 🔥 ALWAYS RUN BOTH FIXES
        syntax_fixed = fix_java_syntax()
        junit_fixed = fix_junit()

        if syntax_fixed or junit_fixed:
            print("\n🔁 Re-running build after fixes...\n")
            log_action("Re-running build after fixes")
            time.sleep(2)
        else:
            print("⚠️ No fix applied")
            log_action("No fix applied")
            break

    print("❌ Build still failing")
    log_action("Build failed after retries")


# -------------------------------
# 🚀 ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    auto_fix()
