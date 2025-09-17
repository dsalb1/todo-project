import logging

from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from todo.forms.todo_form import ToDoForm
from todo.models import ToDo

# Get a logger instance
logger = logging.getLogger(__name__)


def todo_list(request):
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
            return redirect('todo:todo-list')
    else:
        form = ToDoForm()
    return render(request, 'todo/create_todo.html', {'form': form})
