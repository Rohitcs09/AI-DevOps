import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

REPORT_PATH = "target/dependency-check-report.json"
POM_FILE = "pom.xml"


def read_report():
    if not os.path.exists(REPORT_PATH):
        print("❌ OWASP report not found")
        return None

    with open(REPORT_PATH) as f:
        return json.load(f)


def read_pom():
    with open(POM_FILE) as f:
        return f.read()


def analyze_with_ai(report, pom):
    print("\n🤖 Analyzing vulnerabilities using OpenAI...\n")

    prompt = f"""
You are a DevSecOps AI Agent.

Analyze the OWASP dependency-check report and pom.xml.

Tasks:
1. Identify vulnerable dependencies (only HIGH/CRITICAL)
2. Suggest secure versions
3. Return updated pom.xml

Format:

---ISSUES---
<list vulnerabilities with severity>

---FIXED_POM---
<updated pom.xml>

OWASP REPORT:
{json.dumps(report)[:4000]}

POM.XML:
{pom}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


def show_issues(output):
    if "---ISSUES---" in output:
        issues = output.split("---ISSUES---")[1].split("---FIXED_POM---")[0]

        print("🚨 SECURITY ALERT 🚨")
        print("High/Critical vulnerabilities found:\n")
        print(issues.strip())


def apply_fix(output):
    if "---FIXED_POM---" not in output:
        print("⚠️ No fix provided")
        return False

    fixed = output.split("---FIXED_POM---")[1].strip()

    with open(POM_FILE, "w") as f:
        f.write(fixed)

    print("\n🤖 AI is fixing vulnerabilities...\n")
    print("✅ Fix applied by AI\n")
    return True


def main():
    print("🤖 AI DevSecOps Agent Started...\n")

    report = read_report()
    if not report:
        return

    pom = read_pom()

    output = analyze_with_ai(report, pom)

    show_issues(output)

    if apply_fix(output):
        print("🔁 Ready for rebuild")
    else:
        print("⚠️ No changes")


if __name__ == "__main__":
    main()
