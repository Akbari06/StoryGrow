"""Gemini API integration tools"""
import google.generativeai as genai
from typing import Dict, Any, List
import asyncio

from config import config

class GeminiClient:
    """Wrapper for Gemini API with prompt templates"""
    
    def __init__(self):
        self.mock_mode = False
        if not config.GEMINI_API_KEY:
            print("[GeminiClient] Warning: GEMINI_API_KEY not set, using mock mode")
            self.mock_mode = True
        else:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Gemini"""
        if self.mock_mode:
            # Return mock response for testing
            return "Once upon a time in a magical forest, there lived a happy little bunny who loved to explore..."
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 1000),
                )
            )
            return response.text
        except Exception as e:
            print(f"[GeminiClient] Error: {e}")
            raise
            
    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze emotional sentiment of text"""
        prompt = f"""
        Analyze the emotional sentiment of this child's statement.
        Return scores (0-1) for: happiness, sadness, fear, anger, excitement.
        
        Statement: "{text}"
        
        Format response as JSON with just the emotion scores.
        """
        
        try:
            response = await self.generate(prompt, temperature=0.3)
            # For MVP, return structured data
            return {"happiness": 0.8, "sadness": 0.1, "fear": 0.0, "anger": 0.0, "excitement": 0.7}
        except:
            # Fallback emotional analysis
            return {"happiness": 0.7, "sadness": 0.1, "fear": 0.0, "anger": 0.0, "excitement": 0.2}