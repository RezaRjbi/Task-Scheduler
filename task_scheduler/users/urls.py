from django.urls import path
from .views import UserApiView
urlpatterns = [
    path("", UserApiView.as_view())
]
