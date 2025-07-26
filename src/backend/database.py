"""
PostgreSQL database connection and utilities
"""
import os
import asyncio
import asyncpg
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
from google.cloud.sql.connector import Connector

from config import config

class Database:
    """PostgreSQL database connection manager"""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.connector: Optional[Connector] = None
        
        # Database configuration from environment
        self.db_config = {
            'host': os.getenv('DB_HOST', '34.79.91.186'),  # From secretCLAUDE.md
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME', 'storygrow'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'ChangeMeNow123!'),  # Should be changed in production
        }
        
        # For Cloud SQL connection
        self.instance_connection_name = os.getenv(
            'INSTANCE_CONNECTION_NAME', 
            'storygrow-2:europe-west1:storygrow-database'
        )
        
        # Check if running on Cloud Run
        self.is_cloud_run = os.getenv('K_SERVICE') is not None
        
    async def connect(self):
        """Create connection pool"""
        try:
            if self.is_cloud_run and self.instance_connection_name:
                # Use Cloud SQL connector for Cloud Run
                print(f"[Database] Running on Cloud Run (K_SERVICE={os.getenv('K_SERVICE')})")
                print(f"[Database] Connecting via Cloud SQL connector to {self.instance_connection_name}")
                print(f"[Database] Using user: {self.db_config['user']}")
                
                # Initialize connector with explicit project ID
                from google.auth import default
                try:
                    credentials, project = default()
                    print(f"[Database] Using project: {project}")
                except Exception as e:
                    print(f"[Database] Auth error: {e}")
                
                self.connector = Connector(refresh_strategy="lazy")
                
                # Create connection function for the pool
                async def get_conn():
                    conn = await self.connector.connect_async(
                        self.instance_connection_name,
                        "asyncpg",
                        user=self.db_config['user'],
                        password=self.db_config['password'],
                        db=self.db_config['database']
                    )
                    return conn
                
                # Create pool with the connector
                self.pool = await asyncpg.create_pool(
                    connect=get_conn,
                    min_size=1,
                    max_size=10,
                    command_timeout=60
                )
                print(f"[Database] Connected via Cloud SQL connector")
            else:
                # Direct connection for local development
                self.pool = await asyncpg.create_pool(
                    **self.db_config,
                    min_size=1,
                    max_size=10,
                    command_timeout=60
                )
                print(f"[Database] Connected to PostgreSQL at {self.db_config['host']}")
            
            return True
        except Exception as e:
            print(f"[Database] Connection failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            print("[Database] Disconnected from PostgreSQL")
        if self.connector:
            await self.connector.close()
            print("[Database] Closed Cloud SQL connector")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test database connection and get basic info"""
        try:
            async with self.pool.acquire() as conn:
                # Test basic query
                version = await conn.fetchval('SELECT version()')
                
                # Get table count
                table_count = await conn.fetchval("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                
                # Get list of tables
                tables = await conn.fetch("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                
                table_names = [t['table_name'] for t in tables]
                
                return {
                    'status': 'connected',
                    'version': version,
                    'table_count': table_count,
                    'tables': table_names,
                    'database': self.db_config['database'],
                    'host': self.db_config['host']
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'database': self.db_config['database'],
                'host': self.db_config['host']
            }
    
    async def execute_query(self, query: str, *args):
        """Execute a query that doesn't return results"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch_one(self, query: str, *args):
        """Fetch a single row"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    
    async def fetch_all(self, query: str, *args):
        """Fetch multiple rows"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def create_tables(self):
        """Create tables from schema if they don't exist"""
        try:
            # Read schema file
            schema_path = os.path.join(
                os.path.dirname(__file__), 
                'cloud_sql_schema.sql'
            )
            
            if not os.path.exists(schema_path):
                print(f"[Database] Schema file not found: {schema_path}")
                return False
            
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            async with self.pool.acquire() as conn:
                # Execute schema in a transaction
                async with conn.transaction():
                    await conn.execute(schema_sql)
                    
            print("[Database] Tables created successfully")
            return True
            
        except Exception as e:
            print(f"[Database] Error creating tables: {e}")
            return False
    
    async def insert_child(self, parent_id: str, name: str, age: int) -> Optional[str]:
        """Insert a new child record"""
        try:
            query = """
                INSERT INTO children (parent_id, name, age, avatar_style)
                VALUES ($1, $2, $3, $4)
                RETURNING id
            """
            
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, parent_id, name, age, 'default')
                return str(row['id'])
                
        except Exception as e:
            print(f"[Database] Error inserting child: {e}")
            return None
    
    async def get_child(self, child_id: str) -> Optional[Dict[str, Any]]:
        """Get child information"""
        try:
            query = """
                SELECT id, parent_id, name, age, avatar_style,
                       reading_level, favorite_themes, favorite_characters,
                       created_at, updated_at
                FROM children
                WHERE id = $1
            """
            
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, child_id)
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            print(f"[Database] Error getting child: {e}")
            return None

# Singleton instance
db = Database()