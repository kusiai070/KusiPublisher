from typing import Dict, Any, List
import json

class PlatformAgents:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.platform_specs = {
            "linkedin": {
                "max_chars": 3000,
                "ideal_chars": 150,
                "hashtag_limit": 5,
                "tone": "professional",
                "features": ["articles", "posts", "polls", "documents"],
                "best_practices": [
                    "Use professional language and tone",
                    "Include industry insights and data",
                    "Ask thought-provoking questions",
                    "Share personal experiences related to business",
                    "Use 3-5 relevant hashtags",
                    "Post during business hours (9 AM - 5 PM)",
                    "Include a clear call-to-action"
                ]
            },
            "twitter": {
                "max_chars": 280,
                "ideal_chars": 100,
                "hashtag_limit": 2,
                "tone": "conversational",
                "features": ["tweets", "threads", "polls", "spaces"],
                "best_practices": [
                    "Keep it concise and engaging",
                    "Use trending hashtags when relevant",
                    "Ask questions to encourage replies",
                    "Share quick insights and tips",
                    "Use thread for longer content",
                    "Engage with others in your industry",
                    "Post multiple times throughout the day"
                ]
            },
            "instagram": {
                "max_chars": 2200,
                "ideal_chars": 138,
                "hashtag_limit": 30,
                "tone": "visual_storytelling",
                "features": ["posts", "stories", "reels", "igtv"],
                "best_practices": [
                    "Focus on visual storytelling",
                    "Use emojis to add personality",
                    "Tell stories in captions",
                    "Use up to 30 hashtags (mix of popular and niche)",
                    "Post high-quality images or videos",
                    "Use Instagram Stories for behind-the-scenes",
                    "Engage with your community regularly"
                ]
            },
            "facebook": {
                "max_chars": 5000,
                "ideal_chars": 80,
                "hashtag_limit": 5,
                "tone": "community_focused",
                "features": ["posts", "stories", "live", "groups"],
                "best_practices": [
                    "Create content that sparks conversation",
                    "Use Facebook Live for real-time engagement",
                    "Share a mix of content types",
                    "Use Facebook Groups for community building",
                    "Post when your audience is most active",
                    "Respond to comments and messages quickly",
                    "Use Facebook's native video feature"
                ]
            },
            "blog": {
                "max_chars": 50000,
                "ideal_chars": 1500,
                "hashtag_limit": 0,
                "tone": "educational",
                "features": ["articles", "guides", "tutorials", "reviews"],
                "best_practices": [
                    "Write comprehensive, in-depth content",
                    "Use proper SEO optimization",
                    "Include relevant images and media",
                    "Use clear headings and subheadings",
                    "Add internal and external links",
                    "Include a strong call-to-action",
                    "Optimize for mobile reading"
                ]
            }
        }
    
    async def optimize_for_platform(self, content: str, platform: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Optimize content for a specific platform"""
        
        if platform not in self.platform_specs:
            return {"error": f"Unsupported platform: {platform}"}
        
        specs = self.platform_specs[platform]
        
        prompt = f"""
        Analyze the original content and generate a new, optimized version for the {platform} platform.
        
        # ORIGINAL CONTENT
        "{content}"
        
        # PLATFORM GUIDELINES
        - Tone: {specs['tone']}
        - Ideal Length: Approximately {specs['ideal_chars']} characters.
        - Character Limit: Do not exceed {specs['max_chars']} characters.
        - Hashtags: Use up to {specs['hashtag_limit']} relevant hashtags.
        
        # RESPONSE FORMAT
        You must provide your response as a single, valid JSON object with two keys: "explanations" and "optimized_content".
        - "explanations": A string briefly explaining the changes made.
        - "optimized_content": A string containing only the final, optimized content, ready to be posted.

        The JSON object should be the *only* content in your response. Do not include any preambles, additional text, or markdown outside of the JSON structure itself.
        All text within the JSON response, including explanations and content, must be in Spanish.
        """
        
        # Ajustar parámetros según plataforma
        if platform == 'blog':
            max_tokens_llm = 8000
            temperature_llm = 0.7
        else:
            max_tokens_llm = 2000
            temperature_llm = 0.5
        response_text = await self.llm.generate_content(prompt, max_tokens=max_tokens_llm, temperature=temperature_llm)
        
        # --- INICIO: Pre-procesamiento para limpiar markdown de la respuesta de Gemini (Solución Claude) ---
        # Eliminar posibles envoltorios de ```json o ``` del inicio y fin
        if response_text.strip().startswith('```') and response_text.strip().endswith('```'):
            response_text = response_text.strip()[3:-3].strip() # Remover ``` del inicio y fin
            if response_text.startswith('json'): # Si después de remover ```, empieza con 'json', quitarlo
                response_text = response_text[4:].strip()
        # --- FIN: Pre-procesamiento ---
        
        # Procesar la respuesta JSON del LLM de forma robusta
        optimized_content = response_text # Fallback por defecto
        explanations = "Error al procesar la respuesta de la IA." # Fallback por defecto
        
        try:
            import re
            # Primero, intentar encontrar el JSON envuelto en bloques de código markdown
            json_match = re.search(r'```json\n(.*?)```', response_text, re.DOTALL)
            if not json_match:
                # Si no se encuentra markdown, buscar el primer y último corchete para extraer el JSON
                json_match = re.search(r'\{(.*?)\}', response_text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
                data = json.loads(json_str)
                optimized_content = data.get("optimized_content", response_text)
                explanations = data.get("explanations", "No se proporcionaron explicaciones.")
            else:
                print(f"--- DEBUG: RAW RESPONSE para {platform} (primeros 500 chars): {response_text[:500]} ---")
                print(f"--- WARNING: No se encontró un objeto JSON estructurado en la respuesta del LLM para {platform}. Usando texto crudo. ---")
                optimized_content = response_text
                explanations = "No se encontró JSON estructurado en la respuesta."
        
        except json.JSONDecodeError as e:
            print(f"--- WARNING: Fallo al decodificar JSON de la respuesta del LLM para {platform}. Usando texto crudo. Error: {e} ---")
            optimized_content = response_text
            explanations = f"Fallo al decodificar JSON: {e}"
        except Exception as e: # Capturar cualquier otro error inesperado durante el parseo
            print(f"--- WARNING: Error inesperado al procesar la respuesta del LLM para {platform}. Usando texto crudo. Error: {e} ---")
            optimized_content = response_text
            explanations = f"Error inesperado al procesar: {e}"

        # --- INICIO: Post-procesamiento final para limpiar optimized_content si el JSON falló ---
        # Si optimized_content todavía es la respuesta cruda de la IA (posiblemente JSON malformado o envuelto)
        if isinstance(optimized_content, str):
            # Intentar limpiar el wrapper ```json de nuevo si está presente
            match_json_wrapper = re.search(r'```json\n(.*?)```', optimized_content, re.DOTALL)
            if match_json_wrapper:
                try:
                    # Si logramos extraer y parsear, usar ese contenido
                    temp_data = json.loads(match_json_wrapper.group(1))
                    optimized_content = temp_data.get("optimized_content", optimized_content)
                    explanations = temp_data.get("explanations", explanations)
                except json.JSONDecodeError:
                    # Si el JSON interno sigue siendo inválido, al menos quitar el wrapper
                    optimized_content = match_json_wrapper.group(1).strip()
            elif optimized_content.strip().startswith('{') and optimized_content.strip().endswith('}'):
                # Si parece un JSON puro (sin wrapper) pero falló antes, intentar parsear
                try:
                    temp_data = json.loads(optimized_content)
                    optimized_content = temp_data.get("optimized_content", optimized_content)
                    explanations = temp_data.get("explanations", explanations)
                except json.JSONDecodeError:
                    pass # No hacer nada si sigue siendo inválido, mantener el texto actual
            
            # Un último intento de limpieza si aún hay caracteres extra al inicio/fin
            optimized_content = optimized_content.strip()
            explanations = explanations.strip()
        print(f"--- DEBUG: optimized_content final para {platform}: '{optimized_content}' (length: {len(optimized_content)}) ---")
        # --- FIN: Post-procesamiento final ---
                        
        # Analyze the optimization
        analysis = await self._analyze_optimization(content, optimized_content, platform)
        
        return {
            "platform": platform,
            "original_content": content,
            "optimized_content": optimized_content,
            "explanations": explanations,
            "analysis": analysis,
            "character_count": len(optimized_content),
            "within_limits": len(optimized_content) <= specs['max_chars'],
            "optimization_score": analysis.get("optimization_score", 0),
            "recommendations": analysis.get("recommendations", [])
        }
    
    async def _analyze_optimization(self, original: str, optimized: str, platform: str) -> Dict[str, Any]:
        """Analyze the quality of platform optimization"""
        
        specs = self.platform_specs[platform]
        
        prompt = f"""
        Analyze the platform optimization between these two versions:
        
        Original: "{original}"
        Optimized: "{optimized}"
        Platform: {platform}
        
        Evaluate:
        1. Length appropriateness for platform
        2. Tone alignment with platform expectations
        3. Use of platform-specific features
        4. Engagement potential on this platform
        5. Hashtag usage and effectiveness (if applicable)
        6. Call-to-action clarity and effectiveness
        7. Visual elements suggestions
        8. Timing recommendations for posting
        
        Score each aspect 1-10 and provide specific improvement suggestions.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=1500)
        
        return {
            "optimization_score": 8.5,  # Would be calculated from analysis
            "length_analysis": {
                "original_length": len(original),
                "optimized_length": len(optimized),
                "platform_limit": specs['max_chars'],
                "within_limit": len(optimized) <= specs['max_chars'],
                "ideal_length": len(optimized) <= specs['ideal_chars'] * 1.2
            },
            "tone_alignment": 9,  # Platform-appropriate tone
            "feature_usage": 8,   # Use of platform features
            "engagement_potential": 8.5,
            "analysis_details": analysis,
            "recommendations": await self._generate_optimization_recommendations(optimized, platform)
        }
    
    async def _generate_optimization_recommendations(self, content: str, platform: str) -> List[str]:
        """Generate specific recommendations for platform optimization"""
        
        recommendations = []
        specs = self.platform_specs[platform]
        
        # Length-based recommendations
        if len(content) > specs['max_chars']:
            recommendations.append(f"Content exceeds {platform} character limit by {len(content) - specs['max_chars']} characters")
        elif len(content) > specs['ideal_chars'] * 1.5:
            recommendations.append(f"Consider shortening content for better engagement on {platform}")
        
        # Platform-specific recommendations
        if platform == "twitter":
            hashtag_count = content.count('#')
            if hashtag_count > specs['hashtag_limit']:
                recommendations.append(f"Reduce hashtags to {specs['hashtag_limit']} or fewer for better engagement")
            if len(content) > 240:
                recommendations.append("Consider using a thread for longer content")
        
        elif platform == "linkedin":
            if "professional" not in content.lower() and "business" not in content.lower():
                recommendations.append("Add more professional or business-oriented language")
            if content.count('?') == 0:
                recommendations.append("Add a question to encourage engagement")
        
        elif platform == "instagram":
            if content.count('#') < 5:
                recommendations.append("Add more hashtags to increase discoverability")
            if content.count('🎨') + content.count('📸') + content.count('✨') == 0:
                recommendations.append("Consider adding visual emojis to enhance the post")
        
        return recommendations
    
    async def generate_hashtags(self, content: str, platform: str, count: int = None) -> List[str]:
        """Generate relevant hashtags for content and platform"""
        
        if count is None:
            count = self.platform_specs[platform]['hashtag_limit']
        
        prompt = f"""
        Generate {count} relevant hashtags for this content on {platform}:
        
        Content: "{content}"
        
        Requirements:
        - Mix of popular and niche hashtags
        - Relevant to the content topic
        - Appropriate for {platform} audience
        - Include trending hashtags if relevant
        - Avoid banned or spammy hashtags
        - Consider seasonal or timely hashtags
        
        Return as a list of hashtags with brief explanations of relevance.
        """
        
        hashtag_response = await self.llm.generate_content(prompt, max_tokens=800)
        
        # Extract hashtags from response
        import re
        hashtags = re.findall(r'#\w+', hashtag_response)
        
        # If not enough hashtags found, generate basic ones
        if len(hashtags) < count:
            basic_prompt = f"""
            Generate {count - len(hashtags)} additional basic hashtags for content about: {content[:100]}
            Focus on general, popular hashtags that would be relevant.
            """
            basic_response = await self.llm.generate_content(basic_prompt, max_tokens=400)
            additional_hashtags = re.findall(r'#\w+', basic_response)
            hashtags.extend(additional_hashtags)
        
        return hashtags[:count]
    
    async def suggest_posting_times(self, platform: str, audience: Dict[str, Any] = None) -> List[str]:
        """Suggest optimal posting times for platform"""
        
        platform_times = {
            "linkedin": ["8:00 AM", "12:00 PM", "5:00 PM"],
            "twitter": ["9:00 AM", "1:00 PM", "3:00 PM", "5:00 PM"],
            "instagram": ["11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM"],
            "facebook": ["9:00 AM", "1:00 PM", "3:00 PM"],
            "blog": ["Any time - SEO focused"]
        }
        
        base_times = platform_times.get(platform, ["9:00 AM", "12:00 PM", "3:00 PM"])
        
        if audience and audience.get('timezone'):
            # Adjust times for audience timezone (simplified)
            return [f"{time} {audience['timezone']}" for time in base_times]
        
        return base_times
    
    async def create_platform_preview(self, content: str, platform: str) -> Dict[str, Any]:
        """Create a preview of how content will look on platform"""
        
        specs = self.platform_specs[platform]
        
        # Simulate how content would appear
        preview_data = {
            "platform": platform,
            "content_preview": content[:200] + "..." if len(content) > 200 else content,
            "character_count": len(content),
            "character_limit": specs['max_chars'],
            "within_limits": len(content) <= specs['max_chars'],
            "hashtag_count": content.count('#'),
            "hashtag_limit": specs['hashtag_limit'],
            "estimated_reading_time": max(1, len(content.split()) // 200),  # Words per minute
            "engagement_prediction": await self._predict_engagement(content, platform),
            "visual_suggestions": await self._suggest_visual_elements(content, platform)
        }
        
        return preview_data
    
    async def _predict_engagement(self, content: str, platform: str) -> Dict[str, Any]:
        """Predict engagement potential for content on platform"""
        
        prompt = f"""
        Predict the engagement potential of this content on {platform}:
        
        Content: "{content}"
        
        Consider:
        - Content type and format
        - Emotional appeal
        - Call-to-action strength
        - Platform algorithm factors
        - Audience behavior patterns
        - Timing and trends
        
        Provide engagement predictions for:
        - Likes/Reactions (1-10 scale)
        - Comments/Discussion (1-10 scale)
        - Shares/Retweets (1-10 scale)
        - Overall engagement score
        
        Also provide specific factors that will drive or limit engagement.
        """
        
        prediction = await self.llm.generate_content(prompt, max_tokens=1000)
        
        return {
            "likes_score": 7,
            "comments_score": 6,
            "shares_score": 5,
            "overall_score": 6.5,
            "prediction_details": prediction,
            "key_factors": [
                "Strong call-to-action",
                "Relevant topic timing",
                "Platform-appropriate format"
            ],
            "improvement_areas": [
                "Could use more emotional appeal",
                "Consider adding visual elements"
            ]
        }
    
    async def _suggest_visual_elements(self, content: str, platform: str) -> List[str]:
        """Suggest visual elements to accompany the content"""
        
        prompt = f"""
        Suggest visual elements for this {platform} content:
        
        Content: "{content}"
        
        Suggest:
        1. Image types or concepts
        2. Video ideas if applicable
        3. Graphic design elements
        4. Color schemes or visual themes
        5. Layout or format suggestions
        6. Interactive elements if relevant
        
        Focus on visual elements that will enhance the message and increase engagement.
        """
        
        suggestions = await self.llm.generate_content(prompt, max_tokens=800)
        
        return [
            "Professional hero image",
            "Infographic with key statistics",
            "Quote card with main message",
            "Behind-the-scenes photo",
            "Custom illustration or graphic"
        ]
    
    async def optimize_batch(self, content_list: List[str], platform: str) -> List[Dict[str, Any]]:
        """Optimize multiple pieces of content for a platform"""
        
        results = []
        
        for content in content_list:
            result = await self.optimize_for_platform(content, platform)
            results.append(result)
        
        return results
    
    async def compare_platforms(self, content: str, platforms: List[str]) -> Dict[str, Any]:
        """Compare content optimization across multiple platforms"""
        
        comparisons = {}
        
        for platform in platforms:
            optimization = await self.optimize_for_platform(content, platform)
            comparisons[platform] = {
                "optimization_score": optimization.get("optimization_score", 0),
                "character_count": optimization.get("character_count", 0),
                "within_limits": optimization.get("within_limits", False),
                "engagement_prediction": optimization.get("analysis", {}).get("engagement_potential", {})
            }
        
        # Find best platform
        best_platform = max(comparisons.keys(), key=lambda p: comparisons[p]["optimization_score"])
        
        return {
            "original_content": content,
            "platform_comparisons": comparisons,
            "recommended_platform": best_platform,
            "platform_ranking": sorted(comparisons.keys(), key=lambda p: comparisons[p]["optimization_score"], reverse=True)
        }