from fastapi import APIRouter
from fastapi import HTTPException

from backend.app.services.locality_profile_service import (
    fetch_locality_profile,
)

router = APIRouter(
    prefix="/locality",
    tags=["locality-profile"],
)


@router.get("/{locality_name}")
def get_profile(locality_name: str):

    data = fetch_locality_profile(locality_name)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Locality not found",
        )

    return data
