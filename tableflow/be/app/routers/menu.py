from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import menu_service
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemOut
from .deps import get_current_user

router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/", response_model=list[MenuItemOut])
def get_public_menu(db: Session = Depends(get_db)):
    return menu_service.get_menu(db)


@router.get("/all", response_model=list[MenuItemOut])
def get_full_menu(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return menu_service.get_full_menu(db)


@router.post("/", response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
def add_menu_item(
    item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return menu_service.add_item(db, item_data)


@router.patch("/{item_id}", response_model=MenuItemOut)
def update_menu_item(
    item_id: int,
    item_data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = menu_service.update_item(db, item_id, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}/toggle", response_model=MenuItemOut)
def toggle_item_availability(
    item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    item = menu_service.toggle_availability(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
