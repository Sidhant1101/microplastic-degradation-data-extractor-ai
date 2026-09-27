from typing import Optional, List, Literal
from pydantic import BaseModel, Field

ValueType = Literal["reported", "calculated", "digitized_from_figure", "inferred", "unknown"]

class Evidence(BaseModel):
    page: Optional[int] = None
    section: Optional[str] = None
    table: Optional[str] = None
    figure: Optional[str] = None
    text: Optional[str] = None
    confidence: float = Field(default=0.0, ge=0, le=1)

class Endpoint(BaseModel):
    endpoint_type: str
    value: Optional[float] = None
    unit: Optional[str] = None
    measurement_method: Optional[str] = None
    value_type: ValueType = "unknown"
    evidence: Optional[Evidence] = None

class Experiment(BaseModel):
    polymer: Optional[str] = None
    polymer_subtype: Optional[str] = None
    particle_size_min_um: Optional[float] = None
    particle_size_max_um: Optional[float] = None
    particle_shape: Optional[str] = None
    treatment_category: Optional[str] = None
    treatment_specific: Optional[str] = None
    catalyst: Optional[str] = None
    catalyst_concentration: Optional[float] = None
    catalyst_concentration_unit: Optional[str] = None
    temperature_c: Optional[float] = None
    pH: Optional[float] = None
    duration_h: Optional[float] = None
    initial_mass_mg: Optional[float] = None
    final_mass_mg: Optional[float] = None
    endpoints: List[Endpoint] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)

class ExtractionResult(BaseModel):
    paper_title: Optional[str] = None
    doi: Optional[str] = None
    experiments: List[Experiment] = Field(default_factory=list)
    extraction_notes: List[str] = Field(default_factory=list)
