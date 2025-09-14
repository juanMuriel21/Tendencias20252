from rest_framework.routers import DefaultRouter

from products.views import ProductView

router = DefaultRouter()
router.register(r'products', ProductView, "products")

urlpatterns = router.urls