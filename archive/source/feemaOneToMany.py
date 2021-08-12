# ---------------------------------------------------------------------------
# feemaOneToMany.py
# Created on: 2012-09-24 14:28:13.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: feemaOneToMany <SA_STEWARD_TNC_LANDS> <feema1tomany> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
SA_STEWARD_TNC_LANDS = arcpy.GetParameterAsText(0)
if SA_STEWARD_TNC_LANDS == '#' or not SA_STEWARD_TNC_LANDS:
    SA_STEWARD_TNC_LANDS = "SA_STEWARD.TNC_LANDS" # provide a default value if unspecified

feema1tomany = arcpy.GetParameterAsText(1)
if feema1tomany == '#' or not feema1tomany:
    feema1tomany = "feema1tomany" # provide a default value if unspecified

# Local variables:
v1 = SA_STEWARD_TNC_LANDS
v2 = v1
v3 = v2
v4 = v1
v5 = v4
v6 = v1
v7 = v6
v8 = v1
v9 = v8
v10 = v1
v11 = v10
v12 = v1
v13 = v12
v14 = v1
v15 = v14
v16 = v1
v17 = v16
v18 = v1
v19 = v18
v20 = v1
v21 = v20
v22 = v1
v23 = v22
v24 = v1
v25 = v24
SA_STEWARD_TNC_LANDS__2_ = v25

# Process: Join
arcpy.AddJoin_management(SA_STEWARD_TNC_LANDS, "MA_IFMS_ID", feema1tomany, "MA_IFMS_ID", "KEEP_COMMON")

# Process: Select NULL AREANAM
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.AREANAM IS NULL")

# Process: Calculate Field
arcpy.CalculateField_management(v2, "SA_STEWARD.TNC_LANDS.AREANAM", "[feema1tomany.AREANAM] + \" Fee\"", "VB", "")

# Process: Select NULL DESGNTN
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.DESGNTN IS NULL")

# Process: Calculate Field (2)
arcpy.CalculateField_management(v4, "SA_STEWARD.TNC_LANDS.DESGNTN", "\"Conservation Preserve\"", "VB", "")

# Process: Select NULL OWNER
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.OWNER IS NULL")

# Process: Calculate Field (3)
arcpy.CalculateField_management(v6, "SA_STEWARD.TNC_LANDS.OWNER", "\"Private\"", "VB", "")

# Process: Select NULL GAPCAT
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.GAPCAT IS NULL")

# Process: Calculate Field (4)
arcpy.CalculateField_management(v8, "SA_STEWARD.TNC_LANDS.GAPCAT", "\"1\"", "VB", "")

# Process: Select NULL PROTHOLD
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.PROTHOLD IS NULL")

# Process: Calculate Field (5)
arcpy.CalculateField_management(v10, "SA_STEWARD.TNC_LANDS.PROTHOLD", "\"The Nature Conservancy\"", "VB", "")

# Process: Select 4
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL")

# Process: PROTMECH
arcpy.CalculateField_management(v12, "SA_STEWARD.TNC_LANDS.PROTMECH", "\"Fee-simple ownership\"", "VB", "")

# Process: Select 3
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL")

# Process: CLSTRANDA
arcpy.CalculateField_management(v14, "SA_STEWARD.TNC_LANDS.CLSTRANSDA", "[feema1tomany.CLSTRANSDA]", "VB", "")

# Process: Select 2
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL")

# Process: MABR_NAME
arcpy.CalculateField_management(v16, "SA_STEWARD.TNC_LANDS.MABR_NAME", "[feema1tomany.MABR_NAME]", "VB", "")

# Process: Select NULL CMS_INTENT
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.CMS_INTENT IS NULL")

# Process: Calculate Field (9)
arcpy.CalculateField_management(v18, "SA_STEWARD.TNC_LANDS.CMS_INTENT", "\"Biodiversity Focus\"", "VB", "")

# Process: Select NULL CMS_DURATN
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.CMS_DURATN IS NULL")

# Process: Calculate Field (10)
arcpy.CalculateField_management(v20, "SA_STEWARD.TNC_LANDS.CMS_DURATN", "\"Permanent Commitment\"", "VB", "")

# Process: Select NULL CMS_EMP
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL AND SA_STEWARD.TNC_LANDS.CMS_EMP IS NULL")

# Process: Calculate Field (11)
arcpy.CalculateField_management(v22, "SA_STEWARD.TNC_LANDS.CMS_EMP", "\"High Potential\"", "VB", "")

# Process: Select 1
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.MA_IFMS_ID IS NOT NULL AND SA_STEWARD.TNC_LANDS.TR_IFMS_ID IS NULL")

# Process: CLS_ACRES
arcpy.CalculateField_management(v24, "SA_STEWARD.TNC_LANDS.CLS_ACRES", "[feema1tomany.CLS_ACRES]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management(v25, "feema1tomany")

