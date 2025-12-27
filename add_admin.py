from app import app, db, User
from werkzeug.security import generate_password_hash

def add_admin_user():
    # Check if admin already exists
    admin = User.query.filter_by(email="admin@tawasol.com").first()
    if admin:
        print("⚠️ Admin user already exists.")
        return

    # Generate a hashed password
    admin_password = generate_password_hash('password')

    # Create the admin user
    admin_user = User(
        full_name="Admin User",
        email="admin@tawasol.com",
        phone="0000000000",
        role="admin",
        password=admin_password,  # ✅ FIXED COLUMN NAME
        gender="Other"
    )

    # Add the new admin user to the database
    try:
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Failed to create admin user: {e}")

# Run the function within the application context
if __name__ == "__main__":
    with app.app_context():
        add_admin_user()
