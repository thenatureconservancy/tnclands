import arcpy

try:
    # Local variables

    arcpy.env.workspace = r"c:\ArcpyBook\data"
    outFeatureClass = r"c:\ArcpyBook\data\AllTracts.shp"

    # Create a fieldmappings adding the three new fields
    fieldmappings = arcpy.FieldMappings()
    fldmap_STFIPS = arcpy.FieldMap()
    fldmap_COFIPS = arcpy.FieldMap()
    fldmap_TRACT = arcpy.FieldMap()

    # List all feature classes that start with 'County' and type Polygon
    fclss = arcpy.ListFeatureClasses("County*", "Polygon")

    # Create a value table with the FC to merge
    vTab = arcpy.ValueTable()
    for fc in fclss:
        fieldmappings.addTable(fc)
        fldmap_STFIPS.addInputField(fc, "STFID")
        fldmap_COFIPS.addInputField(fc, "STFID")
        fldmap_TRACT.addInputField(fc, "STFID")
        vTab.addRow(fc)

    # Set Starting and ending point from the input as well as the name of the output fields 

    # STFIPS field
    for x in range(0, fldmap_STFIPS.inputFieldCount):
        fldmap_STFIPS.setStartTextPosition(x, 0)
        fldmap_STFIPS.setEndTextPosition(x, 1)

    fld_STFIPS = fldmap_STFIPS.outputField
    fld_STFIPS.name = "STFIPS"
    fldmap_STFIPS.outputField = fld_STFIPS

    # COFIPS field
    for x in range(0, fldmap_COFIPS.inputFieldCount):
        fldmap_COFIPS.setStartTextPosition(x, 2)
        fldmap_COFIPS.setEndTextPosition(x, 4)

    fld_COFIPS = fldmap_COFIPS.outputField
    fld_COFIPS.name = "COFIPS"
    fldmap_COFIPS.outputField = fld_COFIPS

    # TRACT field
    for x in range(0, fldmap_TRACT.inputFieldCount):
        fldmap_TRACT.setStartTextPosition(x, 5)
        fldmap_TRACT.setEndTextPosition(x, 12)

    fld_TRACT = fldmap_TRACT.outputField
    fld_TRACT.name = "TRACT"
    fldmap_TRACT.outputField = fld_TRACT

    # Add fieldmaps into the fieldmappings object
    fieldmappings.addFieldMap(fldmap_STFIPS)
    fieldmappings.addFieldMap(fldmap_COFIPS)
    fieldmappings.addFieldMap(fldmap_TRACT)

    # Run the merge tool
    arcpy.Merge_management(vTab, outFeatureClass, fieldmappings)

    print("Merge completed")
               
except Exception as e:
    print(e.message)
               
               
    
               
