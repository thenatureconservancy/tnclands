import arcpy
import datetime
arcpy.env.overwriteOutput = True

class shareConverter(object):
    def __init__(self):
        """PADUS and NCED Superclass"""
        pass
class PADUS_USGSConverter(shareConverter):
    Category = None
    Own_Type = None
    Own_Name = None
    Loc_Own = None
    Mang_Type = None
    Mang_Name = None
    Loc_Mang = None
    Des_Tp = None
    Loc_Ds = None
    Unit_Nm = None
    Loc_Nm = None
    State_Nm = None
    Agg_Src = None
    GIS_Src = None
    Src_Date = None
    GIS_Acres = None
    Source_PAID = None
    WDPA_Cd = None
    Access = None
    Access_Src = None
    GAP_Sts = None
    GAPCdSrc = None
    GAPCdDt = None
    IUCN_Cat = None
    IUCNCtSrc = None
    IUCNCtDt = None
    Date_Est = None
    Comments = None
    Shape = None
    
    def __init__(self, STATE, AREANAM, GAPCAT, PROTMECH, CLSTRANSDA, TR_IFMS_ID, MA_IFMS_ID): #, Acres):
        self.State = STATE
        self.AreaName = AREANAM
        self.GAPCat = GAPCAT
        self.ProtMech = PROTMECH
        self.CLSTransDate = CLSTRANSDA.strftime('%Y')
        self.TractID = TR_IFMS_ID
        self.ManagedAreaID = MA_IFMS_ID
        #self.Acres = CLS_Acres

    def Category(self):
        if self.ProtMech == 'Fee Ownership':
            return 'Fee'
        elif self.ProtMech == 'Conservation Easement':
            return 'Easement'
    def Own_Type(self):
        return 'NGO'
    def Own_Name(self):
        return 'NGO'
    def Loc_Own(self):
        return 'The Nature Conservancy'
    def Mang_Type(self):
        return 'NGO'
    def Mang_Name(self):
        return 'NGO'
    def Loc_Mang(self):
        return 'The Nature Conservancy'
    def Des_Tp(self):
        if self.ProtMech == 'Fee Ownership':
            return 'PCON'
        elif self.ProtMech == 'Conservation Easement':
            return 'CONE'
    def Loc_Ds(self):
        if self.ProtMech == 'Fee Ownership':
            return 'Private Conservation Land'
        elif self.ProtMech == 'Conservation Easement':
            return 'Private Conservation Easement'
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
    def State_Abbrev(self):
        StateDomain = {}
        StateDomain['AL'] = ['AL', 'Alabama', '01']
        StateDomain['AK'] = ['AK', 'Alaska', '02']
        StateDomain['AZ'] = ['AZ', 'Arizona', '04']
        StateDomain['AR'] = ['AR', 'Arkansas', '05']
        StateDomain['CA'] = ['CA', 'California', '06']
        StateDomain['CO'] = ['CO', 'Colorado', '08']
        StateDomain['CT'] = ['CT', 'Connecticut', '09']
        StateDomain['DE'] = ['DE', 'Deleware', '10']
        StateDomain['DC'] = ['DC', 'District of Columbia', '11']
        StateDomain['FL'] = ['FL', 'Florida', '12']
        StateDomain['GA'] = ['GA', 'Georgia', '13']
        StateDomain['HI'] = ['HI', 'Hawaii', '15']
        StateDomain['ID'] = ['ID', 'Idaho', '16']
        StateDomain['IL'] = ['IL', 'Illinois', '17']
        StateDomain['IN'] = ['IN', 'Indiana', '18']
        StateDomain['IA'] = ['IA', 'Iowa', '19']
        StateDomain['KS'] = ['KS', 'Kansas', '20']
        StateDomain['KY'] = ['KY', 'Kentucky', '21']
        StateDomain['LA'] = ['LA', 'Louisiana', '22']
        StateDomain['ME'] = ['ME', 'Maine', '23']
        StateDomain['MD'] = ['MD', 'Maryland', '24']
        StateDomain['MA'] = ['MA', 'Massachusetts', '25']
        StateDomain['MI'] = ['MI', 'Michigan', '26']
        StateDomain['MN'] = ['MN', 'Minnesota', '27']
        StateDomain['MS'] = ['MS', 'Mississippi', '28']
        StateDomain['MO'] = ['MO', 'Missouri', '29']
        StateDomain['MT'] = ['MT', 'Montana', '30']
        StateDomain['NE'] = ['NE', 'Nebraska', '31']
        StateDomain['NV'] = ['NV', 'Nevada', '32']
        StateDomain['NH'] = ['NH', 'New Hampshire', '33']
        StateDomain['NJ'] = ['NJ', 'New Jersey', '34']
        StateDomain['NM'] = ['NM', 'New Mexico', '35']
        StateDomain['NY'] = ['NY', 'New York', '36']
        StateDomain['NC'] = ['NC', 'North Carolina', '37']
        StateDomain['ND'] = ['ND', 'North Dakota', '38']
        StateDomain['OH'] = ['OH', 'Ohio', '39']
        StateDomain['OK'] = ['OK', 'Oklahoma', '40']
        StateDomain['OR'] = ['OR', 'Oregon', '41']
        StateDomain['PA'] = ['PA', 'Pennsylvania', '42']
        StateDomain['RI'] = ['RI', 'Rhode Island', '44']
        StateDomain['SC'] = ['SC', 'South Carolina', '45']
        StateDomain['SD'] = ['SD', 'South Dakota', '46']
        StateDomain['TN'] = ['TN', 'Tennessee', '47']
        StateDomain['TX'] = ['TX', 'Texas', '48']
        StateDomain['UT'] = ['UT', 'Utah', '49']
        StateDomain['VT'] = ['VT', 'Vermont', '50']
        StateDomain['VA'] = ['VA', 'Virginia', '51']
        StateDomain['WA'] = ['WA', 'Washington', '53']
        StateDomain['WV'] = ['WV', 'West Virginia', '54']
        StateDomain['WI'] = ['WI', 'Wisconsin', '55']
        StateDomain['WY'] = ['WY', 'Wyoming', '56']
        return StateDomain[self.State][0]
    def Agg_Src(self):
        return 'TNC_Lands {}'.format(datetime.date.today()) 
    def GIS_Src(self):
        return 'TNC_Lands'
    def Src_Date(self):
        return str(datetime.date.today())
    def GIS_Acres(self):
        return self.Acres
    def Source_PAID(self):
        if self.ManagedAreaID is not None:
            return 'MAID: {}'.format(str(self.ManagedAreaID).rstrip('.0'))
        else:
            return 'TRID: {}'.format(str(self.TractID).rstrip('.0'))
    def WDPA_Cd(self):
        return None
    def Access(self):
        if self.ProtMech == 'Fee Ownership':
            return 'UK'
        elif self.ProtMech == 'Conservation Easement':
            return 'XA'
    def Access_Src(self):
        return ''
    def GAPSts(self):
        if self.GAPCat == '1':
            return "1"  #1 - managed for biodiversity - disturbance events proceed or are mimicked
        elif self.GAPCat == '2':
            return "2"  #2 - managed for biodiversity - disturbance events suppressed
        elif self.GAPCat == '3':
            return "3"  #3 - managed for multiple uses - subject to extractive (e.g. mining or logging) or OHV use
        elif self.GAPCat == '4':
            return "4"  #4 - no known mandate for protection
    def GAPCdSrc(self):
        return 'GAP Default'
    def GAPCdDt(self):
        return self.CLSTransDate
    def IUCN_Cat(self):
        if self.GAPCat == '1' or self.GAPCat == '2':
            return 'V'
        else:
            return 'VI'
    def IUCNCtSrc(self):
        return ''
    def IUCNCtDt(self):
        return ''
    def Date_Est(self):
        return self.CLSTransDate
    def Comments(self):
        return ''
def do_PADUS_USGS(theSourceTable, theTargetTable):
    theExpression = ' ("STATE" IS NOT NULL) and ("PROTMECH" in (\'Fee Ownership\')) and ("SENSDATA" = \'No\') ' 
    sRows = arcpy.SearchCursor(dataset=theSourceTable, where_clause=theExpression, sort_fields='STATE A')
    try:
        arcpy.TruncateTable_management(theTargetTable)
        print arcpy.GetMessages()
        try:
            iRows = arcpy.InsertCursor(theTargetTable)
            count = 0 
            for sRow in sRows:
                test = PADUS_USGSConverter(sRow.STATE, sRow.AREANAM, sRow.GAPCAT, sRow.PROTMECH, sRow.CLSTRANSDA, sRow.TR_IFMS_ID, sRow.MA_IFMS_ID)#, sRow.Acres)
                iRow = iRows.newRow()
                iRow.Category = test.Category()
                iRow.Own_Type = test.Own_Type()
                iRow.Own_Name = test.Own_Name()
                iRow.Loc_Own = test.Loc_Own()
                iRow.Mang_Type = test.Mang_Type()
                iRow.Mang_Name = test.Mang_Name()
                iRow.Loc_Mang = test.Loc_Mang()
                iRow.Des_Tp = test.Des_Tp()
                iRow.Loc_Ds = test.Loc_Ds()
                iRow.Unit_Nm = test.P_Des_Nm()
                iRow.Loc_Nm = test.P_Des_Nm()
                iRow.State_Nm = test.State_Abbrev()
                iRow.Agg_Src = test.Agg_Src()
                iRow.GIS_Src = test.GIS_Src()
                iRow.Src_Date = test.Src_Date()
                theShape = sRow.Shape
                iRow.Source_PAID = test.Source_PAID()
                iRow.WDPA_Cd = test.WDPA_Cd()
                iRow.Access = test.Access()
                iRow.Access_Src = test.Access_Src()
                iRow.GAP_Sts = test.GAPSts()
                iRow.GAPCdSrc = test.GAPCdSrc()
                iRow.GAPCdDt = test.GAPCdDt()
                iRow.IUCN_Cat = test.IUCN_Cat()
                iRow.IUCNCtSrc = test.IUCNCtSrc()
                iRow.IUCNCtDt = test.IUCNCtDt()
                iRow.Date_Est = test.Date_Est()
                iRow.Comments = test.Comments()
                iRow.Shape = sRow.Shape
                try:
                    iRows.insertRow(iRow)
                except arcpy.ExecuteError:
                    print arcpy.GetMessages(2)
                    print "In arcpy insert test at record {}, local designation {}".format(count, test.Loc_Ds)
                except Exception as e:
                    print e.args[0]
                    print "In python insert test at record {}, local designation {}".format(count, test.Loc_Ds)
                del iRow
                count += 1
                if count % 100 == 0:
                    print "%i records converted" %count
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
            print "In arcpy insert record creating test"
        except Exception as e:
            print e.args[0]
            print "In python insert record creating test"
        
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        print "In arcpy truncate test"
    except Exception as e:
        print e.args[0]
        print "In python truncate test"
 
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
