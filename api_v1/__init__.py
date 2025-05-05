from fastapi import APIRouter
from api_v1.products.views import router as products_router
from api_v1.demo_auth.views import router as basic_auth_router
from api_v1.demo_auth.demo_jwt_auth import router as jwt_router

router = APIRouter()
router.include_router(basic_auth_router, prefix="/demo-auth")
router.include_router(products_router, prefix="/products")
router.include_router(jwt_router)

