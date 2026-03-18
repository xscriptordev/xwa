from sqlmodel import create_engine, Session

sqlite_url = "sqlite:///./xwa.db"

# connect_args={"check_same_thread": False} is needed only for SQLite
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session
