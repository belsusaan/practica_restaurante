from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, func
from app.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(8, 2), nullable=False)
    category = Column(String(80), nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
