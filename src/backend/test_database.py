#!/usr/bin/env python3
"""
Test database connection and setup
"""
import asyncio
import os
import sys
from database import db

async def test_database():
    """Test database connection and setup"""
    print("=" * 60)
    print("StoryGrow Database Test")
    print("=" * 60)
    print()
    
    # Step 1: Test connection
    print("1. Testing database connection...")
    connected = await db.connect()
    
    if not connected:
        print("❌ Failed to connect to database")
        print(f"   Host: {db.db_config['host']}")
        print(f"   Database: {db.db_config['database']}")
        print("\nPlease check:")
        print("- Database credentials in .env or environment variables")
        print("- Cloud SQL instance is running")
        print("- IP whitelist includes your current IP")
        return
    
    print("✅ Connected to database successfully!")
    print()
    
    # Step 2: Get database info
    print("2. Database information:")
    db_info = await db.test_connection()
    
    print(f"   PostgreSQL Version: {db_info.get('version', 'Unknown')[:50]}...")
    print(f"   Database: {db_info.get('database')}")
    print(f"   Host: {db_info.get('host')}")
    print(f"   Table Count: {db_info.get('table_count', 0)}")
    print()
    
    # Step 3: List existing tables
    if db_info.get('tables'):
        print("3. Existing tables:")
        for table in db_info['tables']:
            print(f"   - {table}")
    else:
        print("3. No tables found in database")
    print()
    
    # Step 4: Ask to create tables
    if db_info.get('table_count', 0) == 0:
        print("4. Database appears to be empty.")
        response = input("   Would you like to create the tables from schema? (y/n): ")
        
        if response.lower() == 'y':
            print("\n   Creating tables...")
            success = await db.create_tables()
            
            if success:
                print("   ✅ Tables created successfully!")
                
                # Get updated info
                db_info = await db.test_connection()
                print(f"\n   New table count: {db_info.get('table_count', 0)}")
                print("   Tables created:")
                for table in db_info.get('tables', []):
                    print(f"   - {table}")
            else:
                print("   ❌ Failed to create tables")
                print("   Check the cloud_sql_schema.sql file")
    else:
        print("4. Database already has tables ✅")
    
    print()
    print("=" * 60)
    print("Test complete!")
    
    # Disconnect
    await db.disconnect()

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run test
    asyncio.run(test_database())