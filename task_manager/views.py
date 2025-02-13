from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView

from task_manager.forms import WorkerCreationForm
from task_manager.models import Worker, Task, Project, Team


@login_required
def index(request):
    num_worker = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_projects = Project.objects.count()
    num_teams = Team.objects.count()

    context = {
        "num_worker": num_worker,
        "num_tasks": num_tasks,
        "num_projects": num_projects,
        "num_teams": num_teams,
        "projects": Project.objects.all(),
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
