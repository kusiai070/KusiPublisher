from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    content_history = relationship("ContentHistory", back_populates="user")
    voice_profiles = relationship("VoiceProfile", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")

class VoiceProfile(Base):
    __tablename__ = "voice_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(Text)
    characteristics = Column(JSON)
    sample_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="voice_profiles")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    objective = Column(Text)
    target_audience = Column(JSON)
    platforms = Column(JSON)
    tone = Column(String)
    status = Column(String, default="planning")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="campaigns")
    content_pieces = relationship("ContentPiece", back_populates="campaign")

class ContentPiece(Base):
    __tablename__ = "content_pieces"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    title = Column(String)
    original_text = Column(Text)
    current_text = Column(Text)
    platform = Column(String)
    status = Column(String, default="draft")
    quality_score = Column(Float)
    seo_keywords = Column(JSON)
    visual_suggestions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    campaign = relationship("Campaign", back_populates="content_pieces")
    history = relationship("ContentHistory", back_populates="content_piece")

class ContentHistory(Base):
    __tablename__ = "content_history"
    
    id = Column(Integer, primary_key=True, index=True)
    content_piece_id = Column(Integer, ForeignKey("content_pieces.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer)
    text = Column(Text)
    changes = Column(JSON)
    performance_metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    content_piece = relationship("ContentPiece", back_populates="history")
    user = relationship("User", back_populates="content_history")

class SEOAnalysis(Base):
    __tablename__ = "seo_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    content_piece_id = Column(Integer, ForeignKey("content_pieces.id"))
    keywords = Column(JSON)
    trends = Column(JSON)
    suggestions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class PerformanceMetrics(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    content_piece_id = Column(Integer, ForeignKey("content_pieces.id"))
    platform = Column(String)
    impressions = Column(Integer)
    engagement = Column(Integer)
    clicks = Column(Integer)
    shares = Column(Integer)
    collected_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    key = Column(String)
    value = Column(JSON)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)