import os
import xml.etree.ElementTree as ET

print("🚨 Dependency error detected!")
print("🔧 Fixing dependency issue...")

POM_FILE = "pom.xml"

if not os.path.exists(POM_FILE):
    print("❌ pom.xml not found!")
    exit(0)

print(f"📂 POM Path: {os.path.abspath(POM_FILE)}")

tree = ET.parse(POM_FILE)
root = tree.getroot()

ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

dependencies = root.find('m:dependencies', ns)

if dependencies is None:
    print("❌ No dependencies found!")
    exit(0)

# ✅ Normalize text safely
def get_text(elem):
    return elem.text.strip() if elem is not None and elem.text else ""

# 🚨 STEP 1: Remove wrong dependency
for dep in list(dependencies.findall('m:dependency', ns)):
    g = get_text(dep.find('m:groupId', ns))
    if "wrong.group" in g:
        print("🚨 Removing wrong dependency...")
        dependencies.remove(dep)

# 🚨 STEP 2: Remove duplicate junit
seen = False
for dep in list(dependencies.findall('m:dependency', ns)):
    g = get_text(dep.find('m:groupId', ns))
    a = get_text(dep.find('m:artifactId', ns))

    if g == "junit" and a == "junit":
        if not seen:
            seen = True
        else:
            print("🧹 Removing duplicate junit dependency...")
            dependencies.remove(dep)

# ✅ STEP 3: Check existence AFTER cleanup
exists = False
for dep in dependencies.findall('m:dependency', ns):
    g = get_text(dep.find('m:groupId', ns))
    a = get_text(dep.find('m:artifactId', ns))

    if g == "junit" and a == "junit":
        exists = True
        break

# ✅ STEP 4: Add only if missing
if exists:
    print("✅ Correct dependency already present → skipping add")
else:
    print("➕ Adding correct dependency...")

    new_dep = ET.Element('dependency')
    ET.SubElement(new_dep, 'groupId').text = "junit"
    ET.SubElement(new_dep, 'artifactId').text = "junit"
    ET.SubElement(new_dep, 'version').text = "4.13.2"
    ET.SubElement(new_dep, 'scope').text = "test"

    dependencies.append(new_dep)

# Save
tree.write(POM_FILE)

print("✅ pom.xml CLEANED & UPDATED SUCCESSFULLY!")
