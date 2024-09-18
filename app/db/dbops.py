from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv

from app.models import db_models as mdm
from app.conf import config as cfg

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
                                                mdm.PetInfo])
    

# Get information based on request recieved.
async def get_gut_health_info(search_data):
    pass

async def get_bone_health_info(search_data):
    pass

async def get_dental_health_info(search_data):
    pass

async def get_regular_health_info(search_data):
    pass

async def get_pet_info(search_data):
    pass


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
