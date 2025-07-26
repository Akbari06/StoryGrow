"""
Memory management using PostgreSQL.
Replaces Firestore with Cloud SQL for better relational data handling.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import uuid
import json

from database import Database
from config import config

class MemoryPG:
    """
    Manages persistent memory using PostgreSQL.
    Stores child preferences, story history, and session data.
    """
    
    # Demo ID mappings
    DEMO_MAPPINGS = {
        'demo_child_123': '44444444-4444-4444-4444-444444444444',
        'demo_parent_456': '33333333-3333-3333-3333-333333333333'
    }
    
    def __init__(self, db: Database):
        self.db = db
        print("[MemoryPG] Initialized with PostgreSQL backend")
            
    def _map_id(self, id_str: str) -> str:
        """Map demo IDs to real UUIDs"""
        return self.DEMO_MAPPINGS.get(id_str, id_str)
    
    async def store_story(self, story_data: Dict[str, Any]) -> str:
        """Store a story in PostgreSQL"""
        try:
            story_id = story_data.get('id', str(uuid.uuid4()))
            kid_id = self._map_id(story_data.get('childId', 'demo_child_123'))
            
            async with self.db.pool.acquire() as conn:
                # Insert story
                await conn.execute("""
                    INSERT INTO stories (id, kid_id, title, prompt, status, metadata)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        metadata = EXCLUDED.metadata,
                        updated_at = NOW()
                """, 
                    uuid.UUID(story_id),
                    uuid.UUID(kid_id),
                    story_data.get('title', 'Untitled Story'),
                    story_data.get('metadata', {}).get('inputText', ''),
                    'completed',
                    json.dumps(story_data.get('metadata', {}))
                )
                
                # Insert scenes
                for scene in story_data.get('scenes', []):
                    await conn.execute("""
                        INSERT INTO story_scenes (story_id, scene_number, text, image_prompt)
                        VALUES ($1, $2, $3, $4)
                        ON CONFLICT (story_id, scene_number) DO UPDATE SET
                            text = EXCLUDED.text,
                            image_prompt = EXCLUDED.image_prompt
                    """,
                        uuid.UUID(story_id),
                        scene.get('sceneNumber', 1),
                        scene.get('text', ''),
                        scene.get('imagePrompt', '')
                    )
                
            print(f"[MemoryPG] Stored story {story_id} for child {kid_id}")
            return story_id
            
        except Exception as e:
            print(f"[MemoryPG] Error storing story: {e}")
            raise
            
    async def retrieve_story(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a story by ID"""
        try:
            async with self.db.pool.acquire() as conn:
                # Get story
                story_row = await conn.fetchrow("""
                    SELECT s.*, k.name as child_name 
                    FROM stories s
                    JOIN kids k ON s.kid_id = k.id
                    WHERE s.id = $1
                """, uuid.UUID(story_id))
                
                if not story_row:
                    return None
                
                # Get scenes
                scenes = await conn.fetch("""
                    SELECT scene_number, text, image_prompt, image_url
                    FROM story_scenes
                    WHERE story_id = $1
                    ORDER BY scene_number
                """, uuid.UUID(story_id))
                
                # Build story object
                story = {
                    'id': str(story_row['id']),
                    'childId': str(story_row['kid_id']),
                    'title': story_row['title'],
                    'scenes': [
                        {
                            'sceneNumber': s['scene_number'],
                            'text': s['text'],
                            'imagePrompt': s['image_prompt'],
                            'imageUrl': s['image_url']
                        }
                        for s in scenes
                    ],
                    'metadata': story_row['metadata'] or {},
                    'status': story_row['status'],
                    'createdAt': story_row['created_at'].isoformat()
                }
                
                return story
                
        except Exception as e:
            print(f"[MemoryPG] Error retrieving story: {e}")
            return None
            
    async def store_session(self, session_data: Dict[str, Any]) -> str:
        """Store emotion session data"""
        try:
            kid_id = self._map_id(session_data.get('childId', 'demo_child_123'))
            session_id = str(uuid.uuid4())
            
            async with self.db.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO emotion_sessions (id, kid_id, mood, emotion_scores, story_id)
                    VALUES ($1, $2, $3, $4, $5)
                """,
                    uuid.UUID(session_id),
                    uuid.UUID(kid_id),
                    session_data.get('mood', 'neutral'),
                    json.dumps(session_data.get('emotions', {})),
                    uuid.UUID(session_data.get('storyId')) if session_data.get('storyId') else None
                )
                
            print(f"[MemoryPG] Stored session {session_id}")
            return session_id
            
        except Exception as e:
            print(f"[MemoryPG] Error storing session: {e}")
            raise
            
    async def store_alert(self, alert_data: Dict[str, Any]) -> str:
        """Store parent alert"""
        try:
            kid_id = self._map_id(alert_data.get('childId', 'demo_child_123'))
            alert_id = str(uuid.uuid4())
            
            # Get parent ID for the kid
            async with self.db.pool.acquire() as conn:
                parent_row = await conn.fetchrow("""
                    SELECT parent_id FROM kids WHERE id = $1
                """, uuid.UUID(kid_id))
                
                if not parent_row:
                    print(f"[MemoryPG] No parent found for kid {kid_id}")
                    return alert_id
                
                await conn.execute("""
                    INSERT INTO parent_alerts 
                    (id, parent_id, kid_id, alert_type, severity, message, metadata, story_id)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                    uuid.UUID(alert_id),
                    parent_row['parent_id'],
                    uuid.UUID(kid_id),
                    alert_data.get('type', 'emotional_concern'),
                    alert_data.get('severity', 'low'),
                    alert_data.get('message', ''),
                    json.dumps({'concerns': alert_data.get('concerns', [])}),
                    uuid.UUID(alert_data.get('storyId')) if alert_data.get('storyId') else None
                )
                
            print(f"[MemoryPG] Stored alert {alert_id}")
            return alert_id
            
        except Exception as e:
            print(f"[MemoryPG] Error storing alert: {e}")
            raise
            
    async def get_child_context(self, child_id: str) -> Dict[str, Any]:
        """Get comprehensive context for a child"""
        try:
            real_kid_id = self._map_id(child_id)
            
            async with self.db.pool.acquire() as conn:
                # Get child info
                child_row = await conn.fetchrow("""
                    SELECT * FROM kids WHERE id = $1
                """, uuid.UUID(real_kid_id))
                
                if not child_row:
                    # Return default context
                    return {
                        'child_id': child_id,
                        'preferences': {
                            'age': 5,
                            'favoriteCharacters': ['unicorn', 'dragon', 'fairy'],
                            'favoriteThemes': ['adventure', 'friendship', 'magic']
                        },
                        'recent_stories': []
                    }
                
                # Get recent stories
                recent_stories = await conn.fetch("""
                    SELECT id, title, created_at 
                    FROM stories 
                    WHERE kid_id = $1 
                    ORDER BY created_at DESC 
                    LIMIT 5
                """, uuid.UUID(real_kid_id))
                
                context = {
                    'child_id': child_id,
                    'preferences': child_row['preferences'] or {
                        'age': child_row['age'],
                        'favoriteCharacters': ['unicorn', 'dragon', 'fairy'],
                        'favoriteThemes': ['adventure', 'friendship', 'magic']
                    },
                    'recent_stories': [
                        {
                            'id': str(s['id']),
                            'title': s['title'],
                            'createdAt': s['created_at'].isoformat()
                        }
                        for s in recent_stories
                    ]
                }
                
                return context
                
        except Exception as e:
            print(f"[MemoryPG] Error getting child context: {e}")
            return {
                'child_id': child_id,
                'preferences': {},
                'recent_stories': []
            }
            
    async def get_emotional_history(self, child_id: str, days: int = 7) -> List[Dict]:
        """Get emotion tracking history"""
        try:
            real_kid_id = self._map_id(child_id)
            
            async with self.db.pool.acquire() as conn:
                sessions = await conn.fetch("""
                    SELECT * FROM emotion_sessions 
                    WHERE kid_id = $1 
                    AND created_at > NOW() - INTERVAL '%s days'
                    ORDER BY created_at DESC
                """, uuid.UUID(real_kid_id), days)
                
                return [
                    {
                        'timestamp': s['created_at'],
                        'mood': s['mood'],
                        'emotions': s['emotion_scores'] or {},
                        'storyId': str(s['story_id']) if s['story_id'] else None
                    }
                    for s in sessions
                ]
                
        except Exception as e:
            print(f"[MemoryPG] Error getting emotional history: {e}")
            return []

    # Compatibility methods for existing code
    async def store(self, collection: str, doc_id: str, data: Dict[str, Any]):
        """Compatibility method for Firestore-style storage"""
        if collection == 'stories':
            await self.store_story(data)
        elif collection == 'sessions':
            await self.store_session(data)
        elif collection == 'alerts':
            await self.store_alert(data)
        else:
            print(f"[MemoryPG] Unknown collection: {collection}")
            
    async def retrieve(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Compatibility method for Firestore-style retrieval"""
        if collection == 'stories':
            return await self.retrieve_story(doc_id)
        else:
            print(f"[MemoryPG] Retrieval not implemented for collection: {collection}")
            return None