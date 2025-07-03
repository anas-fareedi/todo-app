from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL="postgresql://tododb_dimv_user:FPvKnZIKBQ59HbfJANb8cKz2zNxHY4Ci@dpg-d1j2p5h5pdvs73cnqsd0-a.oregon-postgres.render.com/tododb_dimv"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
