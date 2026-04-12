import os
import re
import subprocess

# ✅ IMPORTANT: Agent will run inside ai-devops-maven folder
LOG_FILE = "build.log"
POM_FILE = "pom.xml"


def run_command(cmd):
    print(f"⚙️ Running: {cmd}")
    subprocess.run(cmd, shell=True)


def fix_dependency():
    print("🔧 Fixing dependency issue...")

    print("📂 Working Directory:", os.getcwd())
    print("📂 POM Path:", os.path.abspath(POM_FILE))

    if not os.path.exists(POM_FILE):
        print("❌ pom.xml not found")
        return

    with open(POM_FILE, "r") as file:
        content = file.read()

    print("🚨 Removing wrong dependency...")

    # ✅ Strong regex (handles spaces, comments, multiline)
    content = re.sub(
        r"<dependency>[\s\S]*?wrong\.group[\s\S]*?</dependency>",
        "",
        content
    )

    print("➕ Adding correct dependency...")

    correct_dependency = """
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
    """

    # ✅ Insert before closing tag
    content = content.replace("</dependencies>", correct_dependency + "\n</dependencies>")

    with open(POM_FILE, "w") as file:
        file.write(content)

    print("✅ pom.xml UPDATED SUCCESSFULLY!")


def analyze_logs():
    print("🤖 AI analyzing logs...")

    print("📂 Looking for log at:", os.path.abspath(LOG_FILE))

    if not os.path.exists(LOG_FILE):
        print("❌ Log file not found")
        return

    with open(LOG_FILE, "r") as file:
        logs = file.read()

    print("📄 LOG LENGTH:", len(logs))
    print("📄 LOG PREVIEW:\n", logs[:300])

    # ✅ SUPER RELAXED detection (guaranteed trigger)
    if (
        "wrong.group" in logs
        or "fake-artifact" in logs
        or "Could not resolve dependencies" in logs
        or "BUILD FAILURE" in logs
    ):
        print("🚨 Dependency error detected!")
        fix_dependency()
    else:
        print("❌ No dependency issue detected")


if __name__ == "__main__":
    analyze_logs()
