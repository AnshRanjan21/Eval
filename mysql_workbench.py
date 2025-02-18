from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#MYSQL_WORKBENCH_DATABASE_URL = "mysql+pymysql://root:password123@localhost/api_logs"
MYSQL_WORKBENCH_DATABASE_URL = os.getenv("MYSQL_WORKBENCH_DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(MYSQL_WORKBENCH_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()