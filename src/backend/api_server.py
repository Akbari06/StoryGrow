"""
FastAPI server for StoryGrow API
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import os
from datetime import datetime

from config import config
from planner import Planner
from executor import Executor
from memory import Memory
from database import db

# Create FastAPI app
app = FastAPI(
    title="StoryGrow API",
    description="AI-powered family storytelling platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL, "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
planner = Planner()
executor = Executor()
memory = Memory()

# Startup event to connect to database
@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    connected = await db.connect()
    if connected:
        print("[API] Database connected successfully")
    else:
        print("[API] Warning: Database connection failed")

# Shutdown event to disconnect from database
@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from database on shutdown"""
    await db.disconnect()

# Request/Response models
class StoryRequest(BaseModel):
    audio_url: Optional[str] = None
    text_input: Optional[str] = None
    child_id: str
    session_mood: str = "neutral"
    educational_focus: Optional[List[str]] = []
    include_elements: Optional[List[str]] = []

class StoryResponse(BaseModel):
    story_id: str
    status: str
    preview: str
    processing_time: Optional[float] = None

class ChildProfile(BaseModel):
    name: str
    age: int
    avatar: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "StoryGrow API",
        "version": "1.0.0",
        "status": "running",
        "description": "AI-powered family storytelling platform"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "running",
            "memory": "connected" if memory.db else "disconnected",
            "gemini": "configured" if config.GEMINI_API_KEY else "not configured"
        }
    }

@app.get("/database/test")
async def test_database():
    """Test database connection and return info"""
    try:
        # Test database connection
        db_info = await db.test_connection()
        
        # Add additional health info
        db_info['timestamp'] = datetime.now().isoformat()
        db_info['api_status'] = 'running'
        
        return JSONResponse(
            status_code=200 if db_info['status'] == 'connected' else 500,
            content=db_info
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        )

@app.post("/database/init")
async def initialize_database():
    """Initialize database tables from schema"""
    try:
        # Check if already connected
        if not db.pool:
            connected = await db.connect()
            if not connected:
                raise HTTPException(status_code=500, detail="Failed to connect to database")
        
        # Create tables
        success = await db.create_tables()
        
        if success:
            # Get updated table info
            db_info = await db.test_connection()
            return {
                'status': 'success',
                'message': 'Database tables created successfully',
                'tables': db_info.get('tables', []),
                'table_count': db_info.get('table_count', 0)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create tables")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/story/create", response_model=StoryResponse)
async def create_story(request: StoryRequest):
    """
    Create a new story from child input.
    This is the main endpoint that orchestrates all agents.
    """
    start_time = datetime.now()
    
    try:
        print(f"[API] Creating story for child {request.child_id}")
        
        # Validate input
        if not request.text_input and not request.audio_url:
            raise HTTPException(status_code=400, detail="Either text_input or audio_url is required")
        
        # Prepare input for planner
        planner_input = {
            'audio_url': request.audio_url,
            'text_input': request.text_input,
            'child_id': request.child_id,
            'session_mood': request.session_mood,
            'educational_focus': request.educational_focus or [],
            'include_elements': request.include_elements or []
        }
        
        # Plan tasks
        tasks = await planner.plan(planner_input)
        
        # Execute tasks
        results = await executor.execute(tasks)
        
        # Extract story from results
        story = results.get('story', {})
        
        # Store story in memory
        if story and story.get('id'):
            await memory.store('stories', story['id'], story)
            
            # Store session data for emotional tracking
            session_data = {
                'childId': request.child_id,
                'timestamp': datetime.now(),
                'mood': request.session_mood,
                'emotions': results.get('emotions', {}),
                'storyId': story['id']
            }
            await memory.store('sessions', f"{request.child_id}_{datetime.now().timestamp()}", session_data)
            
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return StoryResponse(
            story_id=story.get('id', 'unknown'),
            status='complete',
            preview=story.get('title', 'New Story'),
            processing_time=processing_time
        )
        
    except Exception as e:
        print(f"[API] Error creating story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")

@app.get("/api/story/{story_id}")
async def get_story(story_id: str):
    """Retrieve a specific story"""
    try:
        story = await memory.retrieve('stories', story_id)
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")
        return story
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Story not found")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice/upload")
async def upload_voice(file: UploadFile = File(...), child_id: str = "default"):
    """Handle voice file uploads"""
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Create uploads directory
        os.makedirs("uploads", exist_ok=True)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'webm'
        file_path = f"uploads/{file_id}.{file_extension}"
        
        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # In production, upload to Cloud Storage
        # For now, return local path
        return {
            "upload_url": file_path,
            "file_id": file_id,
            "original_name": file.filename,
            "size": len(content),
            "child_id": child_id
        }
        
    except Exception as e:
        print(f"[API] Error uploading voice file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/child/{child_id}/stories")
async def get_child_stories(child_id: str, limit: int = 10):
    """Get recent stories for a child"""
    try:
        # Get child context which includes recent stories
        context = await memory.get_child_context(child_id)
        
        return {
            "child_id": child_id,
            "stories": context.get('recent_stories', [])[:limit],
            "total": len(context.get('recent_stories', []))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/child/{child_id}/dashboard")
async def get_child_dashboard(child_id: str):
    """Get dashboard data for a child"""
    try:
        # Get child context
        context = await memory.get_child_context(child_id)
        
        # Get recent emotional history
        emotional_history = await memory.get_emotional_history(child_id, days=7)
        
        return {
            "child_id": child_id,
            "profile": {
                "age": context.get('age', 5),
                "preferences": context.get('preferences', {}),
                "avatar": context.get('avatar', {})
            },
            "recent_stories": context.get('recent_stories', [])[:5],
            "favorite_elements": context.get('favorite_elements', {}),
            "badges": [],  # TODO: Implement badge system
            "mood_trend": self._calculate_mood_trend(emotional_history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/parent/insights/{child_id}")
async def get_parent_insights(child_id: str, days: int = 7):
    """Get emotional insights for parent dashboard"""
    try:
        # Get emotional history
        emotional_history = await memory.get_emotional_history(child_id, days=days)
        
        # Get child context
        context = await memory.get_child_context(child_id)
        
        # Calculate insights
        insights = self._calculate_insights(emotional_history, context)
        
        return {
            "child_id": child_id,
            "timeframe": f"Last {days} days",
            "emotional_summary": insights['emotional_summary'],
            "story_engagement": {
                "total_stories": len(context.get('recent_stories', [])),
                "favorite_themes": context.get('favorite_elements', {}).get('themes', [])[:3],
                "favorite_characters": context.get('favorite_elements', {}).get('characters', [])[:3]
            },
            "alerts": insights.get('alerts', []),
            "recommendations": insights.get('recommendations', []),
            "mood_chart_data": self._prepare_mood_chart_data(emotional_history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/child/{child_id}/profile")
async def update_child_profile(child_id: str, profile: ChildProfile):
    """Update child profile"""
    try:
        profile_data = {
            "name": profile.name,
            "age": profile.age,
            "avatar": profile.avatar or {},
            "preferences": profile.preferences or {},
            "updatedAt": datetime.now()
        }
        
        await memory.store('users', child_id, profile_data)
        
        return {"status": "success", "message": "Profile updated"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper methods
def _calculate_mood_trend(emotional_history: List[Dict]) -> str:
    """Calculate overall mood trend"""
    if not emotional_history:
        return "neutral"
    
    recent_moods = [session.get('mood', 'neutral') for session in emotional_history[-5:]]
    positive_moods = sum(1 for mood in recent_moods if mood in ['happy', 'excited'])
    
    if positive_moods >= len(recent_moods) * 0.7:
        return "positive"
    elif positive_moods <= len(recent_moods) * 0.3:
        return "concerning"
    else:
        return "mixed"

def _calculate_insights(emotional_history: List[Dict], context: Dict) -> Dict:
    """Calculate insights from emotional history"""
    insights = {
        'emotional_summary': {},
        'alerts': [],
        'recommendations': []
    }
    
    if not emotional_history:
        return insights
    
    # Calculate emotional averages
    all_emotions = {}
    for session in emotional_history:
        emotions = session.get('emotions', {}).get('emotions', {})
        for emotion, score in emotions.items():
            if emotion not in all_emotions:
                all_emotions[emotion] = []
            all_emotions[emotion].append(score)
    
    # Average emotions
    avg_emotions = {
        emotion: sum(scores) / len(scores) 
        for emotion, scores in all_emotions.items()
    }
    
    insights['emotional_summary'] = avg_emotions
    
    # Generate recommendations
    if avg_emotions.get('happiness', 0) < 0.4:
        insights['recommendations'].append({
            'type': 'emotional_support',
            'message': 'Consider activities that boost your child\'s mood',
            'actions': ['Plan fun activities', 'Spend more one-on-one time', 'Ask about their day']
        })
    
    if avg_emotions.get('sadness', 0) > 0.6:
        insights['alerts'].append({
            'type': 'emotional_concern',
            'severity': 'medium',
            'message': 'Child has shown elevated sadness recently',
            'recommendation': 'Consider talking with your child about their feelings'
        })
    
    return insights

def _prepare_mood_chart_data(emotional_history: List[Dict]) -> List[Dict]:
    """Prepare data for mood chart visualization"""
    chart_data = []
    
    for session in emotional_history[-14:]:  # Last 2 weeks
        timestamp = session.get('timestamp')
        emotions = session.get('emotions', {}).get('emotions', {})
        
        chart_data.append({
            'date': timestamp.isoformat() if timestamp else datetime.now().isoformat(),
            'happiness': emotions.get('happiness', 0),
            'sadness': emotions.get('sadness', 0),
            'fear': emotions.get('fear', 0),
            'anger': emotions.get('anger', 0),
            'overall_mood': session.get('mood', 'neutral')
        })
    
    return chart_data

# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"[API] Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)