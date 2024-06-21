import pandas as pd
from SMTEngine.utils.report_utils import process_inventory_data, process_lab_data, process_edc_data

def report_rule(js, base_path, cols_to_report, keys, id_column, sample_type):

    # Process Inventory data
    ids = process_inventory_data(base_path, js['datasets']['Inventory'], keys, cols_to_report, id_column)
    result = ids.drop_duplicates()

    # Process Lab data
    for lab in js['datasets']['Lab']:
        lab_data, col_rename, samples = process_lab_data(base_path, js['datasets']['Lab'][lab], id_column, cols_to_report)
        result = pd.merge(result, lab_data, on=id_column, how='left')
        result = result.drop_duplicates()
        result.loc[result[sample_type].isin(samples), list(col_rename.values())] = \
            result.loc[result[sample_type].isin(samples), list(col_rename.values())].fillna('Missing')

    # Process EDC data
    edc_data, col_rename_edc = process_edc_data(base_path, js['datasets']['EDC_sample'], id_column, cols_to_report)
    result = pd.merge(result, edc_data, on=id_column, how='left')
    result[list(col_rename_edc.values())] = result[list(col_rename_edc.values())].fillna('Missing')

    # Final data cleanup
    result = result.fillna('Not Available')

    return result
