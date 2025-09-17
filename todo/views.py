import logging

from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import QueryDict
from django.urls import reverse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from todo.forms.todo_form import ToDoForm
from todo.models import ToDo
from todo.serializers import UserSerializer, ToDoSerializer

# Get a logger instance
logger = logging.getLogger(__name__)


def todo_listview(request):
    user = request.user
    todos = ToDo.objects.filter(author=user).order_by('-created_date')
    
    paginator = Paginator(todos, 10) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'todo/todo_list.html', {'todos': page_obj, 'range': range(1, page_obj.paginator.num_pages + 1)})

#TODO add error handling to view
def create_todo(request, *args, **kwargs):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            new_todo = ToDo(
                title=form.cleaned_data["title"], 
                text=form.cleaned_data["text"], 
                author=request.user
            )
            new_todo.save()
            return redirect('todo:todo-listview')
    else:
        form = ToDoForm()
    return render(request, 'todo/create_todo.html', {'form': form})


def edit_todo(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'PUT':
        form = ToDoForm(QueryDict(request.body))
        if form.is_valid():
            todo.title = form.cleaned_data["title"]
            todo.text = form.cleaned_data["text"]
            todo.save()
        return render(request, 'todo/partials/todo.html', {'todo': todo})
    else:
        form = ToDoForm({'title': todo.title, 'text': todo.text})
    return render(request, 'todo/edit_todo.html', {'form': form, 'pk': todo.id})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ToDoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ToDos to be viewed or edited
    """
    queryset = ToDo.objects.all().order_by('created_date')
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]
