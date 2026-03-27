from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    Enum,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    table_number = Column(Integer, nullable=False)

    waiter_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    status = Column(
        Enum(
            "received",
            "preparing",
            "ready",
            "delivered",
            "cancelled",
            name="order_status_enum",
        ),
        nullable=False,
        default="received",
    )
    notes = Column(Text, nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0.00)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )

    menu_item_id = Column(
        Integer, ForeignKey("menu_items.id", ondelete="RESTRICT"), nullable=False
    )

    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(8, 2), nullable=False)
    notes = Column(String(255), nullable=True)

    order = relationship("Order", back_populates="items")
