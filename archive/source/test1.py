#---------------------------------------------------------------------
# Name:             template.py
# Purpose:          
# Author:           
# Created:          YYYYMMDD
# Editor:           
# Last revised:     
# ArcGIS Version:   10
# Python Version:   2.6
# Requires:         
#---------------------------------------------------------------------
import os
import sys
import time
import datetime
import traceback

import arcpy
arcpy.env.overwriteOutput = True
#from arcpy.sa import *
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

#---------------------------------------------------------------------
def buildFieldInfo(inTable):
    """ """
    fields = arcpy.ListFields(inTable)
    fieldInfo = arcpy.FieldInfo()

    try:
        for field in fields:
            if field.name == 'STATE':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'SOURCE':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'AREANAM':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'DESGNTN':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'OWNER':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'GAPCAT':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'PROTMECH':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'COUNTRY':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'MOD_DATE':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'CLSTRANSDA':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'SENSDATA':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'MABR_NAME':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'MA_IFMS_ID':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'TRACT_NAME':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'TR_IFMS_ID':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            elif field.name == 'CLS_ACRES':
                fieldInfo.addField(field.name, field.name, 'VISIBLE', '')
            else:
                fieldInfo.addField(field.name, field.name, 'HIDDEN', '')
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        sys.exit()
    except Exception as e:
        print e.args[0]
        sys.exit() 

    return fieldInfo

#---------------------------------------------------------------------
#---------------------------------------------------------------------
# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE, 
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    # Arguments are optional
    #argv = tuple(arcpy.GetParameterAsText(i)
        #for i in range(arcpy.GetArgumentCount()))
    #do_analysis(*argv)
    '''
    make feature class view
    execute dissolve on all but TRACT_NAME, TR_IFMSID, MOD_DATE
    execute frequency on MA_IFMSID
    find dups and write out
    
    execute dissolve on all but MOD_DATE
    execute frequency on TR_IFMSID
    find dups and write out    
       
    '''    
    logFile = None
    debug = False
    
    inWS = r'Database Connections\saeditor@CD_TNC_LANDS_EDIT.mnsde.tnc.sde'
    outWS = r'D:\GIS_Data\jplatt\Workspace\Data\NACR\TNC Lands\Data\scratch.gdb'
    arcpy.env.workspace = inWS
    table = 'CRLOADER.CD_TNC_LANDS'
    
    sensData = '\'No\''
    protMech = ['\'Fee-simple ownership\'', 
                '\'Full conservation easement\'',
                '\'Deed Restriction\'',
                '\'Agreement\'',
                '\'Lease\'',
                '\'Permit\'',
                '\'Access Right of Way\'',
                '\'Right of Way Tract\'']
    
    endDate = '\'2013-01-31\''
    
    expressions = [
        #['NCED',
         #'("SENSDATA" = {0}) AND ("PROTMECH" = {1}) AND ("CLSTRANSDA" < date {2})'.format(sensData, protMech[1], endDate), 
         #['MA_IFMS_ID', 'STATE', 'AREANAM', 'OWNER', 'CLSTRANSDA', 'GAPCAT']
         #],
        ['PADUS_USGS',
         '("SENSDATA" = {0}) AND ("PROTMECH" <> {0}) AND ("CLSTRANSDA" < date {2})'.format(sensData, protMech[1], endDate),
         ['TR_IFMS_ID', 'STATE', 'AREANAM', 'OWNER', 'CLSTRANSDA', 'GAPCAT']
         ]
    ]
    
    theFieldInfo = buildFieldInfo(table)
    
    for expression in expressions:
        theFCLayer = expression[0]
        arcpy.MakeFeatureLayer_management(table, theFCLayer, expression[1], '', theFieldInfo)
        print 'Number of records in the {0} feature layer: {1}'.format(theFCLayer, int(arcpy.GetCount_management(theFCLayer).getOutput(0)) )
        
        try:
            outFC = os.path.join(outWS, theFCLayer)

            statvTab = arcpy.ValueTable(2)
            statvTab.addRow('CLS_ACRES SUM')
            
            arcpy.Dissolve_management(theFCLayer, outFC, expression[2], statvTab, 'MULTI_PART')
            print arcpy.GetMessages()
            
            print 'Number of records in dissolved {0} feature class: {1}'.format(theFCLayer, arcpy.GetCount_management(outFC))

            try:
                inFC = outFC
                outFreqTable = '{0}_Frequency'.format(inFC)
                arcpy.Frequency_analysis(inFC, outFreqTable, "MA_IFMS_ID", "#")
                print arcpy.GetMessages()
                
                try:
                    freqRows = arcpy.SearchCursor(outFreqTable, '"FREQUENCY" > 1', '', 'FREQUENCY; MA_IFMS_ID' )
                    for freqRow in freqRows:
                        theExpression = '"MA_IFMS_ID" = {0}'.format(freqRow.MA_IFMS_ID)
                        multiRows = arcpy.SearchCursor(outFC, theExpression)
                        print '\n'
                        for multiRow in multiRows:
                            print '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format(long(multiRow.MA_IFMS_ID), multiRow.STATE, multiRow.AREANAM, multiRow.OWNER, multiRow.CLSTRANSDA, multiRow.GAPCAT, multiRow.SUM_CLS_ACRES)
                        
                except arcpy.ExecuteError:
                    print arcpy.GetMessages(2)
                    sys.exit()
                except Exception as e:
                    print e.args[0]
                    sys.exit()                 
            
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
                sys.exit()
            except Exception as e:
                print e.args[0]
                sys.exit()        
            
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            sys.exit()
        except Exception as e:
            print e.args[0]
            sys.exit()
        
    print 'Finished'