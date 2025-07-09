import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from filibustr_api.endpoints.bills import router as bills_router
from filibustr_api.endpoints.users import router as users_router
from filibustr_api.endpoints.forum import router as forum_router
from filibustr_api.database.database import db_manager, init_database
from filibustr_api.libraries.orm_base import Base

# Optional DB creation on startup
if os.getenv("AUTO_CREATE_DB", "false").lower() == "true":
    init_database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with db_manager.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"[WARN] Could not initialize schema: {e}")
    yield


app = FastAPI(title="Filibustr API", lifespan=lifespan)

origins = [
    "https://www.filibustr.com",
    "https://filibustr.com",
    "https://filibustr-ui.vercel.app",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=bills_router,
    prefix="/api/bills",
    tags=["Bills"]
)

app.include_router(
    router=users_router,
    prefix="/api/users",
    tags=["Users"]
)

app.include_router(
    router=forum_router,
    prefix="/api/forum",
    tags=["Forum"]
)
