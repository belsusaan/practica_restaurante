from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.notification import Notification


def create(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    ntype: str,
    related_order_id: int = None,
):
    db_notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=ntype,
        related_order_id=related_order_id,
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_for_user(db: Session, user_id: int):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(desc(Notification.created_at))
        .all()
    )


def mark_read(db: Session, notification_id: int, user_id: int):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )

    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)

    return notification
