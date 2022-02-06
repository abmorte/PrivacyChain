from typing import List, Optional
from pydantic import BaseModel

class TrackingBase(BaseModel):
    canonical_data: str
    anonymized_data: str
    blockchain_id: int
    transaction_id: str
    salt: str
    hash_method: str
    tracking_dt: str
    locator: str
    
class TrackingCreate(TrackingBase):
    pass

class Tracking(TrackingBase):
    tracking_id: int
    canonical_data: str
    anonymized_data: str
    blockchain_id: int
    transaction_id: str
    salt: str
    hash_method: str
    tracking_dt: str
    locator: str
    
    class Config:
        orm_mode = True