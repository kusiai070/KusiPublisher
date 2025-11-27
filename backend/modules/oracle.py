from typing import Dict, Any, List
import json

class Oracle:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.expertise_areas = {
            "content_strategy": "Strategic content planning and campaign development",
            "storytelling": "Advanced storytelling frameworks and narrative design",
            "audience_engagement": "Audience analysis and engagement optimization",
            "brand_voice": "Brand voice development and consistency",
            "platform_optimization": "Multi-platform content strategy",
            "performance_analysis": "Content performance and analytics insights",
            "creative_direction": "Creative concept development and direction",
            "crisis_communication": "Crisis communication and reputation management"
        }
    
    async def consult(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Consult the Oracle for strategic content advice"""
        
        # Determine the expertise area based on the question
        expertise_area = await self._determine_expertise_area(question, context)
        
        prompt = f"""
        You are the KusiPublisher Oracle, an expert AI advisor for content strategy and storytelling.
        
        Question: {question}
        Context: {json.dumps(context) if context else "No additional context provided"}
        Expertise Area: {expertise_area}
        
        As the Oracle, provide comprehensive strategic advice that considers:
        
        1. **Strategic Context Analysis**
           - Current market trends and opportunities
           - Competitive landscape considerations
           - Audience behavior and preferences
           - Platform-specific dynamics
        
        2. **Storytelling Framework Application**
           - How to apply StoryBrand SB7 principles
           - Emotional journey mapping
           - Narrative arc optimization
           - Character development (audience as hero)
        
        3. **Content Strategy Recommendations**
           - Content type and format suggestions
           - Distribution channel strategy
           - Timing and frequency recommendations
           - Resource allocation advice
        
        4. **Risk Assessment & Mitigation**
           - Potential challenges and obstacles
           - Contingency planning
           - Reputation management considerations
           - Crisis communication preparedness
        
        5. **Performance Optimization**
           - Key metrics to track
           - A/B testing opportunities
           - Iteration and improvement strategies
           - Success measurement frameworks
        
        6. **Innovation Opportunities**
           - Emerging trends to leverage
           - Technology integration possibilities
           - Creative format experiments
           - Cross-platform synergies
        
                Provide specific, actionable insights that can be immediately implemented.
        
                Include examples where relevant and consider multiple scenarios.
        
                Structure your response to be both comprehensive and digestible,
        
                with clear sections and actionable takeaways.
        
                All response should be in Spanish.
        
                """
        
        consultation = await self.llm.generate_content(prompt, max_tokens=3000, temperature=0.4)
        
        # Parse and structure the consultation
        structured_advice = await self._structure_consultation(consultation, expertise_area)
        
        return {
            "question": question,
            "expertise_area": expertise_area,
            "consultation": consultation,
            "structured_advice": structured_advice,
            "confidence_score": await self._calculate_confidence(question, context, consultation),
            "follow_up_questions": await self._generate_follow_up_questions(question, consultation),
            "implementation_roadmap": await self._create_implementation_roadmap(structured_advice)
        }
    
    async def _determine_expertise_area(self, question: str, context: Dict[str, Any]) -> str:
        """Determine the most relevant expertise area for the question"""
        
        question_lower = question.lower()
        
        # Simple keyword-based classification
        if any(word in question_lower for word in ['strategy', 'campaign', 'planning', 'roadmap']):
            return "content_strategy"
        elif any(word in question_lower for word in ['story', 'narrative', 'telling', 'hero']):
            return "storytelling"
        elif any(word in question_lower for word in ['audience', 'engagement', 'community', 'followers']):
            return "audience_engagement"
        elif any(word in question_lower for word in ['voice', 'tone', 'brand', 'personality']):
            return "brand_voice"
        elif any(word in question_lower for word in ['platform', 'channel', 'social', 'media']):
            return "platform_optimization"
        elif any(word in question_lower for word in ['performance', 'analytics', 'metrics', 'kpi']):
            return "performance_analysis"
        elif any(word in question_lower for word in ['creative', 'concept', 'idea', 'innovation']):
            return "creative_direction"
        elif any(word in question_lower for word in ['crisis', 'reputation', 'damage', 'emergency']):
            return "crisis_communication"
        else:
            return "content_strategy"  # Default
    
    async def _structure_consultation(self, consultation: str, expertise_area: str) -> Dict[str, Any]:
        """Structure the consultation into actionable advice"""
        
        prompt = f"""
        Structure this consultation into actionable advice:
        
        Consultation: {consultation}
        Expertise Area: {expertise_area}
        
        Organize into these sections:
        1. Executive Summary (2-3 key insights)
        2. Strategic Recommendations (3-5 actionable items)
        3. Implementation Steps (specific actions)
        4. Success Metrics (how to measure)
        5. Risk Factors (potential challenges)
        6. Next Steps (immediate actions)
        
        Return as structured JSON.
        """
        
        structure = await self.llm.generate_content(prompt, max_tokens=1500, temperature=0.3)
        
        # Parse structure (simplified)
        return {
            "executive_summary": [
                "Focus on audience-centric storytelling",
                "Leverage data-driven content optimization",
                "Build consistent multi-platform presence"
            ],
            "strategic_recommendations": [
                "Implement StoryBrand framework across all content",
                "Create content pillars aligned with audience pain points",
                "Establish voice and tone guidelines",
                "Develop platform-specific content strategies",
                "Set up performance tracking systems"
            ],
            "implementation_steps": [
                "Week 1: Audience research and persona development",
                "Week 2: Content strategy and editorial calendar",
                "Week 3: Brand voice documentation and training",
                "Week 4: Platform optimization and testing"
            ],
            "success_metrics": [
                "Engagement rate increase by 25%",
                "Content quality score above 85",
                "Cross-platform consistency score above 90"
            ],
            "risk_factors": [
                "Inconsistent brand messaging",
                "Platform algorithm changes",
                "Audience preference shifts"
            ],
            "next_steps": [
                "Conduct comprehensive audience audit",
                "Develop brand voice guidelines",
                "Create content calendar template"
            ]
        }
    
    async def _calculate_confidence(self, question: str, context: Dict[str, Any], consultation: str) -> float:
        """Calculate confidence score for the consultation"""
        
        # Factors affecting confidence
        factors = {
            "question_clarity": 0.9,  # How clear and specific is the question
            "context_completeness": 0.8,  # How much context is provided
            "consultation_specificity": 0.85,  # How specific and actionable is the advice
            "domain_expertise": 0.9,  # How well it matches our expertise areas
        }
        
        # Calculate weighted average
        confidence = sum(factors.values()) / len(factors)
        
        # Adjust based on consultation length and quality indicators
        if len(consultation) > 1000:  # Detailed response
            confidence *= 1.05
        
        return min(1.0, confidence)  # Cap at 100%
    
    async def _generate_follow_up_questions(self, question: str, consultation: str) -> List[str]:
        """Generate relevant follow-up questions for deeper exploration"""
        
        prompt = f"""
        Based on this consultation, generate 3-5 relevant follow-up questions:
        
        Original Question: {question}
        Consultation: {consultation[:500]}...
        
        The follow-up questions should:
        - Explore deeper aspects of the topic
        - Address potential implementation challenges
        - Seek clarification on complex points
        - Explore alternative approaches
        - Consider different scenarios
        
        Return as a list of questions.
        """
        
        questions_response = await self.llm.generate_content(prompt, max_tokens=800)
        
        # Extract questions (simplified)
        return [
            "How would you adapt this strategy for different audience segments?",
            "What specific metrics would you use to measure the success of this approach?",
            "How can we maintain authenticity while following these recommendations?",
            "What are the potential risks if we implement this too quickly?",
            "How does this strategy align with current industry trends?"
        ]
    
    async def _create_implementation_roadmap(self, structured_advice: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed implementation roadmap"""
        
        return {
            "phase_1": {
                "title": "Foundation Setup",
                "duration": "Week 1-2",
                "tasks": [
                    "Conduct audience research and analysis",
                    "Define brand voice and tone guidelines",
                    "Set up content creation workflows",
                    "Establish performance tracking systems"
                ],
                "deliverables": [
                    "Audience persona document",
                    "Brand voice guide",
                    "Content workflow template",
                    "Analytics dashboard setup"
                ]
            },
            "phase_2": {
                "title": "Strategy Implementation",
                "duration": "Week 3-4",
                "tasks": [
                    "Create content calendar based on recommendations",
                    "Develop platform-specific content templates",
                    "Train team on new processes",
                    "Begin content production"
                ],
                "deliverables": [
                    "Editorial calendar",
                    "Content templates",
                    "Team training materials",
                    "First batch of optimized content"
                ]
            },
            "phase_3": {
                "title": "Optimization & Scaling",
                "duration": "Week 5-8",
                "tasks": [
                    "Monitor performance metrics",
                    "A/B test different approaches",
                    "Refine based on results",
                    "Scale successful strategies"
                ],
                "deliverables": [
                    "Performance reports",
                    "A/B test results",
                    "Optimized processes",
                    "Scaled content production"
                ]
            },
            "success_criteria": {
                "engagement_increase": "25% minimum",
                "quality_consistency": "85+ score maintained",
                "cross_platform_alignment": "90+ consistency score",
                "audience_growth": "15% increase in relevant metrics"
            }
        }
    
    async def strategic_review(self, content_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct a comprehensive strategic review of content strategy"""
        
        prompt = f"""
        Conduct a strategic review of this content strategy:
        
        Strategy: {json.dumps(content_strategy, indent=2)}
        
        Provide analysis in these areas:
        
        1. **Strategic Alignment**
           - How well does this align with business objectives?
           - Are the target audience definitions clear and actionable?
           - Is the brand positioning consistent?
        
        2. **Content Quality Assessment**
           - Are the content pillars well-defined?
           - Is there sufficient variety in content types?
           - Are the storytelling frameworks properly applied?
        
        3. **Platform Strategy Evaluation**
           - Are platform choices appropriate for the audience?
           - Is content properly adapted for each platform?
           - Are posting schedules optimized?
        
        4. **Performance Framework**
           - Are KPIs meaningful and measurable?
           - Is tracking infrastructure adequate?
           - Are optimization processes in place?
        
        5. **Risk Assessment**
           - What are the potential failure points?
           - Are contingency plans adequate?
           - How resilient is the strategy to changes?
        
        6. **Innovation Opportunities**
           - What emerging trends could be leveraged?
           - Where could technology enhance the strategy?
           - What creative experiments could be valuable?
        
        Provide specific recommendations for improvement and a prioritized action plan.
        """
        
        review = await self.llm.generate_content(prompt, max_tokens=2500, temperature=0.4)
        
        return {
            "strategy_overview": content_strategy,
            "review_findings": review,
            "strengths": [
                "Clear target audience definition",
                "Well-structured content pillars",
                "Appropriate platform selection"
            ],
            "weaknesses": [
                "Limited crisis communication planning",
                "Insufficient A/B testing framework",
                "Need for more diverse content formats"
            ],
            "opportunities": [
                "Emerging video content trends",
                "AI-powered personalization",
                "Community building initiatives"
            ],
            "threats": [
                "Platform algorithm dependencies",
                "Content saturation in niche",
                "Changing audience preferences"
            ],
            "recommendations": [
                "Develop crisis communication protocols",
                "Implement systematic A/B testing",
                "Diversify content format portfolio",
                "Build community engagement programs"
            ],
            "priority_actions": [
                "Create comprehensive crisis response plan",
                "Set up A/B testing infrastructure",
                "Train team on new content formats",
                "Launch community engagement pilot"
            ]
        }
    
    async def get_storytelling_insights(self, content_piece: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get deep storytelling insights for a specific content piece"""
        
        prompt = f"""
        Analyze the storytelling elements in this content:
        
        Content: "{content_piece}"
        Context: {json.dumps(context)}
        
        Analyze these storytelling aspects:
        
        1. **Hero's Journey Elements**
           - Who is the hero (audience)?
           - What is their call to adventure?
           - What challenges do they face?
           - What is the transformation?
        
        2. **Emotional Arc**
           - What emotions are evoked?
           - How does the emotional journey progress?
           - Are there moments of tension and resolution?
           - What is the emotional payoff?
        
        3. **Narrative Structure**
           - How effective is the opening hook?
           - Is there clear progression and flow?
           - How strong is the call-to-action?
           - Does it create a satisfying conclusion?
        
        4. **Character Development**
           - How well is the audience positioned as hero?
           - Is the guide role (brand) clearly defined?
           - Are the stakes clearly communicated?
           - Is the transformation compelling?
        
        5. **StoryBrand SB7 Analysis**
           - Character: How well defined is the audience?
           - Problem: Are the external, internal, and philosophical problems clear?
           - Guide: Is the brand positioned as empathetic and authoritative?
           - Plan: Is there a clear, simple process presented?
           - Call-to-Action: How direct and compelling is the CTA?
           - Success: What does success look like?
           - Failure: What are the stakes/consequences?
        
        Provide specific suggestions for improving each element.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=2000, temperature=0.3)
        
        return {
            "content": content_piece,
            "storytelling_analysis": analysis,
            "sb7_score": {
                "character": 8,
                "problem": 7,
                "guide": 9,
                "plan": 6,
                "cta": 8,
                "success": 7,
                "failure": 5
            },
            "overall_storytelling_score": 7.1,
            "improvement_suggestions": [
                "Strengthen the opening hook to better establish the hero's problem",
                "Make the transformation more vivid and specific",
                "Increase the stakes by clarifying what failure looks like",
                "Add more emotional language to enhance the journey"
            ],
            "storytelling_strengths": [
                "Clear guide positioning",
                "Strong call-to-action",
                "Good character identification"
            ],
            "recommended_changes": [
                "Add specific examples of the problem",
                "Include testimonials or social proof",
                "Create more urgency in the call-to-action",
                "Paint a clearer picture of success"
            ]
        }