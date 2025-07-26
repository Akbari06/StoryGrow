"""
Illustrator Agent - Creates visual elements for stories
"""
from typing import Dict, Any, List
import asyncio
import uuid

from tools.gemini_tools import GeminiClient
from config import config

class IllustratorAgent:
    """
    Generates image prompts and manages visual elements for stories.
    In production, would integrate with image generation APIs.
    """
    
    def __init__(self):
        self.gemini = GeminiClient()
        
    async def create_scene_images(self, story_id: str, scenes: List[Dict] = None) -> Dict[str, Any]:
        """
        Create image descriptions for story scenes.
        
        In production, this would:
        1. Generate detailed prompts using Gemini
        2. Call image generation API (Vertex AI Imagen)
        3. Store images in Cloud Storage
        4. Return URLs
        
        For MVP, returns placeholder data with enhanced prompts.
        """
        
        print(f"[Illustrator] Creating images for story {story_id}")
        
        # For MVP, create placeholder image data with enhanced prompts
        image_results = []
        
        if scenes:
            for scene in scenes:
                # Generate enhanced image prompt using Gemini
                enhanced_prompt = await self._enhance_image_prompt(scene['text'])
                
                # Create placeholder image data
                image_data = {
                    'sceneNumber': scene['sceneNumber'],
                    'prompt': enhanced_prompt,
                    'imageUrl': self._generate_placeholder_url(scene['sceneNumber'], enhanced_prompt),
                    'thumbnailUrl': self._generate_thumbnail_url(scene['sceneNumber'])
                }
                
                image_results.append(image_data)
        
        return {
            'storyId': story_id,
            'images': image_results,
            'status': 'complete',
            'total_images': len(image_results)
        }
        
    async def _enhance_image_prompt(self, scene_text: str) -> str:
        """Use Gemini to create detailed image generation prompt"""
        
        prompt = f"""
        Create a detailed image generation prompt for this children's story scene.
        Make it perfect for AI image generation.
        
        Scene: "{scene_text}"
        
        Guidelines:
        - Child-friendly, whimsical illustration style
        - Bright, warm, inviting colors
        - Safe, positive atmosphere
        - Include specific visual details about characters and setting
        - Describe character appearances (clothing, expressions, poses)
        - Set the scene with background elements
        - Use watercolor or digital painting style
        - Suitable for ages 3-8
        
        Format: One detailed paragraph description for an AI image generator.
        Start with "Children's book illustration:"
        """
        
        try:
            enhanced = await self.gemini.generate(prompt, temperature=0.7, max_tokens=200)
            
            # Clean up the response
            if enhanced.startswith('"') and enhanced.endswith('"'):
                enhanced = enhanced[1:-1]
                
            if not enhanced.startswith("Children's book illustration:"):
                enhanced = f"Children's book illustration: {enhanced}"
                
            return enhanced
            
        except Exception as e:
            print(f"[Illustrator] Error enhancing prompt: {e}")
            # Fallback prompt
            return self._create_fallback_prompt(scene_text)
    
    def _create_fallback_prompt(self, scene_text: str) -> str:
        """Create fallback image prompt"""
        # Extract key elements from scene text
        scene_lower = scene_text.lower()
        
        # Determine setting
        setting = "magical forest"
        if any(word in scene_lower for word in ['park', 'playground']):
            setting = "sunny park"
        elif any(word in scene_lower for word in ['home', 'house', 'room']):
            setting = "cozy home"
        elif any(word in scene_lower for word in ['school', 'classroom']):
            setting = "bright classroom"
        elif any(word in scene_lower for word in ['beach', 'ocean', 'sea']):
            setting = "beautiful beach"
        
        # Determine characters
        characters = "a happy child"
        if any(word in scene_lower for word in ['unicorn', 'horse']):
            characters = "a child with a magical unicorn"
        elif any(word in scene_lower for word in ['dragon']):
            characters = "a child with a friendly dragon"
        elif any(word in scene_lower for word in ['friend', 'friends']):
            characters = "children playing together"
        
        return f"Children's book illustration: {characters} in a {setting}. {scene_text[:50]}... Bright watercolor style, warm colors, child-friendly, whimsical and magical atmosphere."
    
    def _generate_placeholder_url(self, scene_number: int, prompt: str) -> str:
        """Generate placeholder image URL with descriptive text"""
        # Create a descriptive placeholder based on the prompt
        scene_desc = prompt.replace("Children's book illustration: ", "")[:50]
        encoded_desc = scene_desc.replace(" ", "+")
        
        return f"https://via.placeholder.com/800x600/FFE4E1/8B4513?text=Scene+{scene_number}:+{encoded_desc}"
    
    def _generate_thumbnail_url(self, scene_number: int) -> str:
        """Generate thumbnail placeholder URL"""
        colors = ["FFB6C1", "98FB98", "87CEEB", "DDA0DD", "F0E68C"]  # Pastel colors
        color = colors[(scene_number - 1) % len(colors)]
        
        return f"https://via.placeholder.com/200x150/{color}/4A4A4A?text=Scene+{scene_number}"
    
    async def generate_character_avatar(self, character_description: str, child_preferences: Dict) -> Dict[str, str]:
        """Generate avatar for recurring characters"""
        # This would be used for character consistency across stories
        avatar_prompt = await self._create_character_prompt(character_description, child_preferences)
        
        return {
            'character': character_description,
            'prompt': avatar_prompt,
            'avatarUrl': f"https://via.placeholder.com/200x200/FFE4E1/8B4513?text={character_description}",
            'style': 'child-friendly cartoon'
        }
    
    async def _create_character_prompt(self, character: str, preferences: Dict) -> str:
        """Create consistent character appearance prompt"""
        age = preferences.get('age', 5)
        favorite_colors = preferences.get('favoriteColors', ['rainbow'])
        
        prompt = f"""
        Create a character design for a {character} in a children's story.
        
        Character: {character}
        Target age: {age} years old
        Favorite colors: {', '.join(favorite_colors)}
        
        Design a friendly, approachable character that a {age}-year-old would love.
        Include specific details about:
        - Appearance and clothing
        - Facial expression (always happy/kind)
        - Color scheme using the child's favorite colors
        - Any magical or special features
        
        Style: Child-friendly cartoon illustration, soft and warm
        """
        
        try:
            character_design = await self.gemini.generate(prompt, temperature=0.6)
            return f"Character design: {character_design}"
        except:
            return f"Friendly {character} character with warm colors, kind expression, child-friendly cartoon style"