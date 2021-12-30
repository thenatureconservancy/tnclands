#Standard imports
import os
import sys
#---------------------------------------------------------------------
#Non-standard imports
import arcpy
#---------------------------------------------------------------------
#arcpy environment settings
arcpy.env.overwriteOutput = True
#---------------------------------------------------------------------
'''Outline:
    set up paths to resources
    
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
                     'Deed Restrictions' : 'Deed Restrictions',
                     'Deed Restrictions - MonReq' : 'Deed Restrictions',
                     'Deed Restrictions - NoMon' : 'Deed Restrictions',
                     'Management Lease or Agreement' : 'Management Lease or Agreement',
                     'Timber Lease or Agreement' : 'Management Lease or Agreement',
                     'Grazing Lease' : 'Management Lease or Agreement',
                     'Grazing Permit' : 'Management Lease or Agreement',
                     'Life Estate' : 'Other',
                     'Right of Way Tract' : 'Right of Way',
                     'Access Right of Way' : 'Right of Way',
                     'Assist' : 'Assist',
                     'Assist - Fee Ownership' : 'Assist',
                     'Assist - Conservation Easement' : 'Assist',
                     'Assist - Deed Restriction' : 'Assist',
                     'Transfer' : 'Transfer',
                     'Transfer - Fee Ownership' : 'Transfer',
                     'Transfer - Conservation Easement' : 'Transfer',
                     'Transfer - Deed Restriction' : 'Transfer',
                     'Transfer - Life Estate' : 'Transfer',
                     'Transfer - Management Lease or Agreement' : 'Transfer',
                     'Transfer - Agreement' : 'Transfer'
                     }
    return dictMapSymbol
    pass

#---------------------------------------------------------------------
def createLRMFieldList():
    print('Creating LRM field list')
    print(arcpy.AddMessage('Creating LRM field list'))
    lstLRMField = ['LRM Tract ID', 'Tract Name', 'Country', 'Primary Geocode', 'Primary Cons Area Name', 'Interest Holder', 
                   'Interest Code','Interest Acres', 'Original Protection Date', 'LRM MU ID', 'Monitoring Unit Name', 
                   'Primary Fee owner name']
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

def setPaths(gdbPath, tncLandsFC):
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
        except Exception as e:
            print(e.args[0])
    #---------------------------------------------------------------------
    #convert LRM Excel report to geodatabase table and create index on LRM tract ID
    print('Converting LRM Excel file/tab to geodatabase table')
    try:
        arcpy.ExcelToTable_conversion(lrmPath, os.path.join(gdbPath, 'lrmReport'), lrmSheetName)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print(e.args[0])
    #---------------------------------------------------------------------
    print('Creating indexes LRM table')
    indexes = arcpy.ListIndexes(os.path.join(gdbPath, 'lrmReport'))
    try:
        if 'indx_trID' not in indexes: 
            arcpy.AddIndex_management(os.path.join(gdbPath, 'lrmReport'), ['LRM_Tract_ID'], 'indx_trID')
        else:
            arcpy.RemoveIndex_management(os.path.join(gdbPath, 'lrmReport'), ['LRM_Tract_ID'])
            arcpy.AddIndex_management(os.path.join(gdbPath, 'lrmReport'), ['LRM_Tract_ID'], 'indx_trID')
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print(e.args[0])
    
    return True

def createLRMSeachCursor():
    pass
def createTNCLandsSearchCursor():
    pass
def createTNCLandsUpdateCursor():
    pass
def updateTNCLands():
    #start checking LRM fields
    #create search cursor on LRM table
    print('Creating search cursor on LRM report table and update cursor on TNC Lands\nand beginning TNC Lands update process')
    lrmCursor = arcpy.da.SearchCursor(os.path.join(gdbPath, 'lrmReport'), ['LRM_Tract_ID', 'Tract_Name'])
    for lrmRow in lrmCursor:
        print(f"Seach cursor expression from LRM table:\n\tLRM_Tract_ID = {lrmRow[0]} and Tract Name = {lrmRow[1]}")
        tractid = f"{lrmRow[0]}"
        #select matching TNC Lands records
        try:
            tncLandsCursor = arcpy.da.UpdateCursor(os.path.join(gdbPath, tncLandsPath), ['LRM_TR_ID', 'LRM_TR_NA'], f"LRM_TR_ID = {tractid}")
            for tncLandsRow in tncLandsCursor:
                print(f"Return from TNC Lands spatial data:\n\tLRM_TR_ID: {tncLandsRow[0]}\tLRM_TR_NA: {tncLandsRow[1]}")
        except arcpy.ExecuteError:
            print(arcpy.GetMessages(2))
        except Exception as e:
            print(e.args[0])
    
#---------------------------------------------------------------------
def main():
    '''
    MAPSYMBOLDICT = createMapSymbolDictionary()
    LRMFIELDLIST = createLRMFieldList()
    TNCLANDSFIELDLIST = createTNCLandsFieldList()
    LRMPATH = arcpy.GetParameterAsText[0]
    LRMSHEETNAME = arcpy.GetParameterAsText[1]
    GDPPATH = arcpy.GetParameterAsText[2]
    FC = arcpy.GetParameterAsText[3]
    '''
    LRMPATH = sys.argv[1]
    LRMSHEETNAME = sys.argv[2]
    GDBPATH = sys.argv[3]
    FC = sys.argv[4]

    # print(f"{LRMPATH}, {LRMSHEETNAME}, {GDBPATH}, {FC}")

    tncLandsPath = setPaths(GDBPATH, FC)
    result = createLRMTable(GDBPATH, LRMPATH, LRMSHEETNAME)

    print(tncLandsPath, result)
    print('fin')

if __name__ == '__main__':
    main()
