from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base

class Tracking(Base):
    __tablename__ = "tracking"
    
    tracking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    canonical_data = Column(String)
    anonymized_data = Column(String)
    blockchain_id = Column(Integer, index=True) 
    transaction_id = Column(String)
    salt = Column(String)
    hash_method = Column(String)
    tracking_dt = Column(String)
    locator = Column(String)
