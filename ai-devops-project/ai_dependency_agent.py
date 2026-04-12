import os
import xml.etree.ElementTree as ET

print("🚨 Dependency error detected!")
print("🔧 Fixing dependency issue...")

POM_FILE = "pom.xml"

if not os.path.exists(POM_FILE):
    print("❌ pom.xml not found!")
    exit(0)

print(f"📂 POM Path: {os.path.abspath(POM_FILE)}")

# ✅ SAFE PARSE (important fix)
try:
    tree = ET.parse(POM_FILE)
    root = tree.getroot()
except ET.ParseError as e:
    print("❌ XML Broken! Cannot fix automatically.")
    print(f"Error: {e}")
    exit(0)

ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
deps = root.find('m:dependencies', ns)

if deps is None:
    print("❌ No <dependencies> found!")
    exit(0)

def text(e):
    return e.text.strip() if e is not None and e.text else ""

# 🚨 REMOVE wrong dependency
for d in list(deps.findall('m:dependency', ns)):
    if "wrong.group" in text(d.find('m:groupId', ns)):
        print("🚨 Removing wrong dependency...")
        deps.remove(d)

# 🧹 REMOVE duplicate junit
found = False
for d in list(deps.findall('m:dependency', ns)):
    g = text(d.find('m:groupId', ns))
    a = text(d.find('m:artifactId', ns))

    if g == "junit" and a == "junit":
        if not found:
            found = True
        else:
            print("🧹 Removing duplicate junit...")
            deps.remove(d)

# ➕ ADD if missing
if not found:
    print("➕ Adding junit dependency...")
    new = ET.Element('dependency')
    ET.SubElement(new, 'groupId').text = "junit"
    ET.SubElement(new, 'artifactId').text = "junit"
    ET.SubElement(new, 'version').text = "4.13.2"
    ET.SubElement(new, 'scope').text = "test"
    deps.append(new)
else:
    print("✅ junit already exists → skip")

tree.write(POM_FILE)
print("✅ pom.xml fixed safely")
