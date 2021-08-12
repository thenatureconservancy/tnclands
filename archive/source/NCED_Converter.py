#---------------------------------------------------------------------
# Name:             dataShareConverter.py
# Purpose:          
# Author:           
# Created:          20131115
# Editor:           
# Last revised:     
# ArcGIS Version:   10.1
# Python Version:   2.7
# Requires:         convertData.py
#---------------------------------------------------------------------
import os
import datetime
import arcpy
from NCED_Data import *

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
    basePath = 'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Ent_GIS/TNC_Lands/Data/TNC_NCED_2018.gdb'
    TNCLandsTable =    os.path.join(basePath, 'TNC_Lands_AlbersUSGS')
    nced_TargetTable = os.path.join(basePath, 'NCED_TNC_2018')
    
    #do_NCED(TNCLandsTable, nced_TargetTable)

    arcpy.Dissolve_management(nced_TargetTable,
                              "{0}_dissolve".format(nced_TargetTable),
                              ["unique_id", "security", "sitename", "esmthldr", "eholdtype", "owntype", 
                               "s_emthd1", "s_emthd2", "purpose", "pubaccess", "duration", "term", 
                               "mon_est", "day_est", "year_est", "state", "rep_acres", "gis_acres", 
                               "pct_diff", "gapcat", "iucncat", "dataagg", "dataentry", "datapvdr", 
                               "datasrc", "source_uid", "conflict", "stacked", "comments", "eholduid1", 
                               "eholduid2", "eholduid3", "report_href", "county", "created_user",
                               "created_date", "last_edited_user", "last_edited_date"],
                              "REP_ACRES_TNC SUM", "MULTI_PART", "DISSOLVE_LINES")
            
    print 'Finished'