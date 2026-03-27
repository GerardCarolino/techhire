from django.urls import path
from .views import RegisterView, MeView, UpgradeMembershipView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("upgrade/", UpgradeMembershipView.as_view(), name="upgrade"),
]
