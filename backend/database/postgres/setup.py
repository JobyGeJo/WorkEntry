from database.postgres import DBSession
from tables import UserTable, UserAccount, UserEmail, UserPhoneNumber, UserAddress
from connection import SessionLocal
from utils.passwords import generate_hash


def create_user(db):
    try:
        # 1. Create a base user
        user = UserTable(full_name="Joby", gender="Male")

        # 2. Add login account (only if this user has credentials)
        account = UserAccount(
            username="jobygejo",
            password_hash=generate_hash("12345678"),  # use bcrypt/argon2 in real apps
            role="Admin",
        )
        account.user = user

        # 3. Add an email
        email = UserEmail(
            email="johndoe@example.com",
            is_primary=True,
        )
        email.user = user

        # 4. Add a phone number
        phone = UserPhoneNumber(
            phone_number="+11234567890",
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
        users = db.query(UserTable).all()

        for user in users:
            print("\n👤 User:", user.full_name, f"(ID: {user.user_id})")

            # Account details (if they have one)
            if user.account:
                print("   🔑 Account ->", user.account.username, "| Role:", user.account.role)

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



if __name__ == "__main__":
    from tables import setup_database

    setup_database(drop_and_recreate=True)
    create_user(SessionLocal())
    add_email(SessionLocal())
    with DBSession() as db:
        fetch(db)
