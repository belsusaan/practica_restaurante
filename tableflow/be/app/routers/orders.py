from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import order_service
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from .deps import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def place_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = order_service.place_order(db, current_user.id, order_data)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order data or kitchen rejected",
        )
    return order


@router.get("/mine", response_model=list[OrderOut])
def get_my_orders(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return order_service.get_my_orders(db, current_user.id)


@router.get("/", response_model=list[OrderOut])
def get_all_orders(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return order_service.get_all_orders(db)


@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = order_service.update_order_status(
        db, order_id, current_user.id, status_data.status
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid status transition",
        )
    return order
