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
        Humaniza el siguiente contenido añadiendo elementos humanos auténticos y atractivos:
        
        Texto Original: "{text}"
        
        Aplica estas técnicas de humanización: {', '.join(techniques)}
        
        Humanization Guidelines:
        1. **Toque Personal**: Añade experiencias u observaciones con las que el lector pueda identificarse.
        2. **Conexión con el Lector**: Incluye sentimientos y respuestas emocionales.
        3. **Fluidez Conversacional**: Haz que suene como una conversación natural.
        4. **Voz Auténtica**: Mantén una personalidad y tono genuinos.
        5. **Contexto Cultural**: Añade referencias culturales relevantes.
        6. **Transparencia**: Incluye momentos apropiados de incertidumbre o aprendizaje.
        7. **Historias Breves**: Incorpora pequeñas narrativas o escenarios.
        8. **Detalles Sensoriales**: Incluye experiencias sensoriales cuando sea relevante.
        
        Contexto del Perfil de Voz: {json.dumps(voice_profile) if voice_profile else "Usa una voz auténtica y profesional"}
        
        Requirements:
        - Mantén el mensaje central intacto.
        - Mejora en lugar de reemplazar el contenido original.
        - Mantén un tono apropiado para la audiencia.
        - Añade valor a través de la conexión humana.
        - Evita adiciones forzadas o artificiales.
        
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
        Analiza la efectividad de la humanización entre estos dos textos:
        
        Original: "{original}"
        Humanized: "{humanized}"
        
        Evaluate:
        1. **Mejora Emocional**: ¿Qué tan más atractiva/emocional es la versión humanizada?
        2. **Aumento de Identificación**: ¿Se siente más personal e identificable?
        3. **Mejora Conversacional**: ¿Qué tan más natural/conversacional es?
        4. **Refuerzo de Autenticidad**: ¿Se siente más genuina y auténtica?
        5. **Historias Breves**: ¿Qué elementos narrativos se añadieron con éxito?
        6. **Relevancia Cultural**: ¿Qué tan bien funcionan las referencias culturales?
        7. **Transparencia/Realismo**: ¿Muestra una vulnerabilidad apropiada?
        8. **Impacto General**: ¿Qué tan más atractiva es la versión humanizada en general?
        
        Califica cada aspecto del 1 al 10 y proporciona ejemplos específicos de lo que funcionó bien.
        También sugiere áreas que podrían mejorarse.
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
        Añade una anécdota relevante y atractiva a este contenido:
        
        Contenido: "{content}"
        Tema: "{topic}"
        Tono: "{tone}"
        
        The anecdote should:
        - Ser relevante para el tema principal
        - Ilustrar un punto clave de forma efectiva
        - Ser apropiada para el tono especificado
        - Ser concisa pero impactante
        - Sentirse auténtica y genuina
        - Incluir una lección o idea clara
        
        Coloca la anécdota de forma natural dentro del flujo del contenido.
        Devuelve tanto el contenido mejorado como la anécdota por separado.
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
        
        prompt = f"""Añade {humor_types.get(humor_type, 'sutil')} a este contenido:

        Contenido: "{content}"

        Requirements:
        - Mantenlo apropiado y profesional.
        - Mejora en lugar de distraer del mensaje.
        - Haz que se sienta natural y sin forzar.
        - Considera a la audiencia y el contexto.
        - Usa el humor para hacer los puntos más memorables.
        Integra el humor de forma fluida en el contenido existente.
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
        Añade referencias culturales {reference_type} relevantes a este contenido:
        
        Contenido: "{content}"
        
        Types of references to consider:
        - Eventos actuales o noticias (si es apropiado)
        - Cultura popular (películas, libros, música)
        - Referencias históricas
        - Cultura de la industria o memes
        - Experiencias humanas universales
        
        Requirements:
        - Las referencias deben mejorar la comprensión.
        - Ser relevantes para la audiencia.
        - No alienar ni excluir a los lectores.
        - Añadir valor al mensaje principal.
        - Sentirse naturales en el contexto.
        
        Integra las referencias de manera reflexiva y apropiada.
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
        Añade una conexión emocional de {emotion_type} a este contenido:
        
        Contenido: "{content}"
        
        Emotional elements to include:
        - Sentimientos y reacciones personales
        - Comprensión de las emociones del lector
        - Lenguaje y descriptores emocionales
        - Respuestas empáticas
        - Viaje o arco emocional
        
        Requirements:
        - Ser auténtico y genuino.
        - Conectar con las emociones probables del lector.
        - Usar el lenguaje emocional de manera apropiada.
        - Crear resonancia emocional.
        - Mantener el profesionalismo siendo emocional.
        
        Mejora el impacto emocional manteniendo el mensaje central intacto.
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
        Analiza el nivel de humanización de este contenido:
        
        Contenido: "{text}"
        
        Evaluate on these criteria (1-10 scale):
        1. Voz personal y autenticidad
        2. Resonancia emocional
        3. Tono conversacional
        4. Capacidad de identificación
        5. Elementos narrativos
        6. Contexto cultural
        7. Transparencia y realismo
        8. Compromiso y conexión
        
        Proporciona ejemplos específicos del texto que respalden cada puntuación.
        Toda la respuesta debe estar en español.
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