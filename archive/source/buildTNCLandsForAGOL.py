#---------------------------------------------------------------------
# Name:             build_TNC_Lands_for_AGOL.py
# Purpose:          This script creates a blank feature class, adds the 
#                   required fields and populates them from the source 
#                   feature calsses
# Author:
# Created:          20210211
# Editor:
# Last revised:
# ArcGIS Version:   Pro 2.71
# Python Version:   3.7
# Requires:
#---------------------------------------------------------------------
import os
import arcpy
#connection path to the feature classes on MNSPATIAL
tncLands_WGS84 = 'C:/Users/jplatt.TNC/Documents/ArcGIS/SQLServer/NACRLOADER@default.mnspatial.tnc.org.sde/tncgdb.NACRLOADER.TNC_Lands'
tncTrnAst_WGS84 = 'C:/Users/jplatt.TNC/Documents/ArcGIS/SQLServer/NACRLOADER@default.mnspatial.tnc.org.sde/tncgdb.NACRLOADER.TNC_TransfersAndAssists'
#feature class names for the projected versions
tncLands_WMAS = 'TNC_Lands_WMAS'
tncTrnAst_WMAS = 'TNC_TransfersAndAssists_WMAS'
#feature class name for the combined datasets
tncLndTrnAst_WMAS = 'TNC_Lands_Transfers_Assists_WMAS'
#local workspace name
workspace = 'D:/jplatt/projects/NorthAmericaRegion/TNC_Lands/data/TNC_Lands_Working.gdb'
#local environment settings
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True
srWGS84 = arcpy.SpatialReference(4326)  #WGS 84 GCS - the source feature class SR 
srWMAS = arcpy.SpatialReference(3857)   #Web Mercator Auxiallry Sphere - WGS84 projected coordinate system - the target feature class SR

##TODO 
#work on fixing case of text fields
#work on separating author from geometry source entries

#tidy up if this is not the first time the script has been run
print('Deleting projected and combined feature classes')
for fc in [tncLands_WMAS, tncTrnAst_WMAS, tncLndTrnAst_WMAS]:
    try:
        fc_toDelete = os.path.join(workspace, fc)
        if arcpy.Exists(fc_toDelete):
            print(f'\tDeleting old {fc} feature class')
            arcpy.management.Delete(fc_toDelete)
        else:
            print(f'\t{fc} feature class doesn\'t exist')
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print(e.args[0])

#project TNC Lands source from the geodatabase on MNSPATIAL.TNC.ORG from WGS84 to Web Mercator Auxiliary Sphere - WGS84
print('Projecting TNC Lands source feature class to WMAS')
try:
    arcpy.management.Project(in_dataset = tncLands_WGS84,
                             out_dataset = tncLands_WMAS,
                             out_coor_system = srWMAS)
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#check for geometry errors after TNC Lands projection
print('Checking projected TNC Lands feature class for geometry errors')
try:
    arcpy.management.CheckGeometry(in_features = tncLands_WMAS,
                                   out_table = 'tncLands_WMAS_check_geometry')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#and fix if necessary
if int(arcpy.management.GetCount('tncLands_WMAS_check_geometry')[0]) > 0:
    print(f'Repairing geometry errors of {tncLands_WMAS}')
    try:
        arcpy.management.RepairGeometry(in_features=tncLands_WMAS)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print(e.args[0])

#project TNC Transfers and Assists source from the geodatabase on MNSPATIAL.TNC.ORG from WGS84 to Web Mercator Auxiliary Sphere - WGS84
print('Projecting Transfers and Assists source feature class to WMAS')
try:
        arcpy.management.Project(in_dataset = tncTrnAst_WGS84,
                                 out_dataset = tncTrnAst_WMAS,
                                 out_coor_system = srWMAS)
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#check for geometry errors after TNC Transfers and Assists projection
print('Checking projected TNC Transfers and Assists feature class for geometry errors')
try:
    arcpy.management.CheckGeometry(in_features = tncTrnAst_WMAS,
                                   out_table = 'tncTransfersAndAssists_WMAS_check_geometry')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#and fix if necessary
if int(arcpy.management.GetCount('tncTransfersAndAssists_WMAS_check_geometry')[0]) > 0:
    print(f'Repairing geometry errors of {tncTrnAst_WMAS}')
    try:
        arcpy.management.RepairGeometry(in_features=tncTrnAst_WMAS)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print(e.args[0])

#create combined feature class
try:
    print(f'Creating combined feature class')
    arcpy.management.CreateFeatureclass(workspace, 
                                        f'{tncLndTrnAst_WMAS}', 
                                        'POLYGON', 
                                        None, 
                                        'DISABLED', 
                                        'DISABLED', 
                                        srWMAS
                                        )
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#add fields to combined feature class
try:
    print('Adding fields to combined feature class')
    arcpy.management.AddFields(f'{tncLndTrnAst_WMAS}', 
                               [['TR_LRM_ID', 'LONG', 'LRM_Tract_ID'],                  #TR_LRM_ID
                                ['TR_LRM_NA', 'TEXT', 'LRM_Tract_Name', 254],           #TRACT_NAME
                                ['COUNTRY', 'TEXT', 'Country', 254],                    #COUNTRY
                                ['STATE', 'TEXT', 'State', 2],                          #STATE
                                ['PUBLIC_NA', 'TEXT', 'Public_Name', 254],              #AREANAME
                                ['CONS_AREA', 'TEXT', 'LRM_Cons_Area_Name', 254],       #NEW FIELD
                                ['PROTHOLD', 'TEXT', 'Holder', 254],                    #PROTHOLD
                                ['TNC_INT', 'TEXT', 'TNC_Interest_Code', 254],          #PROTMECH
                                ['SHARE', 'TEXT', 'Shareable', 32],                     #SENSDATA
                                ['LRM_ACRES', 'DOUBLE', 'LRM_Protected_Acres'],         #LRM_ACRES
                                ['GIS_ACRES', 'DOUBLE', 'GIS_Acres'],                   #NEW FIELD
                                ['PROT_DATE', 'DATE', 'Original_Protection_Date'],      #CLSTRANSDA
                                ['DATE_XFER', 'DATE', 'Date_Transferred'],              #NEW FIELD
                                ['MU_LRM_ID', 'LONG', 'LRM_MU_ID'],                     #MA_LRM_ID
                                ['MU_LRM_NA', 'TEXT', 'LRM_MU_Name', 254],              #MABR_NAME
                                ['MON_REQ', 'TEXT', 'Monitor_Required', 5],             #NEW FIELD
                                ['MON_ID', 'TEXT', 'Monitor_Report_ID', 254],           #NEW FIELD
                                ['MON_NA', 'TEXT', 'Monitor_Report_Name', 254],         #NEW FIELD
                                ['PRSRV', 'TEXT', 'Preserve', 5],                       #NEW FIELD
                                ['PRSRV_NA', 'TEXT', 'Preserve_Name', 254],             #NEW FIELD
                                ['PUB_ACCESS', 'TEXT', 'Public_Access', 24],            #NEW FIELD
                                ['FEE_OWNER', 'TEXT', 'Fee_Owner', 254],                #NEW FIELD
                                ['OTHINTHLDR', 'TEXT', 'Other_Interest_Holder', 254],   #NEW FIELD
                                ['OTHINTTYPE', 'TEXT', 'Other_Interest_Type', 254],     #NEW FIELD
                                ['AUTHOR', 'TEXT', 'Author', 254],                      #SOURCE
                                ['GEOMSRC', 'TEXT', 'Geometry_Source', 254],            #SOURCE
                                ['MOD_DATE', 'DATE', 'Date_Record_Modified'],           #MOD_DATE
                                ['GAP_CAT', 'TEXT', 'GAP_Category',5],                  #GAPCAT
                                ['COMMENTS', 'TEXT', 'Comments', 254],                  #NEW FIELD
                                ['QC_FLAG', 'TEXT', 'QC_Flag', 12],                     #NEW FIELD
                                ['QC_NOTES', 'TEXT', 'QC_Notes', 254],                  #NEW FIELD
                                ['ORIGIN', 'TEXT', 'Original_Data_Source', 56]          #NEW FIELD
                               ]
                            ) 
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#append TNC Lands feature records to new feature class
try:
    print('Appending TNC Lands to combined feature class')
    arcpy.management.Append(f'{tncLands_WMAS}', 
                            f'{tncLndTrnAst_WMAS}', 
                            'NO_TEST', 
                            f"LRM_TR_ID 'LRM_Tract_ID' true true false 4 Long 0 0,First,#,{tncLands_WMAS},TR_LRM_ID,-1,-1;\
                            LRM_TR_NA 'LRM_Tract_Name' true true false 254 Text 0 0,First,#,{tncLands_WMAS},TRACT_NAME,0,254;\
                            COUNTRY 'Country' true true false 254 Text 0 0,First,#,{tncLands_WMAS},COUNTRY,0,254;\
                            STATE 'State' true true false 2 Text 0 0,First,#,{tncLands_WMAS},STATE,0,2;\
                            PUBLIC_NA 'Public_Name' true true false 254 Text 0 0,First,#,{tncLands_WMAS},AREANAM,0,254;\
                            CONS_AREA 'LRM_Cons_Area_Name' true true false 254 Text 0 0,First,#;\
                            PROTHOLD 'Holder' true true false 254 Text 0 0,First,#,{tncLands_WMAS},PROTHOLD,0,225;\
                            TNC_INT 'TNC_Interest_Code' true true false 254 Text 0 0,First,#,{tncLands_WMAS},PROTMECH,0,225;\
                            SHARE 'Shareable' true true false 32 Text 0 0,First,#,{tncLands_WMAS},SENSDATA,0,10;\
                            LRM_ACRES 'LRM_Protected_Acres' true true false 8 Double 0 0,First,#,{tncLands_WMAS},CLS_ACRES,-1,-1;\
                            GIS_ACRES 'GIS_Acres' true true false 8 Double 0 0,First,#;\
                            PROT_DATE 'Original_Protection_Date' true true false 8 Date 0 0,First,#,{tncLands_WMAS},CLSTRANSDA,-1,-1;\
                            DATE_XFER 'Date_Transferred' true true false 8 Date 0 0,First,#;\
                            MU_LRM_ID 'LRM_Monitoring_Unit_ID' true true false 4 Long 0 0,First,#,{tncLands_WMAS},MA_LRM_ID,-1,-1;\
                            MU_LRM_NA 'LRM_Monitoring_Unit_Name' true true false 254 Text 0 0,First,#,{tncLands_WMAS},MABR_NAME,0,254;\
                            MON_REQ 'Monitor_Required' true true false 5 Text 0 0,First,#;\
                            MON_ID 'Monitor_Report_ID' true true false 254 Text 0 0,First,#;\
                            MON_NA 'Monitor_Report_Name' true true false 254 Text 0 0,First,#;\
                            PRSRV 'Preserve' true true false 5 Text 0 0,First,#;\
                            PRSRV_NA 'Preserve Name' true true false 254 Text 0 0,First,#;\
                            PUB_ACCESS 'Public_Access' true true false 24 Text 0 0,First,#;\
                            FEE_OWNER 'Fee_Owner' true true false 254 Text 0 0,First,#;\
                            OTHINTHLDR 'Other_Interest_Holder' true true false 254 Text 0 0,First,#;\
                            OTHINTTYPE 'Other_Interest_Type' true true false 254 Text 0 0,First,#;\
                            AUTHOR 'Author' true true false 254 Text 0 0,First,#,{tncLands_WMAS},SOURCE,0,254;\
                            GEOMSRC 'Geometry_Source' true true false 254 Text 0 0,First,#,{tncLands_WMAS},SOURCE,0,254;\
                            MOD_DATE 'Date_Record_Modified' true true false 8 Date 0 0,First,#,{tncLands_WMAS},MOD_DATE,-1,-1;\
                            GAP_CAT 'GAP_Category' true true false 5 Text 0 0,First,#,{tncLands_WMAS},GAPCAT,0,50;\
                            COMMENTS 'Comments' true true false 1024 Text 0 0,First,#;\
                            QC_FLAG 'QC_Flag' true true false 12 Text 0 0,First,#;\
                            QC_NOTES 'QC_Notes' true true false 1024 Text 0 0,First,#;\
                            ORIGIN 'Original_Data_Source' true true false 56 Text 0 0,First,#",
                            '',
                            '')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#create table view of combined feature class and calculate ORIGIN field to TNC_Lands, 
#so chapter staff will know where a record came from, important to distinquish between transfer and active LRM records
print('Creating table view and calculating origin field for TNC_Lands')
try:
    arcpy.MakeTableView_management(f'{tncLndTrnAst_WMAS}', 'outTableView')
    arcpy.management.CalculateField('outTableView', 'ORIGIN', '"TNC_Lands"', 'PYTHON3', '', 'TEXT')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

arcpy.Delete_management('outTableView')

#append TNC Transfer ans Assist feature records to new feature class
try:
    print('Appending TNC Transfers and Assists to combined feature class')
    arcpy.management.Append(f'{tncTrnAst_WMAS}', 
                            f'{tncLndTrnAst_WMAS}', 
                            'NO_TEST', 
                            f"LRM_TR_ID 'LRM_Tract_ID' true true false 4 Long 0 0,First,#,{tncTrnAst_WMAS},TR_LRM_ID,-1,-1;\
                            LRM_TR_NA 'LRM_Tract_Name' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},TRACT_NAME,0,254;\
                            COUNTRY 'Country' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},COUNTRY,0,254;\
                            STATE 'State' true true false 2 Text 0 0,First,#,{tncTrnAst_WMAS},STATE,0,2;\
                            PUBLIC_NA 'Public_Name' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},AREANAM,0,254;\
                            CONS_AREA 'LRM_Cons_Area_Name' true true false 254 Text 0 0,First,#;\
                            PROTHOLD 'Holder' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},PROTHOLD,0,225;\
                            TNC_INT 'TNC_Interest_Code' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},PROTMECH,0,225;\
                            SHARE 'Shareable' true true false 32 Text 0 0,First,#,{tncTrnAst_WMAS},SENSDATA,0,10;\
                            LRM_ACRES 'LRM_Protected_Acres' true true false 8 Double 0 0,First,#,{tncTrnAst_WMAS},CLS_ACRES,-1,-1;\
                            GIS_ACRES 'GIS_Acres' true true false 8 Double 0 0,First,#;\
                            PROT_DATE 'Original_Protection_Date' true true false 8 Date 0 0,First,#,{tncTrnAst_WMAS},CLSTRANSDA,-1,-1;\
                            DATE_XFER 'Date_Transferred' true true false 8 Date 0 0,First,#;\
                            MU_LRM_ID 'LRM_Monitoring_Unit_ID' true true false 4 Long 0 0,First,#,{tncTrnAst_WMAS},MA_LRM_ID,-1,-1;\
                            MU_LRM_NA 'LRM_Monitoring_Unit_Name' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},MABR_NAME,0,254;\
                            MON_REQ 'Monitor_Required' true true false 5 Text 0 0,First,#;\
                            MON_ID 'Monitor_Report_ID' true true false 254 Text 0 0,First,#;\
                            MON_NA 'Monitor_Report_Name' true true false 254 Text 0 0,First,#;\
                            PRSRV 'Preserve' true true false 5 Text 0 0,First,#;\
                            PRSRV_NA 'Preserve_Name' true true false 254 Text 0 0,First,#;\
                            PUB_ACCESS 'Public_Access' true true false 24 Text 0 0,First,#;\
                            FEE_OWNER 'Fee_Owner' true true false 254 Text 0 0,First,#;\
                            OTHINTHLDR 'Other_Interest_Holder' true true false 254 Text 0 0,First,#;\
                            OTHINTTYPE 'Other_Interest_Type' true true false 254 Text 0 0,First,#;\
                            AUTHOR 'Author' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},SOURCE,0,254;\
                            GEOMSRC 'Geometry_Source' true true false 254 Text 0 0,First,#,{tncTrnAst_WMAS},SOURCE,0,254;\
                            MOD_DATE 'Date_Record_Modified' true true false 8 Date 0 0,First,#,{tncTrnAst_WMAS},MOD_DATE,-1,-1;\
                            GAP_CAT 'GAP_Category' true true false 5 Text 0 0,First,#,{tncTrnAst_WMAS},GAPCAT,0,50;\
                            COMMENTS 'Comments' true true false 1024 Text 0 0,First,#;\
                            QC_FLAG 'QC_Flag' true true false 12 Text 0 0,First,#;\
                            QC_NOTES 'QC_Notes' true true false 1024 Text 0 0,First,#;\
                            ORIGIN 'Original Data Source' true true false 56 Text 0 0,First,#",
                            '',
                            '')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#check for geometry errors after TNC Lands and Transfers and Assists are combined
print('Checking projected TNC Lands, Transfers and Assists feature class for geometry errors')
try:
    arcpy.management.CheckGeometry(in_features = tncLndTrnAst_WMAS,
                                   out_table = 'tncLandsTransfersAndAssists_WMAS_check_geometry')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

#and fix if necessary
if int(arcpy.management.GetCount('tncLandsTransfersAndAssists_WMAS_check_geometry')[0]) > 0:
    print(f'Repairing geometry errors of {tncLndTrnAst_WMAS}')
    try:
        arcpy.management.RepairGeometry(in_features=tncLndTrnAst_WMAS)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print(e.args[0])

#create table view of combined feature class and calculate ORIGIN field to TNC_Transfers and Assists, 
#so chapter staff will know where a record came from, important to distinquish between transfer and active LRM records
print('Creating table view and calculating origin field for TNC_TransfersAndAssists')
try:
    arcpy.management.MakeTableView(f'{tncLndTrnAst_WMAS}', 'outTableView', 'ORIGIN IS NULL', None)
    result = arcpy.management.GetCount('outTableView')
    print(f'number of records in transfers: {result[0]}')
    arcpy.management.CalculateField('outTableView', 'ORIGIN', '"TNC_TransfersAndAssists"', 'PYTHON3', '', 'TEXT')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

arcpy.Delete_management('outTableView')

# print('Dissolving TNC Lands Base features')
# try:
#     arcpy.management.Dissolve(f'{tncLndTrnAst_WMAS}',
#                              "D:/data/TNC_Lands/data/TNC_Lands_working.gdb\TNCLandsBase_Dissolve", 
#                              "TR_LRM_ID;TR_LRM_NA;COUNTRY;STATE;PUBLIC_NA;CONS_AREA;PROTHOLD;TNC_INT;SHARE;LRM_ACRES;\
#                              PROT_DATE;DATE_XFER;MU_LRM_ID;MU_LRM_NA;MON_REQ;MON_ID;PUB_ACCESS;FEE_OWNER;COMMENTS;OTHINTHLDR;\
#                              OTHINTTYPE;AUTHOR;GEOMSOURCE;MOD_DATE;GAP_CAT;COMMENTS;QC_FLAG;QC_NOTES;ORIGIN",
#                              None,
#                              "MULTI_PART", 
#                              "DISSOLVE_LINES")
# except arcpy.ExecuteError:
#     print(arcpy.GetMessages(2))
# except Exception as e:
#     print(e.args[0])

#and finally, calculate GIS acres to 2 decimal places
print('Calculating GIS Acres')
try:
    arcpy.MakeTableView_management(f'{tncLndTrnAst_WMAS}', 'outTableView')
    arcpy.management.CalculateField('outTableView', 'GIS_ACRES', 'round(!shape.area@acres!, 2)', 'PYTHON3', '', 'TEXT')
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as e:
    print(e.args[0])

print('finished')