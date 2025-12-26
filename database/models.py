from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .db import Base

# Tables d'association pour les tags
activity_tags = Table('activity_tags', Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

scelle_tags = Table('scelle_tags', Base.metadata,
    Column('scelle_id', Integer, ForeignKey('scelles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class KanbanColumn(Base):
    __tablename__ = "kanban_columns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    order_index = Column(Integer, default=0)
    
    activities = relationship("Activity", back_populates="column")

    def __repr__(self):
        return self.name

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color = Column(String, default="#CCCCCC")

    def __repr__(self):
        return self.name

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    column_id = Column(Integer, ForeignKey("kanban_columns.id"))

    column = relationship("KanbanColumn", back_populates="activities")
    scelles = relationship("Scelle", back_populates="activity", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=activity_tags, backref="activities")

class Scelle(Base):
    __tablename__ = "scelles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    info = Column(Text, nullable=True) # "Informations"
    
    # New fields
    cta_validated = Column(Boolean, default=False)
    reparations_validated = Column(Boolean, default=False)
    reparations_details = Column(Text, nullable=True)
    important_info = Column(Text, nullable=True)
    
    activity_id = Column(Integer, ForeignKey("activities.id"))

    activity = relationship("Activity", back_populates="scelles")
    traitements = relationship("Traitement", back_populates="scelle", cascade="all, delete-orphan")
    taches = relationship("Tache", back_populates="scelle", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=scelle_tags, backref="scelles")

class Traitement(Base):
    __tablename__ = "traitements"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    done = Column(Boolean, default=False)
    done_at = Column(Date, nullable=True)
    scelle_id = Column(Integer, ForeignKey("scelles.id"))

    scelle = relationship("Scelle", back_populates="traitements")

class Tache(Base):
    __tablename__ = "taches"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    done_at = Column(Date, nullable=True)
    scelle_id = Column(Integer, ForeignKey("scelles.id"))

    scelle = relationship("Scelle", back_populates="taches")
