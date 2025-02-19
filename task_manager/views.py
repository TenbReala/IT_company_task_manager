from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from task_manager.forms import WorkerCreationForm
from task_manager.models import Worker, Task, Project, Team, Position


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


class WorkerListView(ListView):
    model = Worker


class WorkerUpdateView(UpdateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerDetailView(DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("assignees__task_type").select_related("position")


class WorkerDeleteView(DeleteView):
    model = Worker
    success_url = reverse_lazy("")


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
    queryset = Project.objects.all().prefetch_related("tasks")


class ProjectsUpdateView(UpdateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/projects_form.html"
    success_url = reverse_lazy("task_manager:projects_list")


class ProjectsDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:projects_list")


class PositionListView(ListView):
    model = Position


class PositionCreateView(CreateView):
    model = Position
    fields = "__all__"


class PositionDetailView(DetailView):
    model = Position


class PositionUpdateView(UpdateView):
    model = Position
    fields = "__all__"


class PositionDeleteView(DeleteView):
    model = Position
