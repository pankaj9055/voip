#!/usr/bin/env python3

import os
import sys

# Test if the app can be imported and started
try:
    print("Testing app import...")
    from app import create_app
    print("✓ App imported successfully")
    
    print("Testing app creation...")
    app = create_app()
    print("✓ App created successfully")
    
    print("Testing database connection...")
    with app.app_context():
        from models import db
        db.create_all()
        print("✓ Database tables created")
        
        # Test default data creation
        from models import create_default_data
        create_default_data()
        print("✓ Default data created")
        
    print("✓ All tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)