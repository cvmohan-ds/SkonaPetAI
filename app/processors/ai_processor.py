from app.models.models import SkonaAssessment

class AIProcessor:
    def __init__(self, assessment_data: SkonaAssessment) -> None:
        self.assessment_data = assessment_data
    
    def start_process(self):
        print("Processing Request Started")
        # Format the information recieved.
        # Format the prompt as needed.
        # call llm orchestrator 
        # the json sent back is processed to fit the db models and send back the response.