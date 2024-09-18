import os
from dotenv import load_dotenv
import logging

from app.commons.error import InternalError

# loading .env
load_dotenv()

class Config:
    version = "0.0.1"
    title = "SkonaAI"
    
    app_settings = {
        'db_name': os.getenv('MONGO_DB'),
        'mongo_uri': os.getenv('MONGO_URI'),
    }
    
    @classmethod
    def app_settings_validate(cls):
        for k, v in cls.app_settings.items():
            if None in v:
                logging.error(f'Config variable error. {k} cannot be None')
                raise InternalError([{"message": "Server configure error"}])
            else:
                logging.info(f'Config variable {k} is {v}')
    