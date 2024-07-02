from fastapi import FastAPI
import uvicorn
from SMTEngine.Rules.Report import report_rule
from SMTEngine.Rules.Compare import comperison_rule, comp_data_processing
from SMTEngine.Models.RuleModels import RuleModel
import yaml

app = FastAPI()

with open(r'config/key_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

@app.post("/rules/")
async def rules(rule_json : RuleModel):
        
    content = rule_json.model_dump()
    
    base_path = content['basepath']
    keys = config['keys_sample']
    id_column = config['id_column_sample']
    sample_type =  config['sample_type']
    
    if content['rule']['type'] == 'Report':
        cols_to_report = content['rule']['Variable']

        if 'EDC_Subject' in cols_to_report:
            keys = config['keys_subject']
            id_column = config['id_column_subject']       
        
        result = report_rule(content, base_path, cols_to_report, keys, id_column, sample_type)
        
               
    elif content['rule']['type'] == 'Compare':        
        
        comp = {content['rule']['comp_variable']['Source'] : content['rule']['comp_variable']['Variable_name']}
        ref = {i['Source']:i['Variable_name'] for i in content['rule']['ref_variable']}

        if ('EDC_Subject' in comp.keys() or
            'EDC_Subject' in ref.keys()):
            keys = config['keys_subject']
            id_column = config['id_column_subject']  
            
        fad, comp_cols, ref_cols = comp_data_processing(path=base_path, 
                                                        comperator=comp, 
                                                        reference=ref, 
                                                        main_keys=keys, 
                                                        id_column=id_column, 
                                                        sample_type=sample_type, 
                                                        content = content)
        
        result = comperison_rule(data=fad, 
                                 comp_cols=comp_cols, 
                                 ref_cols=ref_cols, 
                                rule_js=content['rule'])       
        
        
    return result.to_dict()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)