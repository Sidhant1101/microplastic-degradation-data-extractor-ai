from typing import Optional
from pydantic import BaseModel,ConfigDict,Field
class Endpoint(BaseModel):
    model_config=ConfigDict(extra='ignore'); endpoint_type:Optional[str]=None; value:Optional[float]=None; unit:Optional[str]=None; measurement_method:Optional[str]=None; evidence:Optional[str]=None; page:Optional[int]=None
class Experiment(BaseModel):
    model_config=ConfigDict(extra='ignore'); polymer:Optional[str]=None; polymer_form:Optional[str]=None; particle_size:Optional[str]=None; treatment_category:Optional[str]=None; treatment_specific:Optional[str]=None; catalyst_reagent:Optional[str]=None; temperature_c:Optional[float]=None; pH:Optional[float]=None; duration_h:Optional[float]=None; initial_mass_mg:Optional[float]=None; final_mass_mg:Optional[float]=None; endpoints:list[Endpoint]=Field(default_factory=list); evidence:Optional[str]=None; page:Optional[int]=None; table_or_figure:Optional[str]=None
class ExtractionResult(BaseModel):
    model_config=ConfigDict(extra='ignore'); experiments:list[Experiment]=Field(default_factory=list)
