"""
Storyteller Agent - Generates personalized stories using Gemini
"""
from typing import Dict, Any, List
import asyncio
import uuid
from datetime import datetime

from tools.gemini_tools import GeminiClient
from config import config

class StorytellerAgent:
    """
    Creates engaging, educational stories based on child input.
    Incorporates child preferences, educational goals, and safety guidelines.
    """
    
    def __init__(self):
        self.gemini = GeminiClient()
        
    async def generate_story(self, 
                           input_text: str,
                           child_id: str,
                           preferences: Dict[str, Any],
                           educational_focus: List[str],
                           include_elements: List[str],
                           emotion_context: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Generate a complete story with multiple scenes.
        
        Returns:
            Dictionary containing story metadata and scenes
        """
        
        # Build comprehensive prompt
        prompt = self._build_story_prompt(
            input_text, preferences, educational_focus, include_elements, emotion_context
        )
        
        # Generate story
        print(f"[Storyteller] Generating story for child {child_id}")
        story_text = await self.gemini.generate(prompt, temperature=0.8, max_tokens=2000)
        
        # Parse story into scenes
        scenes = self._parse_story_scenes(story_text)
        
        # Create story document
        story_doc = {
            'id': str(uuid.uuid4()),
            'childId': child_id,
            'title': self._extract_title(story_text, scenes),
            'scenes': scenes,
            'metadata': {
                'inputText': input_text,
                'educationalTopics': educational_focus,
                'includedElements': include_elements,
                'emotionContext': emotion_context,
                'createdAt': datetime.now().isoformat()
            },
            'status': 'complete'
        }
        
        print(f"[Storyteller] Generated story '{story_doc['title']}' with {len(scenes)} scenes")
        return story_doc
        
    def _build_story_prompt(self, input_text: str, preferences: Dict, 
                           educational_focus: List[str], include_elements: List[str],
                           emotion_context: Dict = None) -> str:
        """Build comprehensive prompt for story generation"""
        
        # Get child's age for appropriate language
        age = preferences.get('age', 5)
        
        # Build character string
        favorite_chars = preferences.get('favoriteCharacters', [])
        char_string = f"Include these favorite characters: {', '.join(favorite_chars)}" if favorite_chars else ""
        
        # Educational elements
        edu_string = f"Subtly teach about: {', '.join(educational_focus)}" if educational_focus else ""
        
        # Emotion-aware adjustments
        emotion_note = ""
        if emotion_context:
            if emotion_context.get('sadness', 0) > 0.5:
                emotion_note = "The child seems sad, so make the story uplifting and reassuring with positive outcomes."
            elif emotion_context.get('fear', 0) > 0.5:
                emotion_note = "The child seems worried, so make the story calming and safe with brave characters."
            elif emotion_context.get('excitement', 0) > 0.7:
                emotion_note = "The child is excited, so make the story adventurous and fun!"
            
        prompt = f"""
        Create a magical children's story for a {age}-year-old based on this input:
        
        Child's words: "{input_text}"
        
        {char_string}
        {edu_string}
        Include these elements: {', '.join(include_elements)}
        {emotion_note}
        
        Guidelines:
        - Create exactly {config.MIN_STORY_SCENES} short scenes
        - Each scene should be 2-3 sentences max
        - Use simple, age-appropriate language for a {age}-year-old
        - Make it engaging and imaginative
        - Include a gentle lesson or positive message
        - Start each scene with "Scene X:" where X is the scene number
        - Give the story a creative title on the first line
        - Keep it positive and child-friendly
        
        Format:
        Title: [Creative Story Title]
        
        Scene 1: [First scene text - 2-3 sentences]
        
        Scene 2: [Second scene text - 2-3 sentences]
        
        Scene 3: [Third scene text - 2-3 sentences]
        
        Scene 4: [Fourth scene text - 2-3 sentences]
        
        Scene 5: [Fifth scene text - 2-3 sentences with happy ending]
        """
        
        return prompt
        
    def _parse_story_scenes(self, story_text: str) -> List[Dict[str, Any]]:
        """Parse generated story into structured scenes"""
        lines = story_text.strip().split('\n')
        scenes = []
        current_scene = None
        
        for line in lines:
            line = line.strip()
            
            # Skip title line and empty lines
            if line.startswith('Title:') or not line:
                continue
                
            # New scene
            if line.startswith('Scene '):
                if current_scene:
                    scenes.append(current_scene)
                    
                scene_num = len(scenes) + 1
                scene_text = line.split(':', 1)[1].strip() if ':' in line else ''
                current_scene = {
                    'sceneNumber': scene_num,
                    'text': scene_text,
                    'imagePrompt': ''
                }
            elif current_scene and line and not line.startswith('Scene'):
                # Continue current scene
                if current_scene['text']:
                    current_scene['text'] += ' ' + line
                else:
                    current_scene['text'] = line
                
        # Add last scene
        if current_scene:
            scenes.append(current_scene)
            
        # Generate image prompts for each scene
        for scene in scenes:
            scene['imagePrompt'] = self._create_image_prompt(scene['text'])
            
        # Ensure we have at least minimum scenes
        while len(scenes) < config.MIN_STORY_SCENES:
            scenes.append({
                'sceneNumber': len(scenes) + 1,
                'text': 'And they all lived happily ever after!',
                'imagePrompt': 'Happy ending with all characters celebrating together'
            })
            
        return scenes[:config.MAX_STORY_SCENES]  # Cap at maximum
        
    def _create_image_prompt(self, scene_text: str) -> str:
        """Create image generation prompt from scene text"""
        return f"Children's book illustration: {scene_text[:100]}... Soft, colorful, friendly watercolor style for kids."
        
    def _extract_title(self, story_text: str, scenes: List[Dict]) -> str:
        """Extract or generate story title"""
        lines = story_text.strip().split('\n')
        for line in lines:
            if line.startswith('Title:'):
                return line.split(':', 1)[1].strip()
        
        # Fallback title generation
        if scenes and len(scenes) > 0:
            first_scene = scenes[0]['text']
            if 'adventure' in first_scene.lower():
                return "The Great Adventure"
            elif 'friend' in first_scene.lower():
                return "A Special Friendship"
            elif 'magic' in first_scene.lower():
                return "The Magical Journey"
        
        return "My Special Story"