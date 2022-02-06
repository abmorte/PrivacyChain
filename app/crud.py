from sqlalchemy.orm import Session
from . import models, schemas

def get_tracking(db: Session, tracking_id: int):
    return db.query(models.Tracking).filter(models.Tracking.tracking_id == tracking_id).first()

def get_tracking_by_transaction_id(db: Session, transaction_id: str):
    return db.query(models.Tracking).filter(models.Tracking.transaction_id == transaction_id).first()

def get_trackings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tracking).offset(skip).limit(limit).all()

def create_tracking(db: Session, tracking: schemas.TrackingCreate):
    db_tracking = models.Tracking(canonical_data = tracking.canonical_data, anonymized_data = tracking.anonymized_data, 
                                                    blockchain_id = tracking.blockchain_id, transaction_id = tracking.transaction_id, 
                                                    salt = tracking.salt, hash_method = tracking.hash_method, 
                                                    tracking_dt = tracking.tracking_dt, locator = tracking.locator)
    db.add(db_tracking)
    db.commit()
    db.refresh(db_tracking)
    return db_tracking

def get_trackings_for_unindex(db: Session, locator: str, datetime: str):
    if datetime:
        print('get_trackings_for_unindex: Datetime is NOT EMPTY string')    
        return db.query(models.Tracking) \
            .filter(models.Tracking.locator == locator) \
            .filter((models.Tracking.tracking_dt == datetime)).all()        
    else:
        print('get_trackings_for_unindex: Datetime is EMPTY string')            
        return db.query(models.Tracking).filter(models.Tracking.locator == locator).all()        
        
def delete_trackings_for_unindex(db: Session, locator: str, datetime: str):
    if datetime:
        print('delete_trackings_for_unindex: Datetime is NOT EMPTY string')
        db_tracking = db.query(models.Tracking) \
            .filter(models.Tracking.locator == locator) \
            .filter((models.Tracking.tracking_dt == datetime)).delete(synchronize_session='fetch')
    else:
        print('delete_trackings_for_unindex: Datetime is EMPTY string')
        db_tracking = db.query(models.Tracking) \
            .filter(models.Tracking.locator == locator).delete(synchronize_session='fetch')
    db.commit()
    return db_tracking