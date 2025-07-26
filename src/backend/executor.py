"""
Executes planned tasks using Gemini API and other tools.
Required for hackathon - demonstrates tool calling and orchestration.
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime

from config import config
from agents.storyteller import StorytellerAgent
from agents.emotion_detector import EmotionDetectorAgent
from agents.illustrator import IllustratorAgent
from memory import Memory

class Executor:
    """
    Executes tasks planned by the Planner.
    Manages agent lifecycle and result aggregation.
    """
    
    def __init__(self):
        # Initialize all agents
        self.agents = {
            'storyteller': StorytellerAgent(),
            'emotion_detector': EmotionDetectorAgent(),
            'illustrator': IllustratorAgent(),
            'memory': Memory()
        }
        self.results = {}
        
    async def execute(self, tasks: List[Any]) -> Dict[str, Any]:
        """
        Execute tasks respecting dependencies and priorities.
        
        Args:
            tasks: List of Task objects from planner
            
        Returns:
            Dictionary of results from all executed tasks
        """
        # Sort tasks by priority
        sorted_tasks = sorted(tasks, key=lambda x: x.priority)
        
        # Track completed tasks
        completed = set()
        results = {}
        
        # Execute tasks
        for task in sorted_tasks:
            # Check dependencies
            if task.depends_on:
                await self._wait_for_dependencies(task.depends_on, completed)
            
            # Execute task
            print(f"[Executor] Running {task.agent}.{task.action}")
            start_time = datetime.now()
            
            try:
                agent = self.agents.get(task.agent)
                if not agent:
                    raise ValueError(f"Unknown agent: {task.agent}")
                
                # Get the method and execute
                method = getattr(agent, task.action)
                
                # Update params with results from dependencies
                if task.depends_on:
                    task.params = self._inject_dependency_results(
                        task.params, task.depends_on, results
                    )
                
                # Execute the task
                result = await method(**task.params)
                
                # Store result
                results[task.task_id] = result
                results[f"{task.agent}_{task.action}"] = result
                
                # Mark as completed
                completed.add(task.task_id)
                
                duration = (datetime.now() - start_time).total_seconds()
                print(f"[Executor] Completed {task.agent}.{task.action} in {duration:.2f}s")
                
            except Exception as e:
                print(f"[Executor] Error in {task.agent}.{task.action}: {str(e)}")
                results[task.task_id] = {'error': str(e)}
                
        # Compile final results
        return self._compile_results(results)
    
    async def _wait_for_dependencies(self, dependencies: List[str], completed: set):
        """Wait for dependent tasks to complete"""
        while not all(dep in completed for dep in dependencies):
            await asyncio.sleep(0.1)
    
    def _inject_dependency_results(self, params: Dict, dependencies: List[str], 
                                  results: Dict) -> Dict:
        """Inject results from dependent tasks into params"""
        # Update params based on dependency results
        for dep_id in dependencies:
            if dep_id in results:
                dep_result = results[dep_id]
                # Smart parameter injection based on result type
                if 'transcript' in dep_result:
                    params['input_text'] = dep_result['transcript']
                if 'emotions' in dep_result:
                    params['emotion_context'] = dep_result['emotions']
                if 'preferences' in dep_result:
                    params['preferences'] = dep_result['preferences']
        return params
    
    def _compile_results(self, results: Dict) -> Dict[str, Any]:
        """Compile all results into final response"""
        compiled = {
            'timestamp': datetime.now().isoformat(),
            'status': 'complete'
        }
        
        # Extract key results
        if 'storyteller_generate_story' in results:
            compiled['story'] = results['storyteller_generate_story']
            
        if 'emotion_detector_analyze_emotion' in results:
            compiled['emotions'] = results['emotion_detector_analyze_emotion']
            
        if 'illustrator_create_scene_images' in results:
            compiled['illustrations'] = results['illustrator_create_scene_images']
            
        return compiled