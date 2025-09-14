from rest_framework.routers import DefaultRouter

from clients.views import ClientView

router = DefaultRouter()

router.register(r'clients', ClientView, basename='clients')

urlpatterns = router.urls