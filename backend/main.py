from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
from contextlib import asynccontextmanager
import asyncio
import traceback

from database.database import get_db, create_tables
from database import crud
from api.llm import LLMManager
from modules.planning import PlanningModule
from modules.voice_analyzer import VoiceAnalyzer
from modules.quality_agent import QualityAgent
from modules.seo_researcher import SEOResearcher
from modules.humanizer import Humanizer
from modules.platform_agents import PlatformAgents
from modules.oracle import Oracle
from modules.visual_generator import VisualGenerator
from modules.journalism_agent import JournalismAgent # Importar JournalismAgent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    app.state.llm_manager = LLMManager()
    app.state.modules = {
        "planning": PlanningModule(app.state.llm_manager),
        "voice_analyzer": VoiceAnalyzer(app.state.llm_manager),
        "quality_agent": QualityAgent(app.state.llm_manager),
        "seo_researcher": SEOResearcher(app.state.llm_manager),
        "humanizer": Humanizer(app.state.llm_manager),
        "platform_agents": PlatformAgents(app.state.llm_manager),
        "oracle": Oracle(app.state.llm_manager),
        "visual_generator": VisualGenerator(app.state.llm_manager),
        "journalism": JournalismAgent(app.state.llm_manager) # Inicializar JournalismAgent
    }
    yield
    # Shutdown
    pass

app = FastAPI(title="KusiPublisher API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "KusiPublisher API"}

# User management
@app.post("/users")
async def create_user(email: str, name: str, db: Session = Depends(get_db)):
    return crud.create_user(db, email, name)

# Campaign management
@app.post("/campaigns")
async def create_campaign(
    user_id: int,
    name: str,
    objective: str,
    target_audience: dict,
    platforms: list,
    tone: str,
    db: Session = Depends(get_db)
):
    return crud.create_campaign(db, user_id, name, objective, target_audience, platforms, tone)

class ContentRequest(BaseModel):
    campaign_id: int
    title: str
    original_text: str
    platform: str
    journalism_mode: bool = False # Añadir journalism_mode

# Content management
@app.post("/content")
async def create_content(request: ContentRequest, db: Session = Depends(get_db)):
    print(f"\n--- DEBUG: Received request for /content ---")
    try:
        if request.journalism_mode:
            print(f"--- DEBUG: Journalism mode enabled for platform: {request.platform} ---")
            journalism_agent = app.state.modules["journalism"]
            # For journalism mode, we use the original_text as topic for generation
            generated = await journalism_agent.generate_journalistic_content(
                topic=request.original_text, 
                platform=request.platform,
                style="opinion" # User specified "opinion" style
            )
            optimized_content = generated["content"]
            explanations = f"Contenido periodístico generado en estilo: {generated['style']}"
            
        else:
            # Generar contenido optimizado con LLM
            platform_agents = app.state.modules["platform_agents"]
            print(f"--- DEBUG: Calling optimize_for_platform with original_text (first 50 chars): {request.original_text[:50]}... and platform: {request.platform} ---")
            optimized = await platform_agents.optimize_for_platform(
                request.original_text, 
                request.platform
            )
            print(f"=== OPTIMIZED RESULT FOR {request.platform} ===")
            print(f"Type: {type(optimized)}")
            print(f"Content (first 200 chars): {str(optimized)[:200]}")
            print(f"Keys (if dict): {optimized.keys() if isinstance(optimized, dict) else 'N/A'}")
            print(f"--- DEBUG: optimize_for_platform returned optimized optimized content. ---")
            optimized_content = optimized.get("optimized_content", request.original_text)
            explanations = optimized.get("explanations", "Contenido optimizado para la plataforma.")
        
        # Guardar en DB con contenido generado
        content = crud.create_content_piece(
            db,
            request.campaign_id,
            request.title,
            request.original_text,
            request.platform
        )
        
        # Actualizar con texto optimizado
        content.current_text = optimized_content
        content.metadata = {"explanations": explanations, "journalism_mode": request.journalism_mode}
        
        print(f"=== GUARDANDO EN DB ===")
        print(f"current_text (first 200): {content.current_text[:200]}")
        
        db.commit()
        db.refresh(content)
        print(f"--- DEBUG: Content created and optimized. ---")
        
        print(f"=== RESPONSE ===")
        print(f"generated_content: {content.current_text[:200]}")

        return {
            "id": content.id,
            "generated_content": content.current_text,
            "platform": content.platform,
            "title": content.title,
            "explanations": explanations
        }
    except Exception as e:
        print(f"!!!!!!!!!!!!!! ERROR IN /content !!!!!!!!!!!!!!")
        traceback.print_exc()
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        raise HTTPException(status_code=500, detail=str(e))

# Planning module
@app.post("/planning/start")
async def start_planning(campaign_id: int, db: Session = Depends(get_db)):
    module = app.state.modules["planning"]
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    result = await module.start_planning_flow(campaign)
    return result

# Voice analysis
@app.post("/analyze/voice")
async def analyze_voice(text: str):
    module = app.state.modules["voice_analyzer"]
    result = await module.analyze_voice(text)
    return result

class QualityRequest(BaseModel):
    content: str

# Quality check
@app.post("/analyze/quality")
async def analyze_quality(request: QualityRequest):
    print(f"\n--- DEBUG: Received request for /analyze/quality ---")
    try:
        module = app.state.modules["quality_agent"]
        print(f"--- DEBUG: Calling quality_check with content (first 50 chars): {request.content[:50]}... ---")
        result = await module.quality_check(request.content)
        print(f"--- DEBUG: /analyze/quality successful. ---")
        return result
    except Exception as e:
        print(f"!!!!!!!!!!!!!! ERROR IN /analyze/quality !!!!!!!!!!!!!!")
        traceback.print_exc()
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        raise HTTPException(status_code=500, detail=str(e))

# SEO research
@app.post("/research/seo")
async def research_seo(topic: str, platform: str = "general"):
    module = app.state.modules["seo_researcher"]
    result = await module.research_keywords(topic, platform)
    return result

class HumanizeRequest(BaseModel):
    text: str
    voice_profile: dict = None

# Content humanization
@app.post("/humanize")
async def humanize_content(request: HumanizeRequest):
    module = app.state.modules["humanizer"]
    result = await module.humanize(request.text, request.voice_profile)
    return result

# Platform optimization
@app.post("/optimize/platform")
async def optimize_for_platform(text: str, platform: str):
    module = app.state.modules["platform_agents"]
    result = await module.optimize_for_platform(text, platform)
    return result

class OracleRequest(BaseModel):
    question: str
    context: dict = None

# Oracle consultation
@app.post("/oracle/consult")
async def consult_oracle(request: OracleRequest):
    module = app.state.modules["oracle"]
    result = await module.consult(request.question, request.context)
    return result

# Visual suggestions
@app.post("/visual/suggest")
async def suggest_visuals(text: str, platform: str = None):
    module = app.state.modules["visual_generator"]
    result = await module.suggest_visuals(text, platform)
    return result

# LLM Provider management
@app.get("/llm/providers")
async def get_providers():
    return app.state.llm_manager.get_available_providers()

@app.post("/llm/switch")
async def switch_provider(provider: str):
    try:
        app.state.llm_manager.switch_provider(provider)
        return {"status": "success", "provider": provider}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Content history
@app.get("/content/{content_id}/history")
async def get_content_history(content_id: int, db: Session = Depends(get_db)):
    history = db.query(models.ContentHistory).filter(
        models.ContentHistory.content_piece_id == content_id
    ).order_by(models.ContentHistory.version.desc()).all()
    return history

# Performance metrics
@app.post("/metrics")
async def save_metrics(
    content_piece_id: int,
    platform: str,
    impressions: int,
    engagement: int,
    clicks: int,
    shares: int,
    db: Session = Depends(get_db)
):
    metric = models.PerformanceMetrics(
        content_piece_id=content_piece_id,
        platform=platform,
        impressions=impressions,
        engagement=engagement,
        clicks=clicks,
        shares=shares
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@app.get("/metrics/summary")
async def get_metrics_summary():
    """
    Returns a summary of key performance metrics for the dashboard.
    (Currently returns dummy data)
    """
    return {
        "total_content": 156,
        "published_content": 89,
        "average_quality_score": 87,
        "content_this_week": 12,
        "total_content_change": "+12%",
        "published_content_change": "+8%"
    }


@app.get("/content/recent")
async def get_recent_content():
    """
    Returns a list of recently generated/published content.
    (Currently returns dummy data)
    """
    return [
        {
            "id": 1,
            "title": "📘 LinkedIn post about AI trends",
            "platform": "LinkedIn",
            "status": "publicado",
            "timestamp": "Hace 2 horas"
        },
        {
            "id": 2,
            "title": "📝 Blog outline for SEO strategies",
            "platform": "Blog",
            "status": "borrador",
            "timestamp": "Hace 4 horas"
        },
        {
            "id": 3,
            "title": "🐦 Twitter thread about productivity",
            "platform": "Twitter",
            "status": "publicado",
            "timestamp": "Ayer"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)