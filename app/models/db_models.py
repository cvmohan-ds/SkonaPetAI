from beanie import Document, Indexed
from pydantic import BaseModel
from typing import Annotated



    
class AssessmentWithRecos(BaseModel):
    assessment: str
    recommendations: str
    def __hash__(self) -> int:
        return hash((self.assessment, self.recommendations))
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, AssessmentWithRecos):
            return self.assessment == value.assessment and self.recommendations == value.recommendations
        return False
    
class NutritionalAssessment(AssessmentWithRecos):
    snacks_recommended: list[str] | None = None
    
class Recos(BaseModel):
    title: str
    total_health_score: float | None = None
    health_based_recos: str
    final_nutritional_reco: str
    snacks_recommended: list[str]
    

class RegularHealth(BaseModel):
    seeing_vet_more_than_12_months: bool
    reg_worming_treatment: bool
    dog_scratching: bool
    
    def __hash__(self) -> int:
        return hash((self.seeing_vet_more_than_12_months, self.reg_worming_treatment, self.dog_scratching))
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, RegularHealth):
            return self.seeing_vet_more_than_12_months == value.seeing_vet_more_than_12_months and self.reg_worming_treatment == value.reg_worming_treatment and self.dog_scratching == value.dog_scratching
        return False
    

class GutHealth(BaseModel):
    fishy_odor: bool
    upset_stomach_3month: bool
    scavenge_feaces: bool
    
    def __hash__(self) -> int:
        return hash((self.fishy_odor, self.upset_stomach_3month, self.scavenge_feaces))
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, GutHealth):
            return self.fishy_odor == value.fishy_odor and self.upset_stomach_3month == value.upset_stomach_3month and self.scavenge_feaces == value.scavenge_feaces
        return False
    
    
class BoneHealth(BaseModel):
    stiff_getting_up: bool
    limp_lag_behind: bool
    mobility_issue: Annotated[str, Indexed()]
    activity_level_change: bool
    specific_movement_struggle: bool
    
    def __hash__(self) -> int:
        return hash((self.stiff_getting_up, self.limp_lag_behind, self.mobility_issue, self.activity_level_change, self.specific_movement_struggle))
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, BoneHealth):
            part_resp =  self.stiff_getting_up == value.stiff_getting_up and self.limp_lag_behind == value.limp_lag_behind and self.activity_level_change == value.activity_level_change and self.specific_movement_struggle == value.specific_movement_struggle
            if "less than a month" in value.mobility_issue.lower() and "less than a month" in self.mobility_issue.lower() and part_resp:
                return True
            elif "more than a month" in value.mobility_issue.lower() and "more than a month" in self.mobility_issue.lower() and part_resp:
                return True
            elif "more than 3 months" in value.mobility_issue.lower() and "more than 3 months" in self.mobility_issue.lower() and part_resp:
                return True
            
        return False
    

class DentalHealth(BaseModel):
    no_brushing_2_months: bool
    dental_stiks: bool
    
    def __hash__(self) -> int:
        return hash((self.no_brushing_2_months, self.dental_stiks))
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, DentalHealth):
            return self.no_brushing_2_months == value.no_brushing_2_months and self.dental_stiks == value.dental_stiks
        return False
    

class FinalSearchCriteria(BaseModel):
    regular_health_info: RegularHealth
    gut_health_info: GutHealth
    bone_health_info: BoneHealth
    dental_health_info: DentalHealth
    
    def __hash__(self) -> int:
        return hash((self.regular_health_info, self.gut_health_info, self.bone_health_info, self.dental_health_info))

    def __eq__(self, value: object) -> bool:
        if isinstance(value, FinalSearchCriteria):
            return self.regular_health_info == value.regular_health_info and self.gut_health_info == value.gut_health_info and self.bone_health_info == value.bone_health_info and self.dental_health_info == value.dental_health_info
        return False
    



class GutHealthAssessment(Document):
    gut_health_info: GutHealth
    assess_recos: list[AssessmentWithRecos]
    
    
class BoneHealthAssessment(Document):
    bone_health_info: BoneHealth
    assess_recos: list[AssessmentWithRecos]
    
    
class DentalHealthAssessment(Document):
    dental_health_info: DentalHealth
    assess_recos: list[AssessmentWithRecos]
 
    
class RegularHealthCareAssessment(Document):
    regular_health_info: RegularHealth
    assess_recos: list[AssessmentWithRecos]


class FinalRecoWithNutrition(Document):
    regular_health_info: RegularHealth
    gut_health_info: GutHealth
    bone_health_info: BoneHealth
    dental_health_info: DentalHealth
    assess_recos: list[AssessmentWithRecos]
    nutritional_assessment: list[NutritionalAssessment]
    
    
    
class PetInfo(Document):
    name: str
    breed: Annotated[str, Indexed()] 
    gender: Annotated[str, Indexed()] 
    weight: Annotated[float, Indexed()] 
    height: Annotated[float, Indexed()]
    age: Annotated[int, Indexed()]
    picture_url: str | None
    bmi: float
    
    
