#---------------------------------------------------------------------
# Name:             RecAndPost.py
# Purpose:          Automate the reconcile and post process of TNC Lands
# Author:           Jim Platt
# Created:          20140129
# Editor:
# Last revised:
# ArcGIS Version:   10.1
# Python Version:   2.7
# Requires:
#---------------------------------------------------------------------
import os
import sys
import time
import datetime
import traceback

import arcpy
#from arcpy.sa import *

arcpy.env.overwriteOutput = True
#---------------------------------------------------------------------
def AddMsgAndPrint(msg, severity = 0):
    '''Adds a Message to the geoprocessor (in case this script is run as a tool) and
       prints the message to the screen (standard output)'''
    msg = str(msg)
    logFile.write(time.strftime('%d%m%Y_%H:%M:%S ') + msg + '\n')
    logFile.flush
    if debug:
##  debug I/O
        print 'Debug: ' + msg
    else:
##  tool I/0
##  Split the message on \n first, so that if it's multiple lines, a gp message will be
##  added for each line
        try:
            for string in msg.split('\n'):
##      Add appropriate geoprocessing message
                if severity == 0:
                    arcpy.AddMessage(string)
                elif severity == 1:
                    arcpy.AddWarning(string)
                elif severity == 2:
                    arcpy.AddError(string)
                if (severity == 2 or severity == 1):
                    trace = traceback.format_exception(sys.exc_info()) #sys.exc_type, exc_value, exc_traceback)
                    for value in trace:
                        print str(value)
                        arcpy.AddError(str(value))
        except:
            pass
#---------------------------------------------------------------------
def do_analysis(*argv):
    """TODO: Add documentation about this function here"""
    try:
        #TODO: Add analysis here
        pass
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
# End do_analysis function
#---------------------------------------------------------------------
#---------------------------------------------------------------------
# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE,
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
        for i in range(arcpy.GetArgumentCount()))
    do_analysis(*argv)
    logFile = None
    debug = False
    proceed = True
    PathToBackup = 'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNC_Lands/Archive/Data/RecAndPost'
    theDate=str(datetime.date.today())
    BackupGDB = '{0}.gdb'.format(theDate.replace("-",""))
    BackupPath = os.path.join(PathToBackup, BackupGDB)
    logfile = 'log.txt'
    #----------------------------------------------------------------------'
    ##Create backup file geodatabase
##    print "Creating backup file geodatabase {0}".format(BackupGDB)
##    try:
##        arcpy.CreateFileGDB_management(PathToBackup, BackupGDB, "Current")
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
    #----------------------------------------------------------------------
    #create archive file geodatabase
    print "Creating archive file geodatabase {0}".format(BackupGDB)
    try:
        arcpy.CreateFileGDB_management(PathToBackup, BackupGDB, "CURRENT")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]

    #copy TNC_Lands_Edit to backup gdb
    print "Copying edit version of {0} to {1} backup".format("TNC_Lands", "TNC_Lands_Edit")
    try:
        arcpy.FeatureClassToFeatureClass_conversion(r"Database Connections\SAEDITOR@TNC_Lands_Edit.mnspatial.tnc.org.sde\tncgdb.NACRLOADER.TNC_Lands", BackupPath, "TNC_Lands_edit")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
    #----------------------------------------------------------------------
    #copy TransfersAndAssists edit to backup gdb
    print "Copying edit version of {0} to {1} backup".format("Transferred_TNC_Lands", "Transferred_TNC_Lands_Edit")
    try:
        arcpy.FeatureClassToFeatureClass_conversion(r"Database Connections\SAEDITOR@Transferred_TNC_Lands_Edit.mnspatial.tnc.org.sde\tncgdb.NACRLOADER.TNC_TransfersAndAssists", BackupPath, "TransfersAndAssists_Edit")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #copy TNC_Lands_QA to backup gdb
    print "Copying QA version of {0} to {1} backup".format("TNC_Lands", "TNC_Lands_QA")
    try:
        arcpy.FeatureClassToFeatureClass_conversion(r"Database Connections\NACRLOADER@TNC_Lands_QA.mnspatial.tnc.org.sde\tncgdb.NACRLOADER.TNC_Lands", BackupPath, "TNC_Lands_QA")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
    #----------------------------------------------------------------------
    #copy Transferred_TNC_Lands_QA to backup gdb
    print "Copying QA version of {0} to {1} backup".format("Transferred_TNC_Lands", "Transferred_TNC_Lands_QA")
    try:
        arcpy.FeatureClassToFeatureClass_conversion(r"Database Connections\NACRLOADER@Transferred_TNC_Lands_QA.mnspatial.tnc.org.sde\tncgdb.NACRLOADER.TNC_TransfersAndAssists", BackupPath, "TransfersAndAssists_QA")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #copy TNC_Lands_Default to backup gdb
    print "Copying default version of {0} to {1} backup".format("TNC_Lands", "TNC_Lands_Default")
    try:
        arcpy.FeatureClassToFeatureClass_conversion(r"Database Connections\NACRLOADER@default.mnspatial.tnc.org.sde\tncgdb.NACRLOADER.TNC_Lands", BackupPath, "TNC_Lands_Default")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]
    #----------------------------------------------------------------------
    #copy Transferred_TNC_Lands_Default to backup gdb
    print "Copying default version of {0} to {1} backup".format("Transferred_TNC_Lands", "Transferred_TNC_Lands_Default")
    try:
        arcpy.FeatureClassToFeatureClass_conversion(r"Database Connections\NACRLOADER@default.mnspatial.tnc.org.sde\tncgdb.NACRLOADER.TNC_TransfersAndAssists", BackupPath, "TransfersAndAssists_Default")
        print arcpy.GetMessages()
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]

##    #----------------------------------------------------------------------
##    #Set TNC_Lands_QA to public
##    print "Setting {0} version to Public".format("TNC_Lands_QA")
##    try:
##        arcpy.AlterVersion_management("Database Connections/nacrloader @ TNC_Lands_QA.mnsde.tnc.sde", "TNC_Lands_QA", "#", "#", "PUBLIC")
##        print arcpy.GetMessages()
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##    ##Set Transferred_TNC_Lands_QA to public
##    print "Setting {0} version to Public".format("Transferred_TNC_Lands_QA")
##    try:
##        arcpy.AlterVersion_management("Database Connections/nacrloader @ Transferred_TNC_Lands_QA.mnsde.tnc.sde", "Transferred_TNC_Lands_QA", "#", "#", "PUBLIC")
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##    #--------------------------------------------------------------------------------------------
##    userlist = arcpy.ListUsers('Database Connections/sde @ default.mnsde.tnc.sde')
##    usernames = (u.Name for u in userlist)
##    for user in usernames:
##        print user
##        #if user not in ['VENTYX_VIEWER', 'VENTYX_STEWARD', 'HARTENERGY_VIEWER']:
##            #proceed = False
##    #if proceed:
##    reconcile_mode = "ALL_VERSIONS"
##    acquire_locks = "LOCK_ACQUIRED"
##    abort_if_conflicts = "ABORT_CONFLICTS"
##    conflict_definition = "BY_OBJECT"
##    conflict_resolution = "FAVOR_EDIT_VERSION"
##    with_post = "NO_POST"
##    with_delete = "KEEP_VERSION"
##    workspace = 'Database Connections/nacrloader @ TNC_Lands_QA.mnsde.tnc.sde'
##    arcpy.env.workspace = workspace
##        #reconcile and post TNC_Lands_Edit to TNC_Lands_QA
##    print 'Reconciling and posting changes from {0} to {1}'.format("TNC_Lands_Edit", "TNC_Lands_QA")
##    try:
##        arcpy.ReconcileVersions_management(workspace,
##                                           reconcile_mode,
##                                           "TNC_Lands_QA",
##                                           "TNC_Lands_Edit",
##                                           acquire_locks,
##                                           abort_if_conflicts,
##                                           conflict_definition,
##                                           conflict_resolution,
##                                           with_post,
##                                           with_delete,
##                                           logfile)
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##        os.sys.exit()
##    #reconcile and post TNC_Lands_QA to Default
##    workspace = 'Database Connections/sde @ default.mnsde.tnc.sde'
##    arcpy.env.workspace = workspace
##    print 'Reconciling and posting changes from {0} to {1}'.format("TNC_Lands_QA", "Default")
##    try:
##        arcpy.ReconcileVersions_management(workspace,
##                                           reconcile_mode,
##                                           "Default",
##                                           "TNC_Lands_QA",
##                                           acquire_locks,
##                                           abort_if_conflicts,
##                                           conflict_definition,
##                                           conflict_resolution,
##                                           with_post,
##                                           with_delete,
##                                           logfile)
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##        os.sys.exit()
##    #----------------------------------------------------------------------
##    #reconcile and post Transferred_TNC_Lands_Edit to Transferred_TNC_Lands_QA
##    workspace = 'Database Connections/nacrloader @ Transferred_TNC_Lands_QA.mnsde.tnc.sde'
##    arcpy.env.workspace = workspace
##    print 'Reconciling and posting changes from {0} to {1}'.format("Transferred_TNC_Lands_Edit", "Transferred_TNC_Lands_QA")
##    try:
##        arcpy.ReconcileVersions_management(workspace,
##                                           reconcile_mode,
##                                           "Transferred_TNC_Lands_QA",
##                                           "Transferred_TNC_Lands_Edit",
##                                           acquire_locks,
##                                           abort_if_conflicts,
##                                           conflict_definition,
##                                           conflict_resolution,
##                                           with_post,
##                                           with_delete,
##                                           logfile)
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##        os.sys.exit()
##    #reconcile and post Transferred_TNC_Lands_QA to Default
##    workspace = 'Database Connections/sde @ default.mnsde.tnc.sde'
##    arcpy.env.workspace = workspace
##    print 'Reconciling and posting changes from {0} to {1}'.format("Transferred_TNC_Lands_QA", "Default")
##    try:
##        arcpy.ReconcileVersions_management(workspace,
##                                           reconcile_mode,
##                                           "Default",
##                                           "Transferred_TNC_Lands_QA",
##                                           acquire_locks,
##                                           abort_if_conflicts,
##                                           conflict_definition,
##                                           conflict_resolution,
##                                           with_post,
##                                           with_delete,
##                                           logfile)
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##        os.sys.exit()
##    #else:
##        #print 'Arrrghh!  Somebody is connected!'
##    #----------------------------------------------------------------------
##    #Set TNC_Lands_QA to protected
##    print "Setting {0} version to Protected".format("TNC_Lands_QA")
##    try:
##        arcpy.AlterVersion_management("Database Connections/nacrloader @ TNC_Lands_QA.mnsde.tnc.sde", "TNC_Lands_QA", "#", "#", "PROTECTED")
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##    #Set Transferred_TNC_Lands_QA to public
##    print "Setting {0} version to Protected".format("Transferred_TNC_Lands_QA")
##    try:
##        arcpy.AlterVersion_management("Database Connections/nacrloader @ Transferred_TNC_Lands_QA.mnsde.tnc.sde", "Transferred_TNC_Lands_QA", "#", "#", "PROTECTED")
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##    #----------------------------------------------------------------------
##    TNCLandsEdit = r'Database Connections/saeditor @ TNC_Lands_Edit.mnsde.tnc.sde/tncgdb.NACRLOADER.TNC_Lands'
##    TNCLandsQA = r'Database Connections/nacrloader @ TNC_Lands_QA.mnsde.tnc.sde/tncgdb.NACRLOADER.TNC_Lands'
##    TNCLandsDefault = r'Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.TNC_Lands'
##    TransferredTNCLandsEdit = r'Database Connections/saeditor @ TNC_Lands_Edit.mnsde.tnc.sde/tncgdb.NACRLOADER.Transferred_TNC_Lands'
##    TransferredTNCLandsQA = r'Database Connections/nacrloader @ TNC_Lands_QA.mnsde.tnc.sde/tncgdb.NACRLOADER.Transferred_TNC_Lands'
##    TransferredTNCLandsDefault = r'Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.Transferred_TNC_Lands'
##    SortField = 'GLOBALID'
##    CompareType = 'ALL'
##    IgnoreOptions = '#'
##    xyTolerance = '#'
##    mTolerance = '#'
##    zTolerance = '#'
##    attributeTolerances = '#'
##    omitField = 'OBJECTID'
##    ContinueCompare = "CONTINUE_COMPARE"
##    #Check TNC_Lands edit with the TNC_Lands_QA
##    print "Checking current TNC Lands edit version with the current TNC Lands QA version"
##    try:
##        compareResult = arcpy.FeatureCompare_management(TNCLandsEdit, TNCLandsQA, SortField, CompareType, IgnoreOptions, xyTolerance, mTolerance,
##                                                        zTolerance, attributeTolerances, omitField, ContinueCompare, 'TNCLANDS_EditToQA.txt')
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##    #Check TNC_Lands_QA edit with the Default
##    print "Checking current TNC Lands QA version with the current TNC Lands Default version"
##    try:
##        compareResult = arcpy.FeatureCompare_management(TNCLandsQA, TNCLandsDefault, SortField, CompareType, IgnoreOptions, xyTolerance, mTolerance,
##                                                        zTolerance, attributeTolerances, omitField, ContinueCompare, 'TNCLANDS_QAToDefault.txt')
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##    #Check Transferred_TNC_Lands_Edit with the Transferred_TNC_Lands_QA
##    print "Checking current Transferred TNC Lands edit version with the current Transferred TNC Lands QA version"
##    try:
##        compareResult = arcpy.FeatureCompare_management(TransferredTNCLandsEdit, TransferredTNCLandsQA, SortField, CompareType, IgnoreOptions, xyTolerance, mTolerance,
##                                                        zTolerance, attributeTolerances, omitField, ContinueCompare, 'TransferredTNCLANDS_EditToQA.txt')
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
##    #Check Transferred_TNC_Lands_QA with the Default
##    print "Checking current Transferred TNC Lands QA version with the current Transferred TNC Lands Default version"
##    try:
##        compareResult = arcpy.FeatureCompare_management(TransferredTNCLandsEdit, TransferredTNCLandsQA, SortField, CompareType, IgnoreOptions, xyTolerance, mTolerance,
##                                                        zTolerance, attributeTolerances, omitField, ContinueCompare, 'TransferredTNCLANDS_QAToDefault.txt')
##    except arcpy.ExecuteError:
##        print arcpy.GetMessages(2)
##    except Exception as e:
##        print e.args[0]
print 'Finished'