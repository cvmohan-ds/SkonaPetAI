import sys
sys.path.append('/Users/sailaja/code/Skona')
from app.models import db_models as mdm
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import random




async def init_db():
    db_name = "skona"
    mongo_uri = "mongodb+srv://vamsi:KastaluBalavantudikeVastai11@testingmongo.lythz.mongodb.net/"
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
    r_int = random.randint(0, len(gut_health_info.assess_recos) - 1)
    only_3 = gut_health_info.assess_recos[r_int]
    print(only_3)
    return gut_health_info

async def get_final_reco_with_nutrition(search_data):
    final_reco_with_nutrition = await mdm.FinalRecoWithNutrition.find_one(mdm.FinalRecoWithNutrition.regular_health_info == search_data.regular_health_info, 
                                                                            mdm.FinalRecoWithNutrition.gut_health_info == search_data.gut_health_info, 
                                                                            mdm.FinalRecoWithNutrition.bone_health_info == search_data.bone_health_info, 
                                                                            mdm.FinalRecoWithNutrition.dental_health_info == search_data.dental_health_info)
    x = final_reco_with_nutrition.assess_recos[random.randint(0, len(final_reco_with_nutrition.assess_recos) - 1)]
    print(type(x))
    print(x.model_dump())
    return final_reco_with_nutrition

async def get_nutrition_info(search_data):
    nutrition_reco = await mdm.FinalRecoWithNutrition.find_one(mdm.FinalRecoWithNutrition.regular_health_info == search_data.regular_health_info, 
                                                                            mdm.FinalRecoWithNutrition.gut_health_info == search_data.gut_health_info, 
                                                                            mdm.FinalRecoWithNutrition.bone_health_info == search_data.bone_health_info, 
                                                                            mdm.FinalRecoWithNutrition.dental_health_info == search_data.dental_health_info)
    if nutrition_reco:
        x = nutrition_reco.nutritional_assessment[random.randint(0, len(nutrition_reco.nutritional_assessment) - 1)]
        print(x)
    else:
        print(type(nutrition_reco))

if __name__ == "__main__":
    print("This is running as a standalone")
    async def main():
        await init_db()
        gut_info = mdm.GutHealth(fishy_odor=False, upset_stomach_3month=True, scavenge_feaces=False)
        reg_info = mdm.RegularHealth(seeing_vet_more_than_12_months=True, reg_worming_treatment=False, dog_scratching=False)
        dental_info= mdm.DentalHealth(no_brushing_2_months=True, dental_stiks=True)
        bone_info = mdm.BoneHealth(stiff_getting_up=True, limp_lag_behind=False, mobility_issue="Recent(more than 3 months ago)", activity_level_change=False, specific_movement_struggle=False)
        search_info = mdm.FinalSearchCriteria(regular_health_info=reg_info, gut_health_info=gut_info, bone_health_info=bone_info, dental_health_info=dental_info)
        #db_data = await get_gut_health_info(search_data=search_info)
        #print(db_data)
        db_data = await get_nutrition_info(search_data=search_info)
        #print(db_data)
    import asyncio
    asyncio.run(main())