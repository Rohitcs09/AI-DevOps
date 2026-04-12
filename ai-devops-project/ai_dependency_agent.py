import xml.etree.ElementTree as ET

POM_FILE = "pom.xml"
BUILD_LOG = "build.log"

# 🔥 FIX: prevent ns0 / namespace issue
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")

# -------------------------
# 📄 READ BUILD LOG
# -------------------------
try:
    with open(BUILD_LOG, "r") as f:
        logs = f.read()
except:
    logs = ""

print("📄 Build log loaded")

# -------------------------
# PARSE POM
# -------------------------
tree = ET.parse(POM_FILE)
root = tree.getroot()

ns = {'m': root.tag.split('}')[0].strip('{')}
deps = root.find('m:dependencies', ns)

def text(e):
    return e.text.strip() if e is not None and e.text else ""

# -------------------------
# 🚨 DETECT ERROR FROM LOG
# -------------------------
junit_issue = "org.junit does not exist" in logs

if junit_issue:
    print("🚨 JUnit issue detected from build.log")

# -------------------------
# ❌ REMOVE WRONG DEPENDENCY
# -------------------------
for d in list(deps.findall('m:dependency', ns)):
    if "wrong.group" in text(d.find('m:groupId', ns)):
        print("🚨 Removing wrong dependency...")
        deps.remove(d)

# -------------------------
# 🧹 REMOVE ALL JUNIT (SAFE RESET)
# -------------------------
for d in list(deps.findall('m:dependency', ns)):
    g = text(d.find('m:groupId', ns))

    if g == "junit":
        print("🧹 Removing existing junit...")
        deps.remove(d)

# -------------------------
# ➕ ADD CORRECT JUNIT
# -------------------------
print("➕ Adding correct junit dependency...")

new = ET.Element("dependency")
ET.SubElement(new, "groupId").text = "junit"
ET.SubElement(new, "artifactId").text = "junit"
ET.SubElement(new, "version").text = "4.13.2"
ET.SubElement(new, "scope").text = "test"

deps.append(new)

# -------------------------
# 💾 SAVE SAFE POM
# -------------------------
tree.write(POM_FILE, encoding="utf-8", xml_declaration=True)

print("✅ pom.xml fixed successfully (ns0 + dependency issues resolved)")
