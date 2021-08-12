#---------------------------------------------------------------------
# Name:             name.py
# Purpose:          
# Author:           Jim Platt
# Created:          the date
# Editor:           
# Last revised:     
# ArcGIS Version:   10
# Python Version:   2.6
# Requires:         ArcGIS 10.x, python 2.7
# Notes:            
#---------------------------------------------------------------------
import os
import sys
import time
import traceback

import arcpy
#from arcpy.sa import *    
#arcpy.CheckOutExtension("Spatial")

arcpy.env.overwriteOutput = True
#arcpy.env.outputCoordinateSystem = 'Coordinate Systems/Projected Coordinate Systems/Continental/North America/USA Contiguous Albers Equal Area Conic USGS.prj'
#arcpy.env.geographicTransformations = 'NAD_1983_To_WGS_1984_5'

debug = True
logFile = open('D:/Workspace/temp/logfile.txt', 'w')

#---------------------------------------------------------------------
def AddMsgAndPrint(logfile, msg, severity = 0):
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
                    trace = traceback.print_exception(sys.exc_info())
                    for value in trace:
                        print str(value)
                        arcpy.AddError(str(value))
        except:
            pass

def do_analysis(*argv):
    """TODO: Add documentation about this function here"""
    try:
        #TODO: Add analysis here
        pass
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]

def updateTNCLandsValues(fc, table, theDefValueDict, theDefValueExp, theCLSFieldList):
    #One Preserve Managed Area to One Tract
    theKeys = theDefValueDict.keys()
    try:
        theRows = arcpy.UpdateCursor(fc, theDefValueExp)
        try:
            for theRow in theRows:        
                for theKey in theKeys:
                    theString = 'if theRow.' + theKey + ' is None: theRow.' + theKey + ' = "' + theDefValueDict[theKey] + '"'
                    print theString
                    exec(compile(theString, '', 'exec'))
                theCLSValueExp = '"MA_IFMS_ID" = %i' % long(theRow.MA_IFMS_ID)
                print theCLSValueExp 
                searchRows = arcpy.SearchCursor(table, theCLSValueExp)
                for searchRow in searchRows:
                    for theCLSField in theCLSFieldList:
                        if theCLSField == 'AREANAM':
                            theString = 'if theRow.' + theCLSField + ' is None: theRow.' + theCLSField + ' = searchRow. ' + theCLSField + '" Fee"'
                            print theString
                            exec(compile(theString, '', 'exec'))
                        else:
                            theString = 'if theRow.' + theCLSField + ' is None: theRow.' + theCLSField + ' = searchRow. ' + theCLSField
                            print theString
                            exec(compile(theString, '', 'exec'))                            
                
                theRows.updateRow(theRow)
                
                del theRow
                del searchRow
                del searchRows
                
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
        except Exception as e:
            print e.args[0]       
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]            

    return True
        
#---------------------------------------------------------------------
#---------------------------------------------------------------------        
# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE, 
# as a geoprocessing script tool, or as a module imported in
# another script

if __name__ == '__main__':
#    Arguments are optional
#    argv = tuple(arcpy.GetParameterAsText(i)
#        for i in range(arcpy.GetArgumentCount()))
#    do_analysis(*argv)
    
    theFC = 'D:/Workspace/Data/NACR/TNCLands/Data/TNCLands_Test.gdb/TNC_Lands'
    theTable = 'D:/Workspace/Data/NACR/TNCLands/Data/feema1to1_new.dbf'
    
    theDict = {}
    theDict['DESGNTN'] = 'Conservation Preserve'
    theDict['OWNER'] = 'Private'
    theDict['GAPCAT'] = '1'
    theDict['PROTHOLD'] = 'The Nature Conservancy'
    theDict['PROTMECH'] = 'Fee-simple ownership'
    theDict['COUNTRY'] = 'United States of America'
    
    theCLSFieldList = ['AREANAM', 'CLSTRANSDA', 'MABR_NAME', 'CLS_ACRES', 'TR_IFMS_ID']
    
    theQuery = '("MA_IFMS_ID" is not NULL) AND ("TR_IFMS_ID" is NULL)'
    
    theResult = updateTNCLandsValues(theFC, theTable, theDict, theQuery, theCLSFieldList)

    print 'Finished'