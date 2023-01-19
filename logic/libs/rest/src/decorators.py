from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from logic.libs.exception.exception import AppException, UnknownException
from logic.libs.logger.logger import logger


def add_decorators(app: FastAPI):
    """
    Carga el handler de error basico para manejo de AppExceptions y excepciones comunes
    """
    @app.exception_handler(AppException)
    def handle_business_exception(request, ae: AppException):
        logger.warning(ae.to_json())
        return JSONResponse(ae.to_json(), 409)

    @app.exception_handler(Exception)
    def handle_exception(request, e: Exception):
        logger.exception(e)
        return JSONResponse(UnknownException(e).to_json(), 500)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
