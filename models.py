from sqlalchemy import Column, Integer, String, Enum, DateTime, TIMESTAMP, func, ForeignKey
from mysql_workbench import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(Enum("admin", "editor", "viewer"), nullable=False)
    api_key = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class BookLog(Base):
    __tablename__ = "book_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    user_id = Column(Integer)