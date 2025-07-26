"""
Emotion Detection Agent - Analyzes child's emotional state
"""
from typing import Dict, Any, List
import asyncio

from tools.gemini_tools import GeminiClient
from config import config

class EmotionDetectorAgent:
    """
    Detects emotions from text and voice inputs.
    Flags potential concerns for parent review.
    """
    
    def __init__(self):
        self.gemini = GeminiClient()
        self.alert_threshold = config.EMOTION_ALERT_THRESHOLD
        
    async def analyze_emotion(self, 
                            text: str,
                            mood: str = 'neutral',
                            audio_features: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze emotional content of child's input.
        
        Returns:
            Dictionary with emotion scores and any alerts
        """
        
        # Text-based emotion analysis
        text_emotions = await self._analyze_text_emotions(text)
        
        # Check for concerning keywords
        concerns = self._check_concerns(text)
        
        # Combine all signals
        combined_emotions = self._combine_emotion_signals(
            text_emotions, mood, audio_features
        )
        
        # Generate alerts if needed
        alerts = self._generate_alerts(combined_emotions, concerns)
        
        result = {
            'emotions': combined_emotions,
            'mood': mood,
            'concerns': concerns,
            'alerts': alerts,
            'requires_parent_review': len(alerts) > 0,
            'overall_sentiment': self._calculate_overall_sentiment(combined_emotions)
        }
        
        print(f"[EmotionDetector] Analysis complete. Alerts: {len(alerts)}, Sentiment: {result['overall_sentiment']}")
        return result
        
    async def _analyze_text_emotions(self, text: str) -> Dict[str, float]:
        """Use Gemini to analyze emotional content"""
        
        prompt = f"""
        Analyze the emotional content of this child's statement.
        Consider their age and be sensitive to subtle emotional cues.
        
        Statement: "{text}"
        
        Score each emotion from 0-1:
        - happiness: joy, excitement, contentment, fun, play
        - sadness: disappointment, loneliness, grief, missing someone
        - fear: worry, anxiety, scared, nervous
        - anger: frustration, annoyance, mad, upset
        - surprise: amazement, confusion, wonder
        - neutral: calm, balanced, matter-of-fact
        
        Also identify any concerning themes like:
        - Bullying or conflict with others
        - Physical hurt or pain
        - Family stress or problems
        - Isolation or loneliness
        
        Respond with just the emotion scores as a simple assessment.
        """
        
        try:
            # For MVP, use rule-based analysis with some Gemini enhancement
            emotions = await self._rule_based_emotion_analysis(text)
            return emotions
        except Exception as e:
            print(f"[EmotionDetector] Error in text analysis: {e}")
            # Fallback to basic analysis
            return self._basic_emotion_analysis(text)
        
    def _rule_based_emotion_analysis(self, text: str) -> Dict[str, float]:
        """Rule-based emotion analysis with keyword matching"""
        text_lower = text.lower()
        emotions = {
            'happiness': 0.0,
            'sadness': 0.0,
            'fear': 0.0,
            'anger': 0.0,
            'surprise': 0.0,
            'neutral': 0.5
        }
        
        # Happiness indicators
        happy_words = ['happy', 'fun', 'play', 'love', 'like', 'good', 'great', 'awesome', 
                      'cool', 'nice', 'laugh', 'smile', 'excited', 'yay', 'wow']
        happiness_score = sum(0.1 for word in happy_words if word in text_lower)
        emotions['happiness'] = min(1.0, happiness_score)
        
        # Sadness indicators
        sad_words = ['sad', 'cry', 'miss', 'lonely', 'hurt', 'upset', 'disappointed']
        sadness_score = sum(0.15 for word in sad_words if word in text_lower)
        emotions['sadness'] = min(1.0, sadness_score)
        
        # Fear indicators
        fear_words = ['scared', 'afraid', 'worry', 'nervous', 'dark', 'monster']
        fear_score = sum(0.15 for word in fear_words if word in text_lower)
        emotions['fear'] = min(1.0, fear_score)
        
        # Anger indicators
        anger_words = ['mad', 'angry', 'hate', 'stupid', 'mean', 'bad']
        anger_score = sum(0.15 for word in anger_words if word in text_lower)
        emotions['anger'] = min(1.0, anger_score)
        
        # Surprise indicators
        surprise_words = ['wow', 'amazing', 'surprised', 'incredible', 'unbelievable']
        surprise_score = sum(0.1 for word in surprise_words if word in text_lower)
        emotions['surprise'] = min(1.0, surprise_score)
        
        # Adjust neutral based on other emotions
        total_emotion = sum(emotions[key] for key in emotions if key != 'neutral')
        emotions['neutral'] = max(0.0, 1.0 - total_emotion)
        
        return emotions
        
    def _basic_emotion_analysis(self, text: str) -> Dict[str, float]:
        """Fallback basic emotion analysis"""
        return {
            'happiness': 0.7,
            'sadness': 0.1,
            'fear': 0.0,
            'anger': 0.0,
            'surprise': 0.2,
            'neutral': 0.0
        }
        
    def _check_concerns(self, text: str) -> List[str]:
        """Check for concerning keywords or phrases"""
        concerns = []
        text_lower = text.lower()
        
        # Check trauma keywords
        for keyword in config.TRAUMA_KEYWORDS:
            if keyword in text_lower:
                concerns.append(f"Mentioned '{keyword}'")
                
        # Check for negative social situations
        bullying_indicators = ['bully', 'mean to me', 'hit me', 'pushed me', 'called me names', 
                              'no one likes', 'everyone hates', 'laughed at me']
        for indicator in bullying_indicators:
            if indicator in text_lower:
                concerns.append("Possible peer conflict or bullying")
                break
                
        # Check for family concerns
        family_stress = ['parents fighting', 'mom and dad angry', 'divorce', 'dad left', 
                        'mom crying', 'yelling at home']
        for stress in family_stress:
            if stress in text_lower:
                concerns.append("Family stress mentioned")
                break
                
        # Check for self-harm or dangerous thoughts
        harm_indicators = ['want to die', 'hurt myself', 'nobody loves me', 'wish I was dead']
        for harm in harm_indicators:
            if harm in text_lower:
                concerns.append("URGENT: Self-harm language detected")
                break
        
        return concerns
        
    def _combine_emotion_signals(self, text_emotions: Dict, mood: str, 
                               audio_features: Dict = None) -> Dict[str, float]:
        """Combine multiple emotion signals"""
        
        # Start with text emotions
        combined = text_emotions.copy()
        
        # Adjust based on selected mood
        mood_adjustments = {
            'happy': {'happiness': 0.2},
            'sad': {'sadness': 0.2},
            'angry': {'anger': 0.2},
            'scared': {'fear': 0.2},
            'excited': {'happiness': 0.15, 'surprise': 0.1},
            'neutral': {}
        }
        
        for emotion, adjustment in mood_adjustments.get(mood, {}).items():
            combined[emotion] = min(1.0, combined.get(emotion, 0) + adjustment)
            
        # Would also incorporate audio features here (pitch, tone, pace)
        if audio_features:
            # Placeholder for audio signal processing
            pass
        
        return combined
        
    def _calculate_overall_sentiment(self, emotions: Dict[str, float]) -> str:
        """Calculate overall sentiment classification"""
        happiness = emotions.get('happiness', 0)
        sadness = emotions.get('sadness', 0)
        fear = emotions.get('fear', 0)
        anger = emotions.get('anger', 0)
        
        if happiness > 0.6:
            return 'positive'
        elif sadness > 0.5 or fear > 0.5 or anger > 0.5:
            return 'negative'
        elif happiness > 0.3:
            return 'mixed_positive'
        else:
            return 'neutral'
        
    def _generate_alerts(self, emotions: Dict[str, float], 
                        concerns: List[str]) -> List[Dict[str, Any]]:
        """Generate alerts for parent review"""
        alerts = []
        
        # High negative emotions
        if emotions.get('sadness', 0) > self.alert_threshold:
            alerts.append({
                'type': 'emotion',
                'severity': 'medium',
                'message': 'Child expressed significant sadness',
                'value': emotions['sadness'],
                'recommendation': 'Consider talking with your child about their feelings'
            })
            
        if emotions.get('fear', 0) > self.alert_threshold:
            alerts.append({
                'type': 'emotion',
                'severity': 'high',
                'message': 'Child expressed fear or anxiety',
                'value': emotions['fear'],
                'recommendation': 'Provide reassurance and discuss their concerns'
            })
            
        if emotions.get('anger', 0) > self.alert_threshold:
            alerts.append({
                'type': 'emotion',
                'severity': 'medium',
                'message': 'Child expressed anger or frustration',
                'value': emotions['anger'],
                'recommendation': 'Help your child identify triggers and coping strategies'
            })
            
        # Concerning content
        if concerns:
            severity = 'critical' if any('URGENT' in concern for concern in concerns) else 'high'
            alerts.append({
                'type': 'content',
                'severity': severity,
                'message': 'Concerning themes detected in child\'s story',
                'details': concerns,
                'recommendation': 'Please review your child\'s input and consider professional guidance if needed'
            })
            
        return alerts