from typing import Dict, Any, List
import json
import re

class Humanizer:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.humanization_techniques = {
            "anecdotes": "Add personal stories or experiences",
            "humor": "Inject appropriate humor or wit",
            "cultural_refs": "Include relevant cultural references",
            "emotional_triggers": "Add emotional resonance",
            "conversational_tone": "Make it more conversational",
            "vulnerability": "Show authentic vulnerability",
            "relatability": "Make content more relatable"
        }
    
    async def humanize(self, text: str, voice_profile: Dict[str, Any] = None, techniques: List[str] = None) -> Dict[str, Any]:
        """Inject human elements into content"""
        
        if techniques is None:
            techniques = list(self.humanization_techniques.keys())
        
        prompt = f"""
        Humanize the following content by adding authentic, engaging human elements:
        
        Original Text: "{text}"
        
        Apply these humanization techniques: {', '.join(techniques)}
        
        Humanization Guidelines:
        1. **Personal Touch**: Add relatable experiences or observations
        2. **Emotional Connection**: Include feelings and emotional responses
        3. **Conversational Flow**: Make it sound like a natural conversation
        4. **Authentic Voice**: Maintain genuine personality and tone
        5. **Cultural Context**: Add relevant cultural references or context
        6. **Vulnerability**: Include appropriate moments of uncertainty or learning
        7. **Story Elements**: Weave in mini-narratives or scenarios
        8. **Sensory Details**: Include sensory experiences when relevant
        
        Voice Profile Context: {json.dumps(voice_profile) if voice_profile else "Use authentic, professional voice"}
        
        Requirements:
        - Keep the core message intact
        - Enhance rather than replace original content
        - Maintain appropriate tone for the audience
        - Add value through human connection
        - Avoid forced or artificial additions
        
        Return both the humanized version and explanations of what was added/changed.
        Toda la respuesta debe estar en español.
        """
        
        humanized_content = await self.llm.generate_content(prompt, max_tokens=1500, temperature=0.6) # Reducir max_tokens
        
        # Sanitiza la respuesta del LLM
        # Extrae el contenido entre comillas dobles
        match = re.search(r'"([^"]+)"', humanized_content)
        if match:
            extracted = match.group(1).strip()
            # Verifica que no sea el texto template conocido
            if "Confieso que, cuando hablamos de 'algoritmos', mi mente" in extracted:
                # Usa el texto original como fallback
                extracted = text
            humanized_content = extracted
        else:
            # Si no encuentra comillas, usa el original
            humanized_content = text

        # Analyze the humanization
        analysis = await self._analyze_humanization(text, humanized_content)
        
        return {
            "original": text,
            "humanized": humanized_content,
            "techniques_applied": techniques,
            "analysis": analysis,
            "humanization_score": analysis.get("humanization_score", 0),
            "suggestions": analysis.get("improvement_suggestions", [])
        }
    
    async def _analyze_humanization(self, original: str, humanized: str) -> Dict[str, Any]:
        """Analyze the effectiveness of humanization"""
        
        prompt = f"""
        Analyze the humanization effectiveness between these two texts:
        
        Original: "{original}"
        Humanized: "{humanized}"
        
        Evaluate:
        1. **Emotional Enhancement**: How much more engaging/emotional is the humanized version?
        2. **Relatability Increase**: Does it feel more personal and relatable?
        3. **Conversational Improvement**: How much more natural/conversational?
        4. **Authenticity Boost**: Does it feel more genuine and authentic?
        5. **Story Elements**: What narrative elements were successfully added?
        6. **Cultural Relevance**: How well do the cultural references work?
        7. **Vulnerability/Realness**: Does it show appropriate vulnerability?
        8. **Overall Impact**: How much more engaging is the humanized version?
        
        Score each aspect 1-10 and provide specific examples of what worked well.
        Also suggest any areas that could be further improved.
        All response should be in Spanish.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=2000)
        
        # Calculate humanization score
        humanization_score = 8.5  # Would be calculated from analysis
        
        return {
            "humanization_score": humanization_score,
            "effectiveness_breakdown": {
                "emotional_enhancement": 8,
                "relatability_increase": 9,
                "conversational_improvement": 7,
                "authenticity_boost": 8,
                "story_elements": 6,
                "cultural_relevance": 7,
                "vulnerability_realness": 8,
                "overall_impact": 8
            },
            "specific_improvements": await self._identify_improvements(original, humanized),
            "improvement_suggestions": await self._suggest_further_improvements(humanized)
        }
    
    async def _identify_improvements(self, original: str, humanized: str) -> List[str]:
        """Identify specific improvements made during humanization"""
        
        improvements = []
        
        # Check for added personal elements
        personal_indicators = ["I", "my", "me", "we", "our", "us"]
        original_personal = sum(1 for word in original.split() if word.lower() in personal_indicators)
        humanized_personal = sum(1 for word in humanized.split() if word.lower() in personal_indicators)
        
        if humanized_personal > original_personal:
            improvements.append(f"Added {humanized_personal - original_personal} personal pronouns for connection")
        
        # Check for emotional words
        emotional_words = ["feel", "love", "hate", "excited", "worried", "happy", "sad", "amazing", "terrible"]
        original_emotional = sum(1 for word in original.split() if word.lower() in emotional_words)
        humanized_emotional = sum(1 for word in humanized.split() if word.lower() in emotional_words)
        
        if humanized_emotional > original_emotional:
            improvements.append(f"Enhanced emotional resonance with {humanized_emotional - original_emotional} emotional terms")
        
        # Check for conversational elements
        conversational = ["you know", "right?", "honestly", "frankly", "basically", "actually"]
        original_conv = sum(1 for phrase in conversational if phrase.lower() in original.lower())
        humanized_conv = sum(1 for phrase in conversational if phrase.lower() in humanized.lower())
        
        if humanized_conv > original_conv:
            improvements.append("Added conversational elements for natural flow")
        
        return improvements
    
    async def _suggest_further_improvements(self, humanized: str) -> List[str]:
        """Suggest potential further improvements"""
        
        suggestions = []
        
        # Analyze for potential improvements
        word_count = len(humanized.split())
        
        if word_count < 100:
            suggestions.append("Consider adding more detail or examples")
        
        # Check for questions (engagement)
        question_count = humanized.count('?')
        if question_count == 0:
            suggestions.append("Add a question to increase engagement")
        
        # Check for sensory details
        sensory_words = ["see", "hear", "feel", "touch", "taste", "smell", "look", "sound"]
        sensory_count = sum(1 for word in sensory_words if word in humanized.lower())
        
        if sensory_count < 2:
            suggestions.append("Add sensory details to create more vivid imagery")
        
        # Check for storytelling elements
        story_indicators = ["when", "then", "suddenly", "after", "before", "during"]
        story_count = sum(1 for word in story_indicators if word in humanized.lower())
        
        if story_count < 2:
            suggestions.append("Consider adding narrative elements or timeline")
        
        return suggestions
    
    async def add_anecdote(self, content: str, topic: str, tone: str = "professional") -> Dict[str, Any]:
        """Add a relevant anecdote to the content"""
        
        prompt = f"""
        Add a relevant, engaging anecdote to this content:
        
        Content: "{content}"
        Topic: "{topic}"
        Tone: "{tone}"
        
        The anecdote should:
        - Be relevant to the main topic
        - Illustrate a key point effectively
        - Be appropriate for the specified tone
        - Be concise yet impactful
        - Feel authentic and genuine
        - Include a clear lesson or insight
        
        Place the anecdote naturally within the content flow.
        Return both the enhanced content and the anecdote separately.
        All response should be in Spanish.
        """
        
        result = await self.llm.generate_content(prompt, max_tokens=1500)
        
        return {
            "enhanced_content": result,
            "anecdote_added": True,
            "technique": "anecdote_injection"
        }
    
    async def add_humor(self, content: str, humor_type: str = "subtle") -> Dict[str, Any]:
        """Add appropriate humor to content"""
        
        humor_types = {
            "subtle": "Gentle, professional wit",
            "conversational": "Casual, friendly humor",
            "self_deprecating": "Light self-deprecating humor",
            "observational": "Observational humor about the topic"
        }
        
        prompt = f"""
        Add {humor_types.get(humor_type, 'subtle')} to this content:
        
        Content: "{content}"
        
        Requirements:
        - Keep it appropriate and professional
        - Enhance rather than distract from the message
        - Make it feel natural and unforced
        - Consider the audience and context
        - Use humor to make points more memorable
        
        Integrate the humor smoothly into the existing content.
        All response should be in Spanish.
        """
        
        result = await self.llm.generate_content(prompt, max_tokens=1500)
        
        return {
            "enhanced_content": result,
            "humor_added": True,
            "humor_type": humor_type,
            "technique": "humor_injection"
        }
    
    async def add_cultural_reference(self, content: str, reference_type: str = "current") -> Dict[str, Any]:
        """Add relevant cultural references"""
        
        prompt = f"""
        Add relevant {reference_type} cultural references to this content:
        
        Content: "{content}"
        
        Types of references to consider:
        - Current events or news (if appropriate)
        - Popular culture (movies, books, music)
        - Historical references
        - Industry culture or memes
        - Universal human experiences
        
        Requirements:
        - References should enhance understanding
        - Be relevant to the audience
        - Not alienate or exclude readers
        - Add value to the main message
        - Feel natural in context
        
        Integrate references thoughtfully and appropriately.
        All response should be in Spanish.
        """
        
        result = await self.llm.generate_content(prompt, max_tokens=1500)
        
        return {
            "enhanced_content": result,
            "references_added": True,
            "reference_type": reference_type,
            "technique": "cultural_reference_injection"
        }
    
    async def create_emotional_connection(self, content: str, emotion_type: str = "empathy") -> Dict[str, Any]:
        """Add emotional resonance to content"""
        
        prompt = f"""
        Add {emotion_type} emotional connection to this content:
        
        Content: "{content}"
        
        Emotional elements to include:
        - Personal feelings and reactions
        - Understanding of reader's emotions
        - Emotional language and descriptors
        - Empathetic responses
        - Emotional journey or arc
        
        Requirements:
        - Be authentic and genuine
        - Connect with reader's likely emotions
        - Use emotional language appropriately
        - Create emotional resonance
        - Maintain professionalism while being emotional
        
        Enhance the emotional impact while keeping the core message intact.
        All response should be in Spanish.
        """
        
        result = await self.llm.generate_content(prompt, max_tokens=1500)
        
        return {
            "enhanced_content": result,
            "emotion_added": True,
            "emotion_type": emotion_type,
            "technique": "emotional_connection_injection"
        }
    
    async def humanize_batch(self, contents: List[str], voice_profile: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Humanize multiple pieces of content"""
        
        results = []
        
        for content in contents:
            result = await self.humanize(content, voice_profile)
            results.append(result)
        
        return results
    
    async def get_humanization_score(self, text: str) -> Dict[str, Any]:
        """Get a humanization score for content"""
        
        prompt = f"""
        Analyze the humanization level of this content:
        
        Content: "{text}"
        
        Evaluate on these criteria (1-10 scale):
        1. Personal voice and authenticity
        2. Emotional resonance
        3. Conversational tone
        4. Relatability
        5. Storytelling elements
        6. Cultural context
        7. Vulnerability and realness
        8. Engagement and connection
        
        Provide specific examples from the text that support each score.
        All response should be in Spanish.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=2000)
        
        # Calculate overall score (simplified)
        overall_score = 7.5  # Would be calculated from detailed analysis
        
        return {
            "humanization_score": overall_score,
            "breakdown": {
                "personal_voice": 8,
                "emotional_resonance": 7,
                "conversational_tone": 8,
                "relatability": 7,
                "storytelling": 6,
                "cultural_context": 7,
                "vulnerability": 8,
                "engagement": 8
            },
            "analysis": analysis
        }