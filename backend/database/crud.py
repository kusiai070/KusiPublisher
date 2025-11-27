from sqlalchemy.orm import Session
from . import models

def create_user(db: Session, email: str, name: str):
    db_user = models.User(email=email, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_campaign(db: Session, user_id: int, name: str, objective: str, target_audience: dict, platforms: list, tone: str):
    db_campaign = models.Campaign(
        user_id=user_id,
        name=name,
        objective=objective,
        target_audience=target_audience,
        platforms=platforms,
        tone=tone
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def create_content_piece(db: Session, campaign_id: int, title: str, original_text: str, platform: str):
    db_content = models.ContentPiece(
        campaign_id=campaign_id,
        title=title,
        original_text=original_text,
        current_text=original_text,
        platform=platform
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def save_content_version(db: Session, content_piece_id: int, user_id: int, text: str, changes: dict):
    # Get current version
    last_version = db.query(models.ContentHistory).filter(
        models.ContentHistory.content_piece_id == content_piece_id
    ).order_by(models.ContentHistory.version.desc()).first()
    
    new_version = (last_version.version + 1) if last_version else 1
    
    db_history = models.ContentHistory(
        content_piece_id=content_piece_id,
        user_id=user_id,
        version=new_version,
        text=text,
        changes=changes
    )
    db.add(db_history)
    
    # Update current text in content piece
    content_piece = db.query(models.ContentPiece).filter(
        models.ContentPiece.id == content_piece_id
    ).first()
    if content_piece:
        content_piece.current_text = text
    
    db.commit()
    return db_history

def create_voice_profile(db: Session, user_id: int, name: str, description: str, characteristics: dict, sample_text: str):
    db_profile = models.VoiceProfile(
        user_id=user_id,
        name=name,
        description=description,
        characteristics=characteristics,
        sample_text=sample_text
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def save_knowledge(db: Session, user_id: int, category: str, key: str, value: dict, confidence: float = 1.0):
    db_knowledge = models.KnowledgeBase(
        user_id=user_id,
        category=category,
        key=key,
        value=value,
        confidence=confidence
    )
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

def get_knowledge_by_category(db: Session, user_id: int, category: str):
    return db.query(models.KnowledgeBase).filter(
        models.KnowledgeBase.user_id == user_id,
        models.KnowledgeBase.category == category
    ).all()