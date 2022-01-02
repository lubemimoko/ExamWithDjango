from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", LoginView.as_view(template_name = "exam/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("course/topic/<id>/", views.topic, name="topic"),
    path("exam/<urltopic>", views.exam, name="exam"),
    path("history/", views.history, name="history"),
    path("submit/", views.submit, name="submit"),
    path("start_exam/", views.start_exam, name="start_exam")
    
]