from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Enum,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(
        Enum(
            "order_received",
            "order_ready",
            "order_cancelled",
            "general",
            name="notification_type_enum",
        ),
        nullable=False,
        default="general",
    )
    is_read = Column(Boolean, nullable=False, default=False)

    related_order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True
    )

    created_at = Column(DateTime, default=func.now(), nullable=False)
