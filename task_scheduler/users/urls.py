from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path("", views.ListCreateUserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)
