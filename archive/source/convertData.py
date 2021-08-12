import os
import sys
import time
import datetime
import traceback
import glob
import zipfile
import zlib
import arcpy
#from arcpy.sa import *
arcpy.env.overwriteOutput = True

abbrevList = ['(Tnc)', '(Pca)', '(Ce)', ' Ce ', ' Acub)']
##------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------

def do_CreateFileGDB(targetGDBName, sourceGDBName):
    """
    Create web or download version of file geodatabase
    """
    #Create web version of the file geodatabase
    print 'Creating file geodatabase {0}'.format(targetGDBName)
    if arcpy.Exists(targetGDBName):
        print 'Deleting previous file geodabase {0}'.format(targetGDBName)
        try:
            arcpy.Delete_management(targetGDBName)
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error deleting previous file geodatabase {0}'.format(targetGDBName)]
        except Exception as e:
            print e.args[0]
            return [False, 'System error deleting previous file geodatabase']

    print 'Creating new file geodabase {0}'.format(targetGDBName)
    try:
        arcpy.CreateFileGDB_management(os.path.dirname(targetGDBName), os.path.basename(targetGDBName), "CURRENT")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating file geodatabase {0}'.format(targetGDBName)]
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating file geodatabase {0}'.format(targetGDBName)]

    print 'Adding domains'
    domainTableList = [(os.path.join(sourceGDBName, 'Domain_tnc_COUNTRY'), 'tnc_COUNTRY', 'Standardized country name'),
                       (os.path.join(sourceGDBName, 'Domain_tnc_GAPCAT'), 'tnc_GAPCAT', 'GAP Category'),
                       (os.path.join(sourceGDBName, 'Domain_tnc_PROTMECH'), 'tnc_PROTMECH', 'The type of protection in place'),
                       (os.path.join(sourceGDBName, 'Domain_tnc_SENSDATA'), 'tnc_SENSDATA', 'Indicates if the record is Internal Use Only'),
                       (os.path.join(sourceGDBName, 'Domain_tnc_STATE'), 'tnc_STATE', 'State abbreviation and name')]
    for domainTable in domainTableList:
        try:
            arcpy.TableToDomain_management(domainTable[0], 'CODE', 'DESC', targetGDBName, domainTable[1], domainTable[2])
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            [False, 'ArcGIS error adding domain {0}'.format(domainTable[0])]
        except Exception as e:
            print e.args[0]
            [False, 'System error adding domain {0}'.format(domainTable[0])]

    return [True, 'Create file GDB completed successfully']

##------------------------------------------------------------------------------------------------
def do_CreatePolygonFeatureClass(targetGDBName, targetFC, addFieldList, spatialReference):
    """
    Create empty TNC Lands feature class and add fields to the table
    """
    print 'Creating new TNC Lands feature class '

    if arcpy.Exists(os.path.join(targetGDBName, targetFC)):
        print 'Deleting previous file feature class {0}'.format(os.path.join(targetGDBName, targetFC))
        try:
            arcpy.Delete_management(os.path.join(targetGDBName, targetFC))
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error deleting previous feature class {0}'.format(targetFC)]
        except Exception as e:
            print e.args[0]
            return [False, 'System error deleting previous feature class {0}'.format(targetFC)]

    try:
        arcpy.CreateFeatureclass_management(targetGDBName, targetFC, 'Polygon', '#', '#', '#', spatialReference, '#', '#', '#', '#')
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating feature class {0}'.format(targetFC)]
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating feature class {0}'.format(targetFC)]

    print 'Adding fields to {0}'.format(targetFC)
    for field in addFieldList:
        try:
            arcpy.AddField_management('{0}'.format(os.path.join(targetGDBName, targetFC)), field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7], field[8])
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error adding field {0}'.format(field[0])]
        except Exception as e:
            print e.args[0]
            return [False, 'System error adding field {0}'.format(field[0])]

    return [True, 'Create {0} feature class completed successfully'.format(targetFC)]

##---------------------------------------------------------------------------------------
def do_CreatePointFeatureClass(sourcePolygonFeatureClass, targetPointFeatureClass):
    '''
    Create point feature class from polygon TNC Lands feature class
    '''
    print "Creating point feature class from polygons"

    if arcpy.Exists(targetPointFeatureClass):
        print 'Deleting previous file point feature class {0}'.format(targetPointFeatureClass)
        try:
            arcpy.Delete_management(targetPointFeatureClass)
            print arcpy.GetMessages()
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error deleting previous feature class {0}'.format('TNC_Lands_pts')]
        except Exception as e:
            print e.args[0]
            return [False, 'System error deleting previous feature class {0}'.format('TNC_Lands_pts')]

    try:
        arcpy.FeatureToPoint_management(sourcePolygonFeatureClass, targetPointFeatureClass)
        print arcpy.GetMessages()
        return [True, 'Create point features finished successfully']
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating point feature class {0}'.format(targetPointFeatureClass)]
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating point feature class {0}'.format(targetPointFeatureClass)]

##------------------------------------------------------------------------------------------------
def do_InsertExternalWebTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    '''
    Insert External TNC Lands records into TNC Lands table
    '''
    print 'Inserting TNC Lands records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands, ' "SENSDATA" = \'No\' ' )
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:
        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.SENSDATA = sRow.SENSDATA
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID
        iRow.MA_IFMS_ID = sRow.MA_IFMS_ID
        iRow.CLS_ACRES = sRow.CLS_ACRES

        if sRow.PROTMECH == 'Management Lease or Agreement':
            iRow.WEBSYM = 'Agreement'
        elif sRow.PROTMECH == 'Grazing Lease':
            iRow.WEBSYM = 'Lease'
        elif sRow.PROTMECH == 'Grazing Permit':
            iRow.WEBSYM = 'Permit'
        elif sRow.PROTMECH == 'Life Estate':
            iRow.WEBSYM = 'Fee Ownership'

        else:
            iRow.WEBSYM = sRow.PROTMECH

        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]

    return [True, 'Insert TNC Lands records finished successfully']

##------------------------------------------------------------------------------------------------
def do_InsertExternalWebTransferredTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    '''
    Insert transferred TNC Lands records into TNC Lands table
    '''
    print 'Inserting Transferred TNC Lands records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands,  '("SENSDATA" = \'No\' OR "SENSDATA" IS NULL )')
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:
        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.SENSDATA = sRow.SENSDATA
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID
        iRow.WEBSYM = "Transferred"
        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]

    return [True, 'Insert Transferred TNC Lands records finished successfully']

##---------------------------------------------------------------------------------------
def do_InsertExternalDownloadTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    '''
    Insert External TNC Lands records into TNC Lands table
    '''
    print 'Inserting TNC Lands download records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands, ' "SENSDATA" = \'No\' ') # AND ("STATE" IS NOT NULL)')
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:

        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.SENSDATA = sRow.SENSDATA
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID
        iRow.MA_IFMS_ID = sRow.MA_IFMS_ID
        iRow.CLS_ACRES = sRow.CLS_ACRES
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]

    try:
        arcpy.MakeTableView_management(in_table = targetGDBTNCLands, out_view = "outView")
        try:
            arcpy.CalculateField_management("outView", "GIS_Acres", "!shape.area@acres!", 'PYTHON_9.3')
            try:
                arcpy.CalculateField_management("outView", "GIS_Acres", "round(!GIS_Acres!, 2)", 'PYTHON_9.3')
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except Exception as e:
                print e.args[0]
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
        except Exception as e:
            print e.args[0]
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]

    return [True, 'Insert TNC Lands records finished successfully']

##------------------------------------------------------------------------------------------------
def do_InsertExternalDownloadTransferredTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    '''
    '''
    print 'Inserting Transferred TNC Lands download records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands,  '("SENSDATA" = \'No\' OR "SENSDATA" IS NULL )' )
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:
        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.SENSDATA = sRow.SENSDATA
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID
        iRow.MA_IFMS_ID = sRow.MA_IFMS_ID
        iRow.CLS_ACRES = sRow.CLS_ACRES
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]

    try:
        arcpy.MakeTableView_management(in_table = targetGDBTNCLands, out_view = "outView")
        try:
            arcpy.CalculateField_management("outView", "GIS_Acres", "!shape.area@acres!", 'PYTHON_9.3')
            try:
                arcpy.CalculateField_management("outView", "GIS_Acres", "round(!GIS_Acres!, 2)", 'PYTHON_9.3')
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except Exception as e:
                print e.args[0]
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
        except Exception as e:
            print e.args[0]
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]


    return [True, 'Insert Transferred TNC Lands records finished successfully']

##------------------------------------------------------------------------------------------------
def do_InsertInternalWebTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    '''
    Insert External TNC Lands records into TNC Lands table
    '''
    print 'Inserting TNC Lands records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:
        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.SOURCE = sRow.SOURCE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.COUNTRY = sRow.COUNTRY
        iRow.MOD_DATE = sRow.MOD_DATE
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.SENSDATA = sRow.SENSDATA
        iRow.TRACT_NAME = sRow.TRACT_NAME
        iRow.MABR_NAME = sRow.MABR_NAME
        iRow.MA_IFMS_ID = sRow.MA_IFMS_ID
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID

        iRow.CLS_ACRES = sRow.CLS_ACRES
        iRow.TAXID = sRow.TAXID
        iRow.HISTAXID = sRow.HISTAXID
        iRow.GLOT = sRow.GLOT
        iRow.SUBD = sRow.SUBD
        iRow.BLOCK = sRow.BLOCK

        if sRow.PROTMECH == 'Management Lease or Agreement':
            iRow.WEBSYM = 'Agreement'
        elif sRow.PROTMECH == 'Grazing Lease':
            iRow.WEBSYM = 'Lease'
        elif sRow.PROTMECH == 'Grazing Permit':
            iRow.WEBSYM = 'Permit'
        elif sRow.PROTMECH == 'Life Estate':
            iRow.WEBSYM = 'Fee Ownership'

        else:
            iRow.WEBSYM = sRow.PROTMECH
        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]

    return [True, 'Insert TNC Lands records finished successfully']

##------------------------------------------------------------------------------------------------
def do_InsertInternalWebTransferredTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    '''
    Insert transferred TNC Lands records into TNC Lands table
    '''
    print 'Inserting Internal Transferred TNC Lands records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:
        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.SOURCE = sRow.SOURCE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.COUNTRY = sRow.COUNTRY
        iRow.MOD_DATE = sRow.MOD_DATE
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.SENSDATA = sRow.SENSDATA
        iRow.TRACT_NAME = sRow.TRACT_NAME
        iRow.MABR_NAME = sRow.MABR_NAME
        iRow.MA_IFMS_ID = sRow.MA_IFMS_ID
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID
        iRow.CLS_ACRES = sRow.CLS_ACRES
        iRow.TAXID = sRow.TAXID
        iRow.HISTAXID = sRow.HISTAXID
        iRow.GLOT = sRow.GLOT
        iRow.SUBD = sRow.SUBD
        iRow.BLOCK = sRow.BLOCK
        iRow.WEBSYM = "Transferred"
        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]

    return [True, 'Insert Transferred TNC Lands records finished successfully']

##------------------------------------------------------------------------------------------------
def do_InsertInternalDownloadTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    """Insert Internal TNC Lands records into TNC Lands tabel"""
    print 'Inserting TNC Lands download records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:
        iRow = iRows.newRow()

        iRow.STATE = sRow.STATE
        iRow.SOURCE = sRow.SOURCE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.COUNTRY = sRow.COUNTRY
        iRow.MOD_DATE = sRow.MOD_DATE
        iRow.GLOBALID = sRow.GLOBALID
        iRow.SENSDATA = sRow.SENSDATA
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.TRACT_NAME = sRow.TRACT_NAME
        iRow.MABR_NAME = sRow.MABR_NAME
        iRow.MA_IFMS_ID = sRow.MA_IFMS_ID
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID
        iRow.CLS_ACRES = sRow.CLS_ACRES
        iRow.TAXID = sRow.TAXID
        iRow.HISTAXID = sRow.HISTAXID
        iRow.GLOT = sRow.GLOT
        iRow.SUBD = sRow.SUBD
        iRow.BLOCK = sRow.BLOCK

        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}/MA_IFMS_ID: {1}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''), str(sRow.MA_IFMS_ID).replace('.0', ''))]

    try:
        arcpy.MakeTableView_management(in_table = targetGDBTNCLands, out_view = "outView")
        try:
            arcpy.CalculateField_management("outView", "GIS_Acres", "!shape.area@acres!", 'PYTHON_9.3')
            try:
                arcpy.CalculateField_management("outView", "GIS_Acres", "round(!GIS_Acres!, 2)", 'PYTHON_9.3')
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except Exception as e:
                print e.args[0]

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
        except Exception as e:
            print e.args[0]
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]


    return [True, 'Insert TNC Lands records finished successfully']
##------------------------------------------------------------------------------------------------
def do_InsertInternalDownloadTransferredTNCLandsRecords(targetGDBTNCLands, sourceGDBTNCLands):
    '''
    '''
    print 'Inserting Transferred TNC Lands download records'
    try:
        iRows = arcpy.InsertCursor(targetGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating insert cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating insert cursor']

    try:
        sRows = arcpy.SearchCursor(sourceGDBTNCLands)
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return [False, 'ArcGIS error creating search cursor']
    except Exception as e:
        print e.args[0]
        return [False, 'System error creating search cursor']

    counter = 0

    for sRow in sRows:
        iRow = iRows.newRow()

        iRow.STATE = sRow.STATE
        iRow.SOURCE = sRow.SOURCE
        iRow.AREANAM = unCapAREANAM(sRow.AREANAM)
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.COUNTRY = sRow.COUNTRY
        iRow.MOD_DATE = sRow.MOD_DATE
        iRow.GLOBALID = sRow.GLOBALID
        iRow.SENSDATA = sRow.SENSDATA
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.TRACT_NAME = sRow.TRACT_NAME
        iRow.MABR_NAME = sRow.MABR_NAME
        iRow.MA_IFMS_ID = sRow.MA_IFMS_ID
        iRow.TR_IFMS_ID = sRow.TR_IFMS_ID
        iRow.CLS_ACRES = sRow.CLS_ACRES
        iRow.TAXID = sRow.TAXID
        iRow.HISTAXID = sRow.HISTAXID
        iRow.GLOT = sRow.GLOT
        iRow.SUBD = sRow.SUBD
        iRow.BLOCK = sRow.BLOCK

        iRow.Shape = sRow.Shape

        try:
            iRows.insertRow(iRow)
            counter += 1
            if counter % 100 == 0:
                print 'Finished inserting {0} records'.format(counter)

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return [False, 'ArcGIS error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]
        except Exception as e:
            print e.args[0]
            return [False, 'System error inserting record TR_IFMS_ID: {0}'.format(str(sRow.TR_IFMS_ID).replace('.0', ''))]

    try:
        arcpy.MakeTableView_management(in_table = targetGDBTNCLands, out_view = "outView")
        try:
            arcpy.CalculateField_management("outView", "GIS_Acres", "!shape.area@acres!", 'PYTHON_9.3')
            try:
                arcpy.CalculateField_management("outView", "GIS_Acres", "round(!GIS_Acres!, 2)", 'PYTHON_9.3')
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except Exception as e:
                print e.args[0]

        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
        except Exception as e:
            print e.args[0]
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]

    return [True, 'Insert Transferred TNC Lands records finished successfully']

##------------------------------------------------------------------------------------------------
def do_zipData(inTNCLands, inTransferredTNCLands, shploc, gdbloc, ziploc, st):
    """
    TODO: Create US-wide file geodatabase zip and shapefile zip of downlaodable data
    """
    # set workspace
    arcpy.env.workspace = shploc
    #create reference to state name state FIPS table
    #st = 'Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.stateList'
    #set search cursor on state table
    stcur = arcpy.SearchCursor(st)
    #create feature layers for TNC Lands and Transferred TNC Lands
    arcpy.MakeFeatureLayer_management(inTNCLands, "TNCLandslyr")
    arcpy.MakeFeatureLayer_management(inTransferredTNCLands, 'TransferredTNCLandslyr')
    # loop through state table, select rows by state, create gdb and feature class, convert feature class to shapefile
    for row in stcur:
        print "Creating TNC_LANDS_{0} state file geodatabase shell".format(row.State)
        arcpy.CreateFileGDB_management(gdbloc, "TNC_Lands_{0}".format(row.State), "CURRENT")
        wc = "\"STATE\" = '{0}'".format(row.FIPS)
        print "Selecting {0}".format(wc)
        print "Adding TNC_Lands from {0} to gdb and creating state shapefile".format(row.State)
        arcpy.SelectLayerByAttribute_management("TNCLandslyr", "NEW_SELECTION", wc)
        if arcpy.GetCount_management('TNCLandsLyr').getOutput(0) > 0:
            arcpy.CopyFeatures_management('TNCLandslyr', '{0}/TNC_Lands_{1}.gdb/TNC_Lands_{1}'.format(gdbloc,row.State))
            print "Creating shapefile from geodatabase feature classes"
            arcpy.FeatureClassToShapefile_conversion("{0}/TNC_Lands_{1}.gdb/TNC_Lands_{1}".format(gdbloc, row.State), shploc)
        else:
            pass
        print 'Adding Transferred_TNC_Lands from {0} to gdb and creating state shapefile'.format(row.State)
        arcpy.SelectLayerByAttribute_management("TransferredTNCLandslyr", "NEW_SELECTION", wc)
        if arcpy.GetCount_management('TransferredTNCLandslyr').getOutput(0) > 0:
            arcpy.CopyFeatures_management('TransferredTNCLandslyr', "{0}/TNC_Lands_{1}.gdb/Transferred_TNC_Lands_{1}".format(gdbloc,row.State))
            arcpy.FeatureClassToShapefile_conversion("{0}/TNC_Lands_{1}.gdb/Transferred_TNC_Lands_{1}".format(gdbloc, row.State), shploc)
        else:
            pass
        #zip new file gdb
        infile = os.path.join(gdbloc, "TNC_Lands_{0}.gdb".format(row.State))
        outfile = os.path.join(ziploc, "TNC_Lands_{0}.gdb.zip".format(row.State))
        zipFileGeodatabase(infile, outfile)
        print "zipped file GDB {0}".format(row.State)
        theZipFile = zipfile.ZipFile("{0}/TNC_Lands_{1}.shp.zip".format(ziploc, row.State), 'w', zlib.DEFLATED)
        zName = 'TNC_Lands_{0}'.format(row.State)
        theZipFile.write("{0}/{1}.dbf".format(shploc, zName), "{0}.dbf".format(zName))
        theZipFile.write("{0}/{1}.prj".format(shploc, zName), "{0}.prj".format(zName))
        theZipFile.write("{0}/{1}.shp".format(shploc, zName), "{0}.shp".format(zName))
        theZipFile.write("{0}/{1}.shx".format(shploc, zName), "{0}.shx".format(zName))
        zName = 'Transferred_TNC_Lands_{0}'.format(row.State)
        theZipFile.write("{0}/{1}.dbf".format(shploc, zName), "{0}.dbf".format(zName))
        theZipFile.write("{0}/{1}.prj".format(shploc, zName), "{0}.prj".format(zName))
        theZipFile.write("{0}/{1}.shp".format(shploc, zName), "{0}.shp".format(zName))
        theZipFile.write("{0}/{1}.shx".format(shploc, zName), "{0}.shx".format(zName))
        theZipFile.close()

##------------------------------------------------------------------------------------------------
def zipFileGeodatabase(inFileGeodatabase, newZipFN):
    if not (os.path.exists(inFileGeodatabase)):
        return False
    if (os.path.exists(newZipFN)):
        os.remove(newZipFN)
    zipobj = zipfile.ZipFile(newZipFN, 'w')
    for infile in glob.glob(inFileGeodatabase + "/*"):
        zipobj.write(infile, os.path.basename(inFileGeodatabase) + "/" + os.path.basename(infile), zipfile.ZIP_DEFLATED)
    zipobj.close()
    return True

##------------------------------------------------------------------------------------------------
def unCapAREANAM(areaName):
    if areaName is not None:
        newName = areaName.title()
        for abbrev in abbrevList:
            try:
                if abbrev in newName:
                    newName = newName.replace(abbrev, abbrev.upper())
                    return newName
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except Exception as e:
                print e.args[0]
        return newName
    else:
        return areaName

if __name__ == '__main__':
    print unCapAREANAM('SMALL SWAMP (TNC)')
    print unCapAREANAM('MEDIUM SWAMP (PCA)')
    print unCapAREANAM('BIG SWAMP (CE)')
    print unCapAREANAM('REALLY BIG SWAMP')
    print unCapAREANAM('REALLY BIG SWAMP CE ')
    print unCapAREANAM('REALLY BIG SWAMP ACUB)')

