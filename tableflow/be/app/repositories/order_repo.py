from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem


def get_all(db: Session):
    return db.query(Order).all()


def get_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_by_waiter(db: Session, waiter_id: int):
    return db.query(Order).filter(Order.waiter_id == waiter_id).all()


def create(
    db: Session, waiter_id: int, table_number: int, notes: str, items: list[dict]
):
    total_amount = sum(i["unit_price"] * i["quantity"] for i in items)

    db_order = Order(
        waiter_id=waiter_id,
        table_number=table_number,
        notes=notes,
        total_amount=total_amount,
        status="received",
    )

    db.add(db_order)
    db.flush()

    for item in items:
        db_item = OrderItem(
            order_id=db_order.id,
            menu_item_id=item["menu_item_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            notes=item.get("notes"),
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


def update_status(db: Session, order: Order, new_status: str):
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
