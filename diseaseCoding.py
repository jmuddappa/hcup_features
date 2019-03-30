import numpy as np
import warnings
import pandas as pd
warnings.filterwarnings('ignore')


class HCUPCodes:
    def __init__(self, name, codes, andFlag=0, dependentCodes=None):
        self.name = name
        self.codes = codes
        self.andFlag = andFlag
        self.dependentCodes = dependentCodes


# add diseases or modify codes here
diseases = []
diseases.append(HCUPCodes('AcalculousCholecystitis', [
                '5750', '57511', '57510', '57512', '5752', '975']))
diseases.append(HCUPCodes('STM Chole', ['973', '57420', '57421']))
diseases.append(HCUPCodes('CalculousCholecystitis', [
                '57400', '57401', '57410', '57411', '971', '972']))
diseases.append(HCUPCodes('Choledocholithiasis', ['57430', '57431', '57440', '57441', '57450', '57451',
                                                  '57460', '57461', '57470', '57471', '57480', '57481', '57490',
                                                  '57491', '974']))
diseases.append(HCUPCodes('AscendingCholang', ['5761']))
diseases.append(HCUPCodes('AcutePancreatitis', ['5770', '991']))
diseases.append(HCUPCodes('AdhesiveSmallBowelObs', ['56081', '9633']))
diseases.append(HCUPCodes('Appendicitis', ['5400', '5409', '541', '542']))
diseases.append(HCUPCodes('AppendicitisAbscess', ['5401']))
diseases.append(HCUPCodes('GIBleed', ['53100', '53101', '53120', '53121', '53140', '53141', '53160', '53161', '53200',
                                      '53201', '53220', '53221', '53240', '53241', '53260', '53261', '53300', '53301', '53320',
                                      '53321', '53340', '53341', '53360', '53361', '53400', '53401', '53420', '53421',
                                      '53440', '53441', '53460', '53461', '53021', '5307', '53082', '53501', '53511',
                                      '53521', '53531', '53541', '53561', '53571', '5693', '56985', '56986', '5780',
                                      '5781', '5789', '56212', '56213', '4560', '4562', '9101', '9102', '9103',
                                      '9104', '9105', '9106', '9107']))
diseases.append(HCUPCodes('UncomplicatedDiverti', ['56211', '56213']))
diseases.append(HCUPCodes('NecrotizingSoftTissue', ['72886', '400']))
diseases.append(HCUPCodes('ComplicatedDiverti', ['5695'], 1, ['56211', '56213']))

# create complications present on arrival list
complications_POA = []
complications_POA.append(HCUPCodes('cv_failure_admiss', ['7855', '78550', '458', '4580', '45800']))
complications_POA.append(HCUPCodes('resp_fail_admis', ['967']))
complications_POA.append(HCUPCodes('neuro_fail_admiss', [
                         '3483', '3483', '293', '293', '3481', '3481']))
complications_POA.append(HCUPCodes('heme_fail_admiss', ['2874', '2874', '2875', '2875',
                                                        '2869', '2869', '2866', '2866']))
complications_POA.append(HCUPCodes('hepatic_fail_admiss', ['570', '5734', '5734']))
complications_POA.append(HCUPCodes('ARF_fail_admiss', ['584']))

# create complications not present on arrival list
complications_NOPOA = []
complications_NOPOA.append(HCUPCodes('pulm_failure', ['51881', '5184', '5185', '5188']))
complications_NOPOA.append(HCUPCodes('pna', ['481', '482', '483', '484', '485', '5070']))
complications_NOPOA.append(HCUPCodes('MI', ['410']))
complications_NOPOA.append(HCUPCodes('vte', ['4151', '45111', '45119', '4512', '45181', '4538']))
complications_NOPOA.append(HCUPCodes('arf', ['584']))
complications_NOPOA.append(HCUPCodes('ssi', ['9583', '9983', '9985', '99859', '99851']))
complications_NOPOA.append(HCUPCodes('gib', ["53082", "5310", "5311", "53120", "53121", "53140",
                                             "53141", "53160", "53161", "5320", "5321", "53220", "53221",
                                             "53240", "53241", "53260", "53261", "5330", "5331", "53320",
                                             "53321", "53340", "53341", "53360", "53361", "5340", "5341",
                                             "53420", "53421", "53440", "53441", "53460", "53461", "53501",
                                             "53511", "53521", "53531", "53541", "53551", "53561", "5789"]))
complications_NOPOA.append(HCUPCodes('hemorr', ['9981']))


def read_data(file):
    DATA = pd.read_csv(file)
    return DATA


def filter_columns(data, column_name, num_characters=0):
    '''
    Function to filter columns, with an option to limit the number of characters
    '''
    if(num_characters != 0):
        filter_col = [col for col in data if (col.startswith(
            column_name) and len(col) <= num_characters)]
        return(data[filter_col])
    else:
        filter_col = [col for col in data if (col.startswith(column_name))]
        return data[filter_col]


CITY = read_data('UT.csv')
data = filter_columns(CITY, 'dx', 4)
dx = list(data)


all_codes = []
for i in range(len(diseases)):
    for code in (diseases[i].codes):
        all_codes.append(code)


def row_handler(row):
    if(any(x in all_codes for x in row)):
        return 1
    return 0


print('Updating the hasDisease feature')

data['hasDisease'] = data.apply(row_handler, axis=1)


def add_columns(data, columns):
    for i in range(len(columns)):
        data[columns[i].name] = 0


add_columns(data, diseases)
add_columns(data, complications_POA)
add_columns(data, complications_NOPOA)
data['hasComplication'] = 0
data['isSurgeon'] = 0

filteredData = data[data['hasDisease'] == 1]

print('Coding the features for all diseases...')


def defineDiseaseFeatures(patient):  # ,diseases):
    for i in range(len(diseases)):
        if((any(x in diseases[i].codes for x in patient)) and (diseases[i].andFlag == 0)):
            # change 0 to 1 in the corresponding disease column for this patient
            patient[diseases[i].name] = 1
            patient['hasDisease'] = 1
        if((any(x in diseases[i].codes for x in patient)) and (diseases[i].andFlag == 1)):
            if(any(x in diseases[i].dependentCodes for x in patient)):
                # change 0 to 1 in the corresponding disease column for this patient
                patient[diseases[i].name] = 1
    return patient


def defineComplicationsFeatures(df, col_to_update, strings_to_search):
    for string in strings_to_search:
        mask = np.column_stack([df[col].str.startswith(string, na=False)
                                for col in dx]).any(axis=1)
        df[col_to_update] = np.where(mask, 1, df[col_to_update])
        df['hasComplication'] = np.where(mask, 1, df['hasComplication'])
    return df


def defineSurgeonFeatures(patient, surg_codes):
    if(any(x in surg_codes for x in patient[['mdspec1', 'mdspec2']])):
        patient['isSurgeon'] = 1
    return patient


filteredData = filteredData.apply(defineDiseaseFeatures, axis=1)

print('Coding the features for all complications...')


for i in range(len(complications_POA)):
    filteredData = defineComplicationsFeatures(
        filteredData, complications_POA[i].name, complications_POA[i].codes)
for i in range(len(complications_NOPOA)):
    filteredData = defineComplicationsFeatures(
        filteredData, complications_NOPOA[i].name, complications_NOPOA[i].codes)

allFeaturesWithDisease = CITY.iloc[filteredData.index]
final = pd.concat([filteredData, allFeaturesWithDisease], axis=1)

print('Coding the isSurgeon feature...')
surg_codes = ('ABS', 'CRS', 'FP/GS', 'FPS', 'GS', 'HS', 'HNS',
              'MFS', 'NS', 'OBG', 'OBS', 'OMS', 'ONS', 'ORS',
              'PDS', 'PDU', 'PRO', 'PS', 'PSF', 'SGO', 'SGO/N',
              'SGO/01', 'TS', 'U', 'US', 'VS')

final = final.apply(defineSurgeonFeatures, axis=1, surg_codes=surg_codes)

final.to_csv('filteredData.csv')
