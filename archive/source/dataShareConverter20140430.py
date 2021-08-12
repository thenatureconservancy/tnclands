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
from convertData import *

if __name__ == '__main__':
    """TODO
    Add websymbol and text id fields to internal data
    Add point versions of parcels to web file geodatabase
    Zip internal and download versions of file geodatabases
    """
    # Arguments are optional
    #argv = tuple(arcpy.GetParameterAsText(i)
        #for i in range(arcpy.GetArgumentCount()))
    #do_analysis(*argv)
    logFile = r''
    debug = False
    #=================================================================================================================================
    TNCLandsTable = 'Database Connections/mnsde_viewer @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.TNC_Lands'
    TNCLANDSTABLE = 'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/TNCLands/source.gdb/TNC_Lands'
    
    TransferredTNCLandsTable = 'Database Connections/mnsde_viewer @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.Transferred_TNC_Lands'
    TRANSFERREDTNCLANDSTABLE = 'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/TNCLands/source.gdb/Transferred_TNC_Lands'
    
    dateString = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    DATESTRING = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    
    basepath = "D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/public"
    BASEPATH = "D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/public"
    #---------------------------------------------------------------------------------------------------------------------------------
    print 'Creating public web version of TNC Lands'
    fileGDBName = "TNCLands_w_{0}.gdb".format(DATESTRING)
    do_PublicTNCLandsWeb(BASEPATH,
                         fileGDBName,
                         TNCLANDSTABLE,
                         TRANSFERREDTNCLANDSTABLE)

    print 'Creating public download version of TNC Lands'
    fileGDBName = "TNCLands_d_{0}.gdb".format(DATESTRING)
    do_PublicTNCLandsDownload(BASEPATH,
                              fileGDBName,
                              TNCLANDSTABLE,
                              TRANSFERREDTNCLANDSTABLE)
    
    print 'Creating zip files'
    fileGDBPath = os.path.join(BASEPATH, fileGDBName)
    zipData(os.path.join(fileGDBPath, "TNC_Lands"), 
            os.path.join(fileGDBPath, "Transferred_TNC_Lands"),
            os.path.join(BASEPATH, "shps"),
            os.path.join(BASEPATH, "gdbs"),
            os.path.join(BASEPATH, "zips"))
    
    #---------------------------------------------------------------------------------------------------------------------------------
    BASEPATH = "D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/internal"    
    fileGDBName = "TNCLands_d_{0}.gdb".format(DATESTRING)
    print 'Creating internal web version of TNC Lands'
    do_InternalTNCLandsWeb(BASEPATH,
                           fileGDBName,
                           TNCLANDSTABLE,
                           TRANSFERREDTNCLANDSTABLE)
    
    print 'Creating internal download version of TNC Lands'
    do_InternalTNCLandsDownload(TNCLANDSTABLE,
                                TRANSFERREDTNCLANDSTABLE)
    
#=================================================================================================================================  
    #nced_TargetTable = r'D:\GIS_Data\jplatt\Workspace\Data\NACR\TNCLands\Data\NCED\TNC_NCED_Easements.gdb\NCED_Poly'
    #do_NCED(TNCLandsTable, nced_TargetTable)
    #arcpy.Dissolve_management(r'D:\GIS_Data\jplatt\Workspace\Data\NACR\TNCLands\Data\NCED\TNC_NCED_Easements.gdb\NCED_Poly',
                              #r'D:\GIS_Data\jplatt\Workspace\Data\NACR\TNCLands\Data\NCED\TNC_NCED_Easements.gdb\NCED_Poly_dissolve',
                              #["unique_id", "security", "sitename", "esmthldr", "eholdtyp", 
                               #"owntype", "s_emthd1", "s_emthd2", "purpose", "gapsts", "pubaccess", 
                               #"duration", "term", "mon_est", "day_est", "year_est", "state", 
                               #"dataagg", "dataentry", "datapvdr", "datasrc", "source_uid",
                               #"pct_diff", "conflict", "stacked", "iucncat", "wpda_cd", "comments"],
                               #"REP_ACRES SUM", "MULTI_PART", "DISSOLVE_LINES")
    
#=================================================================================================================================
    #padus_TargetTable = r'D:\GIS_Data\jplatt\Workspace\Data\NACR\TNC Lands\Data\PADUS_USGS\PADUS1_4Schema10.gdb\PADUS_1_4'
    #do_PADUS_USGS(sourceTable, padus_TargetTable)
    #arcpy.Dissolve_management("PADUS v 1.4", 
                              #"D:\GIS_Data\jplatt\Workspace\Data\NACR\TNC Lands\Data\PADUS_USGS\PADUS1_4Schema10.gdb\PADUS_1_4_dissolve",
                              #['Category', 'Own_Type', 'Own_Name', 'Loc_Own', 'Mang_Name', 'P_Des_Tp', 'P_Loc_Ds', 'P_Des_Nm', 
                               #'P_Loc_Nm', 'Status', 'State_Nm', 'Agg_Src', 'GIS_Src', 'Src_Date', 'GIS_Acres', 'Source_UID', 
                               #'Source_PAID', 'WDPA_Cd', 'S_Des_Tp', 'S_Lc_Ds', 'S_Loc_Nm', 'Access', 'Access_Src', 'GAP_Sts'
                               #'GAPCdSrc', 'GAPCdDt', 'IUCN_Cat', 'Date_Est', 'Comments', 'EsmtHldr', 'EHoldTyp'],
                              #'#', 'MULTI_PART', 'DISSOLVE_LINE')
    #arcpy.CalculateField_management("D:\GIS_Data\jplatt\Workspace\Data\NACR\TNC Lands\Data\PADUS_USGS\PADUS1_4Schema10.gdb\PADUS_1_4_dissolve",
                                    #'GIS_Acres', '!shape.area@acres!', 'PYTHON_9.3', '#')

#=================================================================================================================================
            
    print 'Finished'