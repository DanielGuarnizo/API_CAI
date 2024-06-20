from fastapi import APIRouter

from app.api.routes import (
    history_exercise,
    history_workout,
    items,
    login,
    template_exercise,
    template_workout,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(template_workout.router, tags=["template workout"])
api_router.include_router(template_exercise.router, tags=["template exercise"])
api_router.include_router(history_exercise.router, tags=["history exercise"])
api_router.include_router(history_workout.router, tags=["history workout"])
