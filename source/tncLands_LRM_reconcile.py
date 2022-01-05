#Standard imports
import os
import sys
import datetime

#---------------------------------------------------------------------
#Non-standard imports
# Non-standard imports
import arcpy

# other imports that may be necessary at a future date
# import pandas as pd
# from arcgis.gis import GIS
# from arcgis.features import FeatureLayer
# from arcgis.features import FeatureLayerCollection
# from arcgis.mapping import WebMap
# from arcgis.geometry import Geometry
# gis = GIS("home")

#---------------------------------------------------------------------
#arcpy environment settings
arcpy.env.overwriteOutput = True
#---------------------------------------------------------------------
'''Outline:
    set up paths to script input resources
    convert LRM Excel to geodatabase table
    TODO: check for fields in new table(?)
    
    TODO: create search cursor on LRM table
    TODO: check for field in TNC Lands spatial data(?)
    
    TODO: create search cursor on LRM table
    TODO: create dictionary of tract ids, tract name and state
    TODO: create search cursor on TNC Lands spatial data
    TODO: create dictionary of tract ids tract name and state

    TODO: check LRM against TNC Lands dictionary
    TODO: check TNC Lands against LRM dictionary
    
    create update cursor on TNC Lands spatial data
    step through LRM search cursor and update corresponding
      TNC Lands spatial data
    write out report
'''
#---------------------------------------------------------------------
def createTNCLandsCodeList():
    #Not entirely sure if this will be necessary, but the function is present, just in case.
    #Coded domain lists are used to check that the TNC Interest have have valid entries
    print('Creating TNC Interest coded domain list')
    print(arcpy.AddMessage('Creating TNC Interest coded domain list'))
    #TNC Lands (not LRM) interest codes
    lstTNCInt = ['Fee Ownership', 'Conservation Easement', 'Deed Restrictions', 'Deed Restrictions - MonReq', 'Deed Restrictions - NoMon', 
    'Management Lease or greement', 'Timber Lease or Agreement', 'Grazing Lease', 'Grazing Permit', 'Life Estate', 
    'Right of Way Tract', 'Access Right of Way', 'Assist', 'Assist - Fee Ownership', 'Assist - Conservation Easement', 
    'Assist - Deed Restriction', 'Transfer', 'Transfer - Fee Ownership', 'Transfer - Conservation Easement', 
    'Transfer - Deed Restriction', 'Transfer - Life Estate', 'Transfer - Management Lease or Agreement', 'Transfer - Agreement']
    return lstTNCInt
    pass

def createGAPCATDictionary():
    #create dictionary of GAP codes
    print('Creating GAP category dictionary')
    print(arcpy.AddMessage('Creating GAP category dictionary'))
    dictGAPCAT = {'1': 'managed for biodiversity; disturbance events proceed or are mimicked',
                  '2': 'managed for biodiversity; disturbance events suppressed',
                  '3': 'managed for multiple uses; subject to extractive (eg. mining or logging) or OHV use',
                  '4': 'no known mandate for biodiversity protection'}
    return dictGAPCAT
    pass

def createMapSymbolDictionary():
    #create map symbol dictionary
    print('Creating map symbol dictionary')
    print(arcpy.AddMessage('Creating map symbol dictionary'))
    dictMapSymbol = {'Fee Ownership' : 'Fee Ownership',
                     'Conservation Easement' : 'Conservation Easement', 
                    #  'Deed Restrictions' : 'Deed Restrictions',
                    #  'Deed Restrictions - MonReq' : 'Deed Restrictions',
                    #  'Deed Restrictions - NoMon' : 'Deed Restrictions',
                    #  'Management Lease or Agreement' : 'Management Lease or Agreement',
                    #  'Timber Lease or Agreement' : 'Management Lease or Agreement',
                    #  'Grazing Lease' : 'Management Lease or Agreement',
                    #  'Grazing Permit' : 'Management Lease or Agreement',
                    #  'Life Estate' : 'Other',
                    #  'Right of Way Tract' : 'Right of Way',
                    #  'Access Right of Way' : 'Right of Way',
                    #  'Assist' : 'Assist',
                    #  'Assist - Fee Ownership' : 'Assist',
                    #  'Assist - Conservation Easement' : 'Assist',
                    #  'Assist - Deed Restriction' : 'Assist',
                    #  'Transfer' : 'Transfer',
                    #  'Transfer - Fee Ownership' : 'Transfer',
                    #  'Transfer - Conservation Easement' : 'Transfer',
                    #  'Transfer - Deed Restriction' : 'Transfer',
                    #  'Transfer - Life Estate' : 'Transfer',
                    #  'Transfer - Management Lease or Agreement' : 'Transfer',
                    #  'Transfer - Agreement' : 'Transfer'
                     }
    return dictMapSymbol
    pass

#---------------------------------------------------------------------
def createLRMFieldList():
    print('Creating LRM field list')
    print(arcpy.AddMessage('Creating LRM field list'))
    lstLRMField = ['LRM_Tract_ID', 'Tract_Name', 'Country', 'Primary_State_name', 'Primary_Cons_area_name', 'Holder', 
                   'Interest_Code','Interest_Acres', 'Original_Protection_date', 'LRM_MU_ID', 'Monitoring_Unit_name', 
                   'Primary_Fee_owner_name']
    return lstLRMField
    pass

def createTNCLandsFieldList():
    print('Creating TNC Lands field list')
    print(arcpy.AddMessage('Creating TNC Lands field list'))    
    lstTNCLandsField = ['LRM_TR_ID', 'LRM_TR_NA', 'COUNTRY', 'STATE', 'CONS_AREA', 'PROTHOLD',
                        'TNC_INT', 'LRM_ACRES', 'PROT_DATE', 'LRM_MU_ID', 'LRM_MU_NA', 
                        'FEE_OWNER', 'MAP_SYM']
    return lstTNCLandsField
    pass

def setTNCLandsPath(gdbPath, tncLandsFC):
    # #set path to LRM report
    # print('Setting LRM path and sheet/tab name')
    # print(arcpy.AddMessage('Setting LRM path and sheet/tab name'))

    # lrmPath = 'D:/jplatt/projects/TNC_Lands/data/Fee_CE_Assessments/NAR Fee & Eas report 12-21-21.xlsx'
    # lrmSheetName = 'Sheet1'
    
    # #set path to target or working file geodatabase
    # print('Setting working file geodatabase path')
    # print(arcpy.AddMessage('Setting working file geodatabase path'))
    # gdbPath = 'D:/jplatt/projects/TNC_Lands/data/TNC_Lands_working.gdb'
    # tncLands = 'TNC_Lands_Base'
    
    print('Setting path to TNC Lands Base')
    print(arcpy.AddMessage('Setting path to TNC Lands Base'))
    tncLandsPath = os.path.join(gdbPath, tncLandsFC)
    return tncLandsPath
    pass
    
def createLRMTable(gdbPath, lrmPath, lrmSheetName):
    #delete previous LRM report table in the file geodatabase
    print('Deleting previous LRM table')
    if arcpy.Exists(os.path.join(gdbPath, 'lrmReport')):
        try:
            arcpy.Delete_management(os.path.join(gdbPath, 'lrmReport'))
        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))
            return False
        except Exception as e:
            print(e.args[0])
            return False
    #---------------------------------------------------------------------
    #convert LRM Excel report to geodatabase table and create index on LRM tract ID
    print('Converting LRM Excel file/tab to geodatabase table')
    try:
        arcpy.ExcelToTable_conversion(lrmPath, os.path.join(gdbPath, 'lrmReport'), lrmSheetName)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        return False
    except Exception as e:
        print(e.args[0])
        return False
    #---------------------------------------------------------------------
    print('Creating indexes LRM table')
    indexes = arcpy.ListIndexes(os.path.join(gdbPath, 'lrmReport'))
    try:
        if 'indx_trID' in indexes: 
            arcpy.RemoveIndex_management(os.path.join(gdbPath, 'lrmReport'), ['LRM_Tract_ID'])
        else:
            pass
        arcpy.AddIndex_management(os.path.join(gdbPath, 'lrmReport'), ['LRM_Tract_ID'], 'indx_trID')
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        return False
    except Exception as e:
        print(e.args[0])
        return False

    return True

def createReconciliationReport(gdbPath, tncLandsPath):
    print("Starting LRM and TNC Lands reconcilation")
    lrmCursor = arcpy.da.SearchCursor(os.path.join(gdbPath, 'lrmReport'), 'LRM_Tract_ID')
    lrmTractIDList = []
    for lrmRow in lrmCursor:
        lrmTractIDList.append(lrmCursor[0])
    lrmTractIDList.sort()
    lrmTractIDSet = set(lrmTractIDList)
    lrmCount = len(lrmTractIDSet)

    tncLandsCursor = arcpy.da.SearchCursor(tncLandsPath, 'LRM_TR_ID', "TNC_INT IN ('Fee Ownership', 'FEE', 'Conservation Easement', 'EAS')")
    tncLandsTractIDList = []
    for tncLandsRow in tncLandsCursor:
        if tncLandsCursor[0] is not None:
            tncLandsTractIDList.append(tncLandsCursor[0])
    tncLandsTractIDList.sort()
    tncLandsTractIDSet = set(tncLandsTractIDList)
    tncLandsCount = len(tncLandsTractIDSet)
    
    print(arcpy.AddMessage(f"Number of Tract IDs in LRM report: {lrmCount}"))
    print(arcpy.AddMessage(f"Number of Tract IDs in TNC Lands feature class: {tncLandsCount}"))    

    #Tract IDs from the LRM report that are not in TNC Lands
    diffLRMtoTNCLands = lrmTractIDSet.difference(tncLandsTractIDSet)

    #Tract IDs from TNC Lands that are not in the LRM report
    diffTNCLandstoLRM = tncLandsTractIDSet.difference(lrmTractIDSet)

    #TractIDs that are in both the LRM eport and TNC Lands
    intersectLRMtoTNCLands = lrmTractIDSet.intersection(tncLandsTractIDSet)

    outfile = open(os.path.join(os.path.dirname(gdbPath), 'inLRM_not_in_TNCLands.txt'), 'w')
    outfile.write("LRM Tract ID, Tract Name, Primary Geocode, Primary Cons Area Name, Interest Code, Interest Acres, Original Protection Date\n")
    for tractID in diffLRMtoTNCLands:
        lrmCursor = arcpy.da.SearchCursor(in_table=os.path.join(gdbPath, 'lrmReport'), 
                                          field_names=['LRM_Tract_ID', 'Tract_Name', 'Primary_Geocode', 'Primary_Cons_area_name', 'Interest_Code', 'Interest_Acres', 'Original_Protection_date'],
                                          where_clause = f"LRM_Tract_ID = {tractID}")
        for lrmRow in lrmCursor:
            outfile.write(f"{lrmRow[0]}, {lrmRow[1]}, {lrmRow[2]}, {lrmRow[3]}, {lrmRow[4]}, {lrmRow[5]}, {lrmRow[6]}\n")
    outfile.flush()
    outfile.close()

    outfile = open(os.path.join(os.path.dirname(gdbPath), 'inTNCLands_not_in_LRM.txt'), 'w')
    outfile.write("LRM Tract ID, LRM Tract Name, State, Conservation Area Name, TNC Interest, LRM Acres, Protection Date")
    for tractID in diffTNCLandstoLRM:
        tncLandsCursor = arcpy.da.SearchCursor(in_table=tncLandsPath, 
                                                field_names = ['LRM_TR_ID', 'LRM_TR_NA', 'STATE', 'CONS_AREA', 'TNC_INT', 'LRM_ACRES', 'PROT_DATE'], 
                                                where_clause = f"LRM_TR_ID = {tractID}")
        for tncRow in tncLandsCursor:
            outfile.write(f"{tncRow[0]}, {tncRow[1].strip()}, {tncRow[2]}, {tncRow[3]}, {tncRow[4]}, {tncRow[5]}\n")
    outfile.flush()
    outfile.close()

    return True

def updateTNCLands(gdbPath, tncLandsPath, dictIntCode):
    recordCount = 0
    #start checking LRM fields
    #create search cursor on LRM table
    print('Creating search cursor on LRM report table and update cursor on TNC Lands\nand beginning TNC Lands update process')
    lrmCursor = arcpy.da.SearchCursor(os.path.join(gdbPath, 'lrmReport'), 
                                     ['LRM_Tract_ID', 'Tract_Name', 'Country', 'Primary_Geocode', 
                                      'Primary_Cons_area_name', 'Holder', 'Interest_Code', 'Interest_Acres', 
                                      'Original_Protection_date', 'LRM_MU_ID', 'Monitoring_Unit_name', 'Primary_Fee_owner_name'])
    for lrmRow in lrmCursor:
        #print(f"Seach cursor expression from LRM table:\n\tLRM_Tract_ID = {lrmRow[0]} and Tract_Name = {lrmRow[1]}")
        tractid = f"{lrmRow[0]}"

        if f"{lrmRow[6]}" == 'EAS':
            lrmInterest = 'Conservation Easement'
        elif f"{lrmRow[6]}" == 'FEE':
            lrmInterest = 'Fee Ownership'
        if f"{lrmRow[2]}" == 'US':
            lrmCountry = 'United States of America'
        
        #select matching TNC Lands records
        try:
            tncLandsCursor = arcpy.da.UpdateCursor(os.path.join(gdbPath, tncLandsPath), 
                                                  ['LRM_TR_ID', 'LRM_TR_NA', 'COUNTRY', 'STATE', 
                                                   'CONS_AREA', 'PROTHOLD', 'TNC_INT', 'LRM_ACRES', 
                                                   'PROT_DATE', 'LRM_MU_ID', 'LRM_MU_NA', 'FEE_OWNER', 
                                                   'MAP_SYM'], 
                                                  f"LRM_TR_ID = {tractid}")
            for tncLandsRow in tncLandsCursor:
                #tncLandsRow[0] = lrmRow[0]
                tncLandsRow[1] = lrmRow[1] # 'Tract_Name' -> 'LRM_TR_NA'
                tncLandsRow[2] = lrmCountry # 'Country' -> 'COUNTRY'
                tncLandsRow[3] = lrmRow[3] # 'Primary_Geocode' -> 'STATE'
                tncLandsRow[4] = lrmRow[4] # 'Primary_Cons_area_name' -> 'CONS_AREA'
                tncLandsRow[5] = lrmRow[5] # 'Holder' -> 'PROTHOLD'
                tncLandsRow[6] = lrmInterest # 'Interest_Code' -> 'TNC_INT'
                tncLandsRow[7] = lrmRow[7] # 'Interest_Acres' -> 'LRM_ACRES'
                tncLandsRow[8] = lrmRow[8] # 'Original_Protection_date' -> 'PROT_DATE'
                tncLandsRow[9] = lrmRow[9] # 'LRM_MU_ID' -> 'LRM_MU_ID'
                tncLandsRow[10] = lrmRow[10] # 'Monitoring_Unit_name' -> 'LRM_MU_NA'
                tncLandsRow[11] = lrmRow[11] # 'Primary_Fee_owner_name' -> 'FEE_OWNER'
                tncLandsRow[12] = lrmInterest # 'MAP_SYM'

                tncLandsCursor.updateRow(tncLandsRow)

        except arcpy.ExecuteError:
            print(f'in arcpy error {arcpy.GetMessages(2)}')
        except Exception as e:
            print(f'in general python error {e.args[0]}')
            
        recordCount += 1
        if recordCount % 50 == 0:
            print(f"{recordCount} TNC Lands records updated with LRM attributes")
    
    return True

#---------------------------------------------------------------------
def main():
    '''
    MAPSYMBOLDICT = createMapSymbolDictionary()
    LRMFIELDLIST = createLRMFieldList()
    TNCLANDSFIELDLIST = createTNCLandsFieldList()
    '''

    # LRMPATH = arcpy.GetParameterAsText[0]
    # LRMSHEETNAME = arcpy.GetParameterAsText[1]
    # GDBPATH = arcpy.GetParameterAsText[2]
    # FC = arcpy.GetParameterAsText[3]
    
    LRMPATH = sys.argv[1]
    LRMSHEETNAME = sys.argv[2]
    GDBPATH = sys.argv[3]
    FC = sys.argv[4]

    start = datetime.datetime.now()

    print(f"{LRMPATH}, {LRMSHEETNAME}, {GDBPATH}, {FC}")

    DICTMAPSYMBOL = createMapSymbolDictionary()

    tncLandsPath = setTNCLandsPath(GDBPATH, FC)
    
    result = createLRMTable(GDBPATH, LRMPATH, LRMSHEETNAME)

    print(tncLandsPath, result)

    result = createReconciliationReport(GDBPATH, tncLandsPath)

    result = updateTNCLands(GDBPATH, tncLandsPath, DICTMAPSYMBOL)
    
    print(f'Finished in {datetime.datetime.now() - start}')

if __name__ == '__main__':
    main()
