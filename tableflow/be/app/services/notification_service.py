import asyncio
import json
from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.repositories import notification_repo

_connections: dict[int, WebSocket] = {}


def register_ws(user_id: int, websocket: WebSocket):
    _connections[user_id] = websocket


def unregister_ws(user_id: int):
    if user_id in _connections:
        del _connections[user_id]


async def push(user_id: int, payload_dict: dict):
    websocket = _connections.get(user_id)
    if websocket:
        try:
            await websocket.send_text(json.dumps(payload_dict))
        except Exception:
            unregister_ws(user_id)


async def send(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    ntype: str,
    related_order_id: int = None,
):
    notification = notification_repo.create(
        db,
        user_id=user_id,
        title=title,
        message=message,
        ntype=ntype,
        related_order_id=related_order_id,
    )

    payload = {
        "id": notification.id,
        "title": notification.title,
        "message": notification.message,
        "type": notification.type,
        "related_order_id": notification.related_order_id,
        "created_at": notification.created_at.isoformat(),
    }

    await push(user_id, payload)
    return notification


def get_user_notifications(db: Session, user_id: int):
    return notification_repo.get_for_user(db, user_id)
