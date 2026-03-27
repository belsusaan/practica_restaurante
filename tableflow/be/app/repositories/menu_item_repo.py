from sqlalchemy.orm import Session
from app.models.menu_item import MenuItem


def get_all(db: Session):
    return db.query(MenuItem).all()


def get_available(db: Session):
    return db.query(MenuItem).filter(MenuItem.is_available == True).all()


def get_by_id(db: Session, item_id: int):
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()


def create(db: Session, data_dict: dict):
    db_item = MenuItem(**data_dict)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update(db: Session, item: MenuItem, data_dict: dict):
    for key, value in data_dict.items():
        if value is not None:
            setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def toggle_availability(db: Session, item: MenuItem):
    item.is_available = not item.is_available
    db.commit()
    db.refresh(item)
    return item
