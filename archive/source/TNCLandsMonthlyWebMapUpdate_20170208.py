#---------------------------------------------------------------------
# Name:             TNCLandsMonthlyWebMapUpdate.py
# Purpose:          Primary purpose is to create web and download versions of TNC Lands and Transferred TNC Lands data
# Author:           Jim Platt
# Created:          20131115
# Editor:
# Last revised:     20141125
# ArcGIS Version:   10.2.1
# Python Version:   2.7
# Requires:         convertData.py
#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
import os
import datetime
from convertData import *
#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
#GLOBALS
LOGFILE = None
DEBUG = False

DATESTRING =  datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")

SOURCEPATH = 'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Lands/Archive/Data/MonthlyUpdate'
SOURCEGDB = '{0}.gdb'.format(DATESTRING)
SOURCEGDBPATH = os.path.join(SOURCEPATH, SOURCEGDB)

EXTERNALGDBPATH =       'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Lands/Data/TNC_Lands/external'
EXTERNALSHAPEFILEPATH = os.path.join(EXTERNALGDBPATH, 'shps')
EXTERNALGDBFILEPATH =   os.path.join(EXTERNALGDBPATH, 'gdbs')
EXTERNALZIPFILEPATH =   os.path.join(EXTERNALGDBPATH, 'zips')

INTERNALGDBPATH =       'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Lands/Data/TNC_Lands/internal'
INTERNALSHAPEFILEPATH = os.path.join(INTERNALGDBPATH, 'shps')
INTERNALGDBFILEPATH =   os.path.join(INTERNALGDBPATH, 'gdbs')
INTERNALZIPFILEPATH =   os.path.join(INTERNALGDBPATH, 'zips')

STATELISTPATH =         'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Lands/Data/TNC_Lands/states.dbf'

TNCLANDSFEATURECLASS =            'TNC_Lands'
TRANSFERREDTNCLANDSFEATURECLASS = 'TNC_TransfersAndAssists'
TNCLANDSPOINTFEATURECLASS =       'TNC_Lands_pts'

WEBGDB =      'TNCLands_w_{0}.gdb'.format(DATESTRING)
DOWNLOADGDB = 'TNCLands_d_{0}.gdb'.format(DATESTRING)

SPATIALREFERENCE = 3857

EXTERNALWEBFIELDLIST = [('STATE', 'TEXT', '#', '#', '2', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_STATE'),
                        ('AREANAM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('GAPCAT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_GAPCAT'),
                        ('PROTHOLD', 'TEXT', '#', '#', '100', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('PROTMECH', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_PROTMECH'),
                        ('SENSDATA', 'TEXT', '#', '#', '10', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_SENSDATA'),
                        ('CLSTRANSDA', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('TR_ID_TEXT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('MA_ID_TEXT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('CLS_ACRES', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
##                        Don't use these fields
##                        ('ADD_DATE', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
##                        ('OWNER', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
##                        ('ID_UPDATE', 'LONG', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('WEBSYM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')]

EXTERNALDOWNLOADTNCLANDSFIELDLIST = [('STATE', 'TEXT', '#', '#', '2', 'State', 'NULLABLE', 'NON_REQUIRED', 'tnc_STATE'),
                                     ('AREANAM', 'TEXT', '#', '#', '254', 'Area Name', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('GAPCAT', 'TEXT', '#', '#', '50', 'GAP Category', 'NULLABLE', 'NON_REQUIRED', 'tnc_GAPCAT'),
                                     ('PROTHOLD', 'TEXT', '#', '#', '100', 'Protection Holder', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('PROTMECH', 'TEXT', '#', '#', '50', 'Protection Mechanism', 'NULLABLE', 'NON_REQUIRED', 'tnc_PROTMECH'),
                                     ('SENSDATA', 'TEXT', '#', '#', '10', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_SENSDATA'),
                                     ('TR_IFMS_ID', 'TEXT', '#', '#', '50', 'Tract IFMS ID', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('MA_IFMS_ID', 'TEXT', '#', '#', '50', 'Managed Area IFMS ID', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('CLS_ACRES', 'DOUBLE', '#', '#', '#', 'CLS Protected Acres', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('CLSTRANSDA', 'DATE', '#', '#', '#', 'CLS Transaction Date', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('GIS_ACRES', 'DOUBLE', '#', 2, '#', 'Calculated GIS Acres', 'NULLABLE', 'NON_REQUIRED', '#')]

EXTERNALDOWNLOADTRASNFERREDTNCLANDSFIELDLIST = [('STATE', 'TEXT', '#', '#', '2', 'State', 'NULLABLE', 'NON_REQUIRED', 'tnc_STATE'),
                                                ('AREANAM', 'TEXT', '#', '#', '254', 'Area Name', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('GAPCAT', 'TEXT', '#', '#', '50', 'GAP Category', 'NULLABLE', 'NON_REQUIRED', 'tnc_GAPCAT'),
                                                ('PROTHOLD', 'TEXT', '#', '#', '100', 'Protection Holder', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('PROTMECH', 'TEXT', '#', '#', '50', 'Protection Mechanism', 'NULLABLE', 'NON_REQUIRED', 'tnc_PROTMECH'),
                                                ('SENSDATA', 'TEXT', '#', '#', '10', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_SENSDATA'),
                                                ('TR_IFMS_ID', 'TEXT', '#', '#', '50', 'Tract IFMS ID', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('MA_IFMS_ID', 'TEXT', '#', '#', '50', 'Managed Area IFMS ID', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('CLS_ACRES', 'DOUBLE', '#', '#', '#', 'CLS Protected Acres', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('CLSTRANSDA', 'DATE', '#', '#', '#', 'CLS Transaction Date', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('GIS_ACRES', 'DOUBLE', '#', 2, '#', 'Calculated GIS Acres', 'NULLABLE', 'NON_REQUIRED', '#')]

#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------

INTERNALWEBFIELDLIST = [('STATE', 'TEXT', '#', '#', '2', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_STATE'),
                        ('SOURCE', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('AREANAM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('GAPCAT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_GAPCAT'),
                        ('PROTHOLD', 'TEXT', '#', '#', '100', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('PROTMECH', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_PROTMECH'),
                        ('SENSDATA', 'TEXT', '#', '#', '10', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_SENSDATA'),
                        ('COUNTRY', 'TEXT', '#', '#', '254', 'Country', 'NULLABLE', 'NON_REQUIRED', 'tnc_COUNTRY'),
                        ('MOD_DATE', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('GLOBALID', 'GUID', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('CLSTRANSDA', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('TRACT_NAME', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('MABR_NAME', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('MA_IFMS_ID', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('TR_IFMS_ID', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('CLS_ACRES', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('TAXID', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('HISTAXID', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('GLOT', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('SUBD', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('BLOCK', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                        ('WEBSYM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')]

INTERNALDOWNLOADTNCLANDSFIELDLIST = [('STATE', 'TEXT', '#', '#', '2', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_STATE'),
                                     ('SOURCE', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('AREANAM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('GAPCAT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_GAPCAT'),
                                     ('PROTHOLD', 'TEXT', '#', '#', '100', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('PROTMECH', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_PROTMECH'),
                                     ('SENSDATA', 'TEXT', '#', '#', '10', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_SENSDATA'),
                                     ('COUNTRY', 'TEXT', '#', '#', '254', 'Country', 'NULLABLE', 'NON_REQUIRED', 'tnc_COUNTRY'),
                                     ('MOD_DATE', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('GLOBALID', 'GUID', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('CLSTRANSDA', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('TRACT_NAME', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('MABR_NAME', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('MA_IFMS_ID', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('TR_IFMS_ID', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('CLS_ACRES', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('GIS_ACRES', 'DOUBLE', '#', 2, '#', 'Calculated GIS Acres', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('TAXID', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('HISTAXID', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('GLOT', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('SUBD', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                     ('BLOCK', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')]

INTERNALDOWNLOADTRANSFERREDTNCLANDSFIELDLIST = [('STATE', 'TEXT', '#', '#', '2', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_STATE'),
                                                ('SOURCE', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('AREANAM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('GAPCAT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_GAPCAT'),
                                                ('PROTHOLD', 'TEXT', '#', '#', '100', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('PROTMECH', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_PROTMECH'),
                                                ('SENSDATA', 'TEXT', '#', '#', '10', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_SENSDATA'),
                                                ('COUNTRY', 'TEXT', '#', '#', '254', 'Country', 'NULLABLE', 'NON_REQUIRED', 'tnc_COUNTRY'),
                                                ('MOD_DATE', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('GLOBALID', 'GUID', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('CLSTRANSDA', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('TRACT_NAME', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('MABR_NAME', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('MA_IFMS_ID', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('TR_IFMS_ID', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('CLS_ACRES', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('GIS_ACRES', 'DOUBLE', '#', 2, '#', 'Calculated GIS Acres', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('TAXID', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('HISTAXID', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('GLOT', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('SUBD', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                                                ('BLOCK', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')]

#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    TODO:  copy TNC_Lands and TNC_TransfersAndAssists, plus domain tables to new source file geodatabase
    """
    startTime = datetime.datetime.now()

    print 'Starting at {0}\n'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d %H:%M:%S'))

    print 'Creating external web file geodatabase...'

    '''Create TNC Lands web file geodatabase'''
    resultGDBCreate = do_CreateFileGDB(targetGDBName=os.path.join(EXTERNALGDBPATH, WEBGDB), sourceGDBName=SOURCEGDBPATH)
    #resultGDBCreate = [True]

    '''Create TNC Lands feature class'''
    if resultGDBCreate[0]:
        resultTNCLandsCreate = do_CreatePolygonFeatureClass(targetGDBName=os.path.join(EXTERNALGDBPATH, WEBGDB),
                                                            targetFC=TNCLANDSFEATURECLASS,
                                                            addFieldList=EXTERNALWEBFIELDLIST,
                                                            spatialReference = SPATIALREFERENCE)
        #resultTNCLandsCreate = [True]
    else:
        sys.exit(None)

    '''Insert TNC Lands records'''
    if resultTNCLandsCreate[0]:
        resultInsertTNCLandsRecords = do_InsertExternalWebTNCLandsRecords(targetGDBTNCLands=os.path.join(os.path.join(EXTERNALGDBPATH, WEBGDB), TNCLANDSFEATURECLASS),
                                                                          sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TNCLANDSFEATURECLASS))
        #resultInsertTNCLandsRecords = [True]
    else:
        sys.exit(None)

    '''Insert Transferred TNC Lands records'''
    if resultInsertTNCLandsRecords[0]:
        resultInsertTransferredTNCLandsRecords = do_InsertExternalWebTransferredTNCLandsRecords(targetGDBTNCLands=os.path.join(os.path.join(EXTERNALGDBPATH, WEBGDB), TNCLANDSFEATURECLASS),
                                                                                                sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TRANSFERREDTNCLANDSFEATURECLASS))
        #resultInsertTransferredTNCLandsRecords = [True]
    else:
        sys.exit(None)

    #Create TNC Lands point feature class
    if resultInsertTransferredTNCLandsRecords[0]:
        resultCreatePointFeatureClass = do_CreatePointFeatureClass(sourcePolygonFeatureClass=os.path.join(os.path.join(EXTERNALGDBPATH, WEBGDB), TNCLANDSFEATURECLASS),
                                                                   targetPointFeatureClass=os.path.join(os.path.join(EXTERNALGDBPATH, WEBGDB), TNCLANDSPOINTFEATURECLASS))
        #resultCreatePointFeatureClass = [True]
    else:
        sys.exit(None)

    #---------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------

    print 'Creating external download file geodatabase...'

    '''Create TNC Lands download file geodatabase'''
    resultGDBCreate = do_CreateFileGDB(targetGDBName=os.path.join(EXTERNALGDBPATH, DOWNLOADGDB), sourceGDBName=SOURCEGDBPATH)
    #resultGDBCreate = [True]

    '''Create TNC Lands feature class'''
    if resultGDBCreate[0]:
        resultTNCLandsCreate = do_CreatePolygonFeatureClass(targetGDBName=os.path.join(EXTERNALGDBPATH, DOWNLOADGDB),
                                                            targetFC=TNCLANDSFEATURECLASS,
                                                            addFieldList=EXTERNALDOWNLOADTNCLANDSFIELDLIST,
                                                            spatialReference = SPATIALREFERENCE)
        #resultTNCLandsCreate = [True]
    else:
        sys.exit(None)

    if resultTNCLandsCreate:
        resultInsertTNCRecords = do_InsertExternalDownloadTNCLandsRecords(os.path.join(os.path.join(EXTERNALGDBPATH, DOWNLOADGDB), TNCLANDSFEATURECLASS),
                                                                          sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TNCLANDSFEATURECLASS))
        #resultInsertTNCRecords = [True]
    else:
        sys.exit(None)

    if resultInsertTNCRecords[0]:
        resultTransferredTNCLandsCreate = do_CreatePolygonFeatureClass(targetGDBName=os.path.join(EXTERNALGDBPATH, DOWNLOADGDB),
                                                                       targetFC=TRANSFERREDTNCLANDSFEATURECLASS,
                                                                       addFieldList=EXTERNALDOWNLOADTRASNFERREDTNCLANDSFIELDLIST,
                                                                       spatialReference = SPATIALREFERENCE)
        #resultTransferredTNCLandsCreate = [True]
    else:
        sys.exit(None)

    if resultTransferredTNCLandsCreate[0]:
        resultInsertTransferredTNCLandsRecords = do_InsertExternalDownloadTransferredTNCLandsRecords(targetGDBTNCLands=os.path.join(os.path.join(EXTERNALGDBPATH, DOWNLOADGDB), TRANSFERREDTNCLANDSFEATURECLASS),
                                                                                                     sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TRANSFERREDTNCLANDSFEATURECLASS))
        #resultInsertTransferredTNCLandsRecords = [True]
    else:
        sys.exit(None)

    print 'Creating external download zip files'
    if resultInsertTransferredTNCLandsRecords[0]:
        resultZipData = do_zipData(os.path.join(os.path.join(EXTERNALGDBPATH, DOWNLOADGDB), TNCLANDSFEATURECLASS),
                                   os.path.join(os.path.join(EXTERNALGDBPATH, DOWNLOADGDB), TRANSFERREDTNCLANDSFEATURECLASS),
                                   EXTERNALSHAPEFILEPATH, EXTERNALGDBFILEPATH, EXTERNALZIPFILEPATH, STATELISTPATH)
        #resultZipData = [True]
    else:
        sys.exit(None)

    '''---------------------------------------------------------------------------------------------------------------------------------'''
    '''-------------------------------------------Create internal web file geodatabase--------------------------------------------------'''

    print 'Creating internal web file geodatabase...'

    '''Create TNC Lands web file geodatabase'''
    resultGDBCreate = do_CreateFileGDB(targetGDBName=os.path.join(INTERNALGDBPATH, WEBGDB), sourceGDBName=SOURCEGDBPATH)
    #resultGDBCreate = [True]

    '''Create TNC Lands feature class'''
    if resultGDBCreate[0]:
        resultTNCLandsCreate = do_CreatePolygonFeatureClass(targetGDBName=os.path.join(INTERNALGDBPATH, WEBGDB),
                                                            targetFC=TNCLANDSFEATURECLASS,
                                                            addFieldList=INTERNALWEBFIELDLIST,
                                                            spatialReference = SPATIALREFERENCE)
        #resultTNCLandsCreate = [True]
    else:
        sys.exit(None)

    '''Insert TNC Lands records'''
    if resultTNCLandsCreate[0]:
        resultInsertTNCLandsRecords = do_InsertInternalWebTNCLandsRecords(targetGDBTNCLands=os.path.join(os.path.join(INTERNALGDBPATH, WEBGDB), TNCLANDSFEATURECLASS),
                                                                          sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TNCLANDSFEATURECLASS))
        #resultInsertTNCLandsRecords = [True]
    else:
        sys.exit(None)

    '''Insert Transferred TNC Lands records'''
    if resultInsertTNCLandsRecords[0]:
        resultInsertTransferredTNCLandsRecords = do_InsertInternalWebTransferredTNCLandsRecords(targetGDBTNCLands=os.path.join(os.path.join(INTERNALGDBPATH, WEBGDB), TNCLANDSFEATURECLASS),
                                                                                                sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TRANSFERREDTNCLANDSFEATURECLASS))
        #resultInsertTransferredTNCLandsRecords = [True]
    else:
        sys.exit(None)

    '''Create TNC Lands point feature class'''
    if resultInsertTransferredTNCLandsRecords[0]:
        resultCreatePointFeatureClass = do_CreatePointFeatureClass(sourcePolygonFeatureClass=os.path.join(os.path.join(INTERNALGDBPATH, WEBGDB), TNCLANDSFEATURECLASS),
                                                                   targetPointFeatureClass=os.path.join(os.path.join(INTERNALGDBPATH, WEBGDB), TNCLANDSPOINTFEATURECLASS))
        #resultCreatePointFeatureClass = [True]
    else:
        sys.exit(None)

    #---------------------------------------------------------------------------------------------------------------------------------

    print 'Creating internal download file geodatabase...'

    '''Create TNC Lands download file geodatabase'''
    resultGDBCreate = do_CreateFileGDB(targetGDBName=os.path.join(INTERNALGDBPATH, DOWNLOADGDB), sourceGDBName=SOURCEGDBPATH)
    #resultGDBCreate = [True]

    '''Create TNC Lands feature class'''
    if resultGDBCreate[0]:
        resultTNCLandsCreate = do_CreatePolygonFeatureClass(targetGDBName=os.path.join(INTERNALGDBPATH, DOWNLOADGDB),
                                                            targetFC=TNCLANDSFEATURECLASS,
                                                            addFieldList=INTERNALDOWNLOADTNCLANDSFIELDLIST,
                                                            spatialReference = SPATIALREFERENCE)
        #resultTNCLandsCreate = [True]
    else:
        sys.exit(None)

    if resultTNCLandsCreate:
        resultInsertTNCRecords = do_InsertInternalDownloadTNCLandsRecords(os.path.join(os.path.join(INTERNALGDBPATH, DOWNLOADGDB), TNCLANDSFEATURECLASS),
                                                                          sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TNCLANDSFEATURECLASS))
        #resultInsertTNCRecords = [True]
    else:
        sys.exit(None)

    if resultInsertTNCRecords[0]:
        resultTransferredTNCLandsCreate = do_CreatePolygonFeatureClass(targetGDBName=os.path.join(INTERNALGDBPATH, DOWNLOADGDB),
                                                                       targetFC=TRANSFERREDTNCLANDSFEATURECLASS,
                                                                       addFieldList=INTERNALDOWNLOADTRANSFERREDTNCLANDSFIELDLIST,
                                                                       spatialReference = SPATIALREFERENCE)
        #resultTransferredTNCLandsCreate = [True]
    else:
        sys.exit(None)

    if resultTransferredTNCLandsCreate[0]:
        resultInsertTransferredTNCLandsRecords = do_InsertInternalDownloadTransferredTNCLandsRecords(targetGDBTNCLands=os.path.join(os.path.join(INTERNALGDBPATH, DOWNLOADGDB), TRANSFERREDTNCLANDSFEATURECLASS),
                                                                                                     sourceGDBTNCLands=os.path.join(SOURCEGDBPATH, TRANSFERREDTNCLANDSFEATURECLASS))
        #resultInsertTransferredTNCLandsRecords = [True]
    else:
        sys.exit(None)

    print 'Creating external download zip files'
    if resultInsertTransferredTNCLandsRecords[0]:
        resultZipData = do_zipData(os.path.join(os.path.join(INTERNALGDBPATH, DOWNLOADGDB), TNCLANDSFEATURECLASS),
                                   os.path.join(os.path.join(INTERNALGDBPATH, DOWNLOADGDB), TRANSFERREDTNCLANDSFEATURECLASS),
                                   INTERNALSHAPEFILEPATH, INTERNALGDBFILEPATH, INTERNALZIPFILEPATH, STATELISTPATH)
        #resultZipData = [True]
    else:
        sys.exit(None)

    endTime = datetime.datetime.now()

    print '\nFinished at {0}'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d %H:%M:%S'))

    print 'Time to complete {0}'.format(endTime - startTime)
