import pandas as pd
def read_inventory_data(path, content, main_keys, id_column, inv_cols_comp = None, inv_cols_ref = None):
    """Function to read inventory data for compare rule

    Args:
        path (str): base directory for datasets
        content (dict): content of inventory related data (part of request json)
        inv_cols_comp (list): list of variables to compare
        inv_cols_ref (list): list of variables to reference
        main_keys (list): list of main variables (keys)
        id_column (list): list of id column

    Returns:
        dataframe: dataframe of processed inventory data
    """
    file = content['file_name']

    data = pd.read_excel('\\'.join([path, file]), usecols=main_keys + inv_cols_comp + inv_cols_ref) # !!SHOULD BE CSV
    data = data.dropna(subset=id_column)
    data[inv_cols_comp + inv_cols_ref] = data[inv_cols_comp + inv_cols_ref].fillna('Missing')

    if inv_cols_comp:
        renames_inv_comp = {i: content['Mapping'][i]['Label'] for i in inv_cols_comp}
        data = data.rename(columns=renames_inv_comp)
        comp_cols = list(renames_inv_comp.values())
    else:
        comp_cols = []

    if inv_cols_ref:
        renames_ref = {i: content['Mapping'][i]['Label'] for i in inv_cols_ref}
        data = data.rename(columns=renames_ref)
        ref_cols = list(renames_ref.values())
    else:
        ref_cols = []

    return data, comp_cols, ref_cols

def read_lab_data(path, content, lab_cols_comp, lab_cols_ref, id_column):
    """Function to read laboratory data for compare rule

    Args:
        path (stt): base directory for datasets
        content (dict): content of lab related data (part of request json)
        lab_cols_comp (list): list of variables to compare
        lab_cols_ref (list): list of variables to reference
        id_column (list): list of id column

    Raises:
        ValueError: Incorrect variable names

    Returns:
        dataframe: dataframe of processed laboratory data
    """
    
    
    lab_data = pd.DataFrame()
    col_rename_lab_comp = {}
    col_rename_lab_ref = {}
    samples = []

    for filename in content:

        data = pd.read_csv('\\'.join([path, filename]), usecols=id_column + lab_cols_comp + lab_cols_ref, encoding='unicode_escape')

        if lab_cols_comp:
            renames_lab_comp = {i: content[filename]['Mapping'][i]['Label'] for i in lab_cols_comp}
            if not col_rename_lab_comp:
                col_rename_lab_comp = renames_lab_comp
            elif renames_lab_comp != col_rename_lab_comp:
                raise ValueError('Variable names are not the same')
            data = data.rename(columns=col_rename_lab_comp)

        if lab_cols_ref:
            renames_lab_ref = {i: content[filename]['Mapping'][i]['Label'] for i in lab_cols_ref}
            if not col_rename_lab_ref:
                col_rename_lab_ref = renames_lab_ref
            elif renames_lab_ref != col_rename_lab_ref:
                raise ValueError('Variable names are not the same')
            data = data.rename(columns=col_rename_lab_ref)

        lab_data = pd.concat([lab_data, data], axis=0)
        samples.extend(content[filename]['Samples'])

    return lab_data.drop_duplicates(), list(col_rename_lab_comp.values()), list(col_rename_lab_ref.values()), samples


def read_edc_data(path, edc_samples, edc_cols_comp, edc_cols_ref, id_column):
    """Function to read EDC data for compare rule

    Args:
        path (str): base directory for datasets
        edc_samples (list): list of EDC related data (part of request json)
        edc_cols_comp (list): list of variables to compare
        edc_cols_ref (list): list of variables to reference
        id_column (list): list of id column

    Raises:
        ValueError: Incorrect variable names

    Returns:
        dataframe: dataframe of processed EDC data
    """
    edc_data = pd.DataFrame()
    
    col_rename_edc_comp = {}
    col_rename_edc_ref = {}

    for edc in edc_samples:
        file_edc = edc['file_name']
        data = pd.read_sas('\\'.join([path, file_edc]), encoding='utf-8')  # SHOULD BE CSV
        data = data[id_column +  edc_cols_comp + edc_cols_ref]
        data = data.dropna(subset=id_column)

        if edc_cols_comp:
            
            renames_edc_comp = {i: edc['Mapping'][i]['Label'] for i in edc_cols_comp}
            if not col_rename_edc_comp:
                col_rename_edc_comp = renames_edc_comp
            elif renames_edc_comp != col_rename_edc_comp:
                raise ValueError('Variable names are not the same')
            data = data.rename(columns=col_rename_edc_comp)

        if edc_cols_ref:
            
            renames_edc_ref = {i: edc['Mapping'][i]['Label'] for i in edc_cols_ref}
            if not col_rename_edc_ref:
                col_rename_edc_ref = renames_edc_ref
            elif renames_edc_ref != col_rename_edc_ref:
                raise ValueError('Variable names are not the same')
            data = data.rename(columns=col_rename_edc_ref)

        edc_data = pd.concat([edc_data, data], axis=0)

    return edc_data.drop_duplicates(), list(col_rename_edc_comp.values()), list(col_rename_edc_ref.values())