from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

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


class ProjectsListView(ListView):
    model = Project
    template_name = "task_manager/projects_list.html"


class ProjectsCreateView(CreateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/projects_form.html"
    success_url = reverse_lazy("task_manager:projects_list")


class ProjectsDetailView(DetailView):
    model = Project


class ProjectsUpdateView(UpdateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/projects_form.html"
    success_url = reverse_lazy("task_manager:projects_list")


class ProjectsDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:projects_list")
