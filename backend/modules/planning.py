from typing import Dict, Any, List
import json

class PlanningModule:
    def __init__(self, llm_manager):
        self.llm = llm_manager
        self.planning_stages = {
            "requirements": {
                "name": "Requisitos del Contenido",
                "description": "Definir objetivo, audiencia, plataformas y tono",
                "fields": ["objective", "target_audience", "platforms", "tone", "key_messages"]
            },
            "storytelling": {
                "name": "Diseño de Storytelling",
                "description": "Aplicar frameworks SB7, Guber y Salas",
                "fields": ["hero", "problem", "plan", "call_to_action", "emotional_hooks"]
            },
            "tasks": {
                "name": "Tareas de Contenido",
                "description": "Desglose granular de tareas específicas",
                "fields": ["research_tasks", "writing_tasks", "visual_tasks", "review_tasks"]
            }
        }
    
    async def start_planning_flow(self, campaign) -> Dict[str, Any]:
        """Start the planning workflow for a campaign"""
        
        results = {
            "campaign_id": campaign.id,
            "campaign_name": campaign.name,
            "stages": {}
        }
        
        # Stage 1: Requirements Analysis
        results["stages"]["requirements"] = await self._analyze_requirements(campaign)
        
        # Stage 2: Storytelling Design
        results["stages"]["storytelling"] = await self._design_storytelling(campaign)
        
        # Stage 3: Task Breakdown
        results["stages"]["tasks"] = await self._breakdown_tasks(campaign)
        
        return results
    
    async def _analyze_requirements(self, campaign) -> Dict[str, Any]:
        """Analyze campaign requirements using storytelling frameworks"""
        
        prompt = f"""
        Analyze the content requirements for this campaign:
        
        Campaign: {campaign.name}
        Objective: {campaign.objective}
        Target Audience: {campaign.target_audience}
        Platforms: {campaign.platforms}
        Tone: {campaign.tone}
        
        Using storytelling frameworks, identify:
        1. The core problem this content solves
        2. The transformation the audience seeks
        3. Key emotional triggers
        4. Platform-specific considerations
        5. Success metrics for each platform
        
        Return a structured analysis with actionable insights.
        """
        
        analysis = await self.llm.generate_content(prompt, max_tokens=1500)
        
        return {
            "status": "completed",
            "analysis": analysis,
            "requires_approval": True,
            "next_stage": "storytelling"
        }
    
    async def _design_storytelling(self, campaign) -> Dict[str, Any]:
        """Design storytelling using SB7, Guber, and Salas frameworks"""
        
        prompt = f"""
        Design the storytelling strategy for this campaign:
        
        Campaign: {campaign.name}
        Objective: {campaign.objective}
        Audience: {campaign.target_audience}
        
        Apply these frameworks:
        
        1. **StoryBrand SB7 Framework**:
           - Character (Hero): Who is the audience?
           - Problem: What problem do they face?
           - Guide: How does the brand help?
           - Plan: What's the step-by-step solution?
           - Call to Action: What should they do?
           - Success: What does success look like?
           - Failure: What happens if they don't act?
        
        2. **Guber's FEEL/DO Framework**:
           - FEEL: What should the audience feel?
           - DO: What should the audience do?
        
        3. **Salas Hooks**:
           - Pattern Interrupt: How to grab attention?
           - Open Loop: What question to pose?
           - Social Proof: What credibility to establish?
           - Future Pace: What vision to paint?
        
        Create a cohesive narrative that incorporates all frameworks.
        """
        
        storytelling = await self.llm.generate_content(prompt, max_tokens=2000)
        
        return {
            "status": "completed",
            "storytelling_framework": storytelling,
            "requires_approval": True,
            "next_stage": "tasks"
        }
    
    async def _breakdown_tasks(self, campaign) -> Dict[str, Any]:
        """Break down content creation into granular tasks"""
        
        prompt = f"""
        Break down the content creation process for campaign: {campaign.name}
        
        Create a detailed task breakdown including:
        
        1. **Research Tasks**:
           - Audience research activities
           - Competitor analysis tasks
           - Trend research tasks
           - Keyword research tasks
        
        2. **Content Writing Tasks**:
           - Outline creation
           - Draft writing (per platform)
           - Review and editing tasks
           - Optimization tasks
        
        3. **Visual Content Tasks**:
           - Image research/generation
           - Video concept development
           - Graphic design tasks
           - Brand consistency checks
        
        4. **Quality Assurance Tasks**:
           - Grammar and spell check
           - Brand voice consistency
           - Platform optimization
           - Legal compliance review
        
        Each task should have:
        - Clear description
        - Estimated time
        - Dependencies
        - Success criteria
        """
        
        tasks = await self.llm.generate_content(prompt, max_tokens=2000)
        
        return {
            "status": "completed",
            "task_breakdown": tasks,
            "requires_approval": True,
            "next_stage": "execution"
        }
    
    async def approve_stage(self, stage_name: str, approval_data: Dict[str, Any]) -> Dict[str, Any]:
        """Approve a planning stage and move to the next"""
        
        return {
            "stage": stage_name,
            "status": "approved",
            "approved_at": "2025-01-24T10:00:00Z",  # This would be actual timestamp
            "approval_data": approval_data,
            "next_stage": self.planning_stages.get(stage_name, {}).get("next_stage")
        }
    
    async def get_planning_summary(self, campaign_id: int) -> Dict[str, Any]:
        """Get a summary of the planning process"""
        
        return {
            "campaign_id": campaign_id,
            "current_stage": "storytelling",  # This would be dynamic
            "completed_stages": ["requirements"],
            "pending_stages": ["storytelling", "tasks"],
            "overall_progress": 33,
            "next_action": "Complete storytelling design"
        }