from fastapi import APIRouter


router = APIRouter()


@router.get("/program/{name}/")
def get_program_by_name(name: str):
    pass
