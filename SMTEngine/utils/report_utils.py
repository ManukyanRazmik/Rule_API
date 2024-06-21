import os
import pandas as pd

def process_inventory_data(base_path, inventory, keys, cols_to_report, id_column):
    ids = pd.DataFrame()
    
    for inv in inventory:
        file = inventory[inv]['file_name']
        data = pd.read_excel(os.path.join(base_path, file), usecols=keys + cols_to_report, dtype='object')
        data[cols_to_report] = data[cols_to_report].fillna('Missing')
        data = data.dropna(subset=id_column)
        rename_columns = {i: inventory[inv]['Mapping'][i]['Label'] for i in cols_to_report}
        data = data.rename(columns=rename_columns)
        ids = pd.concat([ids, data], axis=0)
    
    return ids.drop_duplicates()

def process_lab_data(base_path, lab, id_column, cols_to_report):
    result = pd.DataFrame()
    col_rename = {}
    samples = []
    
    for filename in lab:
        data = pd.read_csv(os.path.join(base_path, filename), usecols=id_column + cols_to_report, dtype='object', encoding='unicode_escape')
        renames_lab = {i: lab[filename]['Mapping'][i]['Label'] for i in cols_to_report}
        if not col_rename:
            col_rename = renames_lab
        elif renames_lab != col_rename:
            raise ValueError('Variable names are not the same')
        
        data = data.rename(columns=renames_lab)
        result = pd.concat([result, data], axis=0)
        samples.extend(lab[filename]['Samples'])
    
    return result.drop_duplicates(), col_rename, samples

def process_edc_data(base_path, edc_samples, id_column, cols_to_report):
    edc_data = pd.DataFrame()
    col_rename_edc = {}
    
    for edc in edc_samples:
        file_edc = edc['file_name']
        data = pd.read_sas(os.path.join(base_path, file_edc), encoding='utf-8')
        data = data[id_column + cols_to_report]
        data = data.dropna(subset=id_column)
        renames_edc = {i: edc['Mapping'][i]['Label'] for i in cols_to_report}
        if not col_rename_edc:
            col_rename_edc = renames_edc
        elif renames_edc != col_rename_edc:
            raise ValueError('Variable names are not the same')
        data = data.rename(columns=col_rename_edc)
        edc_data = pd.concat([edc_data, data], axis=0)
    
    return edc_data.drop_duplicates(), col_rename_edc
