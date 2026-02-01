from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig

from .views import PaymentViewSet, SubscriptionAPIView, UserViewSet, CustomTokenObtainPairView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("payment", PaymentViewSet)
router.register("", UserViewSet)
urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
]
urlpatterns += router.urls
