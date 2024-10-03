import nbformat
import json
import re
import sys
import os
sys.path.append('/Users/sailaja/code/Skona')
from app.models import db_models as mdm
from app.utils import mod_utility as mu


from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

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

class LoadData:
    def __init__(self, data_dir, is_notebook=True) -> None:
        self.data_dir = data_dir
        self.is_notebook = is_notebook
    
    
    async def start_loading(self):
        await init_db()
        db_models = {}
        db_models["reg"] = []
        db_models["gut"] = []
        db_models["bone"] = []
        db_models["dental"] = []
        db_models["final"] = []
        files = os.listdir(self.data_dir)
        for f in files:
            if f != "data.ipynb":
                continue
            final_db_insert_data = await self.process_list_of_jsons(db_models, os.path.join(self.data_dir, f))
            # Access the mongodb and insert the data
            for key, value in final_db_insert_data.items():
                if key == "reg":
                    await mdm.RegularHealthCareAssessment.insert_many(value)
                elif key == "gut":
                    await mdm.GutHealthAssessment.insert_many(value)
                elif key == "bone":
                    await mdm.BoneHealthAssessment.insert_many(value)
                elif key == "dental":
                    await mdm.DentalHealthAssessment.insert_many(value)
                elif key == "final":
                    await mdm.FinalRecoWithNutrition.insert_many(value)
        
        
    
    async def process_list_of_jsons(self, db_models, f_path):
        if self.is_notebook:
            json_data = await parse_notebooks_for_jsons(f_path)
        else:
            json_data = await parse_jsons(f_path)
        # Get the scrubbed data for loading for futher proessing
        for each_json in json_data:
            reg_health_info, gut_health_info, bone_health_info, dental_health_info, final_reco_with_nutrition = scrub_dicts_for_models(each_json)
            db_models["reg"].append(reg_health_info)
            db_models["gut"].append(gut_health_info)
            db_models["bone"].append(bone_health_info)
            db_models["dental"].append(dental_health_info)
            db_models["final"].append(final_reco_with_nutrition)
        db_insert_data = db_model_consolidation(db_models)
        return db_insert_data

    
        
    
        

# loading jsons directly
async def parse_jsons(json_file):
    json_data = []
    with open(json_file, 'r') as f:
        json_data.append(json.load(f))
    return json_data

# Loading notebooks for getting the jsons
async def parse_notebooks_for_jsons(notebook_file):
    json_data = []
    try:
        with open(notebook_file, 'r') as f:
            nb = nbformat.read(f, as_version=4)
            cno = 0
            for cell in nb.cells:
                cno += 1
                if cell.cell_type == 'code':
                    try:
                        cell_data = format_to_json(cell.source)
                        json_cell_data = json.loads(cell_data)
                        json_data.append(json_cell_data)
                    except json.JSONDecodeError as jerr:
                        print(f"Not a valid json cell number : {cno}, error : {jerr} \n cell_data : {cell_data[:300]}")
                        break
    except Exception as e:
        print(f"The exception is {e} for file {notebook_file}")
        raise Exception(e)
    return json_data

def format_to_json(data):
    if '"""' in data:
        start = data.find('"""') + 3
        end = data.find('"""', start)
        docstring = data[start:end]
        docstring = re.sub(f'\\s+', ' ', docstring)
        new_docstring = re.sub(r'[\r\n]', ';', docstring)
        new_docstring = docstring.replace("\n", " ")
        new_docstring = docstring.replace("Gut", ";Gut").replace("Bone", ";Bone").replace("Dental", ";Dental")
        data = data[:start] + new_docstring + data[end:]
        data = data.replace('"""', '"')
    else:
        print("No docstring found")
    return data

# Scrubbing Dictionnaries and loading into model classes
def scrub_dicts_for_models(dict_data: dict):
    # parse and understand the metadata.
    reg_health, gut_health, bone_health, dental_health = normalize_metadata(dict_data['metadata'])
    # for each healthcare get the list and consolidate.
    reg_assess_recos, gut_assess_recos, bone_assess_recos, dental_assess_recos, total_nutrition_list, total_assessment_list = normalize_assessments_recommendations(dict_data)
    # Form the db models
    reg_health_assessment = mdm.RegularHealthCareAssessment(regular_health_info=reg_health, assess_recos=reg_assess_recos)
    gut_health_assessment = mdm.GutHealthAssessment(gut_health_info=gut_health, assess_recos=gut_assess_recos)
    bone_health_assessment = mdm.BoneHealthAssessment(bone_health_info=bone_health, assess_recos=bone_assess_recos)
    dental_health_assessment = mdm.DentalHealthAssessment(dental_health_info=dental_health, assess_recos=dental_assess_recos)
    final_reco_with_nutrition = mdm.FinalRecoWithNutrition(regular_health_info=reg_health, gut_health_info=gut_health, bone_health_info=bone_health, dental_health_info=dental_health,
                                                            assess_recos=total_assessment_list, nutritional_assessment=total_nutrition_list)
    return reg_health_assessment, gut_health_assessment, bone_health_assessment, dental_health_assessment, final_reco_with_nutrition



# Normalizing the metadata to model classes
def normalize_metadata(metadata: str):
    meta_scubbed = {}
    meta_parts = metadata.split(";")
    for part in meta_parts:
        p_split = part.split("--")
        category = p_split[0].strip()
        answers_string = p_split[1].strip().lstrip("(").rstrip(")")
        answers = answers_string.split(",")
        meta_scubbed[category] = answers
    reg_health = None
    gut_health = None
    bone_health = None
    dental_health = None
    for key, value in meta_scubbed.items():
        if "Regular" in key:
            seeing_vet_more_than_12_months = True if value[0].lower() == "yes" else False
            reg_worming_treatment = True if value[1].lower() == "yes" else False
            dog_scratching = True if value[2].lower() == "yes" else False
            reg_health = mdm.RegularHealth(seeing_vet_more_than_12_months=seeing_vet_more_than_12_months,
                                            reg_worming_treatment=reg_worming_treatment,
                                            dog_scratching=dog_scratching)
        elif "Gut" in key:
            fishy_odor = True if value[0].lower() == "yes" else False
            upset_stomach_3month = True if value[1].lower() == "yes" else False
            scavenge_feaces = True if value[2].lower() == "yes" else False
            gut_health = mdm.GutHealth(fishy_odor=fishy_odor,
                                        upset_stomach_3month=upset_stomach_3month,
                                        scavenge_feaces=scavenge_feaces)
        elif "Bone" in key:
            stiff_getting_up = True if value[0].lower() == "yes" else False
            limp_lag_behind = True if value[1].lower() == "yes" else False
            mobility_issue = value[2]
            activity_level_change = True if value[3].lower() == "yes" else False
            specific_movement_struggle = True if value[4].lower() == "yes" else False
            bone_health = mdm.BoneHealth(stiff_getting_up=stiff_getting_up,
                                        limp_lag_behind=limp_lag_behind,
                                        mobility_issue=mobility_issue,
                                        activity_level_change=activity_level_change,
                                        specific_movement_struggle=specific_movement_struggle)
        elif "Dental" in key:
            no_brushing_2_months = True if value[0].lower() == "yes" else False
            dental_stiks = True if value[1].lower() == "yes" else False
            dental_health = mdm.DentalHealth(no_brushing_2_months=no_brushing_2_months,
                                            dental_stiks=dental_stiks)
        else:
            raise ValueError("Do not recognize the category")

    return reg_health, gut_health, bone_health, dental_health



# Normalize assessments and recommendations into models
def normalize_assessments_recommendations(data):
    reg_assess_list = []
    gut_assess_list = []
    bone_assess_list = []
    dental_assess_list = []
    total_nutrition_list = []
    total_assessment_list = []
    for key, value in data.items():
        if "Regular" in key:
            for ele in value:
                reg_assess_list.append(create_assess_reco_model(ele))
        elif "Gut" in key:
            for ele in value:
                gut_assess_list.append(create_assess_reco_model(ele))
        elif "Bone" in key:
            for ele in value:
                bone_assess_list.append(create_assess_reco_model(ele))
        elif "Dental" in key:
            for ele in value:
                dental_assess_list.append(create_assess_reco_model(ele))
        elif "Nutrition" in key:
            if type(value) == list:
                for ele in value:
                    total_nutrition_list.append(create_nutrtional_assessment(ele))
            elif type(value) == dict:
                total_nutrition_list.append(create_nutrtional_assessment(value))
        elif "Final" in key:
            if type(value) == list:
                for ele in value:
                    total_assessment_list.append(create_assess_reco_model(ele))
            elif type(value) == dict:
                total_assessment_list.append(create_assess_reco_model(value))
    
    return reg_assess_list, gut_assess_list, bone_assess_list, dental_assess_list, total_nutrition_list, total_assessment_list


def create_assess_reco_model(info: dict):
    assessment = ""
    recommendation = ""
    for key, value in info.items():
        if "Assess" in key:
            assessment = value
        elif "Reco" in key:
            if type(value) == list:
                for e in value:
                    recommendation += e + "\n"
            else:
                recommendation = value
    return mdm.AssessmentWithRecos(assessment=assessment, recommendations=recommendation)

def create_nutrtional_assessment(info: dict):
    assessment = ""
    recommendation = ""
    for key, value in info.items():
        if "Assess" in key:
            assessment = value
        elif "Reco" in key:
            if type(value) == list:
                for e in value:
                    recommendation += e + "\n"
            else:
                recommendation = value
    snacks_recommendation = []
    return mdm.NutritionalAssessment(assessment=assessment, recommendations=recommendation, snacks_recommended=snacks_recommendation)




def db_model_consolidation(db_models: dict):
    final_db_insert_data = {}
    for key, value in db_models.items():
        if key == "reg":
            db_data = mu.create_reg_health_instances()
            db_ready_models = []
            for element in db_data:
                temp_list = []
                for v in value:
                    if v.regular_health_info == element:
                        temp_list.extend(v.assess_recos)
                ar_unique = list(set(temp_list))
                db_ready_models.append(mdm.RegularHealthCareAssessment(regular_health_info=element, assess_recos=ar_unique))
            final_db_insert_data[key] = db_ready_models
                
        elif key == "gut":
            db_data = mu.create_gut_health_instances()
            db_ready_models = []
            for element in db_data:
                temp_list = []
                for v in value:
                    if v.gut_health_info == element:
                        temp_list.extend(v.assess_recos)
                ar_unique = list(set(temp_list))
                db_ready_models.append(mdm.GutHealthAssessment(gut_health_info=element, assess_recos=ar_unique))
            final_db_insert_data[key] = db_ready_models
        elif key == "bone":
            db_data = mu.create_bone_health_instances()
            db_ready_models = []
            for element in db_data:
                temp_list = []
                for v in value:
                    if v.bone_health_info == element:
                        temp_list.extend(v.assess_recos)
                ar_unique = list(set(temp_list))
                db_ready_models.append(mdm.BoneHealthAssessment(bone_health_info=element, assess_recos=ar_unique))
            final_db_insert_data[key] = db_ready_models
        elif key == "dental":
            db_data = mu.create_dental_health_instances()
            db_ready_models = []
            for element in db_data:
                temp_list = []
                for v in value:
                    if v.dental_health_info == element:
                        temp_list.extend(v.assess_recos)
                ar_unique = list(set(temp_list))
                db_ready_models.append(mdm.DentalHealthAssessment(dental_health_info=element, assess_recos=ar_unique))
            final_db_insert_data[key] = db_ready_models
        elif key == "final":
            final_db_insert_data[key] = value
    
    return final_db_insert_data





if __name__ == "__main__":
    print("This is running as a standalone")
    # json_data = parse_notebooks_for_jsons("/Users/sailaja/code/data/Skona/Project_3.ipynb")
    async def main():
        
        load_data = LoadData("/Users/sailaja/code/data/Skona/", is_notebook=True)
        await load_data.start_loading()
    asyncio.run(main())
    print("Done")