import pandas as pd
from SMTEngine.utils.compare_utils import read_inventory_data, read_lab_data, read_edc_data


def comp_data_processing(path, comperator, reference, main_keys, id_column, sample_type, content):
    
    comp_cols = []
    ref_cols = []
    
    inv_cols_comp = comperator.get('Inventory', [])
    inv_cols_ref = reference.get('Inventory', [])
    
    result = pd.DataFrame()
    for inv_content in content['datasets']['Inventory'].values():
        data_inv = read_inventory_data(path, inv_content, inv_cols_comp, inv_cols_ref,main_keys,  id_column)
        result = pd.concat([result, data_inv[0]], axis = 0)
        comp_cols.extend(data_inv[1])
        ref_cols.extend(data_inv[2])
        
    result = result.drop_duplicates()
    
    lab_cols_comp = comperator.get('Lab', [])
    lab_cols_ref = reference.get('Lab', [])
    
    for lab_content in content['datasets']['Lab'].values():
        lab_data = read_lab_data(path, lab_content, lab_cols_comp, lab_cols_ref, id_column)
        result = pd.merge(result, lab_data[0], on=id_column, how='left')
        result = result.drop_duplicates()
        result.loc[result[sample_type].isin(lab_data[3]), lab_data[1] + lab_data[2]] = \
                result.loc[result[sample_type].isin(lab_data[3]), lab_data[1] + lab_data[2]].fillna('Missing')
        comp_cols.extend(lab_data[1])
        ref_cols.extend(lab_data[2])
    
    
    edc_cols_comp = comperator.get('EDC', [])
    edc_cols_ref = reference.get('EDC', [])
    
    if edc_cols_comp + edc_cols_ref:
        edc_content = content['datasets']['EDC_sample']
        data_edc = read_edc_data(path, edc_content, edc_cols_comp, edc_cols_ref, id_column)
        result = pd.merge(result, data_edc[0], on=id_column, how='left')
        result[data_edc[1] + data_edc[2]] = result[data_edc[1] + data_edc[2]].fillna('Missing')
        comp_cols.extend(data_edc[1])
        ref_cols.extend(data_edc[2])

    return result, comp_cols, ref_cols




def comperison_rule(data, comp_cols, ref_cols, rule_js):
    mask = (data[comp_cols + ref_cols] == 'Missing').any(axis = 1)
    data['Flag'] = ''
    data['Issues'] = [[]] * len(data)
    
    data.loc[mask, 'Flag'] = 'Missing'
    data.loc[mask, 'Issues'] = (data.loc[mask, comp_cols + ref_cols] == 'Missing').apply(lambda x: list(x.index[x]), axis = 1)
    
    for refer in comp_cols:
        mask1 = data[refer].notnull()
        for j in ref_cols:        
            mask2 = (data['Flag'] != "Missing") & data[j].notnull()
            if rule_js['data_type'] == 'date':
                cast = ".astype('datetime64[ns]')"
            elif rule_js['data_type'] == 'number':
                cast = ".astype('float')"
            else:
                cast = ".astype('str')"
            mask_result = eval(f"(data.loc[mask1 & mask2, refer]){cast} {rule_js['Sign']}(data.loc[mask1 & mask2, j]){cast}")
            data.loc[mask1 & mask2 & ~mask_result, 'Issues'] = data.loc[mask1 & mask2 & ~mask_result].apply(lambda x: x['Issues'] + [j], axis = 1)
            data.loc[mask1 & mask2 & ~mask_result, 'Flag'] = False
    data['Issues'] = data['Issues'].apply(lambda x: ', '.join(x))
    
    return data.fillna('Not Available')