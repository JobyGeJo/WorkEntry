from sqlalchemy.orm import joinedload

from Enums import Roles

if __name__ != "__main__":
    print("This is not a package.")
    exit(0)

from database.postgres import DBSession
from database.postgres.tables import UserTable, UserAccount, UserEmail, UserPhoneNumber, UserAddress
from database.postgres.connection import SessionLocal
from utils.passwords import generate_hash


def create_user(db):
    try:
        # 1. Create a base user
        user = UserTable(full_name="John", gender="Male")

        # 2. Add login account (only if this user has credentials)
        account = UserAccount(
            username="john",
            password_hash=generate_hash("12345678"),  # use bcrypt/argon2 in real apps
            role=Roles.OWNER,
        )
        account.user = user

        # 3. Add an email
        email = UserEmail(
            email="jobygej@example.com",
            is_primary=True,
        )
        email.user = user

        # 4. Add a phone number
        phone = UserPhoneNumber(
            phone_number="+11234567880",
            type="Mobile",
            is_primary=True,
        )
        phone.user = user

        # 5. Add an address
        address = UserAddress(
            address_line1="123 Main St",
            city="New York",
            state="NY",
            country="USA",
            postal_code="10001",
            type="Home",
            is_primary=True,
        )
        address.user = user

        # Add to session
        db.add(user)  # user will cascade to account, email, phone, address
        db.commit()

        print("✅ User and related data inserted successfully!")

    except Exception as e:
        db.rollback()
        print("❌ Error inserting data:", e)

    finally:
        db.close()

def fetch(db):
    try:
        # Fetch all users with relationships
        users = db.query(UserTable).options(
            joinedload(UserTable.account),
            joinedload(UserTable.emails),
            joinedload(UserTable.phone_numbers),
            joinedload(UserTable.addresses)
        ).all()

        for user in users:
            print("\n👤 User:", user.full_name, f"(ID: {user.user_id})")

            # Account details (if they have one)
            if user.account:
                print("   🔑 Account ->", user.account.username, "| Role:", user.account.role.value)

            # Emails
            for email in user.emails:
                primary = "(Primary)" if email.is_primary else ""
                print("   📧 Email ->", email.email, primary)

            # Phone numbers
            for phone in user.phone_numbers:
                primary = "(Primary)" if phone.is_primary else ""
                print("   📱 Phone ->", phone.phone_number, "| Type:", phone.type, primary)

            # Addresses
            for addr in user.addresses:
                primary = "(Primary)" if addr.is_primary else ""
                print(
                    f"   🏠 Address -> {addr.address_line1}, {addr.city}, {addr.state} {addr.postal_code}, {addr.country} {primary}")

    except Exception as e:
        print("❌ Error fetching data:", e)

    finally:
        db.close()

def add_email(db):
    try:
        email = UserEmail(
            email="dai_ivanda@aamada.com",
            user_id=1,
        )

        db.add(email)
        db.commit()

        print("✅ User and related data inserted successfully!")
    except Exception as e:
        db.rollback()
        print("❌ Error inserting data:", e)

    finally:
        db.close()

def setup_database(drop_and_recreate=False):
    """
    Drops all tables (optional) and creates all database tables defined in models.Base.

    Args:
        drop_and_recreate (bool): If True, drops all tables first before creating new ones.
    Returns:
        SessionLocal: A configured session factory.
    """
    from database.postgres.connection import engine
    from database.postgres.tables import Base

    if drop_and_recreate and input("Are you sure you want to drop and recreate all tables? (y/n): ").lower() == "y":
        print("⚠️ Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)

    print("📦 Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("✅ Database setup complete.")

def create_sample_users(db):
    try:
        # --- User 1 ---
        user1 = UserTable(full_name="Alice Johnson", gender="Female")
        account1 = UserAccount(
            username="alice",
            password_hash=generate_hash("alicePass123"),
            role=Roles.ADMIN,
        )
        account1.user = user1

        email1 = UserEmail(email="alice.j@example.com", is_primary=True)
        email1.user = user1

        phone1 = UserPhoneNumber(phone_number="+14155550101", type="Mobile", is_primary=True)
        phone1.user = user1

        address1 = UserAddress(
            address_line1="45 Park Ave",
            city="San Francisco",
            state="CA",
            country="USA",
            postal_code="94103",
            type="Home",
            is_primary=True,
        )
        address1.user = user1

        # --- User 2 ---
        user2 = UserTable(full_name="Michael Smith", gender="Male")
        account2 = UserAccount(
            username="mike",
            password_hash=generate_hash("mikeSecure99"),
            role=Roles.USER,
        )
        account2.user = user2

        email2 = UserEmail(email="mike.smith@example.com", is_primary=True)
        email2.user = user2

        phone2 = UserPhoneNumber(phone_number="+442071234567", type="Work", is_primary=True)
        phone2.user = user2

        address2 = UserAddress(
            address_line1="78 High Street",
            city="London",
            state="",
            country="UK",
            postal_code="SW1A 1AA",
            type="Office",
            is_primary=True,
        )
        address2.user = user2

        # --- User 3 ---
        user3 = UserTable(full_name="Sophia Martinez", gender="Female")
        account3 = UserAccount(
            username="sophia",
            password_hash=generate_hash("sophia2024!"),
            role=Roles.MANAGER,
        )
        account3.user = user3

        email3 = UserEmail(email="sophia.m@example.com", is_primary=True)
        email3.user = user3

        phone3 = UserPhoneNumber(phone_number="+61234567890", type="Mobile", is_primary=True)
        phone3.user = user3

        address3 = UserAddress(
            address_line1="200 George St",
            city="Sydney",
            state="NSW",
            country="Australia",
            postal_code="2000",
            type="Home",
            is_primary=True,
        )
        address3.user = user3

        # Add all to session
        db.add_all([user1, user2, user3])
        db.commit()
        print("✅ Sample users inserted successfully!")

    except Exception as e:
        db.rollback()
        print("❌ Error inserting users:", e)

    finally:
        db.close()


if __name__ == "__main__":
    # setup_database(drop_and_recreate=True)

    with DBSession() as session:
        # create_user(session)
        # add_email(session)
        create_sample_users(session)
        fetch(session)
