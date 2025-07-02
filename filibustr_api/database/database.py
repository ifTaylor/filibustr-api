import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.is_dev = os.getenv("DEV", "false").lower() == "true"
        self.database_url = os.getenv("DATABASE_URL")
        self.admin_database_url = os.getenv("ADMIN_DATABASE_URL") if self.is_dev else None

        if not self.database_url:
            raise ValueError("DATABASE_URL is required.")

        self.engine = create_async_engine(self.database_url, echo=True)
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.Base = declarative_base()

    def ensure_database_exists(self):
        if not self.is_dev:
            print("[INFO] Skipping ensure_database_exists() in production mode")
            return

        if not self.admin_database_url:
            print("[WARN] ADMIN_DATABASE_URL is not set. Skipping.")
            return

        try:
            admin_engine = create_engine(self.admin_database_url, isolation_level="AUTOCOMMIT")
            with admin_engine.connect() as conn:
                db_name = self._extract_db_name(self.database_url)
                result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": db_name})
                if not result.scalar():
                    print(f"[INFO] Creating database '{db_name}'...")
                    conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                else:
                    print(f"[INFO] Database '{db_name}' already exists.")
        except Exception as e:
            print(f"[WARN] Could not connect to admin DB: {e}")

    def _extract_db_name(self, url: str) -> str:
        return url.rsplit("/", 1)[-1].split("?")[0]

    @staticmethod
    async def get_session() -> AsyncSession:
        async with db_manager.AsyncSessionLocal() as session:
            yield session

# Singleton instance
db_manager = DatabaseManager()

def init_database():
    db_manager.ensure_database_exists()
