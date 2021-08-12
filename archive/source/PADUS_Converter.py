#---------------------------------------------------------------------
# Name:             PADUS_Converter.py
# Purpose:          Converts TNC Fee lands data into 2017 schema for PADUS-USGS
# Author:           Jim Platt
# Created:          20131115
# Editor:           
# Last revised:     20170514
# ArcGIS Version:   10.4.1
# Python Version:   2.7
# Requires:         PADUS_Data.py
#---------------------------------------------------------------------
import os
import datetime
import arcpy
from PADUS_Data import *

if __name__ == '__main__':
    """TODO
    """
    # Arguments are optional
    #argv = tuple(arcpy.GetParameterAsText(i)
        #for i in range(arcpy.GetArgumentCount()))
    #do_analysis(*argv)
    logFile = r''
    debug = False
    #=================================================================================================================================
    #TNCLandsTable = 'Database Connections/MNSPATIAL_VIEWER@mnspatial.tnc.org.sde/tncgdb.NACRLOADER.TNC_Lands'
    TNCLandsTable = 'E:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Lands/Data/20170509.gdb/TNC_Lands_AEAC_USGS'
    PADUS_TargetTable = 'E:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Lands/Data/PADUS_USGS/2017/PADUS_Schema4_22_16.gdb/PADUS_SchemaFee_TNC'
    
    theResult = do_PADUS_USGS(TNCLandsTable, PADUS_TargetTable)
    
    print theResult

    try:
        print 'Dissolving fee lands'
        output = "{0}_dissolve".format(PADUS_TargetTable)
        arcpy.Dissolve_management(PADUS_TargetTable,
                                  output,
                                  ['Category', 'Own_Type', 'Own_Name', 'Loc_Own', 'Mang_Type', 'Mang_Name', 
                                   'Loc_Mang', 'Des_Tp', 'Loc_Ds', 'Unit_Nm', 'Loc_Nm', 'State_Nm', 'Agg_Src',
                                   'GIS_Src', 'Src_Date', 'GIS_Acres', 'Source_PAID', 'WDPA_Cd', 'Access', 'Access_Src',
                                   'GAP_Sts', 'GAPCdSrc', 'GAPCdDt', 'IUCN_Cat', 'IUCNCtSrc', 'IUCNCtDt', 'Date_Est',
                                   'Comments'], 
                                  '', "MULTI_PART", "DISSOLVE_LINES")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        print "Arcpy error in dissolve"            
    except Exception as e:
        print e.args[0]
        print "General exception in dissolve"
    
    try:
        print 'Calculating GIS_Acres field'
        arcpy.CalculateField_management(in_table=output, 
                                        field="GIS_Acres", 
                                        expression="!shape.area@acres!", 
                                        expression_type="PYTHON_9.3", 
                                        code_block="")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        print "Arcpy error in calculating GIS_Acres"    
    except Exception as e:
        print e.args[0]
        print "General exception in calculating GIS_Acres"    
    
    print 'Finished'