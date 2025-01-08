import os

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine  # noqa: F401

db_file_name: str = "database.sqlite"
db_file_dir: str = "assets"


if not os.path.exists(db_file_dir):
    os.makedirs(db_file_dir)


db_path: str = os.path.join(db_file_dir, db_file_name)
db_uri: str = f"sqlite:///{db_path}"
db_engine: Engine = create_engine(db_uri, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)
