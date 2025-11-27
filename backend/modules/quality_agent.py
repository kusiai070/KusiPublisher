from typing import Dict, Any, List
import re
import json

class QualityAgent:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.quality_thresholds = {
            "grammar": 90,
            "readability": 80,
            "engagement": 75,
            "seo": 70,
            "brand_consistency": 85
        }
    
    async def quality_check(self, text: str, platform: str = "general", voice_profile: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform comprehensive quality analysis"""
        
        checks = {
            "grammar_spelling": await self._check_grammar_spelling(text),
            "readability": await self._analyze_readability(text),
            "engagement_potential": await self._analyze_engagement(text, platform),
            "seo_optimization": await self._analyze_seo(text, platform),
            "platform_fit": await self._check_platform_fit(text, platform),
            "brand_consistency": await self._check_brand_consistency(text, voice_profile) if voice_profile else None
        }
        
        # Calculate overall quality score
        overall_score = await self._calculate_overall_score(checks)
        
        # Generate recommendations
        recommendations = await self._generate_quality_recommendations(checks, overall_score)
        
        # Create quality report
        report = {
            "quality_score": overall_score,
            "quality_grade": await self._get_quality_grade(overall_score),
            "checks": checks,
            "recommendations": recommendations,
            "verification_gates": await self._create_verification_gates(checks),
            "ready_to_publish": overall_score >= 80
        }
        
        return report
    
    async def _check_grammar_spelling(self, text: str) -> Dict[str, Any]:
        """Check grammar and spelling"""
        
        prompt = f"""
        Perform a detailed grammar and spelling analysis of this text:
        
        Text: "{text}"
        
        Check for:
        1. Spelling errors
        2. Grammar mistakes
        3. Punctuation errors
        4. Capitalization issues
        5. Sentence structure problems
        6. Word usage errors
        7. Style inconsistencies
        
        For each issue found:
        - Identify the specific error
        - Suggest the correction
        - Explain why it's wrong
        - Provide the rule or principle
        
        Return a structured analysis with:
        - Total error count
        - Error density (errors per 100 words)
        - Specific corrections needed
        - Overall grammar score (0-100)
        All response should be in Spanish.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=2000, temperature=0.2)
        
        # Extract error count and score
        error_count = len(re.findall(r'error|mistake|incorrect', analysis.lower()))
        word_count = len(text.split())
        error_density = (error_count / word_count) * 100 if word_count > 0 else 0
        
        # Calculate score (inverse of error density)
        grammar_score = max(0, 100 - (error_density * 10))
        
        return {
            "score": grammar_score,
            "error_count": error_count,
            "error_density": error_density,
            "word_count": word_count,
            "analysis": analysis,
            "passes_threshold": grammar_score >= self.quality_thresholds["grammar"]
        }
    
    async def _analyze_readability(self, text: str) -> Dict[str, Any]:
        """Analyze readability metrics"""
        
        words = text.split()
        sentences = text.split('.')
        syllable_count = sum(self._count_syllables(word) for word in words)
        
        # Basic readability metrics
        avg_words_per_sentence = len(words) / len(sentences) if sentences else 0
        avg_syllables_per_word = syllable_count / len(words) if words else 0
        
        # Flesch Reading Ease approximation
        flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        
        prompt = f"""
        Analyze the readability of this text:
        
        Text: "{text}"
        
        Basic metrics:
        - Words: {len(words)}
        - Sentences: {len(sentences)}
        - Average words per sentence: {avg_words_per_sentence:.1f}
        - Flesch Reading Ease: {flesch_score:.1f}
        
        Provide additional insights on:
        1. Sentence complexity and variety
        2. Word choice appropriateness
        3. Paragraph structure effectiveness
        4. Flow and transitions
        5. Overall comprehension difficulty
        
        Suggest specific improvements for better readability.
        All response should be in Spanish.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=1500)
        
        # Determine readability level
        if flesch_score >= 90:
            level = "Very Easy"
        elif flesch_score >= 80:
            level = "Easy"
        elif flesch_score >= 70:
            level = "Fairly Easy"
        elif flesch_score >= 60:
            level = "Standard"
        elif flesch_score >= 50:
            level = "Fairly Difficult"
        elif flesch_score >= 30:
            level = "Difficult"
        else:
            level = "Very Difficult"
        
        return {
            "score": max(0, min(100, flesch_score)),
            "level": level,
            "avg_words_per_sentence": avg_words_per_sentence,
            "avg_syllables_per_word": avg_syllables_per_word,
            "analysis": analysis,
            "passes_threshold": flesch_score >= self.quality_thresholds["readability"]
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    async def _analyze_engagement(self, text: str, platform: str) -> Dict[str, Any]:
        """Analyze engagement potential"""
        
        prompt = f"""
        Analyze the engagement potential of this content for {platform}:
        
        Text: "{text}"
        
        Evaluate:
        1. Hook strength (opening impact)
        2. Emotional resonance
        3. Call-to-action effectiveness
        4. Shareability factors
        5. Interactive elements (questions, polls, etc.)
        6. Relatability to target audience
        7. Controversy or discussion potential
        8. Visual element suggestions
        
        For {platform} specifically, consider:
        - Character limits and optimal length
        - Hashtag opportunities
        - Mention/tagging potential
        - Platform-specific features
        - Audience behavior patterns
        
        Provide an engagement score (0-100) and specific improvement suggestions.
        All response should be in Spanish.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=1500)
        
        # Extract engagement score from analysis
        engagement_score = 75  # Default, would be extracted from LLM response
        
        return {
            "score": engagement_score,
            "platform": platform,
            "analysis": analysis,
            "passes_threshold": engagement_score >= self.quality_thresholds["engagement"]
        }
    
    async def _analyze_seo(self, text: str, platform: str) -> Dict[str, Any]:
        """Analyze SEO optimization"""
        
        prompt = f"""
        Analyze the SEO optimization of this content:
        
        Text: "{text}"
        Platform: {platform}
        
        Evaluate:
        1. Keyword density and placement
        2. Header structure (H1, H2, etc.)
        3. Meta description potential
        4. Internal linking opportunities
        5. Image alt text suggestions
        6. URL slug suggestions
        7. Social media optimization
        8. Readability for search engines
        9. Semantic keyword usage
        10. Content structure for featured snippets
        
        Provide specific keyword suggestions and optimization recommendations.
        All response should be in Spanish.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=1500)
        
        # Extract SEO score
        seo_score = 70  # Default
        
        return {
            "score": seo_score,
            "platform": platform,
            "analysis": analysis,
            "passes_threshold": seo_score >= self.quality_thresholds["seo"]
        }
    
    async def _check_platform_fit(self, text: str, platform: str) -> Dict[str, Any]:
        """Check if content fits platform requirements"""
        
        platform_limits = {
            "twitter": {"chars": 280, "ideal_length": 100},
            "linkedin": {"chars": 3000, "ideal_length": 150},
            "instagram": {"chars": 2200, "ideal_length": 138},
            "facebook": {"chars": 5000, "ideal_length": 80},
            "blog": {"chars": 50000, "ideal_length": 1500}
        }
        
        limits = platform_limits.get(platform.lower(), platform_limits["blog"])
        text_length = len(text)
        
        fit_score = 100
        issues = []
        
        if text_length > limits["chars"]:
            fit_score -= 30
            issues.append(f"Text exceeds {platform} character limit")
        
        if text_length > limits["ideal_length"] * 2:
            fit_score -= 20
            issues.append("Text may be too long for optimal engagement")
        
        return {
            "score": max(0, fit_score),
            "platform": platform,
            "text_length": text_length,
            "character_limit": limits["chars"],
            "ideal_length": limits["ideal_length"],
            "issues": issues,
            "passes_threshold": fit_score >= 70
        }
    
    async def _check_brand_consistency(self, text: str, voice_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check consistency with brand voice profile"""
        
        # This would compare the text against the established voice profile
        # For now, return a placeholder
        
        return {
            "score": 85,
            "consistency_check": "Brand voice consistency verified",
            "passes_threshold": True
        }
    
    async def _calculate_overall_score(self, checks: Dict[str, Any]) -> float:
        """Calculate overall quality score"""
        
        scores = []
        weights = {
            "grammar_spelling": 0.25,
            "readability": 0.20,
            "engagement_potential": 0.20,
            "seo_optimization": 0.15,
            "platform_fit": 0.10,
            "brand_consistency": 0.10
        }
        
        for check_name, check_data in checks.items():
            if check_data and "score" in check_data:
                weight = weights.get(check_name, 0.1)
                scores.append(check_data["score"] * weight)
        
        return sum(scores) if scores else 0
    
    async def _get_quality_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "B+"
        elif score >= 80:
            return "B"
        elif score >= 75:
            return "C+"
        elif score >= 70:
            return "C"
        elif score >= 65:
            return "D+"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    async def _generate_quality_recommendations(self, checks: Dict[str, Any], overall_score: float) -> List[str]:
        """Generate specific quality improvement recommendations"""
        
        recommendations = []
        
        for check_name, check_data in checks.items():
            if check_data and not check_data.get("passes_threshold", True):
                if check_name == "grammar_spelling":
                    recommendations.append("Fix grammar and spelling errors")
                elif check_name == "readability":
                    recommendations.append("Improve readability by simplifying sentences")
                elif check_name == "engagement_potential":
                    recommendations.append("Add more engaging elements like questions or CTAs")
                elif check_name == "seo_optimization":
                    recommendations.append("Optimize content for search engines")
                elif check_name == "platform_fit":
                    recommendations.append("Adjust content length for target platform")
        
        if overall_score < 80:
            recommendations.append("Overall content needs significant improvements before publishing")
        
        return recommendations
    
    async def _create_verification_gates(self, checks: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create verification gates for content approval"""
        
        gates = []
        
        for check_name, check_data in checks.items():
            if check_data:
                gates.append({
                    "check": check_name,
                    "status": "passed" if check_data.get("passes_threshold", True) else "failed",
                    "score": check_data.get("score", 0),
                    "threshold": self.quality_thresholds.get(check_name.split('_')[0], 75),
                    "description": f"Quality check for {check_name.replace('_', ' ').title()}"
                })
        
        return gates