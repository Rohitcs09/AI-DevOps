import xml.etree.ElementTree as ET

POM_FILE = "pom.xml"

tree = ET.parse(POM_FILE)
root = tree.getroot()

# auto detect namespace
ns = {'m': root.tag.split('}')[0].strip('{')}

deps = root.find('m:dependencies', ns)

def text(e):
    return e.text.strip() if e is not None and e.text else ""

# ❌ remove wrong dependency
for d in list(deps.findall('m:dependency', ns)):
    if "wrong.group" in text(d.find('m:groupId', ns)):
        print("🚨 Removing wrong dependency...")
        deps.remove(d)

# 🧹 remove ALL junit first (important fix)
for d in list(deps.findall('m:dependency', ns)):
    g = text(d.find('m:groupId', ns))
    a = text(d.find('m:artifactId', ns))

    if g == "junit" and a == "junit":
        deps.remove(d)

# ➕ add ONLY ONE junit
print("➕ Adding single junit dependency...")
new = ET.Element('dependency')
ET.SubElement(new, 'groupId').text = "junit"
ET.SubElement(new, 'artifactId').text = "junit"
ET.SubElement(new, 'version').text = "4.13.2"
ET.SubElement(new, 'scope').text = "test"

deps.append(new)

tree.write(POM_FILE)
print("✅ pom.xml fixed (no duplicates)")
