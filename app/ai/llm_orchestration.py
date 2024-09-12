from langchain_nvidia_ai_endpoints import ChatNVIDIA
from prompts import Prompts

class Orchestrater:
    
    def __init__(self) -> None:
        pass
    
    
def get_started():
    client = ChatNVIDIA(
        model="meta/llama-3.1-8b-instruct",
        api_key="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",
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024
    )
    data = """ """
    skona_prompt = Prompts().zero_shot_prompts()

    for chunk in client.stream(skona_prompt): 
        data += chunk
    return data


print(get_started())
    
