#---------------------------------------------------------------------
# Name:             name.py
# Purpose:          
# Author:           Jim Platt
# Created:          the date
# Editor:           
# Last revised:     
# ArcGIS Version:   10
# Python Version:   2.6
# Requires:         ArcGIS 10.x, python 2.6
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
logFile = open('c:/temp/logfile.txt', 'w')

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

def feeManagedAreasToTracts():
    '''
    One Preserve Managed Area to One Tract
    '''
    pass
    
    '''
    One Preserve Managed Area to Multiple Tracts (For preserves mad up of two or more 
    tracts with the separate tract boundaries).
    '''
    pass

def feeTractsToManagedAreas():
    '''
    TODO: explain this one
    '''
    pass

def ceManagedAreasToTracts():
    '''
    One Conservation Easement Managed Area to One Tract
    '''
    pass

    '''
    One Conservation Easement Managed Area to Multiple Tracts (For Conservation 
    Easements made up of two or more tracts without the separate tract boundaries)
    '''
    pass

def ceTractsToManagedAreas():
    '''
    One Conservation Easement Tract to One Managed Area
    '''
    pass

    '''
    One Conservation Easement Tract to Multiple Managed Areas
    '''
    pass

def rstManagedAreasToTracts():
    '''
    One Deed Restriction Managed Area to One Tract
    '''
    pass
    '''
    One Deed Restriction Managed Area to Multiple Tracts
    '''
    pass

def rstTractsToManagedAreas():
    '''
    Deed Restriction Tracts
    '''
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

#---------------------------------------------------------------------
#---------------------------------------------------------------------        
# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE, 
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    #Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i) 
        for i in range(arcpy.GetArgumentCount()))
    do_analysis(*argv)




