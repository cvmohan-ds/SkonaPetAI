import prompt_content

class Prompts:
    def __init__(self) -> None:
        pass
    
    def zero_shot_prompts(self) -> list:
        z_prompt = [{"role": "system", "content": prompt_content.zero_system_content_scooch},
                    {"role": "user", "content": prompt_content.zero_user_content}]
        return z_prompt
    
    def few_shot_prompts(self) -> list:
        fs_prompt = []
        return fs_prompt
    
    def chain_of_thoughts_prompts(self) -> list:
        cot_prompt = []
        return cot_prompt
    

if __name__ == "__main__":
    print("This is running as a standalone")
    
