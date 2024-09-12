from app.models import models
from app.models import db_models


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
        

def start_process():
    print("Processing Request Started")
    # Check each health info in mongodb
    # for those present in mongodb fetch them and add them to response info.
    # if not present in mongodb send the info to AI processor and add the returned info to response info.
    # return response.