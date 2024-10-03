from langchain_nvidia_ai_endpoints import ChatNVIDIA
from app.processors import ai_processor
import logging

class Orchestrater:
    
    def __init__(self) -> None:
        pass
    
    
async def get_started(prompts):
    logging.info(f"Number of prompts recieved: {len(prompts)}")
    print(f"Number of prompts recieved: {len(prompts)}")
    print(prompts.keys())
    client = ChatNVIDIA(
        model="nvidia/nemotron-4-340b-instruct",
        api_key="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", 
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024
    )
    responses_dict = {}
    for key, prompt in prompts.items():
        data = """ """

        for chunk in client.stream(prompt): 
            data += chunk.content
        # data_parts = data.split("{")[1].split(":")
        # assessment = data_parts[1].split('"')[1].strip()
        # reco = data_parts[2].split('"')[1].strip()
        data_parts = data.split("\n")
        for p in data_parts:
            if '"Assessment":' in p:
                assessment = p.split(":")[1].strip().strip('"')
                print(assessment)
            elif '"Recommendation":' in p:
                reco = p.split(":")[1].strip().strip('"')
                print(reco)
        assess_reco_dict = {"Assessment": assessment, "Recommendation": reco}
        responses_dict[key] = assess_reco_dict
    return responses_dict

    
