from app.models.models import SkonaAssessment
from app.ai import prompt_content as prompts
from app.ai import llm_orchestration as llm


class AIProcessor:
    def __init__(self, assessment_data: dict) -> None:
        self.assessment_data = assessment_data
    
    async def start_process(self):
        print("Processing Request Started")
        # Format the information recieved.
        # pet_info = self.assessment_data.pet_info
        # Need to check if we have any assessment missing
        # Based on the assessment we need to grab the prompt and add information to it
        # These prompts are stored in a dict 
        prompts_dict = {}
        for key, value in self.assessment_data.items():
            if key == "general_assessment":
                reg_assess_pr = prompts.gen_assess_recos.format(answer(value["seeing_vet_more_than_12_months"]), 
                                                                answer(value["reg_worming_treatment"]), 
                                                                answer(value["dog_scratching"]))
                reg_assess_pr += prompts.output_instructions
                prompts_dict["general_assessment"] = reg_assess_pr
            elif key == "gut_health_assessment":
                gut_assess_pr = prompts.gut_assess_recos.format(answer(value["fishy_odor"]), 
                                                                answer(value["upset_stomach_3month"]), 
                                                                answer(value["scavenge_feaces"]))
                gut_assess_pr += prompts.output_instructions
                prompts_dict["gut_health_assessment"] = gut_assess_pr
            elif key == "bone_health_assessment":
                bone_assess_pr = prompts.bone_assess_recos.format(answer(value["stiff_getting_up"]), 
                                                                answer(value["limp_lag_behind"]), 
                                                                value["mobility_issue"], 
                                                                answer(value["activity_level_change"]), 
                                                                answer(value["specific_movement_struggle"]))
                bone_assess_pr += prompts.output_instructions
                prompts_dict["bone_health_assessment"] = bone_assess_pr
            elif key == "dental_health_assessment":
                dental_assess_pr = prompts.dental_assess_recos.format(answer(value["no_brushing_2_months"]), 
                                                                answer(value["dental_stiks"]))
                dental_assess_pr += prompts.output_instructions
                prompts_dict["dental_health_assessment"] = dental_assess_pr
            elif key == "bmi_info":
                bmi_assess_pr = prompts.bmi_assess_recos.format(value["name"], value["gender"], value["breed"], 
                                                                value["weight"], value["height"], value["age"], value["bmi"])
                bmi_assess_pr += prompts.output_instructions
                prompts_dict["bmi_info"] = bmi_assess_pr
            elif key == "nutritional_recommendation":
                nutrition_assess_pr = prompts.nutritional_assess_recos.format(answer(value["seeing_vet_more_than_12_months"]), 
                                                                answer(value["reg_worming_treatment"]), 
                                                                answer(value["dog_scratching"]),
                                                                answer(value["no_brushing_2_months"]), 
                                                                answer(value["dental_stiks"]),
                                                                answer(value["fishy_odor"]), 
                                                                answer(value["upset_stomach_3month"]), 
                                                                answer(value["scavenge_feaces"]),
                                                                answer(value["stiff_getting_up"]), 
                                                                answer(value["limp_lag_behind"]), 
                                                                value["mobility_issue"], 
                                                                answer(value["activity_level_change"]), 
                                                                answer(value["specific_movement_struggle"])
                                                                )
                nutrition_assess_pr += prompts.output_instructions
                prompts_dict["nutritional_recommendation"] = nutrition_assess_pr
            elif key == "final_assessment":
                fa_assess_pr = prompts.final_health_assess_recos.format(answer(value["seeing_vet_more_than_12_months"]), 
                                                                answer(value["reg_worming_treatment"]), 
                                                                answer(value["dog_scratching"]),
                                                                answer(value["no_brushing_2_months"]), 
                                                                answer(value["dental_stiks"]),
                                                                answer(value["fishy_odor"]), 
                                                                answer(value["upset_stomach_3month"]), 
                                                                answer(value["scavenge_feaces"]),
                                                                answer(value["stiff_getting_up"]), 
                                                                answer(value["limp_lag_behind"]), 
                                                                value["mobility_issue"], 
                                                                answer(value["activity_level_change"]), 
                                                                answer(value["specific_movement_struggle"])
                                                                )
                fa_assess_pr += prompts.output_instructions
                prompts_dict["final_assessment"] = fa_assess_pr
        
        # call llm orchestrator 
        # send the prompts to llm orchestrator and get back the responses
        resps_dict = await llm.get_started(prompts_dict)
        # To fit the db models send back the response.
        return resps_dict

def answer(boolean_value):
    if boolean_value:
        return "Yes"
    else:
        return "No"