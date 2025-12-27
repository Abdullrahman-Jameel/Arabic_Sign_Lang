from app import app, db
from add_admin import add_admin_user

# Initialize database and create admin user
with app.app_context():
    # Create all tables if they don't exist
    db.create_all()
    print("✅ Database tables created successfully.")

    # Add admin user (uses the function from add_admin.py)
    add_admin_user()
    print("✅ Admin user created (if not already exists).")
