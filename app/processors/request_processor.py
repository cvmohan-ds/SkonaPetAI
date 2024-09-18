from app.models import models
from app.models import db_models
from app.db import dbops
from app.processors.ai_processor import AIProcessor




class RequestProcessor:
    def __init__( self, 
                 basic_info: models.BasicInfo, 
                 regular_health_care: models.RegularHealthCare, 
                 gut_health: models.GutHealth, 
                 bone_health: models.BoneHealth, 
                 dental_health: models.DentalHealth) -> None:
        self.basic_info = basic_info
        self.regular_health_care = regular_health_care
        self.gut_health = gut_health
        self.bone_health = bone_health
        self.dental_health = dental_health
        

def start_process(self):
    print("Processing Request Started")
    # Check each health info in mongodb
    db_reg_health = dbops.get_regular_health_info(self.regular_health_care)
    db_gut_health = dbops.get_gut_health_info(self.gut_health)
    db_bone_health = dbops.get_bone_health_info(self.bone_health)
    db_dental_health = dbops.get_dental_health_info(self.dental_health)
    db_pet_info = dbops.get_pet_info(self.basic_info)
    # for those present in mongodb add them to response info.
    response = models.SkonaAssessment()
    if db_reg_health:
        response.general_assessment = db_reg_health
    if db_gut_health:
        response.gut_health_assessment = db_gut_health
    if db_bone_health:
        response.bone_health_assessment = db_bone_health
    if db_dental_health:
        response.dental_health_assessment = db_dental_health
    if db_pet_info:
        response.pet_info = db_pet_info
    # if not present in mongodb send the info to AI processor and add the returned info to response info.
    if not db_reg_health or not db_gut_health or not db_bone_health or not db_dental_health or not db_pet_info:
        AIProcessor(response).start_process()
    return response
    