from fastapi import Depends, HTTPException

from ..models.categories import Category

from ..config.database import SessionLocal

from .has_access import has_access


def is_category_owner(data = Depends(has_access)):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == data['req'].path_params['id']).first()
    if not category:
        raise HTTPException(status_code=403, detail="Forbidden")
    if category.user_id != data['payload']['id']:
        raise HTTPException(status_code=403, detail="Forbidden")