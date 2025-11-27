from typing import Dict, Any, List
import json
import re

class VoiceAnalyzer:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.voice_profiles = {}
    
    async def analyze_voice(self, text: str, profile_name: str = None) -> Dict[str, Any]:
        """Analyze voice and style characteristics from text"""
        
        prompt = f"""
        Perform a comprehensive voice and style analysis of the following text:
        
        Text: "{text}"
        
        Analyze these characteristics:
        
        1. **Tone Analysis**:
           - Overall tone (formal/casual/neutral)
           - Emotional temperature (warm/cool/hot)
           - Professional level (expert/intermediate/beginner-friendly)
           - Personality traits (authoritative/friendly/humorous/etc.)
        
        2. **Writing Style**:
           - Sentence structure (simple/complex/varied)
           - Vocabulary level (basic/intermediate/advanced)
           - Use of literary devices (metaphors, analogies, etc.)
           - Rhythm and flow
           - Paragraph structure
        
        3. **Brand Voice Elements**:
           - Unique phrases or expressions
           - Signature words or terminology
           - Communication patterns
           - Consistency markers
           - Authenticity indicators
        
        4. **Engagement Style**:
           - Call-to-action approach
           - Question usage
           - Storytelling elements
           - Emotional appeals
           - Logical arguments
        
        5. **Technical Aspects**:
           - Readability score
           - Average sentence length
           - Passive voice usage
           - Adverb density
           - Repetition patterns
        
        Return a detailed JSON analysis with scores (0-100) for each characteristic
        and specific examples from the text that support your analysis.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=2500, temperature=0.3)
        
        # Parse the analysis
        try:
            # Extract JSON if present
            json_match = re.search(r'\{.*\}', analysis, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
            else:
                analysis_data = {"detailed_analysis": analysis}
        except:
            analysis_data = {"detailed_analysis": analysis}
        
        # Calculate overall voice coherence score
        coherence_score = await self._calculate_coherence_score(analysis_data)
        
        result = {
            "analysis": analysis_data,
            "coherence_score": coherence_score,
            "text_length": len(text),
            "recommendations": await self._generate_recommendations(analysis_data),
            "voice_fingerprint": await self._create_voice_fingerprint(analysis_data)
        }
        
        # Save to profile if name provided
        if profile_name:
            self.voice_profiles[profile_name] = result
        
        return result
    
    async def _calculate_coherence_score(self, analysis_data: Dict[str, Any]) -> float:
        """Calculate overall voice coherence score"""
        
        # This would analyze consistency across multiple dimensions
        # For now, return a placeholder based on key metrics
        
        scores = []
        
        # Extract various scores from the analysis
        if "tone_analysis" in analysis_data:
            tone_scores = analysis_data.get("tone_analysis", {})
            scores.extend([
                tone_scores.get("consistency", 75),
                tone_scores.get("clarity", 80),
                tone_scores.get("authenticity", 70)
            ])
        
        if "writing_style" in analysis_data:
            style_scores = analysis_data.get("writing_style", {})
            scores.extend([
                style_scores.get("consistency", 75),
                style_scores.get("readability", 85)
            ])
        
        # Calculate weighted average
        if scores:
            return sum(scores) / len(scores)
        
        return 75.0  # Default score
    
    async def _generate_recommendations(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for voice improvement"""
        
        recommendations = []
        
        # Analyze tone consistency
        if analysis_data.get("tone_analysis", {}).get("consistency", 100) < 80:
            recommendations.append("Maintain more consistent tone throughout the content")
        
        # Check readability
        if analysis_data.get("writing_style", {}).get("readability_score", 100) < 70:
            recommendations.append("Simplify sentence structure for better readability")
        
        # Check for engagement
        if analysis_data.get("engagement_style", {}).get("cta_presence", 0) < 1:
            recommendations.append("Add clear call-to-actions to improve engagement")
        
        # Check authenticity
        if analysis_data.get("brand_voice", {}).get("authenticity", 100) < 75:
            recommendations.append("Use more personal anecdotes to increase authenticity")
        
        return recommendations
    
    async def _create_voice_fingerprint(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a unique voice fingerprint for consistent replication"""
        
        fingerprint = {
            "tone_profile": {
                "primary_tone": analysis_data.get("tone_analysis", {}).get("primary_tone", "neutral"),
                "emotional_temperature": analysis_data.get("tone_analysis", {}).get("emotional_temperature", "moderate"),
                "professional_level": analysis_data.get("tone_analysis", {}).get("professional_level", "intermediate")
            },
            "style_profile": {
                "sentence_complexity": analysis_data.get("writing_style", {}).get("sentence_complexity", "medium"),
                "vocabulary_level": analysis_data.get("writing_style", {}).get("vocabulary_level", "intermediate"),
                "paragraph_style": analysis_data.get("writing_style", {}).get("paragraph_style", "standard")
            },
            "signature_elements": {
                "common_phrases": analysis_data.get("brand_voice", {}).get("signature_phrases", []),
                "preferred_words": analysis_data.get("brand_voice", {}).get("preferred_vocabulary", []),
                "structural_patterns": analysis_data.get("writing_style", {}).get("patterns", [])
            },
            "engagement_approach": {
                "cta_style": analysis_data.get("engagement_style", {}).get("cta_approach", "direct"),
                "question_usage": analysis_data.get("engagement_style", {}).get("question_frequency", "moderate"),
                "story_elements": analysis_data.get("engagement_style", {}).get("story_usage", "occasional")
            }
        }
        
        return fingerprint
    
    async def compare_voices(self, text1: str, text2: str) -> Dict[str, Any]:
        """Compare two texts for voice consistency"""
        
        analysis1 = await self.analyze_voice(text1)
        analysis2 = await self.analyze_voice(text2)
        
        comparison = {
            "similarity_score": 0,
            "tone_match": 0,
            "style_match": 0,
            "differences": [],
            "recommendations": []
        }
        
        # Compare tone profiles
        tone1 = analysis1["voice_fingerprint"]["tone_profile"]
        tone2 = analysis2["voice_fingerprint"]["tone_profile"]
        
        tone_matches = sum(1 for key in tone1 if tone1[key] == tone2[key])
        comparison["tone_match"] = (tone_matches / len(tone1)) * 100
        
        # Compare style profiles
        style1 = analysis1["voice_fingerprint"]["style_profile"]
        style2 = analysis2["voice_fingerprint"]["style_profile"]
        
        style_matches = sum(1 for key in style1 if style1[key] == style2[key])
        comparison["style_match"] = (style_matches / len(style1)) * 100
        
        # Overall similarity
        comparison["similarity_score"] = (comparison["tone_match"] + comparison["style_match"]) / 2
        
        # Identify differences
        if comparison["tone_match"] < 80:
            comparison["differences"].append("Tone inconsistency detected")
        
        if comparison["style_match"] < 80:
            comparison["differences"].append("Writing style inconsistency detected")
        
        # Recommendations
        if comparison["similarity_score"] < 75:
            comparison["recommendations"].append("Review and align voice consistency")
        
        return comparison
    
    async def generate_voice_guide(self, profile_name: str) -> Dict[str, Any]:
        """Generate a comprehensive voice guide from a profile"""
        
        if profile_name not in self.voice_profiles:
            return {"error": "Voice profile not found"}
        
        profile = self.voice_profiles[profile_name]
        
        prompt = f"""
        Create a comprehensive voice and style guide based on this analysis:
        
        {json.dumps(profile, indent=2)}
        
        The guide should include:
        
        1. **Voice Overview**: Clear description of the voice personality
        2. **Do's and Don'ts**: Specific examples of what to do and avoid
        3. **Writing Guidelines**: Sentence structure, vocabulary, and style rules
        4. **Tone Variations**: How to adapt tone for different contexts
        5. **Brand Voice Examples**: Before/after examples of text optimization
        6. **Consistency Checklist**: Quick reference for maintaining voice
        
        Make it actionable and easy to follow for content creators.
        """
        
        guide = await self.llm.generate_content(prompt, max_tokens=3000)
        
        return {
            "profile_name": profile_name,
            "voice_guide": guide,
            "quick_reference": profile["voice_fingerprint"],
            "quality_score": profile["coherence_score"]
        }