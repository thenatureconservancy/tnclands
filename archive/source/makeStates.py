import arcpy
import os
import zipfile
import glob
import zlib

def zipFileGeodatabase(inFileGeodatabase, newZipFN):
    if not (os.path.exists(inFileGeodatabase)):
        return False
    if (os.path.exists(newZipFN)):
        os.remove(newZipFN)
    zipobj = zipfile.ZipFile(newZipFN,'w')
    for infile in glob.glob(inFileGeodatabase+"/*"):
        zipobj.write(infile, os.path.basename(inFileGeodatabase)+"/"+os.path.basename(infile), zipfile.ZIP_DEFLATED)
    zipobj.close()
    return True

arcpy.env.overwriteOutput = True
# set workspace
arcpy.env.workspace = 'D:/Workspace/Data/NACR/TNCLands/Data/tncLands/shps'
#state table
st = 'Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.stateList'
#set search cursor on state table
stcur = arcpy.SearchCursor(st)
#create feature layer for TNC Lands
arcpy.MakeFeatureLayer_management(r'Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.TNC_Lands', "lyr")
#file paths
shploc = "D:/Workspace/Data/NACR/TNCLands/Data/tncLands/shps"
ziploc = "D:/Workspace/Data/NACR/TNCLands/Data/tncLands/zips"
# loop through state table, select rows by state, create gdb and feature class, convert feature class to shapefile
for row in stcur:
    wc = "\"STATE\" = '{0}'".format(row.FIPS)
    print "Selecting {0}".format(wc)
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", wc)
    print "Creating File GDB TNC_LANDS_{0}".format(row.State)
    arcpy.CreateFileGDB_management(ziploc, "TNC_Lands_{0}".format(row.State), "10.0")
    print "Adding TNC_Lands_{0} layer to gdb".format(row.State)
    arcpy.CopyFeatures_management("lyr",  "{0}/TNC_Lands_{1}.gdb/TNC_Lands_{1}".format(ziploc,row.State))
    print "Creating shapefile"
    arcpy.FeatureClassToShapefile_conversion("{0}/TNC_Lands_{1}.gdb/TNC_Lands_{1}".format(ziploc, row.State), shploc)
    #zip new file gdb
    infile = "D:/Workspace/Data/NACR/TNCLands/Data/tncLands/zips/TNC_Lands_{0}.gdb".format(row.State)
    outfile = "D:/Workspace/Data/NACR/TNCLands/Data/tncLands/zips/TNC_Lands_{0}.zip".format(row.State)
    zipFileGeodatabase(infile,outfile)
    print "zipped file GDB {0}".format(row.State)
#zip shapefile after state loop
sFiles = arcpy.ListFeatureClasses()
    
for s in sFiles:
    zName = s[:-4]
    theZip = zipfile.ZipFile("{0}/{1}.zip".format(shploc, zName), 'w', zlib.DEFLATED)
    theZip.write("{0}/{1}.dbf".format(shploc, zName),  "{0}.dbf".format(zName))
    theZip.write("{0}/{1}.prj".format(shploc, zName),  "{0}.prj".format(zName))
    theZip.write("{0}/{1}.shp".format(shploc, zName),  "{0}.shp".format(zName))
    theZip.write("{0}/{1}.shx".format(shploc, zName),  "{0}.shx".format(zName))
    theZip.close()
    print "Zipped shapefile {0}".format(zName)
    
print '{0}'.format('finished')