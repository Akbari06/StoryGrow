"""Configuration management for StoryGrow"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Google Cloud
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'storygrow-2')
    GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'bucketstorygrow')
    
    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 8080))
    
    # Frontend URL
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # Story Generation Settings
    MAX_STORY_SCENES = 7
    MIN_STORY_SCENES = 5
    MAX_RECORDING_DURATION = 120  # seconds
    
    # Safety Settings
    EMOTION_ALERT_THRESHOLD = 0.8
    TRAUMA_KEYWORDS = ['scared', 'hurt', 'pain', 'cry', 'hit']

config = Config()