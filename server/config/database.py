from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

db_file_path: str = "/assets/database.sqlite"
db_uri: str = f"sqlite://{db_file_path}"
db_engine: Engine = create_engine(db_uri)

SQLModel.metadata.create_all(db_engine, echo=True)
