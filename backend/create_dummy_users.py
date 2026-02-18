"""
Script to create dummy users for testing
Run this after starting the backend for the first time
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app import models
from app.auth import get_password_hash


def create_dummy_users():
    """Create dummy users for testing"""
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
        if existing_admin:
            print("Dummy users already exist!")
            return
        
        # Create admin user
        admin_user = models.User(
            email="admin@monitoring.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True
        )
        db.add(admin_user)
        
        # Create regular user
        regular_user = models.User(
            email="user@monitoring.com",
            username="user",
            full_name="Regular User",
            hashed_password=get_password_hash("user123"),
            is_admin=False,
            is_active=True
        )
        db.add(regular_user)
        
        # Create demo user
        demo_user = models.User(
            email="demo@monitoring.com",
            username="demo",
            full_name="Demo User",
            hashed_password=get_password_hash("demo123"),
            is_admin=False,
            is_active=True
        )
        db.add(demo_user)
        
        db.commit()
        
        print("\n✅ Dummy users created successfully!")
        print("\n📋 Login Credentials:")
        print("=" * 50)
        print("\n1. Admin User:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Role: Administrator")
        
        print("\n2. Regular User:")
        print("   Username: user")
        print("   Password: user123")
        print("   Role: Regular User")
        
        print("\n3. Demo User:")
        print("   Username: demo")
        print("   Password: demo123")
        print("   Role: Regular User")
        print("\n" + "=" * 50)
        print("\n🚀 You can now login with any of these credentials!")
        print("📍 API Docs: http://localhost:8000/api/docs")
        
    except Exception as e:
        print(f"❌ Error creating dummy users: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_dummy_users()
