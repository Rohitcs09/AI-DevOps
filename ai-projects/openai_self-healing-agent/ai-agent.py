import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LOG_FILE = "build.log"

def read_logs():
    if not os.path.exists(LOG_FILE):
        return "No logs found"
    
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()[-4000:]  # last logs only (important for token limit)

def analyze_logs(logs):
    prompt = f"""
You are a Senior DevOps Engineer.

Analyze Jenkins build logs and:
- Identify exact error
- Root cause
- Give fix (command/code)

Logs:
{logs}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Expert in CI/CD, Jenkins, Maven, debugging."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def auto_fix(logs):
    if "outdated" in logs.lower():
        print("🔧 Updating dependencies...")
        os.system("mvn clean install -U")

    elif "compilation error" in logs.lower():
        print("⚠️ Syntax issue detected (manual fix required)")

    else:
        print("🤖 AI suggested fix required")

if __name__ == "__main__":
    print("📄 Reading Jenkins logs...")
    logs = read_logs()

    print("🤖 Sending logs to AI Agent...")
    result = analyze_logs(logs)

    print("\n🔍 AI Analysis:\n")
    print(result)

    print("\n⚙️ Attempting Auto Fix...\n")
    auto_fix(logs)
