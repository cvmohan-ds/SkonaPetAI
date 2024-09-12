from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Annotated


class NutritionalAssessment(BaseModel):
    assessment: str
    recommendations: str
    snacks_recommended: list[str] | None = None
    
class AssessmentWithRecos(BaseModel):
    assessment: str
    recommendations: str
    
class Recos(BaseModel):
    title: str
    total_health_score: float | None = None
    health_based_recos: str
    final_nutritional_reco: str
    snacks_recommended: list[str]

class GutHealthAssessment(Document):
    fishy_odor: bool
    upset_stomach_3month: bool
    scavenge_feaces: bool
    assess_recos: list[AssessmentWithRecos]
    nutritional_info: NutritionalAssessment | None = None
    
class BoneHealthAssessment(Document):
    stiff_getting_up: bool
    limp_lag_behind: bool
    mobility_issue: Annotated[str, Indexed()]
    activity_level_change: bool
    specific_movement_struggle: bool
    assess_recos: list[AssessmentWithRecos]
    nutritional_info: NutritionalAssessment | None = None
    
class DentalHealthAssessment(Document):
    no_brushing_2_months: bool
    dental_stiks: bool
    assess_recos: list[AssessmentWithRecos]
    nutritional_info: NutritionalAssessment | None = None
    
class RegularHealthCareAssessment(Document):
    seeing_vet_more_than_12_months: bool
    reg_worming_treatment: bool
    dog_scratching: bool
    assess_recos: list[AssessmentWithRecos]
    nutritional_info: NutritionalAssessment | None = None
    
class PetInfo(Document):
    name: str
    breed: Annotated[str, Indexed()] 
    gender: Annotated[str, Indexed()] 
    weight: Annotated[float, Indexed()] 
    height: Annotated[float, Indexed()]
    age: Annotated[int, Indexed()]
    picture_url: str | None
    recos: Recos
    
