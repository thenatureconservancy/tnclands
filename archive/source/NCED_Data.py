
import sys
import time
import datetime
import traceback

import arcpy
#from arcpy.sa import *
arcpy.env.overwriteOutput = True

class shareConverter(object):
    def __init__(self):
        """PADUS and NCED Superclass"""
        pass

class NCEDConverter(shareConverter):
    #31
    unique_id = None
    #security = 'No Restrictions'
    security = 'NR'
    sitename = None
    esmthldr = 'The Nature Conservancy'
    #eholdtyp = 'Non-Governental Organization'
    eholdtyp = 'NGO'
    #owntype = 'Private'
    owntype = 'PVT'
    s_emthd1 = None
    s_emthd2 = None
    s_emthd3 = None
    #purpose = 'Environmental System'
    purpose = 'ENV'
    gapsts = None
    #pubaccess = 'Closed'
    pubaccess = 'XA'
    #duration = 'Unknown'
    duration = 'PERM'
    term = None
    mon_est = None
    day_est = None
    year_est = None
    state = None
    #dataagg = 'The Nature Conservancy'
    dataagg = None
    dataentry = datetime.datetime.now()
    #datapvdr = None
    datapvdr = 'The Nature Conservancy'
    datasrc = 'The Nature Conservancy'
    source_uid = None
    #boundcf = 'Unknown'
    rep_acres = None
    gis_acres = None
    pct_diff = None
    conflict = None
    stacked = None
    iucncat = None
    wpda_cd = None
    comments = None
    def __init__(self, AREANAM, CLS_ACRES, CLSTRANSDA, GAPCAT, STATE):
        self.sitename = AREANAM
        try:
            self.Reported_Acres = int(CLS_ACRES)
        except:
            self.Reported_Acres = 0 
        self.DOE = CLSTRANSDA
        self.GAPCat = GAPCAT
        self.State = STATE
    def EstablishmentDate(self, dateComponent):
        '''Extract day portion of CLSTRANSDA'''
        if dateComponent == 'day':
            return self.DOE.day
        elif dateComponent == 'month':
            return self.DOE.month
        elif dateComponent == 'year':
            return self.DOE.year
    def GAPStatus(self):
        if self.GAPCat == '1':
            return "'Managed for biodiversity - disturbance events proceed or are mimicked'"
        elif self.GAPCat == '2':
            return "'Managed for biodiversity - disturbance events suppressed'"
        elif self.GAPCat == '3':
            return "'Managed for multiple uses - subject to extractive (e.g. mining or logging) or OHV use'"
        elif self.GAPCat == '4':
            return "'No known mandate for protection'"
    def Owner(self):
        try:
            return self.owntype.title()
        except Exception as e:
            print e.args[0]
            return None
    def AreaName(self):
        try:
            if len(self.sitename) > 100:
                return "{0}*".format(self.sitename[:99].title())
            else:
                return "{0}".format(self.sitename[:len(self.sitename)].title())
        except Exception as e:
            print e.args[0]  
            return None
    def ReportedAcres(self):
        return self.Reported_Acres
    def StateName(self):
        return self.State

def do_NCED(theSourceTable, theTargetTable):
    theExpression = '("PROTMECH" = \'Conservation Easement\') AND ("CLSTRANSDA" IS NOT NULL) AND ("SENSDATA" = \'No\')' 
    sRows = arcpy.SearchCursor(theSourceTable, theExpression)
    try:
        arcpy.TruncateTable_management(theTargetTable)
        print arcpy.GetMessages()
        try:
            iRows = arcpy.InsertCursor(theTargetTable)
            count = 0 
            for sRow in sRows:
                test = NCEDConverter(sRow.AREANAM, sRow.CLS_ACRES, sRow.CLSTRANSDA, sRow.GAPCAT, sRow.state)
                iRow = iRows.newRow()
                iRow.unique_id = ''                                
                iRow.security = test.security                       
                iRow.sitename= test.AreaName()                        
                iRow.esmthldr = test.esmthldr                       
                iRow.eholdtype = test.eholdtyp                         
                iRow.owntype = test.Owner()                       
                iRow.s_emthd1 = test.s_emthd1                       
                iRow.s_emthd2 = test.s_emthd2                       
                iRow.purpose = test.purpose                        
                iRow.pubaccess = test.pubaccess                        
                iRow.duration = test.duration                      
                iRow.term = test.term                              
                iRow.mon_est = test.EstablishmentDate('month')     
                iRow.day_est = test.EstablishmentDate('day')       
                iRow.year_est = test.EstablishmentDate('year')     
                iRow.state = test.StateName()                      
                iRow.rep_acres_tnc = test.ReportedAcres()
                #iRow.gis_acres = ''                                                                          
                #iRow.pct_diff = ''                                      
                iRow.gapcat = test.GAPStatus()                      
                iRow.iucncat = test.iucncat                                          
                iRow.dataagg = test.dataagg                        
                iRow.dataentry = test.dataentry                     
                iRow.datapvdr = test.datapvdr                      
                iRow.datasrc = test.datasrc                        
                #iRow.source_uid = sRow.GlobalID                   
                
                #use the Managed Area ID for the source_uid                            
                if sRow.MA_IFMS_ID is not None:
                    iRow.source_uid = str(int(sRow.MA_IFMS_ID))
                else:
                    iRow.source_uid = ''
                
                iRow.conflict = test.conflict                                          
                iRow.stacked = test.stacked                                          
                iRow.comments = test.comments                                          
                
                iRow.Shape = sRow.Shape
                iRows.insertRow(iRow)
                del iRow
                count += 1
                if count % 50 == 0:
                    print "{0} records converted".format(count)
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return False
        except Exception as e:
            print e.args[0]
            return False
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return False
    except Exception as e:
        print e.args[0]
        return False  
    return True

class PADUS_USGSConverter(shareConverter):
    #34
    #OBJECTID
    #SHAPE
    Category = None
    Own_Type = '06'
    Own_Name = '0630' 
    Loc_Own = 'The Nature Conservancy'
    Mang_Name = None
    P_Des_Tp = '700'
    P_Des_Ds = 'Private Conservation Land'
    P_Des_Nm = None
    P_Loc_Nm = None
    Status = 'Designated'
    State_Nm = None
    Agg_Src = 'TheNatureConservancy_TNC_Lands2013.mnsde.tnc/TNC_Lands'
    GIS_Src = 'TNC_Lands'
    Src_Date = str(datetime.date.today())
    GIS_Acres = None
    Source_UID = None
    Source_PAID = None
    WDPA_Cd = None
    #S_Des_Tp = None
    #S_Lc_Ds = None
    #S_Loc_Nm = None
    Access = 'UK'
    Access_Src = None
    GAP_Sts = None
    GAPCdSrc = 'GAP Default'
    GAPCdDt = None
    IUCN_Cat = None
    Date_Est = None
    Comments = None
    EsmtHldr = None
    EHoldTyp = None
    #SHAPE_Length
    #SHAPE_Area
    def __init__(self, PROTMECH, AREANAM, STATE, TR_IFMS_ID, MA_IFMS_ID, GAPCAT, CLSTRANSDA, IUCNCAT):
        self.ProtMech = PROTMECH
        self.AreaName = AREANAM
        self.State = STATE
        self.TractID = TR_IFMS_ID
        self.ManagedAreaID = MA_IFMS_ID
        self.GAPCat = GAPCAT
        self.CLSTransDate = CLSTRANSDA.strftime('%Y')
        self.IUCNCat = IUCNCAT
    def Category(self):
        if self.ProtMech <> 'Fee':
            return 'Other'
        else:
            return self.ProtMech
    def Loc_Own(self):
        if self.ProtMech <> 'Fee':
            return 'Unknown'
        else:
            return 'TNC'
    def P_Des_Nm(self):
        if self.AreaName is not None:
            try:
                if len(self.AreaName) > 200:
                    return "{0}*".format(self.AreaName[:199].title())
                else:
                    return "{0}".format(self.AreaName[:len(self.AreaName)].title())
            except Exception as e:
                print e.args[0]  
                return None
        else:
            return 'Conservation Preserve'
    def State_Nm(self):
        StateDomain = {}
        StateDomain['AL'] = '01'
        StateDomain['AK'] = '02'
        StateDomain['AZ'] = '04'
        StateDomain['AR'] = '05'
        StateDomain['CA'] = '06'
        StateDomain['CO'] = '08'
        StateDomain['CT'] = '09'
        StateDomain['DE'] = '10'
        StateDomain['DC'] = '11'
        StateDomain['FL'] = '12'
        StateDomain['GA'] = '13'
        StateDomain['HI'] = '16'
        StateDomain['ID'] = '16'
        StateDomain['IL'] = '17'
        StateDomain['IN'] = '18'
        StateDomain['IA'] = '19'
        StateDomain['KS'] = '20'
        StateDomain['KY'] = '21'
        StateDomain['LA'] = '22'
        StateDomain['ME'] = '23'
        StateDomain['MD'] = '24'
        StateDomain['MA'] = '25'
        StateDomain['MI'] = '26'
        StateDomain['MN'] = '27'
        StateDomain['MS'] = '28'
        StateDomain['MO'] = '29'
        StateDomain['MT'] = '30'
        StateDomain['NE'] = '31'
        StateDomain['NV'] = '32'
        StateDomain['NH'] = '33'
        StateDomain['NJ'] = '34'
        StateDomain['NM'] = '35'
        StateDomain['NY'] = '36'
        StateDomain['NC'] = '37'
        StateDomain['ND'] = '38'
        StateDomain['OH'] = '39'
        StateDomain['OK'] = '40'
        StateDomain['OR'] = '41'
        StateDomain['PA'] = '42'
        StateDomain['RI'] = '44'
        StateDomain['SC'] = '45'
        StateDomain['SD'] = '46'
        StateDomain['TN'] = '47'
        StateDomain['TX'] = '48'
        StateDomain['UT'] = '49'
        StateDomain['VT'] = '50'
        StateDomain['VA'] = '51'
        StateDomain['WA'] = '53'
        StateDomain['WV'] = '54'
        StateDomain['WI'] = '55'
        StateDomain['WY'] = '56'
        return StateDomain[self.State]
    def Source_UID(self):
        return self.TractID
    def Source_PAID(self):
        return self.ManagedAreaID
    def GAPSts(self):
        if self.GAPCat == '1':
            return "1 - Managed for biodiversity - disturbance events proceed or are mimicked"
        elif self.GAPCat == '2':
            return "2 - Managed for biodiversity - disturbance events suppressed"
        elif self.GAPCat == '3':
            return "3 - Managed for multiple uses - subject to extractive (e.g. mining or logging) or OHV use"
        elif self.GAPCat == '4':
            return "4 - No known mandate for protection"
    def GapCdDt(self):
        return self.CLSTransDate
    def IUCN_Cat(self):
        if self.GAPCat == '1' or self.GAPCat == '2':
            return 'V'
        else:
            return 'VI'
    def Date_Est(self):
        return self.CLSTransDate

class PADUS_CBIConverter(shareConverter):
    def __init__(self):
        pass

def do_PADUS_USGS(theSourceTable, theTargetTable):
    theExpression = '("PROTMECH" <> \'Full conservation easement\') AND ("CLSTRANSDA" IS NOT NULL) AND ("SENSDATA" = \'No\')' 
    sRows = arcpy.SearchCursor(theSourceTable, theExpression)
    try:
        arcpy.TruncateTable_management(theTargetTable)
        print arcpy.GetMessages()
        try:
            iRows = arcpy.InsertCursor(theTargetTable)
            count = 0 
            for sRow in sRows:
                test = PADUS_USGSConverter(sRow.PROTMECH, sRow.AREANAM, sRow.STATE, sRow.TR_IFMS_ID, sRow.MA_IFMS_ID, sRow.GAPCAT, sRow.CLSTRANSDA, sRow.IUCNCAT)
                iRow = iRows.newRow()
                #iRow.UNIQUE_ID = ''
                iRow.Category = test.Category()
                iRow.Own_Type = test.Own_Type
                iRow.Own_Name = test.Own_Name
                iRow.Loc_Own = test.Loc_Own()
                iRow.Mang_Name = test.Mang_Name
                iRow.P_Des_Tp = test.P_Des_Tp
                iRow.P_Loc_Ds = test.P_Des_Ds
                iRow.P_Des_Nm = test.P_Des_Nm()
                iRow.P_Loc_Nm = test.P_Des_Nm()
                iRow.Status = test.Status
                iRow.State_Nm = test.State_Nm()
                iRow.Agg_Src = test.Agg_Src
                iRow.GIS_Src = test.GIS_Src
                iRow.Src_Date = test.Src_Date
                #iRow.GIS_Acres = 0
                iRow.Source_UID = test.Source_UID()
                iRow.Source_PAID = test.Source_PAID()
                iRow.WDPA_Cd = test.WDPA_Cd
                iRow.Access = test.Access
                iRow.Access_Src = test.Access_Src
                iRow.GAP_Sts = test.GAPSts()
                iRow.GAPCdSrc = test.GAPCdSrc
                iRow.IUCN_Cat = test.IUCN_Cat()
                iRow.Date_Est = test.Date_Est()
                iRow.Comments = test.Comments
                iRow.EsmtHldr = test.EsmtHldr
                iRow.EHoldTyp = test.EHoldTyp
                iRow.Shape = sRow.Shape
                iRows.insertRow(iRow)
                del iRow
                count += 1
                if count % 50 == 0:
                    print "%i records converted" %count
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            return False
        except Exception as e:
            print e.args[0]
            return False
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        return False
    except Exception as e:
        print e.args[0]
        return False  
    return True

def AddMsgAndPrint(msg, severity = 0):
    '''Adds a Message to the geoprocessor (in case this script is run as a tool) and
       prints the message to the screen (standard output)'''
    msg = str(msg)
    logFile.write(time.strftime('%d%m%Y_%H:%M:%S ') + msg + '\n')
    logFile.flush
    if debug:
#  debug I/O
        print 'Debug: ' + msg
    else:
#  tool I/0
#  Split the message on \n first, so that if it's multiple lines, a gp message will be
#  added for each line
        try:
            for string in msg.split('\n'):
#      Add appropriate geoprocessing message
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
