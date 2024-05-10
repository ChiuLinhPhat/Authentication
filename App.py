from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from loguru import logger
from fastapi.staticfiles import StaticFiles
from Settings.config import Settings
from starlette.middleware.cors import CORSMiddleware
import os
import sentry_sdk
import Template

# from API.Routers.Router import router as auth_router
current_dir = os.path.dirname(os.path.abspath(__file__))
Settings = Settings()
templates = Jinja2Templates(directory=os.path.join(current_dir, "Template"))
if Settings.SENTRY_DSN and Settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(Settings.SENTRY_DSN), enable_tracing=True)
app = FastAPI(
    title=Settings.PROJECT_NAME,
    openapi_url=f"{Settings.API_V1_STR}/openapi.json",
    # generate_unique_id_function=custom_generate_unique_id,
)
if Settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in Settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount("/Template/image", StaticFiles(directory=os.path.join(current_dir, "Template/image")), name="image")
app.mount("/Template", StaticFiles(directory=os.path.join(current_dir, "Template")), name="")


@app.on_event("startup")
async def create_db_client():
    try:
        create_engine(str(Settings.SQLALCHEMY_DATABASE_URI))
        logger.info("Successfully connected to Sql database")
    except Exception as e:
        logger.error(e)
        logger.error("An error occurred while connecting to Sql database.")


@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
