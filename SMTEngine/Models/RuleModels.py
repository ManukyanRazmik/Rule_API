from pydantic import BaseModel
from typing import Dict, Any, List, Union

class MappingItem(BaseModel):
    Label: str
    Native_Name: str
    

class SampleItem(BaseModel):
    file_name: str
    Mapping: Dict[str, MappingItem]
    Samples: List[str]

class LabData(BaseModel):
    Mapping: Dict[str, MappingItem]
    Samples: List[str]

class InventoryData(BaseModel):
    file_name: str
    Mapping: Dict[str, MappingItem]
    Samples: List[str]


class RuleVariableData(BaseModel):
    Source: str
    Variable_name: List[str]

class ReportRuleData(BaseModel):
    type: str
    Variable: List[str]

class CompareRuleData(BaseModel):
    type: str
    data_type: str
    comp_variable: RuleVariableData
    ref_variable: List[RuleVariableData]
    Sign: str

class Datasets(BaseModel):
    EDC_subject: List[SampleItem]
    EDC_sample: List[SampleItem]
    Lab: Dict[str, Dict[str, LabData]]
    Inventory: Dict[str, InventoryData]

class RuleModel(BaseModel):
    basepath: str
    datasets: Datasets
    rule: Union[ReportRuleData, CompareRuleData]