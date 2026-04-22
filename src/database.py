"""
Database configuration and models for the High School Management System.

Uses SQLAlchemy with SQLite for persistent data storage of activities and participants.
"""

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from pathlib import Path

# Database setup
DATABASE_URL = "sqlite:///./mergington_school.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for many-to-many relationship between Activities and Participants
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('participant_email', String, ForeignKey('participants.email'), primary_key=True)
)


class Activity(Base):
    """Model for an extracurricular activity"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    schedule = Column(String)
    max_participants = Column(Integer)

    # Relationship to participants
    participants = relationship(
        "Participant",
        secondary=activity_participants,
        back_populates="activities"
    )


class Participant(Base):
    """Model for a student participant"""
    __tablename__ = "participants"

    email = Column(String, primary_key=True, index=True)

    # Relationship to activities
    activities = relationship(
        "Activity",
        secondary=activity_participants,
        back_populates="participants"
    )


def init_db():
    """Initialize database tables and populate with seed data"""
    Base.metadata.create_all(bind=engine)
    
    # Only populate if database is empty
    db = SessionLocal()
    try:
        if db.query(Activity).count() == 0:
            # Seed data from original in-memory database
            seed_activities = [
                {
                    "name": "Chess Club",
                    "description": "Learn strategies and compete in chess tournaments",
                    "schedule": "Fridays, 3:30 PM - 5:00 PM",
                    "max_participants": 12,
                    "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
                },
                {
                    "name": "Programming Class",
                    "description": "Learn programming fundamentals and build software projects",
                    "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                    "max_participants": 20,
                    "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
                },
                {
                    "name": "Gym Class",
                    "description": "Physical education and sports activities",
                    "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                    "max_participants": 30,
                    "participants": ["john@mergington.edu", "olivia@mergington.edu"]
                },
                {
                    "name": "Soccer Team",
                    "description": "Join the school soccer team and compete in matches",
                    "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                    "max_participants": 22,
                    "participants": ["liam@mergington.edu", "noah@mergington.edu"]
                },
                {
                    "name": "Basketball Team",
                    "description": "Practice and play basketball with the school team",
                    "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
                    "max_participants": 15,
                    "participants": ["ava@mergington.edu", "mia@mergington.edu"]
                },
                {
                    "name": "Art Club",
                    "description": "Explore your creativity through painting and drawing",
                    "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                    "max_participants": 15,
                    "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
                },
                {
                    "name": "Drama Club",
                    "description": "Act, direct, and produce plays and performances",
                    "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                    "max_participants": 20,
                    "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
                },
                {
                    "name": "Math Club",
                    "description": "Solve challenging problems and participate in math competitions",
                    "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
                    "max_participants": 10,
                    "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
                },
                {
                    "name": "Debate Team",
                    "description": "Develop public speaking and argumentation skills",
                    "schedule": "Fridays, 4:00 PM - 5:30 PM",
                    "max_participants": 12,
                    "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
                }
            ]

            for activity_data in seed_activities:
                participants_emails = activity_data.pop("participants")
                activity = Activity(**activity_data)
                
                for email in participants_emails:
                    participant = db.query(Participant).filter(
                        Participant.email == email
                    ).first()
                    if not participant:
                        participant = Participant(email=email)
                    activity.participants.append(participant)
                
                db.add(activity)
            
            db.commit()
    finally:
        db.close()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
