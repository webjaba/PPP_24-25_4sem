from fastapi import APIRouter

from app.schemas.schemas import Site


router = APIRouter(prefix="/parse")


@router.post("/parse_website")
def parse_site(site: Site) -> dict:
    return {
        "task_id": 0,
    }


@router.get("/parse_status")
def status(task_id: str) -> dict:
    return {
        "status": "",
        "progress": 0,
        "result": "",
    }
