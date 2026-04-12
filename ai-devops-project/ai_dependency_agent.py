import os
import xml.etree.ElementTree as ET

print("🚨 Dependency error detected!")
print("🔧 Fixing dependency issue...")

POM_FILE = "pom.xml"

if not os.path.exists(POM_FILE):
    print("❌ pom.xml not found!")
    exit(0)

print(f"📂 POM Path: {os.path.abspath(POM_FILE)}")

# Parse XML
tree = ET.parse(POM_FILE)
root = tree.getroot()

# Namespace fix
ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

dependencies = root.find('m:dependencies', ns)

if dependencies is None:
    print("❌ No <dependencies> found!")
    exit(0)

# ✅ Function: check if dependency exists
def dependency_exists(groupId, artifactId):
    for dep in dependencies.findall('m:dependency', ns):
        g = dep.find('m:groupId', ns)
        a = dep.find('m:artifactId', ns)

        if g is not None and a is not None:
            if g.text.strip() == groupId and a.text.strip() == artifactId:
                return True
    return False

# 🚨 Step 1: Remove wrong dependency
removed = False
for dep in list(dependencies.findall('m:dependency', ns)):
    g = dep.find('m:groupId', ns)
    if g is not None and "wrong.group" in g.text:
        print("🚨 Removing wrong dependency...")
        dependencies.remove(dep)
        removed = True

# ✅ Step 2: Add only if not exists
if dependency_exists("junit", "junit"):
    print("✅ Correct dependency already present → skipping update")
else:
    print("➕ Adding correct dependency...")

    new_dep = ET.Element('dependency')

    ET.SubElement(new_dep, 'groupId').text = "junit"
    ET.SubElement(new_dep, 'artifactId').text = "junit"
    ET.SubElement(new_dep, 'version').text = "4.13.2"
    ET.SubElement(new_dep, 'scope').text = "test"

    dependencies.append(new_dep)

# Save changes
tree.write(POM_FILE)

print("✅ pom.xml UPDATED SUCCESSFULLY!")
