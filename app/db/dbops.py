from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
import random

from app.models import db_models as mdm
from app.conf.config import Config as cfg

load_dotenv()

async def init_db():
    db_name = cfg.app_settings['db_name']
    mongo_uri = cfg.app_settings['mongo_uri']
    db_client = AsyncIOMotorClient(mongo_uri)
    db = db_client[db_name]
    await init_beanie(
        database=db, document_models=[mdm.GutHealthAssessment, 
                                                mdm.BoneHealthAssessment, 
                                                mdm.DentalHealthAssessment, 
                                                mdm.RegularHealthCareAssessment,
                                                mdm.FinalRecoWithNutrition, 
                                                mdm.PetInfo])
    

# Get information based on request recieved.
async def get_gut_health_info(search_data):
    gut_health_info = await mdm.GutHealthAssessment.find_one(mdm.GutHealthAssessment.gut_health_info == search_data)
    if gut_health_info and gut_health_info.assess_recos:
        rand_assess_reco = gut_health_info.assess_recos[random.randint(0, len(gut_health_info.assess_recos) - 1)]
    else:
        rand_assess_reco = None
    return rand_assess_reco


async def get_bone_health_info(search_data):
    bone_health_info = await mdm.BoneHealthAssessment.find_one(mdm.BoneHealthAssessment.bone_health_info == search_data)
    if bone_health_info and bone_health_info.assess_recos:
        rand_assess_reco = bone_health_info.assess_recos[random.randint(0, len(bone_health_info.assess_recos) - 1)]
    else:
        rand_assess_reco = None
    return rand_assess_reco


async def get_dental_health_info(search_data):
    dental_health_info = await mdm.DentalHealthAssessment.find_one(mdm.DentalHealthAssessment.dental_health_info == search_data)
    if dental_health_info and dental_health_info.assess_recos:
        rand_assess_reco = dental_health_info.assess_recos[random.randint(0, len(dental_health_info.assess_recos) - 1)]
    else:
        rand_assess_reco = None
    return rand_assess_reco



async def get_regular_health_info(search_data):
    regular_health_info = await mdm.RegularHealthCareAssessment.find_one(mdm.RegularHealthCareAssessment.regular_health_info == search_data)
    if regular_health_info and regular_health_info.assess_recos:
        rand_assess_reco = regular_health_info.assess_recos[random.randint(0, len(regular_health_info.assess_recos) - 1)]
    else:
        rand_assess_reco = None
    return rand_assess_reco

async def get_final_reco_with_nutrition(search_data):
    final_reco_with_nutrition = await mdm.FinalRecoWithNutrition.find_one(mdm.FinalRecoWithNutrition.regular_health_info == search_data.regular_health_info, 
                                                                            mdm.FinalRecoWithNutrition.gut_health_info == search_data.gut_health_info, 
                                                                            mdm.FinalRecoWithNutrition.bone_health_info == search_data.bone_health_info, 
                                                                            mdm.FinalRecoWithNutrition.dental_health_info == search_data.dental_health_info)
    if final_reco_with_nutrition:
        return final_reco_with_nutrition.assess_recos[random.randint(0, len(final_reco_with_nutrition.assess_recos) - 1)]
    else:
        return None

async def get_nutrition_info(search_data):
    nutrition_reco = await mdm.FinalRecoWithNutrition.find_one(mdm.FinalRecoWithNutrition.regular_health_info == search_data.regular_health_info, 
                                                                            mdm.FinalRecoWithNutrition.gut_health_info == search_data.gut_health_info, 
                                                                            mdm.FinalRecoWithNutrition.bone_health_info == search_data.bone_health_info, 
                                                                            mdm.FinalRecoWithNutrition.dental_health_info == search_data.dental_health_info)
    if nutrition_reco:
        return nutrition_reco.nutritional_assessment[random.randint(0, len(nutrition_reco.nutritional_assessment) - 1)]
    else:
        return None

async def get_pet_info(search_data):
    pet_info = await mdm.PetInfo.find_one(mdm.PetInfo.name == search_data.name)
    return pet_info




# Insert data generated from llms
async def insert_gut_health_info():
    pass

async def insert_bone_health_info():
    pass

async def insert_dental_health_info():
    pass

async def insert_regular_health_info():
    pass

async def insert_pet_info():
    pass


# update data with different and new formats of assessments and recommendations
async def update_gut_health_info():
    pass

async def update_bone_health_info():
    pass

async def update_dental_health_info():
    pass

async def update_regular_health_info():
    pass

async def update_pet_info():
    pass
