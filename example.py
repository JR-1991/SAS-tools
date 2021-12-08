from data_model.datablubb import Fileinfo, Column, List_, Value, Parameter, Group

fileinfo = Fileinfo(version="lolololol")

# Add columns
column = Column(key="Coole Column")

for _ in range(10):
    column.value.append(
        Value(value=100)
    )

# Add column to fielinfo
fileinfo.columns.append(column)

# Create parameters
param_1 = Parameter(key="Kaka", index=100, value=[Value(100)], type="integer")

# Add parameter to fileinfo
fileinfo.parameters.append(param_1)

# Create groups
group_1 = Group(
    isdevice=False,
    category="Lol",
    sub="sample",
    key="Coole Group",
    id="lel"
)

group_1.list_.append(
    List_(key="lol", islimited=True, value=[Value(100)])
)
fileinfo.setup.groups.append(group_1)


xml_string = fileinfo.toXML()

print(Fileinfo.fromXMLString(xml_string))
