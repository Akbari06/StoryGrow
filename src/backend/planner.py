"""
Master orchestrator that breaks down user goals into subtasks.
Required for hackathon - demonstrates agent planning pattern.
"""
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

from config import config
from tools.gemini_tools import GeminiClient

@dataclass
class Task:
    """Represents a single task for an agent to execute"""
    task_id: str
    agent: str
    action: str
    params: Dict[str, Any]
    priority: int
    depends_on: Optional[List[str]] = None

class Planner:
    """
    Plans and coordinates all agent activities.
    Implements the ReAct (Reasoning + Acting) pattern.
    """
    
    def __init__(self):
        self.gemini = GeminiClient()
        self.task_counter = 0
        
    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        self.task_counter += 1
        return f"task_{datetime.now().timestamp()}_{self.task_counter}"
    
    async def plan(self, user_input: Dict[str, Any]) -> List[Task]:
        """
        Break down story creation request into subtasks.
        
        Args:
            user_input: Contains audio_url/text_input, child_id, mood, context
            
        Returns:
            List of tasks to execute in order
        """
        tasks = []
        
        # Task 1: Process input (audio or text)
        if user_input.get('audio_url'):
            transcribe_task = Task(
                task_id=self._generate_task_id(),
                agent='transcriber',
                action='transcribe_audio',
                params={'audio_url': user_input['audio_url']},
                priority=1
            )
            tasks.append(transcribe_task)
            input_task_id = transcribe_task.task_id
        else:
            input_task_id = None
            
        # Task 2: Analyze emotion
        emotion_task = Task(
            task_id=self._generate_task_id(),
            agent='emotion_detector',
            action='analyze_emotion',
            params={
                'text': user_input.get('text_input', ''),
                'mood': user_input.get('session_mood', 'neutral'),
                'audio_features': user_input.get('audio_features', {})
            },
            priority=2,
            depends_on=[input_task_id] if input_task_id else None
        )
        tasks.append(emotion_task)
        
        # Task 3: Retrieve child context and memories
        memory_task = Task(
            task_id=self._generate_task_id(),
            agent='memory',
            action='get_child_context',
            params={'child_id': user_input['child_id']},
            priority=2
        )
        tasks.append(memory_task)
        
        # Task 4: Generate story
        story_task = Task(
            task_id=self._generate_task_id(),
            agent='storyteller',
            action='generate_story',
            params={
                'input_text': user_input.get('text_input', ''),
                'child_id': user_input['child_id'],
                'preferences': {},  # Will be filled by memory task
                'educational_focus': user_input.get('educational_focus', []),
                'include_elements': user_input.get('include_elements', [])
            },
            priority=3,
            depends_on=[emotion_task.task_id, memory_task.task_id]
        )
        tasks.append(story_task)
        
        # Task 5: Generate illustrations
        illustrate_task = Task(
            task_id=self._generate_task_id(),
            agent='illustrator',
            action='create_scene_images',
            params={'story_id': None},  # Will be filled after story generation
            priority=4,
            depends_on=[story_task.task_id]
        )
        tasks.append(illustrate_task)
        
        # Log the plan
        print(f"[Planner] Created {len(tasks)} tasks for story generation")
        for task in tasks:
            print(f"  - {task.agent}.{task.action} (priority: {task.priority})")
            
        return tasks
    
    async def plan_quest(self, quest_input: Dict[str, Any]) -> List[Task]:
        """Plan tasks for quest/chore gamification"""
        # Implementation for quest planning
        pass