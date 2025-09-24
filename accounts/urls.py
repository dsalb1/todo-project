from django.urls import include, path

from accounts import views

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("logout", views.logout_view, name="logout")
]