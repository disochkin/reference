import sqlite3

from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

path = "database.db"
engine = create_engine(f"sqlite:///{path}", echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db = SessionLocal()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        print("проверяем, что это SQLite")
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()