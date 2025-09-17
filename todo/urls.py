from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'todos',views.ToDoViewSet)

urlpatterns = [
    path("", views.todo_list, name="todo-list"),
    path("create/", views.create_todo, name="create-todo"),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
