from sqlalchemy.orm import Session
from app.repositories import order_repo, menu_item_repo
from app.services import kitchen_grpc_client, notification_service
from app.schemas.order import OrderCreate


def place_order(db: Session, waiter_id: int, data: OrderCreate):
    items_dicts = []
    for item in data.items:
        menu_item = menu_item_repo.get_by_id(db, item.menu_item_id)
        if not menu_item or not menu_item.is_available:
            return None

        items_dicts.append(
            {
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "unit_price": menu_item.price,
                "notes": item.notes,
            }
        )

    order = order_repo.create(db, waiter_id, data.table_number, data.notes, items_dicts)

    accepted = kitchen_grpc_client.submit_order(order.id, order.table_number)
    if not accepted:
        return None

    notification_service.send(
        db,
        user_id=waiter_id,
        title="Orden Recibida",
        message=f"La orden para la mesa {order.table_number} ha sido enviada a cocina.",
        ntype="order_received",
        related_order_id=order.id,
    )

    return order


def get_my_orders(db: Session, waiter_id: int):
    return order_repo.get_by_waiter(db, waiter_id)


def get_all_orders(db: Session):
    return order_repo.get_all(db)


def update_order_status(
    db: Session, order_id: int, requesting_user_id: int, new_status: str
):
    order = order_repo.get_by_id(db, order_id)
    if not order:
        return None

    success = kitchen_grpc_client.update_order_status(order_id, new_status)
    if not success:
        return None

    updated_order = order_repo.update_status(db, order, new_status)

    if new_status == "ready":
        notification_service.send(
            db,
            user_id=order.waiter_id,
            title="¡Orden Lista!",
            message=f"La orden de la mesa {order.table_number} está lista para entregar.",
            ntype="order_ready",
            related_order_id=order.id,
        )

    return updated_order
