# ---------------------------------------------------------------------------
# rstTracts.py
# Created on: 2012-09-24 14:29:43.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: rstTracts <SA_STEWARD_TNC_LANDS__2_> <rsttracts__2_> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
SA_STEWARD_TNC_LANDS__2_ = arcpy.GetParameterAsText(0)
if SA_STEWARD_TNC_LANDS__2_ == '#' or not SA_STEWARD_TNC_LANDS__2_:
    SA_STEWARD_TNC_LANDS__2_ = "SA_STEWARD.TNC_LANDS" # provide a default value if unspecified

rsttracts__2_ = arcpy.GetParameterAsText(1)
if rsttracts__2_ == '#' or not rsttracts__2_:
    rsttracts__2_ = "rsttracts" # provide a default value if unspecified

# Local variables:
v1 = SA_STEWARD_TNC_LANDS__2_
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
v18 = v1
v19 = v18
v20 = v1
v21 = v20
v22 = v1
v23 = v22
v10__2_ = v1
v13 = v10__2_
v11_1_ = v1
v15 = v11_1_
v15_1_ = v1
v17 = v15_1_
v17_1_ = v1
v25__2_ = v17_1_
v23_2_ = v1
v25__3_ = v23_2_
SA_STEWARD_TNC_LANDS = v25__3_
v24_1_ = v1
v25 = v24_1_

# Process: Add Join
arcpy.AddJoin_management(SA_STEWARD_TNC_LANDS__2_, "TR_IFMS_ID", rsttracts__2_, "TR_IFMS_ID", "KEEP_COMMON")

# Process: Select NULL AREANAM
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.AREANAM IS NULL")

# Process: Calculate Field
arcpy.CalculateField_management(v2, "SA_STEWARD.TNC_LANDS.AREANAM", "[rsttracts.AREANAM] + \" Restriction\"", "VB", "")

# Process: Select NULL DESGNTN
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.DESGNTN IS NULL")

# Process: Calculate Field (2)
arcpy.CalculateField_management(v4, "SA_STEWARD.TNC_LANDS.DESGNTN", "\"Conservation Preserve\"", "VB", "")

# Process: Select NULL OWNER
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.OWNER IS NULL")

# Process: Calculate Field (3)
arcpy.CalculateField_management(v6, "SA_STEWARD.TNC_LANDS.OWNER", "\"Private\"", "VB", "")

# Process: Select NULL GAPCAT
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.GAPCAT IS NULL")

# Process: Calculate Field (4)
arcpy.CalculateField_management(v8, "SA_STEWARD.TNC_LANDS.GAPCAT", "\"2\"", "VB", "")

# Process: Select NULL PROTHOLD
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.PROTHOLD IS NULL")

# Process: Calculate Field (5)
arcpy.CalculateField_management(v10, "SA_STEWARD.TNC_LANDS.PROTHOLD", "\"The Nature Conservancy\"", "VB", "")

# Process: SELECT 1 = 1
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "1 = 1")

# Process: PROTECH
arcpy.CalculateField_management(v10__2_, "SA_STEWARD.TNC_LANDS.PROTMECH", "\"Deed Restriction\"", "VB", "")

# Process: SELECT 1 = 1 [1]
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "1 = 1")

# Process: CLSTRANSDA
arcpy.CalculateField_management(v11_1_, "SA_STEWARD.TNC_LANDS.CLSTRANSDA", "[rsttracts.CLSTRANSDA]", "VB", "")

# Process: SELECT 1 = 1[2]
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "1 = 1")

# Process: MABR_NAME
arcpy.CalculateField_management(v15_1_, "SA_STEWARD.TNC_LANDS.MABR_NAME", "[rsttracts.MABR_NAME]", "VB", "")

# Process: Select NULL CMS_INTENT
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.CMS_INTENT IS NULL")

# Process: Calculate Field (9)
arcpy.CalculateField_management(v18, "SA_STEWARD.TNC_LANDS.CMS_INTENT", "\"Biodiversity Compatible\"", "VB", "")

# Process: Select NULL CMS_DURATN
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.CMS_DURATN IS NULL")

# Process: Calculate Field (10)
arcpy.CalculateField_management(v20, "SA_STEWARD.TNC_LANDS.CMS_DURATN", "\"Long Term Commitment\"", "VB", "")

# Process: Select NULL CMS_EMP
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "SA_STEWARD.TNC_LANDS.CMS_EMP IS NULL")

# Process: Calculate Field (11)
arcpy.CalculateField_management(v22, "SA_STEWARD.TNC_LANDS.CMS_EMP", "\"Moderate Potential\"", "VB", "")

# Process: SELECT 1 = 1 (6)
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "1 = 1")

# Process: CLS_ACRES
arcpy.CalculateField_management(v24_1_, "SA_STEWARD.TNC_LANDS.CLS_ACRES", "[rsttracts.CLS_ACRES]", "VB", "")

# Process: SELECT 1 = 1 [3]
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "1 = 1")

# Process: TRACT_NAME
arcpy.CalculateField_management(v17_1_, "SA_STEWARD.TNC_LANDS.TRACT_NAME", "[rsttracts.TRACT_NAME]", "VB", "")

# Process: SELECT 1 = 1[5]
arcpy.SelectLayerByAttribute_management(v1, "NEW_SELECTION", "1 = 1")

# Process: MA_IFMS_ID
arcpy.CalculateField_management(v23_2_, "SA_STEWARD.TNC_LANDS.MA_IFMS_ID", "[rsttracts.MA_IFMS_ID]", "VB", "")

# Process: Remove Join
arcpy.RemoveJoin_management(v25__3_, "rsttracts")

