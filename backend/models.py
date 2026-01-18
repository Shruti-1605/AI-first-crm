from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

Base = declarative_base()

class HCPInteraction(Base):
    __tablename__ = "hcp_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), nullable=False)
    hcp_specialty = Column(String(100))
    interaction_type = Column(String(50))  # visit, call, email, etc.
    interaction_date = Column(DateTime, default=datetime.utcnow)
    raw_notes = Column(Text)
    ai_summary = Column(Text)
    key_topics = Column(Text)  # JSON string of extracted topics
    sentiment = Column(String(20))  # positive, neutral, negative
    next_action = Column(String(255))
    priority_level = Column(String(20))  # high, medium, low
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HCPProfile(Base):
    __tablename__ = "hcp_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(100))
    hospital_clinic = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    preferred_contact_method = Column(String(50))
    last_interaction_date = Column(DateTime)
    total_interactions = Column(Integer, default=0)
    relationship_strength = Column(Float, default=0.0)  # 0-10 scale
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm_database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()