from fastapi import APIRouter


router = APIRouter(prefix="/parse")


@router.post("/parse_website")
def parse_site():
    pass


@router.get("/parse_status")
def status():
    pass
