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

class shareConverter(object):
    def __init__(self):
        """PADUS and NCED Superclass"""
        pass

class NCEDConverter(shareConverter):
    #31
    unique_id = None
    security = 'No Restrictions'
    sitename = None
    esmthldr = 'The Nature Conservancy'
    eholdtyp = 'Non-Governental Organization'
    owntype = 'Private'
    s_emthd1 = None
    s_emthd2 = None
    purpose = 'Environmental System'
    gapsts = None
    pubaccess = 'Closed'
    duration = 'Unknown'
    term = None
    mon_est = None
    day_est = None
    year_est = None
    state = None
    dataagg = 'The Nature Conservancy'
    dataentry = datetime.datetime.now()
    datapvdr = None
    datasrc = 'The Nature Conservancy'
    source_uid = None
    #boundcf = 'Unknown'
    rep_acres = None
    gis_acres = None
    pct_diff = None
    conflict = 'No Known Conflict'
    stacked = 'No'
    iucncat = None
    wpda_cd = None
    comments = None
    def __init__(self, AREANAM, CLS_ACRES, CLSTRANSDA, GAPCAT, STATE):
        self.DOE = CLSTRANSDA
        self.GAPCat = GAPCAT
        self.sitename = AREANAM
        try:
            self.Reported_Acres = int(CLS_ACRES)
        except:
            self.Reported_Acres = 0 
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
                iRow.unique_id = ''                               #Auto-Populated
                iRow.security = test.security                      #print test.security                            
                iRow.sitename= test.AreaName()                     #print test.AreaName()                            
                iRow.esmthldr = test.esmthldr                      #print test.esmthldr                            
                iRow.eholdtyp = test.eholdtyp                      #print test.eholdtypE                             
                #iRow.owntype = test.Owner()                        #print test.Owner()                           
                iRow.s_emthd1 = test.s_emthd1                      #print test.s_emthd1                            
                iRow.s_emthd2 = test.s_emthd2                      #print test.s_emthd2                            
                iRow.purpose = test.purpose                        #print test.purpose                           
                iRow.gapsts = test.GAPStatus()                     #print test.GAPStatus()                          
                iRow.pubaccess = test.pubaccess                    #print test.pubaccess                             
                iRow.duration = test.duration                      #print test.duration                            
                iRow.term = test.term                              #print test.term                        
                iRow.mon_est = test.EstablishmentDate('month')     #print test.EstablishmentDate('month')  
                iRow.day_est = test.EstablishmentDate('day')       #print test.EstablishmentDate('day')    
                iRow.year_est = test.EstablishmentDate('year')     #print test.EstablishmentDate('year')   
                iRow.state = test.StateName()                      #print sRow.state                         
                iRow.dataagg = test.dataagg                        #print test.dataagg                           
                iRow.dataentry = test.dataentry                    #print test.dataentry                            
                iRow.datapvdr = test.datapvdr                      #print test.datapvdr                            
                iRow.datasrc = test.datasrc                        #print test.datasrc                           
                #iRow.source_uid = sRow.GlobalID                    #print sRow.GlobalID
                #use the Managed Area ID for the source_uid                            
                iRow.source_uid = str(int(sRow.MA_IFMS_ID))
                #iRow.boundcf = test.boundcf                        #print test.BOUNDCF                           
                iRow.rep_acres = test.ReportedAcres()              #print sRow.CLS_ACRES                             
                #iRow.gis_acres = ''                               #Auto-Populated                                                        
                #iRow.pct_diff = ''                                #Auto-Populated                   
                iRow.conflict = test.conflict                      #print test.conflict                            
                iRow.stacked = test.stacked                        #print test.stacked                           
                iRow.iucncat = test.iucncat                        #print test.iucncat                           
                iRow.wpda_cd = test.wpda_cd                        #print test.wpda_cd                           
                iRow.comments = test.comments                      #print test.comments                            
                #iRow.MA_IFMS_ID = test.MA_IFMS_ID
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

def do_PublicTNCLandsWeb(basepath, fileGDBName, TNCLands, TransferredTNCLands):
    """
    Create the public web-map and download file geodatabase and shapefile versions 
    of the TNC Lands and Transferred TNC Lands feature classes.
    
    The main difference between this version and the web and download versions of the 
    internal data is that TR_IFMS_ID and MA_IFMS_ID are cast as strings rather than 
    double (numeric) data types.
    
    TODO:  Convert polygons to point feature class
    TODO:  Add selection of non-sensitive transferred lands    
    
    """
    #Create web version of the file geodatabase
    print 'Creating TNC Lands web-version file geodatabase'    
    #dateString = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    #basepath = "D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/public"
    #fileGDBName = "TNCLands_w_{0}.gdb".format(dateString)
    fileGDBPath = os.path.join(basepath, fileGDBName)
    if arcpy.Exists(fileGDBPath):
        print 'Deleting previous file geodabase {0}'.format(fileGDBPath)
        arcpy.Delete_management(fileGDBPath)
    print 'Creating new file geodabase {0}'.format(fileGDBPath)
    arcpy.CreateFileGDB_management(basepath, fileGDBName, "CURRENT")
    print 'Adding domains'
    domainTableList = [('Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.Domain_tnc_COUNTRY', 'tnc_COUNTRY', 'Standardized country name'),
                       ('Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.Domain_tnc_GAPCAT', 'tnc_GAPCAT', 'GAP Category'),
                       ('Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.Domain_tnc_PROTMECH', 'tnc_PROTMECH', 'The type of protection in place'),
                       ('Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.Domain_tnc_SENSDATA', 'tnc_SENSDATA', 'Indicates if the record is Internal Use Only'), 
                       ('Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.Domain_tnc_STATE', 'tnc_STATE', 'State abbreviation and name')]
    for domainTable in domainTableList:
        arcpy.TableToDomain_management(domainTable[0], 'CODE', 'DESC_', os.path.join(basepath, fileGDBName), domainTable[1], domainTable[2])
    print 'Setting output spatial reference to WGS 1984 Web Mercator (Auxiliary Sphere)'
    sr = arcpy.SpatialReference(3857)  
    arcpy.env.outputCoordinateSystem = sr
    #------------------------------------------------------------------------------------------------
    print 'Creating new TNC Lands feature class '
    arcpy.CreateFeatureclass_management(os.path.join(basepath, fileGDBName), 'TNC_Lands', 'Polygon', '#', '#', '#', sr, '#', '#', '#', '#')
    addFieldList = [('STATE', 'TEXT', '#', '#', '2', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_STATE'),
                    ('AREANAM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('GAPCAT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_GAPCAT'),
                    ('PROTHOLD', 'TEXT', '#', '#', '100', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('PROTMECH', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_PROTMECH'),
                    ('CLSTRANSDA', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('SENSDATA', 'TEXT', '#', '#', '10', '', 'NULLABLE', 'NON_REQUIRED', 'tnc_SENSDATA'),
                    ('TR_ID_TEXT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('MA_ID_TEXT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('CLS_ACRES', 'DOUBLE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('ADD_DATE', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('OWNER', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('ID_UPDATE', 'LONG', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('WEBSYM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')]
    print 'Adding fields to TNC Lands'
    for field in addFieldList:
        arcpy.AddField_management("{0}/TNC_Lands".format(os.path.join(basepath, fileGDBName)), 
                                  field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7], field[8])
    print 'Inserting records'
    iRows = arcpy.InsertCursor("{0}/TNC_Lands".format(os.path.join(basepath, fileGDBName)))
    sRows = arcpy.SearchCursor(TNCLands, '("SENSDATA" = \'No\') AND ("STATE" IS NOT NULL)')
    for sRow in sRows:
        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.AREANAM = sRow.AREANAM
        iRow.GAPCAT = sRow.GAPCAT
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.PROTMECH = sRow.PROTMECH
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.SENSDATA = sRow.SENSDATA
        iRow.TR_ID_TEXT = str(sRow.TR_IFMS_ID).replace('.0', '')
        iRow.MA_ID_TEXT = str(sRow.MA_IFMS_ID).replace('.0', '')
        iRow.CLS_ACRES = sRow.CLS_ACRES
        if sRow.PROTMECH == 'Life Estate':
            iRow.WEBSYM = 'Fee Ownership'
        if sRow.PROTMECH == 'Grazing lease':
            iRow.WEBSYM = 'Lease'
        elif sRow.PROTMECH == 'Grazing permit':
            iRow.WEBSYM = 'Permit'
        elif sRow.PROTMECH == 'Full conservation easement':
            iRow.WEBSYM = 'Conservation Easement'
        elif sRow.PROTMECH == 'Management lease or agreement':
            iRow.WEBSYM = 'Agreement'
        else:
            iRow.WEBSYM = sRow.PROTMECH
        iRow.Shape = sRow.Shape
        iRows.insertRow(iRow)
    
    #------------------------------------------------------------------------------------------------
    """
    Copy US Transferred TNC_Lands feature class from MNSDE into US TNC Lands web map geodatabase 
    """
    print 'Copying Transferred TNC Lands to web map file geodatabase'
    arcpy.CreateFeatureclass_management(os.path.join(basepath, fileGDBName), 'Transferred_TNC_Lands', 'Polygon', '#', '#', '#', sr, '#', '#', '#', '#')
    addFieldList = [('STATE', 'TEXT', '#', '#', '2', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('SOURCE', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('AREANAM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('PROTMECH', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('COUNTRY', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('CLSTRANSDA', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('TR_ID_TEXT', 'TEXT', '#', '#', '50', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('TRACT_NAME', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('PROTHOLD', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('ADD_DATE', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('OWNER', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('ID_UPDATE', 'LONG', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#'),
                    ('WEBSYM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')]
    print 'Adding fields to Transferred TNC Lands'
    for field in addFieldList:
        arcpy.AddField_management("{0}/Transferred_TNC_Lands".format(os.path.join(basepath, fileGDBName)), 
                                  field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7], field[8])
    print 'Inserting records'
    iRows = arcpy.InsertCursor("{0}/Transferred_TNC_Lands".format(os.path.join(basepath, fileGDBName)))
    sRows = arcpy.SearchCursor(TransferredTNCLands, '("SENSDATA" <> \'Yes\') AND ("STATE" IS NOT NULL)')
    for sRow in sRows:
        iRow = iRows.newRow()
        iRow.STATE = sRow.STATE
        iRow.SOURCE = sRow.SOURCE
        iRow.AREANAM = sRow.AREANAM
        iRow.PROTMECH = sRow.PROTMECH
        iRow.COUNTRY = sRow.COUNTRY
        iRow.CLSTRANSDA = sRow.CLSTRANSDA
        iRow.TR_ID_TEXT = str(sRow.TR_IFMS_ID).replace('.0', '')
        iRow.TRACT_NAME = sRow.TRACT_NAME     
        iRow.PROTHOLD = sRow.PROTHOLD
        iRow.ADD_DATE = sRow.ADD_DATE
        iRow.OWNER = sRow.OWNER
        iRow.ID_UPDATE = sRow.ID_UPDATE
        iRow.WEBSYM = "Transferred"
        iRow.Shape = sRow.Shape
        iRows.insertRow(iRow)
    print "Appending Transferred TNC Lands to TNC Lands feature class"
    try:
        arcpy.Append_management("{0}/Transferred_TNC_Lands".format(os.path.join(basepath, fileGDBName)),
                                "{0}/TNC_Lands".format(os.path.join(basepath, fileGDBName)),
                                "NO_TEST",
                                "#",
                                "#")
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]    
    arcpy.Delete_management("{0}/Transferred_TNC_Lands".format(fileGDBPath))
    
    #---------------------------------------------------------------------------------------
    print "Creating point feature class from polygons"
    try:
        arcpy.FeatureToPoint_management("{0}/TNC_Lands".format(os.path.join(basepath, fileGDBName)),
                                        "{0}/TNC_Lands_pts".format(os.path.join(basepath, fileGDBName)))
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0]     
    
    #---------------------------------------------------------------------------------------
    print "Finished creating public web version of TNC Lands"
    return True

def do_PublicTNCLandsDownload(basepath, fileGDBName, TNCLands, TransferredTNCLands):
    """
    Create download version of public TNC Lands
    TODO:  
    """    
    print 'Creating TNC Lands download-version file geodatabase'    
    #dateString = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    #basepath = "D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/public"
    #fileGDBName = "TNCLands_d_{0}.gdb".format(dateString)
    fileGDBPath = os.path.join(basepath, fileGDBName)
    if arcpy.Exists(fileGDBPath):
        print 'Deleting previous file geodabase {0}'.format(fileGDBPath)
        arcpy.Delete_management(fileGDBPath)
    arcpy.CreateFileGDB_management(basepath, fileGDBName, "CURRENT")
    print 'Exporting public version of TNC Lands feature class to public download file geodatabase'
    fieldinfo = arcpy.FieldInfo()
    fields = arcpy.ListFields(TNCLands)
    for field in fields:
        '''
        Remove:"SOURCE", "COUNTRY", "MOD_DATE", "GLOBALID", "TRACT_NAME", "MABR_NAME", "TAXID", "HISTAXID", 
        "GLOT", "SUBD", "BLOCK", "SHAPE.STArea()", "SHAPE.STLength()"  
        
        Leave: STATE, AREANAM, GAPCAT, PROTHOLD, PROTMECH, TR_IFMS_ID, MA_IFMS_ID, CLS_ACRES, CLSTRANSDA
        '''
        if field.name in ("SOURCE", "COUNTRY", "MOD_DATE", "GLOBALID", "TRACT_NAME", "MABR_NAME", 
                          "TAXID", "HISTAXID", "GLOT", "SUBD", "BLOCK", "SHAPE.STArea()", "SHAPE.STLength()"):
            fieldinfo.addField(field.name, field.name, "HIDDEN", "")
    theExpression = '"SENSDATA" = \'No\''
    arcpy.MakeFeatureLayer_management(TNCLands, 'PublicTNC', theExpression, "", fieldinfo )
    arcpy.CopyFeatures_management('PublicTNC', os.path.join(fileGDBPath, "TNC_Lands"))
    
    print 'Exporting public version of Transferred TNC Lands feature class to public download file geodatabase'
    if arcpy.Exists(fieldinfo):
        arcpy.Delete_management(fieldinfo)
    fieldinfo = arcpy.FieldInfo()
    fields = arcpy.ListFields(TransferredTNCLands)
    for field in fields:
        '''
        Remove "SHAPE.STArea()", "SHAPE.STLength()"
        Leave all the remaining fields
        '''
        if field.name in ("SHAPE.STArea()", "SHAPE.STLength()"):
            fieldinfo.addField(field.name, field.name, "HIDDEN", "")
    arcpy.MakeFeatureLayer_management(TransferredTNCLands, 'PublicTransferredTNCLands', "", "", fieldinfo )
    arcpy.CopyFeatures_management('PublicTransferredTNCLands', os.path.join(fileGDBPath, "Transferred_TNC_Lands"))
    arcpy.Delete_management('PublicTransferredTNCLands')  
    

    
def do_InternalTNCLandsWeb(basepath, fileGDBName, TNCLands, TransferredTNCLands):
    """
    Create the internal web-map file geodatabase TNC Lands and Transferred TNC Lands feature classes. 
    TODO:  Fix the file geodatabase zip file name
    TODO:  Make US shapefile and zip it"""
    #dateString = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    #basepath = "D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/internal"
    #fileGDBName = "TNCLands_Internal_w_{0}.gdb".format(dateString)
    fileGDBPath = os.path.join(basepath, fileGDBName)
    if arcpy.Exists(fileGDBPath):
        arcpy.Delete_management(fileGDBPath)
    arcpy.CreateFileGDB_management(basepath, fileGDBName, "CURRENT")
    sr = arcpy.SpatialReference(3857)    
    arcpy.env.outputCoordinateSystem = sr
    fieldinfo = arcpy.FieldInfo()
    fields = arcpy.ListFields(TNCLands)
    for field in fields:
        """Leave all fields but SDE area and length"""
        if field.name in ("SHAPE.STArea()", "SHAPE.STLength()"):
            fieldinfo.addField(field.name, field.name, "HIDDEN", "")
    arcpy.MakeFeatureLayer_management(TNCLands, 'InternalTNCLands', "", "", fieldinfo)
    arcpy.CopyFeatures_management('InternalTNCLands', os.path.join(fileGDBPath, "TNC_Lands"))
    arcpy.Delete_management('InternalTNCLands')
    arcpy.AddField_management("{0}/TNC_Lands".format(fileGDBPath), 'ADD_DATE', 'DATE', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#')
    arcpy.AddField_management("{0}/TNC_Lands".format(fileGDBPath), 'OWNER', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')
    arcpy.AddField_management("{0}/TNC_Lands".format(fileGDBPath), 'ID_UPDATE', 'LONG', '#', '#', '#', '', 'NULLABLE', 'NON_REQUIRED', '#')
    arcpy.AddField_management("{0}/TNC_Lands".format(fileGDBPath), 'WEBSYM', 'TEXT', '#', '#', '254', '', 'NULLABLE', 'NON_REQUIRED', '#')   
    
    #calculate everthing to the current protection mechanism
    theExpression = '!PROTMECH!'
    arcpy.CalculateField_management("{0}/TNC_Lands".format(fileGDBPath), "WEBSYM", theExpression, 'PYTHON_9.3')
    
    #select the grazing leases
    theExpression = '"PROTMECH" = \'Grazing lease\''
    arcpy.MakeTableView_management("{0}/TNC_Lands".format(fileGDBPath), "internalTNCLands", theExpression)
    #calculate to 'Lease'
    theExpression = "\'Lease\'"
    arcpy.CalculateField_management("internalTNCLands", "WEBSYM", theExpression, 'PYTHON_9.3')
    
    #select grazing permits 
    theExpression = '"PROTMECH" = \'Grazing permit\''
    arcpy.MakeTableView_management("{0}/TNC_Lands".format(fileGDBPath), "internalTNCLands", theExpression)
    #calculate to 'Permit'
    theExpression = "\'Permit\'"
    arcpy.CalculateField_management("internalTNCLands", "WEBSYM", theExpression, 'PYTHON_9.3')    

    #select 'Full Conservation Easement'
    theExpression = '"PROTMECH" = \'Full conservation easement\''
    arcpy.MakeTableView_management("{0}/TNC_Lands".format(fileGDBPath), "internalTNCLands", theExpression)
    #calculate to 'Conservation easement'
    theExpression = "\'Conservation easement\'"
    arcpy.CalculateField_management("internalTNCLands", "WEBSYM", theExpression, 'PYTHON_9.3')      
    
    #select 'Management lease or agreement'
    theExpression = '"PROTMECH" = \'Management lease or agreement\''
    arcpy.MakeTableView_management("{0}/TNC_Lands".format(fileGDBPath), "internalTNCLands", theExpression)
    #calculate to 'Agreement
    theExpression = "\'Agreement\'"
    arcpy.CalculateField_management("internalTNCLands", "WEBSYM", theExpression, 'PYTHON_9.3')

    #select 'Life Estate'
    theExpression = '"PROTMECH" = \'Life Estate\''
    arcpy.MakeTableView_management("{0}/TNC_Lands".format(fileGDBPath), "internalTNCLands", theExpression)
    #calculate to 'Agreement
    theExpression = "\'Fee Ownership\'"
    arcpy.CalculateField_management("internalTNCLands", "WEBSYM", theExpression, 'PYTHON_9.3')
    
    fieldinfo = arcpy.FieldInfo()
    fields = arcpy.ListFields(TransferredTNCLands)
    for field in fields:
        """Leave all fields but SDE area and length"""
        if field.name in ("SHAPE.STArea()", "SHAPE.STLength()"):
            fieldinfo.addField(field.name, field.name, "HIDDEN", "")
    arcpy.MakeFeatureLayer_management(TransferredTNCLands, 'InternalTransferredTNCLands', "", "", fieldinfo)
    arcpy.CopyFeatures_management('InternalTransferredTNCLands', os.path.join(fileGDBPath, "Transferred_TNC_Lands"))
    arcpy.Delete_management('InternalTransferredTNCLands')
    arcpy.AddField_management("{0}/Transferred_TNC_Lands".format(fileGDBPath), 'WEBSYM', 'TEXT', '#', '#', '254', 'WEBSYM', 'NULLABLE', 'NON_REQUIRED', '#')    
    
    theExpression = "\'Transferred\'"
    arcpy.CalculateField_management("{0}/Transferred_TNC_Lands".format(fileGDBPath), "WEBSYM", theExpression, 'PYTHON_9.3')
    
    print "Appending Transferred TNC Lands to TNC Lands feature class"
    try:
        arcpy.Append_management("{0}/Transferred_TNC_Lands".format(os.path.join(basepath, fileGDBName)),
                                "{0}/TNC_Lands".format(os.path.join(basepath, fileGDBName)),
                                "NO_TEST",
                                "#",
                                "#") 
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except Exception as e:
        print e.args[0] 

    arcpy.Delete_management("{0}/Transferred_TNC_Lands".format(fileGDBPath))

def do_InternalTNCLandsDownload(TNCLands, TransferredTNCLands):
    """
    Create the internal web-map file geodatabase TNC Lands and Transferred TNC Lands feature classes. 
    TODO:  Convert polygons to point feature class
    TODO:  Add text TR_IFMSID
    TODO:  Add text MA_IFMSID
    TODO:  Fix the zip file names"""
    dateString = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    basepath = "D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/internal"
    fileGDBName = "TNCLands_Internal_d_{0}.gdb".format(dateString)
    fileGDBPath = os.path.join(basepath, fileGDBName)
    if arcpy.Exists(fileGDBPath):
        arcpy.Delete_management(fileGDBPath)
    arcpy.CreateFileGDB_management(basepath, fileGDBName, "CURRENT")
    sr = arcpy.SpatialReference(3857)    
    arcpy.env.outputCoordinateSystem = sr
    fieldinfo = arcpy.FieldInfo()
    fields = arcpy.ListFields(TNCLands)
    for field in fields:
        """Leave all fields but SDE area and length"""
        if field.name in ("SHAPE.STArea()", "SHAPE.STLength()"):
            fieldinfo.addField(field.name, field.name, "HIDDEN", "")
    arcpy.MakeFeatureLayer_management(TNCLands, 'InternalTNCLands', "", "", fieldinfo)
    arcpy.CopyFeatures_management('InternalTNCLands', os.path.join(fileGDBPath, "TNC_Lands"))
    arcpy.Delete_management('InternalTNCLands')

    fieldinfo = arcpy.FieldInfo()
    fields = arcpy.ListFields(TransferredTNCLands)
    for field in fields:
        """Leave all fields but SDE area and length"""
        if field.name in ("SHAPE.STArea()", "SHAPE.STLength()"):
            fieldinfo.addField(field.name, field.name, "HIDDEN", "")
    arcpy.MakeFeatureLayer_management(TransferredTNCLands, 'InternalTransferredTNCLands', "", "", fieldinfo)
    arcpy.CopyFeatures_management('InternalTransferredTNCLands', os.path.join(fileGDBPath, "Transferred_TNC_Lands"))
    arcpy.Delete_management('InternalTransferredTNCLands')

    """
    TODO: Create US-wide file geodatabase zip and shapefile zip of downlaodable data
    """
    zipData(os.path.join(fileGDBPath, "TNC_Lands"),
            os.path.join(fileGDBPath, 'Transferred_TNC_Lands'),
            'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/internal/shps', 
            'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/internal/gdbs',
            'D:/GIS_Data/jplatt/Workspace/Data/NACR/TNCLands/Data/tncLands/internal/zips')
    
def zipData(inTNCLands, inTransferredTNCLands, shploc, gdbloc, ziploc):
    """
    TODO: Create US-wide file geodatabase zip and shapefile zip of downlaodable data
    """
    # set workspace
    arcpy.env.workspace = shploc
    #create reference to state name state FIPS table
    st = 'Database Connections/nacrloader @ default.mnsde.tnc.sde/tncgdb.NACRLOADER.stateList'
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
