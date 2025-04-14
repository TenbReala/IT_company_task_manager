from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from task_manager.forms import WorkerCreationForm, WorkerUpdateForm
from task_manager.models import Worker, Task, Project, Team, Position, TaskType


@login_required
def index(request):
    user = request.user

    my_tasks = Task.objects.filter(assignees=user)
    upcoming_tasks = my_tasks.filter(
        deadline__gte=timezone.now(),
        deadline__lte=timezone.now() + timedelta(days=7)
    )

    my_team = Team.objects.filter(members=request.user).first()
    my_team_members = (
        my_team.members.annotate(task_count=Count("assignees")) if my_team else []
    )

    projects = (
        my_team.projects.all().prefetch_related("teams", "teams__members")
        if my_team else Project.objects.none()
    )

    context = {
        "my_tasks": my_tasks[:5],
        "upcoming_tasks": upcoming_tasks[:5],
        "my_team": my_team_members,
        "projects": projects
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerListView(ListView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("position")
    paginate_by = 20


class WorkerUpdateView(UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDetailView(DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("assignees__task_type").select_related("position")


class WorkerDeleteView(DeleteView):
    model = Worker
    success_url = reverse_lazy("")


class ProjectsListView(ListView):
    model = Project
    queryset = Project.objects.all().prefetch_related("teams")
    paginate_by = 20


class ProjectsCreateView(CreateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:projects-list")


class ProjectsDetailView(DetailView):
    model = Project
    queryset = Project.objects.prefetch_related("tasks").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress"] = self.object.progress()
        return context


class ProjectsUpdateView(UpdateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:projects-list")


class ProjectsDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:projects-list")


class PositionListView(ListView):
    model = Position
    queryset = Position.objects.all().prefetch_related("worker_set")
    paginate_by = 20


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
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(ListView):
    model = TaskType
    paginate_by = 20


class TaskTypeCreateView(CreateView):
    model = TaskType
    fields = "__all__"


class TaskTypeDetailView(DetailView):
    model = TaskType
    queryset = TaskType.objects.all()


class TaskTypeUpdateView(UpdateView):
    model = TaskType
    fields = "__all__"


class TaskTypeDeleteView(DeleteView):
    model = TaskType


class TaskListView(ListView):
    model = Task
    queryset = Task.objects.all().prefetch_related("assignees")
    paginate_by = 20


class TaskCreateView(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")

    def form_valid(self, form):
        if not form.instance.project and self.kwargs.get("project_pk"):
            form.instance.project = get_object_or_404(Project, pk=self.kwargs["project_pk"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get("project_pk"):
            context["project_locked"] = True
        return context


class TaskDetailView(DetailView):
    model = Task
    queryset = Task.objects.all()


class TaskUpdateView(UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(DeleteView):
    model = Task


class TaskCompleteView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user in task.assignees.all():
            task.is_complete = True
            task.save()
        return redirect("task_manager:index")


class TeamListView(ListView):
    model = Team
    queryset = Team.objects.all().prefetch_related("projects__teams")
    paginate_by = 20


class TeamCreateView(CreateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team-list")


class TeamDetailView(DetailView):
    model = Team
    queryset = Team.objects.all().prefetch_related("projects__teams")


class TeamUpdateView(UpdateView):
    model = Team
    fields = "__all__"


class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")
