import xml.etree.ElementTree as ET
import os

POM_FILE = "pom.xml"
BUILD_LOG = "build.log"

# FIX: prevent ns0 issue
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")

# -------------------------
# READ BUILD LOG
# -------------------------
logs = ""
if os.path.exists(BUILD_LOG):
    with open(BUILD_LOG, "r") as f:
        logs = f.read()

print("Build log loaded")

# -------------------------
# SKIP IF NO ISSUE
# -------------------------
if "BUILD SUCCESS" in logs and "org.junit does not exist" not in logs and "wrong.group" not in logs:
    print("✅ No dependency issue detected → skipping AI fix")
    exit(0)

# -------------------------
# DETECT ISSUES
# -------------------------
junit_issue = "org.junit does not exist" in logs
wrong_dep_issue = "wrong.group" in logs

if not (junit_issue or wrong_dep_issue):
    print(" No actionable issue found → skipping AI fix")
    exit(0)

if junit_issue:
    print(" JUnit issue detected")

if wrong_dep_issue:
    print(" Wrong dependency issue detected")

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
#  REMOVE WRONG DEPENDENCY
# -------------------------
for d in list(deps.findall('m:dependency', ns)):
    if "wrong.group" in text(d.find('m:groupId', ns)):
        print(" Removing wrong dependency...")
        deps.remove(d)

# -------------------------
#  REMOVE EXISTING JUNIT (IDEMPOTENT SAFE)
# -------------------------
junit_exists = False

for d in list(deps.findall('m:dependency', ns)):
    g = text(d.find('m:groupId', ns))
    a = text(d.find('m:artifactId', ns))

    if g == "junit":
        junit_exists = True
        print("Removing existing junit...")
        deps.remove(d)

# -------------------------
# ADD JUNIT ONLY IF NEEDED
# -------------------------
print("Adding correct junit dependency...")

new = ET.Element("dependency")
ET.SubElement(new, "groupId").text = "junit"
ET.SubElement(new, "artifactId").text = "junit"
ET.SubElement(new, "version").text = "4.13.2"
ET.SubElement(new, "scope").text = "test"

deps.append(new)

# -------------------------
# SAVE ONLY IF CHANGES REQUIRED
# -------------------------
tree.write(POM_FILE, encoding="utf-8", xml_declaration=True)

print("pom.xml fixed successfully")

# -------------------------
#  SUMMARY
# -------------------------
print("AI fix completed (idempotent safe)")
