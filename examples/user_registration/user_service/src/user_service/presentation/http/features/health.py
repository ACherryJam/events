from fastapi import Response
from fastapi.routing import APIRouter


health_router = APIRouter(prefix="/health")


@health_router.get("/")
async def check():
    return Response(status_code=200)
