import os
from openai import OpenAI

# -------------------------------
# 🔑 INIT OPENAI
# -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

POM_FILE = "pom.xml"


# -------------------------------
# 📄 READ POM
# -------------------------------
def read_pom():
    if not os.path.exists(POM_FILE):
        print("❌ pom.xml not found!")
        return None

    with open(POM_FILE, "r") as f:
        return f.read()


# -------------------------------
# 🤖 AI ANALYSIS
# -------------------------------
def analyze_with_ai(pom_content):
    print("\n🤖 Sending pom.xml to OpenAI for security analysis...\n")

    prompt = f"""
You are a DevSecOps AI Agent.

Analyze the given Maven pom.xml file and identify vulnerable dependencies.

Tasks:
1. Detect vulnerable dependencies
2. Mention reason (CVE or risk)
3. Suggest secure/latest version
4. Return updated pom.xml

Output format strictly:

---ISSUES---
<list vulnerabilities>

---FIXED_POM---
<updated pom.xml>

pom.xml:
{pom_content}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


# -------------------------------
# 🔍 DISPLAY ISSUES
# -------------------------------
def show_issues(output):
    if "---ISSUES---" in output:
        issues = output.split("---ISSUES---")[1].split("---FIXED_POM---")[0]

        print("🚨 SECURITY ALERT 🚨")
        print("We found vulnerabilities in pom.xml:\n")
        print(issues.strip())


# -------------------------------
# 🔧 APPLY FIX
# -------------------------------
def apply_fix(output):
    if "---FIXED_POM---" not in output:
        print("⚠️ No fix provided by AI")
        return False

    fixed_pom = output.split("---FIXED_POM---")[1].strip()

    with open(POM_FILE, "w") as f:
        f.write(fixed_pom)

    print("\n🤖 AI is fixing vulnerabilities...\n")
    print("✅ Vulnerabilities fixed by OpenAI Agent\n")

    return True


# -------------------------------
# 🚀 MAIN FLOW
# -------------------------------
def main():
    print("🤖 AI DevSecOps Agent Started...\n")

    pom_content = read_pom()
    if not pom_content:
        return

    output = analyze_with_ai(pom_content)

    show_issues(output)

    changed = apply_fix(output)

    if changed:
        print("🔁 Changes applied successfully. Ready for rebuild!")
    else:
        print("⚠️ No changes applied.")


# -------------------------------
# 🚀 ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    main()
