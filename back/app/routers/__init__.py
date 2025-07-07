from fastapi import APIRouter
from app.routers.clinic_router import router as clinic_router
from app.routers.call_router import router as call_router
from app.routers.evaluation_router import router as evaluation_router
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.test_router import router as test_router
from app.routers.metrics_router import router as metrics_router

# Main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(clinic_router)
api_router.include_router(call_router)
api_router.include_router(evaluation_router)
api_router.include_router(user_router)
api_router.include_router(test_router)
api_router.include_router(metrics_router)

# You can add more routers here as you create them:
# from app.routers.call_router import router as call_router
# from app.routers.evaluation_router import router as evaluation_router
# api_router.include_router(call_router)
# api_router.include_router(evaluation_router) 