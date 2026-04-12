import os
import subprocess

# 📌 Correct log file path (as per your project)
LOG_FILE = "ai-devops-maven/build.log"

def run_command(cmd):
    """Run shell command"""
    print(f"⚙️ Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("❌ Command failed")
    return result.returncode


def fix_dependency():
    print("🔧 Fixing dependency issue...")

    pom_path = "pom.xml"

    if not os.path.exists(pom_path):
        print("❌ pom.xml not found")
        return

    with open(pom_path, "r") as file:
        content = file.read()

    # ❌ Wrong dependency (same as demo)
    wrong_dep = """
        <dependency>
            <groupId>wrong.group</groupId>
            <artifactId>fake-artifact</artifactId>
            <version>1.0.0</version>
        </dependency>
    """

    # ✅ Correct dependency (example)
    correct_dep = """
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    """

    if "wrong.group" in content:
        content = content.replace(wrong_dep, correct_dep)

        with open(pom_path, "w") as file:
            file.write(content)

        print("✅ Dependency fixed in pom.xml")

        # 🔥 Git commit + push
        run_command('git config user.email "ai-bot@example.com"')
        run_command('git config user.name "AI Bot"')
        run_command('git add .')
        run_command('git commit -m "AI auto-fix dependency error"')

        # ⚠️ IMPORTANT: Replace with your username + token
        run_command('git push https://USERNAME:TOKEN@github.com/USERNAME/REPO.git HEAD:main')

    else:
        print("⚠️ No wrong dependency found")


def analyze_logs():
    print("🤖 AI analyzing logs...")

    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return

    with open(LOG_FILE, "r") as file:
        logs = file.read()

    if "Could not find artifact" in logs:
        print("🔍 Dependency error detected!")
        fix_dependency()
    else:
        print("✅ No dependency issue detected")


if __name__ == "__main__":
    analyze_logs()
