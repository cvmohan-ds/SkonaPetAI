from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

from app.commons.error import BadRequest, UnprocessableError
from app.db.dbops import init_db
from app.conf.logging import setup_logging
from app.api import assess_pet as pet


# Logging
setup_logging()
# app
app = FastAPI(dependencies= [Depends(init_db)])



# HTTP error responses
@app.exception_handler(BadRequest)
async def bad_request_handler(req: Request, exc: BadRequest) -> JSONResponse:
    return exc.gen_err_resp()


@app.exception_handler(RequestValidationError)
async def invalid_req_handler(
    req: Request,
    exc: RequestValidationError
) -> JSONResponse:
    logging.error(f'Request invalid. {str(exc)}')
    return JSONResponse(
        status_code=400,
        content={
            "type": "about:blank",
            'title': 'Bad Request',
            'status': 400,
            'detail': [str(exc)]
        }
    )

@app.exception_handler(UnprocessableError)
async def unprocessable_error_handler(
    req: Request,
    exc: UnprocessableError
) -> JSONResponse:
    return exc.gen_err_resp()

# API Paths
app.include_router(pet.router)

@app.get("/")
async def root():
    return {"message": "Hello from Skona AI!"}


