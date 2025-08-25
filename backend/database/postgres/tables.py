from sqlalchemy import (
    Column, String, BigInteger, Boolean, Date, ForeignKey, TIMESTAMP,
    func, Index, Text, Time
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TimesheetTable(Base):
    __tablename__ = "timesheets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    # Core activity details
    machine = Column(String(100))  # e.g. Machine name / ID
    description = Column(Text, nullable=False)
    remark = Column(Text)
    # Tracking & Review
    reviewed_by = Column(BigInteger, ForeignKey("users.user_id"))  # another user (admin/manager)
    status = Column(String(50), default="Pending")  # Pending, Approved, Rejected
    # Time tracking
    date = Column(Date, nullable=False)  # Work date
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    # Meta
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("UserTable", foreign_keys=[user_id], back_populates="timesheets")
    reviewer = relationship("UserTable", foreign_keys=[reviewed_by])

# -----------------------
# 1. Users
# -----------------------
class UserTable(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    dob = Column(Date)
    gender = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    account = relationship("UserAccount", back_populates="user", uselist=False)
    emails = relationship("UserEmail", back_populates="user", cascade="all, delete-orphan")
    phone_numbers = relationship("UserPhoneNumber", back_populates="user", cascade="all, delete-orphan")
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")
    timesheets = relationship("TimesheetTable", foreign_keys=[TimesheetTable.user_id], back_populates="user", cascade="all, delete-orphan")

# -----------------------
# 2. User Accounts (for login + roles)
# -----------------------
class UserAccount(Base):
    __tablename__ = "user_accounts"

    account_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    api_key = Column(String(60), nullable=True)
    role = Column(String(50), nullable=False)  # e.g., "Admin", "User", "SuperAdmin"
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationship
    user = relationship("UserTable", back_populates="account")


# -----------------------
# 3. User Emails
# -----------------------
class UserEmail(Base):
    __tablename__ = "user_emails"

    email_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_primary = Column(Boolean, default=False)

    user = relationship("UserTable", back_populates="emails")

    # Use a partial unique index to ensure only one primary email per user (when is_primary is TRUE)
    # noinspection PyUnresolvedReferences
    __table_args__ = (
        Index(
            "uq_user_primary_email",
            "user_id",
            unique=True,
            postgresql_where=is_primary.is_(True),
        ),
    )


# -----------------------
# 4. User Phone Numbers
# -----------------------
class UserPhoneNumber(Base):
    __tablename__ = "user_phone_numbers"

    phone_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    phone_number = Column(String(20), nullable=False)
    type = Column(String(50))  # e.g., "Mobile", "Home", "Work"
    is_primary = Column(Boolean, default=False)

    user = relationship("UserTable", back_populates="phone_numbers")

    # noinspection PyUnresolvedReferences
    __table_args__ = (
        Index(
            "uq_user_primary_phone",
            "user_id",
            unique=True,
            postgresql_where=is_primary.is_(True),
        ),
    )


# -----------------------
# 5. User Addresses
# -----------------------
class UserAddress(Base):
    __tablename__ = "user_addresses"

    address_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    type = Column(String(50))  # e.g., "Home", "Office"
    is_primary = Column(Boolean, default=False)

    user = relationship("UserTable", back_populates="addresses")

    # noinspection PyUnresolvedReferences
    __table_args__ = (
        Index(
            "uq_user_primary_address",
            "user_id",
            unique=True,
            postgresql_where=is_primary.is_(True),
        ),
    )


from sqlalchemy.orm import sessionmaker

# -----------------------
# Database Setup Function
# -----------------------
def setup_database(drop_and_recreate=False):
    """
    Drops all tables (optional) and creates all database tables defined in models.Base.

    Args:
        drop_and_recreate (bool): If True, drops all tables first before creating new ones.
    Returns:
        SessionLocal: A configured session factory.
    """
    from connection import engine

    if drop_and_recreate and input("Are you sure you want to drop and recreate all tables? (y/n): ").lower() == "y":
        print("⚠️ Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)

    print("📦 Creating tables...")
    Base.metadata.create_all(bind=engine)

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("✅ Database setup complete.")
    return SessionLocal

# -----------------------
# Example Usage
# -----------------------
if __name__ == "__main__":
    setup_database(drop_and_recreate=True)
