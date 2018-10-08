import xml.etree.ElementTree as ET

tree = ET.parse('D:\\xiayang_py\Servers600.dat')
root = tree.getroot()
#print(root.tag,root.attrib)


#for child in root:
#    print(child.tag,child.attrib)

print(root.attrib['create'])
print(root.getchildren()[1].attrib['url'])

