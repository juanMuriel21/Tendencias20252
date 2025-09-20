from rest_framework.routers import DefaultRouter

from auth import views

router = DefaultRouter()
router.register(r'auth', views.AuthView, basename='auth')

urlpatterns = router.urls