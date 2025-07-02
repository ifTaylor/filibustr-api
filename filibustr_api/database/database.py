import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_password = os.getenv("DB_PASSWORD", "Bastian123")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")
        self.db_name = os.getenv("DB_NAME", "filibustr")

        self.database_url = (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        self.admin_database_url = (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/postgres"
        )

        self.engine = create_async_engine(self.database_url, echo=True)
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.Base = declarative_base()

    def ensure_database_exists(self):
        admin_engine = create_engine(self.admin_database_url, isolation_level="AUTOCOMMIT")
        with admin_engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": self.db_name},
            )
            if not result.scalar():
                print(f"[INFO] Creating database '{self.db_name}'...")
                conn.execute(text(f'CREATE DATABASE "{self.db_name}"'))
            else:
                print(f"[INFO] Database '{self.db_name}' already exists.")

    @staticmethod
    async def get_session() -> AsyncSession:
        async with db_manager.AsyncSessionLocal() as session:
            yield session

# Singleton instance
db_manager = DatabaseManager()
db_manager.ensure_database_exists()
