from pydantic import BaseModel, Field, computed_field

# Request Information Models
class BasicInfo(BaseModel):
    name: str
    breed: str | None = None
    gender: str | None = None
    weight: float = Field(default= 1, description="weight should be given in pounds")
    height: float = Field(default= 1, description="height should be given in inches")
    age: int = Field(default= 1, description="age should be given in months")
    picture_url: str | None = None
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight*703/(self.height**2)
    # TODO Implement Body Score Condition BSC (This is breed Specific) and has many factors in it.
    
    
class RegularHealthCare(BaseModel):
    seeing_vet_more_than_12_months: bool
    reg_worming_treatment: bool
    dog_scratching: bool
    
    
class GutHealth(BaseModel):
    fishy_odor: bool
    upset_stomach_3month: bool
    scavenge_feaces: bool
    
    
class BoneHealth(BaseModel):
    stiff_getting_up: bool
    limp_lag_behind: bool
    mobility_issue: str
    activity_level_change: bool
    specific_movement_struggle: bool
  
    
class DentalHealth(BaseModel):
    no_brushing_2_months: bool
    dental_stiks: bool
    

# Response Model
    
    
class SkonaAssessment(BaseModel):
    name: str
    welcome_title: str
    welcome_message: str
    note: str
    bmi: float
    bmi_assessment: dict
    general_assessment: dict
    gut_health_assessment: dict
    bone_health_assessment: dict
    dental_health_assessment: dict
    final_assessment: dict
    nutritional_recommendation: dict
    
    


    
    
    