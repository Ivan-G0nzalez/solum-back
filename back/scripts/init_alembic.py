#!/usr/bin/env python3
"""
Script to initialize Alembic and create the first migration.
Run this script to set up your database migrations.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main function to initialize Alembic."""
    print("🚀 Initializing Alembic for Solum Health...")
    
    # Check if we're in the right directory
    if not Path("alembic.ini").exists():
        print("❌ alembic.ini not found. Make sure you're in the project root directory.")
        sys.exit(1)
    
    # Initialize Alembic (if not already done)
    if not Path("alembic").exists():
        if not run_command("alembic init alembic", "Initializing Alembic"):
            sys.exit(1)
    
    # Create initial migration
    if not run_command('alembic revision --autogenerate -m "Initial migration"', "Creating initial migration"):
        sys.exit(1)
    
    print("\n🎉 Alembic initialization completed!")
    print("\n📋 Next steps:")
    print("1. Review the generated migration in alembic/versions/")
    print("2. Run: alembic upgrade head")
    print("3. Start your FastAPI application")

if __name__ == "__main__":
    main() 