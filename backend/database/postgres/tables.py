from .connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


# noinspection SpellCheckingInspection
class UserTable(Base):
    """
    Represents the 'users' table in a database.

    This class defines the schema for the 'users' table, including its columns and
    relationships with other tables. It is used to map database rows to Python objects
    and vice versa, leveraging SQLAlchemy for database operations.

    Attributes:
        __tablename__ (str): The name of the database table being represented.
        id (Integer): The primary key of the users table. Automatically indexed.
        username (String): The username of the user. Must be non-null and has a max
            length of 50 characters.
        password (String): The encrypted password of the user. Must be non-null and
            has a max length of 60 characters.
        phone_number (String): The phone number of the user. Must be unique, can be
            null, and has a max length of 15 characters.
        role_id (Integer): A foreign key reference to the id column of the roles table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    api_key = Column(String(60), unique=True, nullable=True)

# noinspection SpellCheckingInspection
class RoleTable(Base):
    """
    Represents the Role table in the database.

    This class maps to the 'roles' table in the database and is used to store
    information regarding different roles. Each role is uniquely identified
    by an id and has a label associated with it. It provides the ORM mapping
    facilities for interacting with the database table.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(50), nullable=False)

# noinspection SpellCheckingInspection
class TimesheetTable(Base):
    """

    """
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # machine_id = Column(Integer, ForeignKey("machines.id"))
    machine_name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

