from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from backend.core.config import settings
from backend.routers.v1.auth_route import router as auth_router
from backend.routers.v1.master.user_route import router as user_router

# FastAPI settings
app = FastAPI(title=settings.PROJECT_NAME, version=settings.APP_VERSION)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={ "code": 422, "error": [{"field_name": item["loc"][1], "msg": item["msg"]} for item in exc._errors],},
    )

# CORS settings
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth_router)
app.include_router(user_router)

@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(
#     request: Request, exc: StarletteHTTPException
# ):
#     logging.error(exc)
#     return JSONResponse(content=exc.detail, status_code=exc.status_code)


# @app.exception_handler(Exception)
# async def unhandled_exception(request: Request, exc: Exception):
#     logging.error(exc)
#     return JSONResponse(
#         status_code=500,
#         content={"message": "Server error", "code": 500, "data": None},
#     )

@app.get("/", tags=["Ping Endpoint"])
async def ping():
    """
    Route for alb
    """
    return {"status": status.HTTP_200_OK}