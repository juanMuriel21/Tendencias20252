from rest_framework import routers

from transactions import views

router = routers.DefaultRouter()
router.register(r'transactions', views.TransactionViewSet, basename='transactions')

urlpatterns = router.urls