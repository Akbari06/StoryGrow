"""
Memory management using Firestore.
Required for hackathon - demonstrates stateful agent memory.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio

from config import config

class Memory:
    """
    Manages persistent memory for the AI agents.
    Stores child preferences, story history, and session data.
    """
    
    def __init__(self):
        # Initialize Firestore client
        try:
            from google.cloud import firestore
            from google.cloud.firestore_v1 import FieldFilter
            self.db = firestore.Client(
                project=config.GCP_PROJECT_ID,
                database="database-storygrow"  # Use specific database ID
            )
            self.FieldFilter = FieldFilter
            print("[Memory] Connected to Firestore (database-storygrow)")
        except Exception as e:
            print(f"[Memory] Warning: Firestore not configured: {e}")
            self.db = None
            self.FieldFilter = None
            
    async def store(self, collection: str, doc_id: str, data: Dict[str, Any]):
        """Store data in Firestore"""
        if not self.db:
            print("[Memory] Skipping store - Firestore not configured")
            return
            
        try:
            # Add timestamp
            data['updatedAt'] = datetime.now()
            if 'createdAt' not in data:
                data['createdAt'] = datetime.now()
                
            # Store document
            self.db.collection(collection).document(doc_id).set(data, merge=True)
            print(f"[Memory] Stored document {doc_id} in {collection}")
            
        except Exception as e:
            print(f"[Memory] Error storing document: {e}")
            
    async def retrieve(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single document"""
        if not self.db:
            return None
            
        try:
            doc = self.db.collection(collection).document(doc_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            print(f"[Memory] Error retrieving document: {e}")
            return None
            
    async def get_child_context(self, child_id: str) -> Dict[str, Any]:
        """
        Get comprehensive context for a child including:
        - Preferences and settings
        - Recent stories
        - Favorite characters/themes
        - Learning progress
        """
        context = {
            'child_id': child_id,
            'preferences': {
                'age': 5,
                'favoriteCharacters': ['unicorn', 'dragon', 'fairy'],
                'favoriteThemes': ['adventure', 'friendship', 'magic']
            },
            'recent_stories': [],
            'favorite_elements': {
                'characters': [('unicorn', 3), ('dragon', 2), ('fairy', 2)],
                'themes': [('adventure', 4), ('friendship', 3), ('magic', 3)]
            },
            'educational_progress': {}
        }
        
        if not self.db:
            return context
            
        try:
            # Get child profile
            child_data = await self.retrieve('users', child_id)
            if child_data:
                context['preferences'] = child_data.get('preferences', context['preferences'])
                context['age'] = child_data.get('age', 5)
                context['avatar'] = child_data.get('avatar', {})
                
            # Get recent stories (last 5)
            from google.cloud import firestore
            stories_query = (
                self.db.collection('stories')
                .where(filter=self.FieldFilter('childId', '==', child_id))
                .order_by('createdAt', direction=firestore.Query.DESCENDING)
                .limit(5)
            )
            
            stories = stories_query.get()
            context['recent_stories'] = [
                {
                    'id': doc.id,
                    'title': doc.to_dict().get('title'),
                    'themes': doc.to_dict().get('themes', []),
                    'characters': doc.to_dict().get('characters', [])
                }
                for doc in stories
            ]
            
            # Extract favorite elements from recent stories
            all_characters = []
            all_themes = []
            for story in context['recent_stories']:
                all_characters.extend(story.get('characters', []))
                all_themes.extend(story.get('themes', []))
                
            # Count frequency
            from collections import Counter
            if all_characters or all_themes:
                context['favorite_elements'] = {
                    'characters': Counter(all_characters).most_common(3),
                    'themes': Counter(all_themes).most_common(3)
                }
            
            print(f"[Memory] Retrieved context for child {child_id}")
            return context
            
        except Exception as e:
            print(f"[Memory] Error getting child context: {e}")
            return context
            
    async def get_emotional_history(self, child_id: str, days: int = 7) -> List[Dict]:
        """Get emotion tracking history"""
        if not self.db:
            # Return mock data for MVP
            return [
                {
                    'timestamp': datetime.now(),
                    'mood': 'happy',
                    'emotions': {'happiness': 0.8, 'sadness': 0.1, 'fear': 0.0}
                }
            ]
            
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            sessions_query = (
                self.db.collection('sessions')
                .where(filter=self.FieldFilter('childId', '==', child_id))
                .where(filter=self.FieldFilter('timestamp', '>=', cutoff_date))
                .order_by('timestamp')
            )
            
            sessions = sessions_query.get()
            
            return [
                {
                    'timestamp': doc.to_dict().get('timestamp'),
                    'mood': doc.to_dict().get('mood'),
                    'emotions': doc.to_dict().get('emotions', {})
                }
                for doc in sessions
            ]
            
        except Exception as e:
            print(f"[Memory] Error getting emotional history: {e}")
            return []