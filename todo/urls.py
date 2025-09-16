from django.urls import path

from . import views

urlpatterns = [
    path("", views.todo_list, name="todo-list"),
    path("create", views.create_todo, name="create-todo"),
]
