# tables.py
from database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"))

class RoleTable(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), nullable=False)

