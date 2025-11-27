from typing import Dict, Any, List
import json
import re

class SEOResearcher:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.platform_seo_factors = {
            "twitter": {
                "max_length": 280,
                "hashtag_limit": 2,
                "keyword_density": "moderate",
                "focus": "trending topics"
            },
            "linkedin": {
                "max_length": 3000,
                "hashtag_limit": 5,
                "keyword_density": "high",
                "focus": "professional keywords"
            },
            "instagram": {
                "max_length": 2200,
                "hashtag_limit": 30,
                "keyword_density": "moderate",
                "focus": "visual hashtags"
            },
            "facebook": {
                "max_length": 5000,
                "hashtag_limit": 5,
                "keyword_density": "low",
                "focus": "engagement keywords"
            },
            "blog": {
                "max_length": 50000,
                "hashtag_limit": 0,
                "keyword_density": "high",
                "focus": "search intent"
            }
        }
    
    async def research_keywords(self, topic: str, platform: str = "general", location: str = None) -> Dict[str, Any]:
        """Research keywords and trends for a given topic"""
        
        prompt = f"""
        Perform comprehensive SEO and keyword research for the topic: "{topic}"
        
        Platform focus: {platform}
        Location: {location or "Global"}
        
        Research areas:
        
        1. **Primary Keywords** (High volume, high intent):
           - Main topic keywords
           - Long-tail variations
           - Question-based keywords
           - Local variations (if applicable)
        
        2. **Secondary Keywords** (Supporting terms):
           - Related concepts
           - Semantic variations
           - LSI (Latent Semantic Indexing) keywords
           - Synonyms and alternatives
        
        3. **Trending Keywords** (Current momentum):
           - Rising search terms
           - Seasonal variations
           - News-related terms
           - Viral keywords
        
        4. **Competitor Keywords** (Strategic insights):
           - Gap opportunities
           - Underserved keywords
           - Content opportunities
           - Ranking difficulties
        
        5. **Platform-Specific Keywords**:
           - Hashtag suggestions for social platforms
           - Platform-specific terminology
           - Community language
           - Trending platform topics
        
        For each keyword provide:
        - Search volume (estimated)
        - Competition level (high/medium/low)
        - Intent type (informational/navigational/commercial)
        - Trend status (rising/stable/declining)
        - Content opportunity score (1-10)
        
        Return as structured JSON with actionable insights.
        """
        
        research = await self.llm.generate_content(prompt, max_tokens=3000, temperature=0.4)
        
        # Parse and structure the research results
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', research, re.DOTALL)
            if json_match:
                keyword_data = json.loads(json_match.group())
            else:
                keyword_data = {"raw_analysis": research}
        except:
            keyword_data = {"raw_analysis": research}
        
        # Add platform-specific optimizations
        platform_optimizations = await self._get_platform_optimizations(topic, platform)
        
        return {
            "topic": topic,
            "platform": platform,
            "research_date": "2025-01-24",  # Would be actual timestamp
            "primary_keywords": keyword_data.get("primary_keywords", []),
            "secondary_keywords": keyword_data.get("secondary_keywords", []),
            "trending_keywords": keyword_data.get("trending_keywords", []),
            "hashtag_suggestions": platform_optimizations.get("hashtags", []),
            "content_suggestions": await self._generate_content_suggestions(keyword_data, platform),
            "seo_recommendations": await self._generate_seo_recommendations(keyword_data, platform),
            "competitive_analysis": keyword_data.get("competitive_analysis", {})
        }
    
    async def _get_platform_optimizations(self, topic: str, platform: str) -> Dict[str, Any]:
        """Get platform-specific optimizations"""
        
        if platform == "general":
            return {}
        
        platform_data = self.platform_seo_factors.get(platform.lower(), {})
        
        prompt = f"""
        Generate {platform}-specific optimizations for the topic: "{topic}"
        
        Consider:
        - Character limits: {platform_data.get("max_length", "N/A")}
        - Hashtag strategy: {platform_data.get("hashtag_limit", "N/A")} hashtags
        - Keyword density: {platform_data.get("keyword_density", "moderate")}
        - Platform focus: {platform_data.get("focus", "general")}
        
        Provide:
        1. Optimal hashtag suggestions (relevant and trending)
        2. Platform-specific keyword placement
        3. Content structure recommendations
        4. Engagement optimization tips
        5. Algorithm-friendly formatting
        """
        
        optimization = await self.llm.generate_content(prompt, max_tokens=1500)
        
        # Extract hashtags
        hashtags = re.findall(r'#\w+', optimization)
        if not hashtags:
            # Generate hashtags if none found
            hashtags = await self._generate_hashtags(topic, platform)
        
        return {
            "hashtags": hashtags[:platform_data.get("hashtag_limit", 10)],
            "optimization_tips": optimization,
            "character_count": len(topic),
            "max_characters": platform_data.get("max_length", 5000)
        }
    
    async def _generate_hashtags(self, topic: str, platform: str) -> List[str]:
        """Generate relevant hashtags for the topic and platform"""
        
        prompt = f"""
        Generate relevant hashtags for the topic "{topic}" on {platform}.
        
        Requirements:
        - Mix of popular and niche hashtags
        - Relevant to the topic
        - Appropriate for {platform} audience
        - Include trending variations
        - Community and industry tags
        
        Provide 10-15 hashtag suggestions with brief explanations of their relevance.
        """
        
        hashtag_analysis = await self.llm.generate_content(prompt, max_tokens=800)
        
        # Extract hashtags from response
        hashtags = re.findall(r'#\w+', hashtag_analysis)
        
        # If no hashtags found, generate basic ones
        if not hashtags:
            topic_words = topic.lower().split()
            hashtags = [f"#{word}" for word in topic_words[:5]]
        
        return hashtags
    
    async def _generate_content_suggestions(self, keyword_data: Dict[str, Any], platform: str) -> List[Dict[str, Any]]:
        """Generate content suggestions based on keyword research"""
        
        primary_keywords = keyword_data.get("primary_keywords", [])[:3]
        secondary_keywords = keyword_data.get("secondary_keywords", [])[:5]
        
        suggestions = []
        
        # Blog post suggestions
        if platform in ["blog", "general"]:
            for keyword in primary_keywords:
                suggestions.append({
                    "type": "blog_post",
                    "title": f"Complete Guide to {keyword}",
                    "primary_keyword": keyword,
                    "secondary_keywords": secondary_keywords[:3],
                    "content_type": "educational",
                    "estimated_words": 1500
                })
        
        # Social media suggestions
        if platform in ["twitter", "linkedin", "instagram", "facebook"]:
            for keyword in primary_keywords:
                suggestions.append({
                    "type": "social_post",
                    "content": f"💡 Key insight about {keyword}",
                    "primary_keyword": keyword,
                    "hashtags": await self._generate_hashtags(keyword, platform),
                    "content_type": "educational",
                    "call_to_action": "Learn more"
                })
        
        return suggestions
    
    async def _generate_seo_recommendations(self, keyword_data: Dict[str, Any], platform: str) -> List[str]:
        """Generate SEO recommendations based on research"""
        
        recommendations = []
        
        # Basic SEO recommendations
        recommendations.extend([
            "Use primary keywords in the first 100 words",
            "Include keywords in headings and subheadings",
            "Optimize meta descriptions with target keywords",
            "Use semantic keywords throughout the content",
            "Include internal and external links where relevant"
        ])
        
        # Platform-specific recommendations
        if platform == "blog":
            recommendations.extend([
                "Optimize URL structure with primary keyword",
                "Add alt text to images with relevant keywords",
                "Use schema markup for better search visibility"
            ])
        elif platform in ["twitter", "linkedin", "instagram"]:
            recommendations.extend([
                "Place most important hashtags first",
                "Use a mix of popular and niche hashtags",
                "Include keywords naturally in the content"
            ])
        
        return recommendations
    
    async def analyze_content_performance(self, content: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content performance and suggest improvements"""
        
        prompt = f"""
        Analyze the performance of this content:
        
        Content: "{content}"
        Performance Metrics: {json.dumps(metrics, indent=2)}
        
        Identify:
        1. What worked well (high engagement elements)
        2. What could be improved
        3. Why certain metrics performed as they did
        4. Specific optimization opportunities
        5. A/B testing suggestions for future content
        
        Provide actionable insights for improving future content performance.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=2000)
        
        return {
            "content": content[:100] + "...",  # Truncate for display
            "metrics": metrics,
            "analysis": analysis,
            "improvement_suggestions": await self._extract_improvements(analysis),
            "success_factors": await self._extract_success_factors(analysis)
        }
    
    async def _extract_improvements(self, analysis: str) -> List[str]:
        """Extract improvement suggestions from analysis"""
        
        improvements = []
        
        # Look for improvement patterns
        improvement_patterns = [
            r"could be improved.*",
            r"should consider.*",
            r"recommend.*",
            r"suggestion.*",
            r"optimize.*"
        ]
        
        for pattern in improvement_patterns:
            matches = re.findall(pattern, analysis, re.IGNORECASE)
            improvements.extend(matches)
        
        return improvements[:5]  # Limit to top 5
    
    async def _extract_success_factors(self, analysis: str) -> List[str]:
        """Extract success factors from analysis"""
        
        factors = []
        
        # Look for success patterns
        success_patterns = [
            r"worked well.*",
            r"successful.*",
            r"effective.*",
            r"high engagement.*",
            r"performed well.*"
        ]
        
        for pattern in success_patterns:
            matches = re.findall(pattern, analysis, re.IGNORECASE)
            factors.extend(matches)
        
        return factors[:5]  # Limit to top 5
    
    async def get_trending_topics(self, niche: str = None, location: str = None) -> List[Dict[str, Any]]:
        """Get trending topics for content creation"""
        
        prompt = f"""
        Identify trending topics for content creation:
        
        Niche: {niche or "General"}
        Location: {location or "Global"}
        
        Focus on:
        1. Current trending hashtags
        2. Emerging topics in the industry
        3. Seasonal trends
        4. News-related opportunities
        5. Community discussions
        6. Viral content patterns
        
        For each trend provide:
        - Trend name/topic
        - Trending level (high/medium/low)
        - Time sensitivity (urgent/soon/flexible)
        - Content opportunities
        - Target platforms
        - Estimated engagement potential
        
        Return as structured data for immediate content planning.
        """
        
        trends = await self.llm.generate_content(prompt, max_tokens=2000)
        
        # Parse trends (simplified)
        trending_topics = []
        
        # Extract trend names and basic info
        trend_lines = trends.split('\n')
        for line in trend_lines:
            if any(keyword in line.lower() for keyword in ['trend', 'trending', 'popular']):
                trending_topics.append({
                    "topic": line.strip(),
                    "trending_level": "high",
                    "time_sensitivity": "flexible",
                    "platforms": ["twitter", "linkedin"],
                    "engagement_potential": 8
                })
        
        return trending_topics[:10]  # Return top 10 trends