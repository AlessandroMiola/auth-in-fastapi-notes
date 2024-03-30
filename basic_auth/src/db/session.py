from sqlmodel import Session, create_engine

from config import settings

DATABASE_URL = settings.database_url
engine = create_engine(url=DATABASE_URL, echo=True)


def get_session() -> Session:
    with Session(engine) as session:
        yield session