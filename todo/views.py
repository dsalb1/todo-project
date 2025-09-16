from django.http import HttpResponse
from django.shortcuts import redirect, render
from todo.models import ToDo
import logging

# Get a logger instance
logger = logging.getLogger(__name__)

# def index(request):
#     return HttpResponse("Hello world, this is your todo index.")

def todo_list(request):
    user = request.user
    todos = ToDo.objects.filter(author=user).order_by('created_date')
    return render(request, 'todo/todo_list.html', {'todos': todos})


def create_todo(request, *args, **kwargs):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        text = request.POST.get('text', '')
        author = request.user
        new_todo = ToDo(title=title, text=text, author=author)
        new_todo.save()
        return redirect('todo:todo-list')
    else:
        return render(request, 'todo/create_todo.html')
