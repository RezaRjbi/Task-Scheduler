from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path("", views.ListCreateUserView.as_view(), name="users"),
    path("<int:pk>/", views.RetrieveUpdateDestroyUserView.as_view(), name="user"),
    path('login/', views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout")
]

urlpatterns = format_suffix_patterns(urlpatterns)
