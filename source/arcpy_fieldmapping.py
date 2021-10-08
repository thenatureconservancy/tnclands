import arcpy
arcpy.env.workspace = "D:/jplatt/data/scratch/test.gdb"
arcpy.env.overwriteOutput = True

outfc  = 'D:/jplatt/data/scratch/test.gdb/AllBlocks'
fc1 ='D:/jplatt/data/scratch/test.gdb/Blocks1'  
fc2 ='D:/jplatt/data/scratch/test.gdb/Blocks2' 

fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(fc1)
fieldmappings.addTable(fc2)

fieldmap = fieldmappings.getFieldMap(fieldmappings.findFieldMapIndex("TRACT2000"))
fieldmap.addInputField(fc2, "TRACTCODE")
fieldmappings.replaceFieldMap(fieldmappings.findFieldMapIndex("TRACT2000"), fieldmap)

fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex("TRACTCODE"))

try:
    vTab = arcpy.ValueTable()
except:
    print('fail')

vTab.addRow(fc1)
vTab.addRow(fc2)

arcpy.Merge_management(vTab, outfc, fieldmappings)