from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/authcode/ui")
def ui(state: str, ):
    return {}