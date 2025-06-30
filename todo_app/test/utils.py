from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from todo_app.database import Base
from todo_app.main import app
from fastapi.testclient import TestClient
import pytest
from todo_app.models import Todos,Users
from todo_app.routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread':False},
    poolclass=StaticPool
)

TestingSessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username':'anas','id':1,'user_role':'admin'}



client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title = "learn to code",
        description = "need to learn",
        priority = 5,
        complete=False,
        owner_id=1,
    )
    
    db = TestingSessionlocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM TODOS;"))
        connection.commit()
        
   
@pytest.fixture
def test_user():
    user = Users(
        username="my-name",
        email = "code@gmail.com",
        first_name = "anas",
        last_name = "bhai",
        hashed_password = bcrypt_context.hash("test1234"),
        role = "admin",
        phone_number = "1234567890"
    )  
    db = TestingSessionlocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()