import xml.etree.ElementTree as ET

POM_FILE = "pom.xml"

# 🔥 FIX: prevents ns0/ns1 issue permanently
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")

tree = ET.parse(POM_FILE)
root = tree.getroot()

# namespace handling (unchanged logic)
ns = {'m': root.tag.split('}')[0].strip('{')}

deps = root.find('m:dependencies', ns)

def text(e):
    return e.text.strip() if e is not None and e.text else ""

# ❌ remove wrong dependency (UNCHANGED LOGIC)
for d in list(deps.findall('m:dependency', ns)):
    if "wrong.group" in text(d.find('m:groupId', ns)):
        print("🚨 Removing wrong dependency...")
        deps.remove(d)

# 🧹 remove ALL junit first (UNCHANGED LOGIC)
for d in list(deps.findall('m:dependency', ns)):
    g = text(d.find('m:groupId', ns))
    a = text(d.find('m:artifactId', ns))

    if g == "junit" and a == "junit":
        print("🧹 Removing old junit...")
        deps.remove(d)

# ➕ add ONLY ONE junit (UNCHANGED LOGIC)
print("➕ Adding single junit dependency...")
new = ET.Element('dependency')
ET.SubElement(new, 'groupId').text = "junit"
ET.SubElement(new, 'artifactId').text = "junit"
ET.SubElement(new, 'version').text = "4.13.2"
ET.SubElement(new, 'scope').text = "test"

deps.append(new)

# 💾 SAFE WRITE (ONLY FIX HERE)
tree.write(POM_FILE, encoding="utf-8", xml_declaration=True)

print("✅ pom.xml fixed (ns0 issue resolved, logic unchanged)")
