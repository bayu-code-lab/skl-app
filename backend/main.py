from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.routers.v1.auth import router as auth_router

# FastAPI settings
app = FastAPI(title=settings.PROJECT_NAME, version=settings.APP_VERSION)
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