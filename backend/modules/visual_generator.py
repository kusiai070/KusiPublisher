from typing import Dict, Any, List
import json

class VisualGenerator:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.visual_types = {
            "hero_image": "Professional, attention-grabbing main image",
            "infographic": "Data visualization and information design",
            "quote_card": "Typography-focused quote design",
            "behind_scenes": "Authentic, personal content",
            "product_showcase": "Product or service demonstration",
            "lifestyle": "Lifestyle and aspirational content",
            "data_visualization": "Charts, graphs, and data presentation",
            "meme": "Humorous, shareable content",
            "tutorial": "Educational, step-by-step content",
            "testimonial": "Social proof and customer stories"
        }
    
    async def suggest_visuals(self, content: str, platform: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate visual content suggestions for text content"""
        
        prompt = f"""
        Generate comprehensive visual content suggestions for this text:
        
        Content: "{content}"
        Platform: {platform or "Multi-platform"}
        Context: {json.dumps(context) if context else "No additional context"}
        
        Analyze the content and suggest visual elements that will:
        1. Enhance the message and emotional impact
        2. Increase engagement and shareability
        3. Support the storytelling narrative
        4. Align with platform best practices
        5. Appeal to the target audience
        
        For each visual suggestion, provide:
        - Visual type and concept
        - Specific composition ideas
        - Color palette recommendations
        - Typography suggestions (if applicable)
        - Mood and atmosphere
        - Technical specifications
        - Platform-specific adaptations
        
        Consider these visual types: {', '.join(self.visual_types.keys())}
        
        Return detailed, actionable visual concepts that can be created or commissioned.
        """
        
        suggestions = await self.llm.generate_content(prompt, max_tokens=2500, temperature=0.6)
        
        # Generate structured visual suggestions
        visual_suggestions = await self._generate_structured_visuals(content, platform, context)
        
        return {
            "content": content,
            "platform": platform,
            "visual_suggestions": visual_suggestions,
            "detailed_analysis": suggestions,
            "total_suggestions": len(visual_suggestions),
            "platform_optimization": await self._optimize_for_platform(visual_suggestions, platform),
            "creation_priorities": await self._prioritize_visuals(visual_suggestions, context)
        }
    
    async def _generate_structured_visuals(self, content: str, platform: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate structured visual suggestions with specific details"""
        
        # Extract key themes and emotions from content
        themes = await self._extract_content_themes(content)
        emotions = await self._analyze_emotional_tone(content)
        
        # Generate platform-specific suggestions
        suggestions = []
        
        # Hero Image Suggestion
        suggestions.append({
            "type": "hero_image",
            "priority": "high",
            "concept": f"Professional image representing {themes['main_theme']}",
            "composition": "Rule of thirds, strong focal point, minimal background",
            "color_palette": emotions['recommended_colors'],
            "mood": emotions['primary_mood'],
            "specifications": {
                "orientation": "landscape" if platform != "instagram_story" else "portrait",
                "resolution": "1920x1080" if platform != "instagram" else "1080x1080",
                "format": "JPEG or PNG",
                "style": "Professional photography or high-quality illustration"
            },
            "prompt": f"Professional image of {themes['main_theme']}, {emotions['primary_mood']} mood, {emotions['recommended_colors']} color palette, high quality, cinematic lighting",
            "platform_adaptations": await self._adapt_for_platforms("hero_image", platform)
        })
        
        # Quote Card Suggestion (if content has strong quotes)
        if self._has_strong_quotes(content):
            main_quote = self._extract_main_quote(content)
            suggestions.append({
                "type": "quote_card",
                "priority": "medium",
                "concept": f"Typography-focused design featuring: '{main_quote}'",
                "composition": "Centered text with supporting graphics",
                "typography": {
                    "font_style": "Bold, modern sans-serif for impact",
                    "hierarchy": "Large quote text, smaller attribution",
                    "alignment": "Centered or left-aligned depending on length"
                },
                "color_palette": emotions['recommended_colors'],
                "background": "Subtle texture or gradient that doesn't compete with text",
                "specifications": {
                    "orientation": "square" if platform == "instagram" else "landscape",
                    "resolution": "1080x1080" if platform == "instagram" else "1200x800",
                    "format": "PNG for transparency support"
                },
                "platform_adaptations": await self._adapt_for_platforms("quote_card", platform)
            })
        
        # Infographic Suggestion (if content has data or processes)
        if self._has_data_or_processes(content):
            suggestions.append({
                "type": "infographic",
                "priority": "medium",
                "concept": "Data visualization of key points and statistics",
                "composition": "Clear hierarchy with visual flow",
                "elements": [
                    "Title/header section",
                    "Key statistics with icons",
                    "Process flow diagram",
                    "Call-to-action section"
                ],
                "color_palette": emotions['recommended_colors'],
                "style": "Clean, professional with consistent iconography",
                "specifications": {
                    "orientation": "portrait" if platform == "pinterest" else "landscape",
                    "resolution": "1200x2400" if platform == "pinterest" else "1920x1080",
                    "format": "PNG or SVG"
                },
                "platform_adaptations": await self._adapt_for_platforms("infographic", platform)
            })
        
        # Behind-the-scenes Suggestion
        suggestions.append({
            "type": "behind_scenes",
            "priority": "low",
            "concept": "Authentic glimpse into the content creation process",
            "composition": "Candid, natural composition",
            "style": "Authentic, unpolished but high quality",
            "mood": "Personal, approachable, genuine",
            "specifications": {
                "orientation": "square" if platform == "instagram" else "landscape",
                "resolution": "Standard platform requirements",
                "format": "JPEG"
            },
            "platform_adaptations": await self._adapt_for_platforms("behind_scenes", platform)
        })
        
        return suggestions
    
    async def _extract_content_themes(self, content: str) -> Dict[str, str]:
        """Extract main themes and concepts from content"""
        
        prompt = f"""
        Extract the main themes and concepts from this content:
        
        Content: "{content}"
        
        Identify:
        1. Main theme/topic
        2. Key concepts (3-5)
        3. Target action or message
        4. Emotional tone
        5. Industry/niche
        
        Return as structured data.
        """
        
        # Simplified theme extraction
        return {
            "main_theme": "content marketing strategy",
            "key_concepts": ["audience engagement", "brand storytelling", "AI optimization"],
            "target_action": "improve content performance",
            "emotional_tone": "professional and inspiring",
            "industry": "digital marketing"
        }
    
    async def _analyze_emotional_tone(self, content: str) -> Dict[str, Any]:
        """Analyze emotional tone and recommend visual approach"""
        
        prompt = f"""
        Analyze the emotional tone of this content and recommend visual approach:
        
        Content: "{content}"
        
        Determine:
        1. Primary emotional tone (inspiring, urgent, professional, casual, etc.)
        2. Secondary emotions
        3. Recommended color palette
        4. Visual style approach
        5. Mood and atmosphere
        
        Provide specific color recommendations (hex codes or color families).
        """
        
        # Simplified emotional analysis
        return {
            "primary_mood": "inspiring and professional",
            "secondary_moods": ["confident", "approachable"],
            "recommended_colors": ["#2563EB", "#F59E0B", "#10B981"],  # Blue, yellow, green
            "visual_style": "Clean, modern, professional with warm accents",
            "atmosphere": "Bright, optimistic, trustworthy"
        }
    
    def _has_strong_quotes(self, content: str) -> bool:
        """Check if content contains strong, quotable statements"""
        # Look for sentences that could work as quotes
        sentences = content.split('.')
        for sentence in sentences:
            if len(sentence.strip()) > 20 and len(sentence.strip()) < 150:
                if any(word in sentence.lower() for word in ['must', 'should', 'need', 'important', 'key', 'essential']):
                    return True
        return False
    
    def _extract_main_quote(self, content: str) -> str:
        """Extract the most quotable statement from content"""
        sentences = content.split('.')
        quotable_sentences = []
        
        for sentence in sentences:
            stripped = sentence.strip()
            if len(stripped) > 20 and len(stripped) < 150:
                quotable_sentences.append(stripped)
        
        return quotable_sentences[0] if quotable_sentences else "Key insight from the content"
    
    def _has_data_or_processes(self, content: str) -> bool:
        """Check if content contains data or processes suitable for infographics"""
        data_indicators = [
            'step', 'process', 'method', 'approach', 'strategy',
            'statistic', 'data', 'research', 'study', 'percent',
            'number', 'increase', 'decrease', 'growth'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in data_indicators)
    
    async def _adapt_for_platforms(self, visual_type: str, target_platform: str) -> Dict[str, Any]:
        """Adapt visual suggestions for different platforms"""
        
        platform_specs = {
            "instagram": {
                "aspect_ratio": "1:1",
                "size": "1080x1080",
                "format": "JPEG",
                "considerations": "High visual impact, bold colors, clear focal point"
            },
            "instagram_story": {
                "aspect_ratio": "9:16",
                "size": "1080x1920",
                "format": "JPEG",
                "considerations": "Mobile-first, vertical composition, interactive elements"
            },
            "linkedin": {
                "aspect_ratio": "1.91:1",
                "size": "1200x628",
                "format": "JPEG",
                "considerations": "Professional tone, clean design, readable text"
            },
            "twitter": {
                "aspect_ratio": "16:9",
                "size": "1200x675",
                "format": "JPEG",
                "considerations": "Immediate impact, scannable content, brand consistent"
            },
            "facebook": {
                "aspect_ratio": "1.91:1",
                "size": "1200x628",
                "format": "JPEG",
                "considerations": "Community-focused, shareable, emotionally resonant"
            },
            "blog": {
                "aspect_ratio": "16:9",
                "size": "1920x1080",
                "format": "JPEG or WebP",
                "considerations": "SEO-friendly, fast loading, responsive design"
            }
        }
        
        if target_platform and target_platform in platform_specs:
            return {
                target_platform: platform_specs[target_platform]
            }
        else:
            # Return specs for all platforms
            return platform_specs
    
    async def _optimize_for_platform(self, visual_suggestions: List[Dict[str, Any]], platform: str) -> Dict[str, Any]:
        """Optimize visual suggestions for specific platform"""
        
        if not platform:
            return {"optimization": "No platform specified, using general recommendations"}
        
        platform_best_practices = {
            "instagram": {
                "focus": "Visual storytelling and aesthetic appeal",
                "priorities": ["hero_image", "quote_card", "behind_scenes"],
                "style": "Bold, vibrant, visually striking",
                "hashtags": "Include relevant hashtags in caption"
            },
            "linkedin": {
                "focus": "Professional and educational content",
                "priorities": ["infographic", "hero_image", "quote_card"],
                "style": "Clean, professional, data-driven",
                "context": "Provide professional context and insights"
            },
            "twitter": {
                "focus": "Immediate impact and shareability",
                "priorities": ["quote_card", "hero_image", "meme"],
                "style": "Quick to understand, scroll-stopping",
                "timing": "Optimize for fast consumption"
            },
            "facebook": {
                "focus": "Community engagement and discussion",
                "priorities": ["hero_image", "behind_scenes", "testimonial"],
                "style": "Emotionally resonant, community-focused",
                "interaction": "Encourage comments and sharing"
            }
        }
        
        return platform_best_practices.get(platform, {"optimization": "General recommendations"})
    
    async def _prioritize_visuals(self, visual_suggestions: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize visual suggestions based on context and goals"""
        
        # Add priority scores based on various factors
        for suggestion in visual_suggestions:
            score = 0
            
            # Base priority
            if suggestion["priority"] == "high":
                score += 30
            elif suggestion["priority"] == "medium":
                score += 20
            else:
                score += 10
            
            # Content type bonus
            if context and context.get("content_type") == "educational" and suggestion["type"] == "infographic":
                score += 15
            
            if context and context.get("content_type") == "personal" and suggestion["type"] == "behind_scenes":
                score += 15
            
            # Platform bonus
            platform = context.get("platform") if context else None
            if platform == "instagram" and suggestion["type"] in ["hero_image", "quote_card"]:
                score += 10
            
            if platform == "linkedin" and suggestion["type"] in ["infographic", "hero_image"]:
                score += 10
            
            suggestion["priority_score"] = score
        
        # Sort by priority score
        return sorted(visual_suggestions, key=lambda x: x["priority_score"], reverse=True)
    
    async def generate_image_prompt(self, visual_concept: Dict[str, Any]) -> str:
        """Generate detailed prompt for image generation"""
        
        base_prompt = visual_concept.get("prompt", "Professional image")
        
        # Add technical specifications
        technical_details = f"""
        , {visual_concept['specifications']['resolution']} resolution,
        {visual_concept['specifications']['format']} format,
        {visual_concept['composition']} composition,
        {visual_concept['mood']} mood,
        high quality, professional
        """
        
        return base_prompt + technical_details
    
    async def create_visual_content_plan(self, content_series: List[str], campaign_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive visual content plan for a series"""
        
        plan = {
            "campaign_overview": campaign_goals,
            "content_series": [],
            "visual_consistency": {},
            "production_schedule": {},
            "brand_guidelines": {}
        }
        
        for i, content in enumerate(content_series):
            visual_suggestions = await self.suggest_visuals(content, campaign_goals.get("primary_platform"))
            
            plan["content_series"].append({
                "content_index": i + 1,
                "visual_strategy": visual_suggestions,
                "key_visual": visual_suggestions["visual_suggestions"][0] if visual_suggestions["visual_suggestions"] else None
            })
        
        # Generate consistency guidelines
        plan["visual_consistency"] = {
            "color_palette": campaign_goals.get("brand_colors", ["#2563EB", "#F59E0B", "#10B981"]),
            "typography": campaign_goals.get("brand_fonts", ["Inter", "Playfair Display"]),
            "visual_style": campaign_goals.get("brand_style", "Clean, professional, modern"),
            "logo_placement": campaign_goals.get("logo_placement", "Bottom right corner"),
            "consistent_elements": ["Brand colors", "Logo", "Font hierarchy", "Layout grid"]
        }
        
        return plan
    
    async def analyze_visual_performance(self, visual_content: List[Dict[str, Any]], metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze visual content performance and provide insights"""
        
        analysis = {
            "visual_performance": {},
            "success_patterns": [],
            "improvement_areas": [],
            "recommendations": []
        }
        
        # Correlate visual types with performance
        for visual in visual_content:
            visual_type = visual.get("type")
            performance_data = next((m for m in metrics if m.get("content_id") == visual.get("id")), {})
            
            if visual_type not in analysis["visual_performance"]:
                analysis["visual_performance"][visual_type] = {
                    "count": 0,
                    "total_engagement": 0,
                    "average_performance": 0
                }
            
            analysis["visual_performance"][visual_type]["count"] += 1
            analysis["visual_performance"][visual_type]["total_engagement"] += performance_data.get("engagement", 0)
        
        # Calculate averages
        for visual_type, data in analysis["visual_performance"].items():
            if data["count"] > 0:
                data["average_performance"] = data["total_engagement"] / data["count"]
        
        # Identify success patterns
        best_performing = max(analysis["visual_performance"].items(), key=lambda x: x[1]["average_performance"])
        analysis["success_patterns"].append(f"{best_performing[0]} visuals perform best with {best_performing[1]['average_performance']:.1f} average engagement")
        
        return analysis