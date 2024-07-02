import os
import pandas as pd

def process_inventory_data(base_path, inventory, keys, cols_to_report, id_column):
    """Function to process inventory data for report rule.

    Args:
        base_path (str): base directory for datasets
        inventory (dict): dictionary for inventory related data (part of request json)
        keys (list): list of keys for inventory
        cols_to_report (list): list of columns to report
        id_column (list): list containing id column

    Returns:
        dataframe: datafrme of processed inventory data
    """
    ids = pd.DataFrame()
    
    for inv in inventory:
        file = inventory[inv]['file_name']
        data = pd.read_excel(os.path.join(base_path, file), usecols=keys + cols_to_report, dtype='object') # !!SHOULD BE CHANGED TO CSV IN PROD
        data[cols_to_report] = data[cols_to_report].fillna('Missing')
        data = data.dropna(subset=id_column)
        rename_columns = {i: inventory[inv]['Mapping'][i]['Label'] for i in cols_to_report}
        data = data.rename(columns=rename_columns)
        ids = pd.concat([ids, data], axis=0)
    
    return ids.drop_duplicates()

def process_lab_data(base_path, lab, id_column, cols_to_report):
    """Function to process Laboratory data for report rule.

    Args:
        base_path (str): base directory for datasets
        lab (dict): dictionary for laboratory related data (part of request json)
        cols_to_report (list): list of columns to report
        id_column (list): list containing id column
        
    Raises:
        ValueError: Incorrect variable names

    Returns:
        dataframe: datafrme of processed laboratory data
    """
        
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
    """Function to process EDC data for report rule.

    Args:
        base_path (str): base directory for datasets
        edc_samples (list): list of EDC related data (part of request json)
        cols_to_report (list): list of columns to report
        id_column (list): list containing id column

     Raises:
        ValueError: Incorrect variable names

    Returns:
        dataframe: datafrme of processed EDC data
    """
    edc_data = pd.DataFrame()
    col_rename_edc = {}
    
    for edc in edc_samples:
        file_edc = edc['file_name']
        data = pd.read_sas(os.path.join(base_path, file_edc), encoding='utf-8')  #!! SHOULD BE CSV IN PROD
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