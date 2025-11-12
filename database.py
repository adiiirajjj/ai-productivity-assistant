from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./productivity.db"

Base = declarative_base()

class ProductivityRecord(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    hours_worked = Column(Float)
    sleep_hours = Column(Float)
    tasks_completed = Column(Integer)
    breaks_taken = Column(Integer)
    focus_level = Column(Float)
    prediction = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
