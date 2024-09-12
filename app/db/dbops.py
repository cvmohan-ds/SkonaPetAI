from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models import db_models as mdm

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.skona, document_models=[mdm.GutHealthAssessment, 
                                                mdm.BoneHealthAssessment, 
                                                mdm.DentalHealthAssessment, 
                                                mdm.RegularHealthCareAssessment, 
                                                mdm.PetInfo])
    

# Get information based on request recieved.
async def get_gut_health_info():
    pass

async def get_bone_health_info():
    pass

async def get_dental_health_info():
    pass

async def get_regular_health_info():
    pass

async def get_pet_info():
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
