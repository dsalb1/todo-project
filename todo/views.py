from django.http import HttpResponse
from django.shortcuts import render


# def index(request):
#     return HttpResponse("Hello world, this is your todo index.")

def todo_list(request):
    return render(request, 'todo/todo_list.html', {})
