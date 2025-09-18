import logging

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import QueryDict
from rest_framework import permissions, viewsets
from todo.forms.todo_form import ToDoForm
from todo.models import ToDo
from todo.serializers import UserSerializer, ToDoSerializer

# Get a logger instance
logger = logging.getLogger(__name__)


@login_required
def todo_listview(request):
    user = request.user
    is_completed_todos = request.GET.get('is_completed') 
    todos = ToDo.objects.filter(author=user)

    if is_completed_todos:
        todos = todos.filter(is_completed=True)
    else:
        todos = todos.filter(is_completed=False)
    
    todos = todos.order_by('-created_at')
    
    paginator = Paginator(todos, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = f'Your {"Completed " if is_completed_todos else ""}ToDos'

    return render(request, 'todo/todo_list.html', {
        'todos': page_obj, 
        'title': title, 
        'range': range(1, page_obj.paginator.num_pages + 1)
    })


@login_required
def create_todo(request, *args, **kwargs):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            new_todo = ToDo(
                title=form.cleaned_data["title"], 
                text=form.cleaned_data["text"], 
                is_completed=form.cleaned_data["is_completed"],
                author=request.user
            )
            new_todo.save()
            return redirect('todo:list-todo')
    else:
        form = ToDoForm()
    return render(request, 'todo/create_todo.html', {'form': form})


@login_required
def todo(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    return render(request, 'todo/partials/todo.html', {'todo': todo})

@login_required
def edit_todo(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.method == 'PUT':
        form = ToDoForm(QueryDict(request.body))
        if form.is_valid():
            todo.title = form.cleaned_data["title"]
            todo.text = form.cleaned_data["text"]
            todo.is_completed = form.cleaned_data["is_completed"]
            todo.save()
        return render(request, 'todo/partials/todo.html', {'todo': todo})
    else:
        form = ToDoForm({'title': todo.title, 'text': todo.text, 'is_completed': todo.is_completed})
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
    queryset = ToDo.objects.all().order_by('created_at')
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]
