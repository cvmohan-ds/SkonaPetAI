from app.models import models
from app.models import db_models as mdm
from app.db import dbops
from app.processors.ai_processor import AIProcessor
from app.utils import statics as st
import random






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
        

    async def start_process(self):
        print("Processing Request Started")
        # Check each health info in mongodb
        reg_search, gut_search, bone_search, dental_search, pet_search, final_info_search = create_db_models(self.regular_health_care, self.gut_health, self.bone_health, self.dental_health, self.basic_info)
        reg_assess_recos = await dbops.get_regular_health_info(reg_search)
        gut_assess_recos = await dbops.get_gut_health_info(gut_search)
        bone_assess_recos = await dbops.get_bone_health_info(bone_search)
        dental_assess_recos = await dbops.get_dental_health_info(dental_search)
        final_recos = await dbops.get_final_reco_with_nutrition(final_info_search)
        nutritional_recos = await dbops.get_nutrition_info(final_info_search)
        # for those present in mongodb add them to response info.
        # From Basic Information populate name and BMI
        
        # We have Static Welcome title and message
        r_int = random.randint(0, len(st.WELCOME_MESSAGES) - 1)
        welcome_message = format_welcome_message(st.WELCOME_MESSAGES[r_int], self.basic_info.gender, self.basic_info.name, r_int)
        
        # BMI Assessment will come from LLM
        ai_dict = {}
        db_dict = {}
        # General Assessment to nutritition recommendation are taken from mongodb if exist else the LLM
        if reg_assess_recos:
            db_dict["general_assessment"] = reg_assess_recos.model_dump()
        else:
            ai_dict["general_assessment"] = reg_search.model_dump()
        if gut_assess_recos:
            db_dict["gut_health_assessment"] = gut_assess_recos.model_dump()
        else:
            ai_dict["gut_health_assessment"] = gut_search.model_dump()
        if bone_assess_recos:
            db_dict["bone_health_assessment"] = bone_assess_recos.model_dump()
        else:
            ai_dict["bone_health_assessment"] = bone_search.model_dump()
        if dental_assess_recos:
            db_dict["dental_health_assessment"] = dental_assess_recos.model_dump()
        else:
            ai_dict["dental_health_assessment"] = dental_search.model_dump()
        if final_recos:
            db_dict["final_assessment"] = final_recos.model_dump()
        else:
            ai_dict["final_assessment"] = create_final_assess_search_dict(final_info_search)
        if nutritional_recos:
            db_dict["nutritional_recommendation"] = nutritional_recos.model_dump()
        else:
            ai_dict["nutritional_recommendation"] = create_final_assess_search_dict(final_info_search)
        ai_dict["bmi_info"] = pet_search.model_dump()
        # if not present in mongodb send the info to AI processor and add the returned info to response info.
        resps_dict = await AIProcessor(ai_dict).start_process()
        # Create the Response Pydantic model to send back
        resps_dict.update(db_dict)
        print("response dict keys that we have are ", resps_dict.keys())
        resp = models.SkonaAssessment(name=self.basic_info.name, welcome_title=st.WELCOME_TITLE, 
                                    welcome_message=welcome_message, note=st.NOTE, bmi=self.basic_info.bmi,
                                    bmi_assessment=resps_dict["bmi_info"], general_assessment=resps_dict["general_assessment"],
                                    gut_health_assessment=resps_dict["gut_health_assessment"],bone_health_assessment=resps_dict["bone_health_assessment"],
                                    dental_health_assessment=resps_dict["dental_health_assessment"], final_assessment=resps_dict["final_assessment"],
                                    nutritional_recommendation=resps_dict["nutritional_recommendation"])
        return resp
    

def create_db_models(reg_health, gut_health, bone_health, dental_health, pet_info):
    reg_db = mdm.RegularHealth(seeing_vet_more_than_12_months=reg_health.seeing_vet_more_than_12_months,
                               reg_worming_treatment=reg_health.reg_worming_treatment,
                               dog_scratching=reg_health.dog_scratching)
    gut_db = mdm.GutHealth(fishy_odor=gut_health.fishy_odor,
                            upset_stomach_3month=gut_health.upset_stomach_3month,
                            scavenge_feaces=gut_health.scavenge_feaces)
    bone_db = mdm.BoneHealth(stiff_getting_up=bone_health.stiff_getting_up, limp_lag_behind=bone_health.limp_lag_behind,
                            mobility_issue=bone_health.mobility_issue, activity_level_change=bone_health.activity_level_change,
                            specific_movement_struggle=bone_health.specific_movement_struggle)
    dental_db = mdm.DentalHealth(no_brushing_2_months=dental_health.no_brushing_2_months, dental_stiks=dental_health.dental_stiks)
    pet_db = mdm.PetInfo(name=pet_info.name, breed=pet_info.breed, gender=pet_info.gender, weight=pet_info.weight,
                        height=pet_info.height, age=pet_info.age, picture_url=pet_info.picture_url, bmi=pet_info.bmi)
    
    final_db = mdm.FinalSearchCriteria(regular_health_info=reg_db, gut_health_info=gut_db, bone_health_info=bone_db, dental_health_info=dental_db)
    return reg_db, gut_db, bone_db, dental_db, pet_db, final_db


def format_welcome_message(welcome_message, gender, name, r_int):
    if gender == "male":
        title = "his"
        pronoun = "he"
        we_call = "boy"
    else:
        title = "her"
        pronoun = "she"
        we_call = "girl"
    if r_int == 0:
        formatted_welcome_message = welcome_message.format(name, name, title)
    elif r_int == 1:
        formatted_welcome_message = welcome_message.format(name, we_call, pronoun)
    elif r_int == 2:
        formatted_welcome_message = welcome_message.format(name, name, title)
    elif r_int == 3:
        formatted_welcome_message = welcome_message.format(name, we_call)
    return formatted_welcome_message

def create_final_assess_search_dict(info: mdm.FinalSearchCriteria):
    search_criteria = {}
    reg = info.regular_health_info.model_dump()
    dental= info.dental_health_info.model_dump()
    bone = info.bone_health_info.model_dump()
    gut = info.gut_health_info.model_dump()
    search_criteria.update(reg)
    search_criteria.update(dental)
    search_criteria.update(bone)
    search_criteria.update(gut)
    return search_criteria
    