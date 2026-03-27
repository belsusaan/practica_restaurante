from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Query
from app.services import auth_service, notification_service
from jose import JWTError

router = APIRouter(tags=["notifications"])


@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    try:
        token_data = auth_service.decode_token(token)
        user_id = token_data.user_id

        await websocket.accept()
        notification_service.register_ws(user_id, websocket)

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            notification_service.unregister_ws(user_id)

    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    except Exception:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
