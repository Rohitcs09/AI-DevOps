import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LOG_FILE = "ai-devops-maven/build.log"
JAVA_FILE = "ai-devops-maven/src/main/java/App.java"
POM_FILE = "ai-devops-maven/pom.xml"

def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

def ask_ai(log, java_code, pom):
    prompt = f"""
You are a DevOps AI agent.

Build failed with this error:
{log}

Java Code:
{java_code}

POM File:
{pom}

Fix all issues:
- syntax errors
- outdated dependencies

Return ONLY updated Java code and pom.xml in this format:

---JAVA---
<fixed java code>

---POM---
<fixed pom.xml>
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def apply_fix(ai_output):
    if "---JAVA---" in ai_output and "---POM---" in ai_output:
        java_part = ai_output.split("---JAVA---")[1].split("---POM---")[0]
        pom_part = ai_output.split("---POM---")[1]

        write_file(JAVA_FILE, java_part.strip())
        write_file(POM_FILE, pom_part.strip())

        print("✅ AI Fix Applied")
        return True

    print("⚠️ AI response invalid")
    return False


def main():
    print("🤖 AI Agent Started...")

    log = read_file(LOG_FILE)

    if not log:
        print("❌ build.log not found or empty")
        return

    java_code = read_file(JAVA_FILE)
    pom = read_file(POM_FILE)

    ai_output = ask_ai(log, java_code, pom)

    print("\n🤖 AI Response:\n", ai_output)

    apply_fix(ai_output)


if __name__ == "__main__":
    main()
