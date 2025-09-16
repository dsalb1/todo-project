from django.shortcuts import render
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
