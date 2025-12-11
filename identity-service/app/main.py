from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers.auth import auth_router

app = FastAPI()

app.include_router(
    prefix="/auth",
    router=auth_router
)

# @app.exception_handler(Exception)
# def handle_generic_exceptions(request: Request, exc: Exception):
#     if exc.args.
#     return JSONResponse()