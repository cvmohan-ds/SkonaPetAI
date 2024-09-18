from fastapi import APIRouter, Depends
from app.models import models
from app.processors.request_processor import RequestProcessor


router = APIRouter()

@router.get("/assessment/", tags=["Assessment"])
async def pet_assessment(basic: models.BasicInfo, regular_health: models.RegularHealthCare, 
                         gut_health: models.GutHealth, bone_health: models.BoneHealth, 
                         dental_health: models.DentalHealth) -> models.SkonaAssessment:
    
    # Call the request processor to process the request and get back the response.
    return RequestProcessor(basic, regular_health, gut_health, bone_health, dental_health).start_process()



    