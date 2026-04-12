import os
import subprocess
import re

LOG_FILE = "ai-devops-maven/build.log"   # 🔥 IMPORTANT (same folder)

def run_command(cmd):
    print(f"⚙️ Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def fix_dependency():
    print("🔧 Fixing dependency issue...")

    pom_path = "pom.xml"   # ✅ correct path

    print(f"📂 Using file: {os.path.abspath(pom_path)}")

    if not os.path.exists(pom_path):
        print("❌ pom.xml not found")
        return

    with open(pom_path, "r") as file:
        content = file.read()

    # 🔍 check मौजूद है या नहीं
    if "wrong.group" not in content:
        print("⚠️ No wrong dependency found")
        return

    print("🔍 Removing wrong dependency...")

    # ❌ remove wrong dependency (regex)
    content = re.sub(
        r"<dependency>.*?wrong\.group.*?</dependency>",
        "",
        content,
        flags=re.DOTALL
    )

    print("➕ Adding correct dependency...")

    # ✅ correct dependency
    correct_dep = """
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
    """

    # insert before </dependencies>
    content = content.replace("</dependencies>", correct_dep + "\n</dependencies>")

    # 💾 write back
    with open(pom_path, "w") as file:
        file.write(content)

    print("✅ pom.xml updated successfully!")

    # 🔥 Git commit + push
    run_command('git config user.email "ai-bot@example.com"')
    run_command('git config user.name "AI Bot"')
    run_command('git add .')
    run_command('git commit -m "AI auto-fix dependency error"')

    # ⚠️ Replace this
    run_command('git push https://USERNAME:TOKEN@github.com/USERNAME/REPO.git HEAD:main')


def analyze_logs():
    print("🤖 AI analyzing logs...")

    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return

    with open(LOG_FILE, "r") as file:
        logs = file.read()

    if "Could not find artifact" in logs:
        print("🚨 Dependency error detected!")
        fix_dependency()
    else:
        print("✅ No dependency issue detected")


if __name__ == "__main__":
    analyze_logs()
