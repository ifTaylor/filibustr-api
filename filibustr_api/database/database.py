import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise ValueError("DATABASE_URL is not set")

        self.engine = create_async_engine(self.database_url, echo=True)
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.Base = declarative_base()

    def ensure_database_exists(self):
        try:
            parsed = urlparse(self.database_url)
            db_name = self._extract_db_name(parsed)

            # Build admin connection URL (sync)
            admin_url = self._build_admin_url(parsed)
            admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

            with admin_engine.connect() as conn:
                result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": db_name})
                if not result.scalar():
                    print(f"[INFO] Creating database '{db_name}'...")
                    conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                else:
                    print(f"[INFO] Database '{db_name}' already exists.")
        except Exception as e:
            print(f"[WARN] Could not ensure database exists: {e}")

    def _extract_db_name(self, parsed_url) -> str:
        return parsed_url.path.lstrip("/").split("?")[0]

    def _build_admin_url(self, parsed_url) -> str:
        # Strip "+asyncpg" and override database with "postgres"
        scheme = parsed_url.scheme.replace("+asyncpg", "")
        netloc = parsed_url.netloc
        return f"{scheme}://{netloc}/postgres"

    @staticmethod
    async def get_session() -> AsyncSession:
        async with db_manager.AsyncSessionLocal() as session:
            yield session

# Singleton instance
db_manager = DatabaseManager()

def init_database():
    db_manager.ensure_database_exists()
