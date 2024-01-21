import os
from fastapi import FastAPI
from routers import organisations, donations
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Cryptocurrency donation API",
    description="Cryptocurrency donation Application Programmable Interface",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Joel KUMWENDA",
        "url": "http://https://github.com/jkumwenda/",
        "email": "jkumwenda@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    os.getenv("CLIENT_ORIGIN"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    organisations.router, tags=["Organisations"], prefix="/organisations"
)
app.include_router(donations.router, tags=["Donations"], prefix="/donations")
