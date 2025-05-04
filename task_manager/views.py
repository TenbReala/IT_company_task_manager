from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)

from task_manager.forms import (
    WorkerCreationForm,
    WorkerUpdateForm,
    WorkerSearchForm,
    ProjectSearchForm,
    TaskSearchForm,
    TeamSearchForm, TaskForm,
)
from task_manager.models import Worker, Task, Project, Team, Position, TaskType


@login_required
def index(request):
    user = request.user

    my_tasks = Task.objects.filter(assignees=user)
    upcoming_tasks = my_tasks.filter(
        deadline__gte=timezone.now(), deadline__lte=timezone.now() + timedelta(days=7)
    )

    my_team = Team.objects.filter(members=request.user).first()
    my_team_members = (
        my_team.members.annotate(task_count=Count("assignees")) if my_team else []
    )

    projects = (
        my_team.projects.all().prefetch_related("teams", "teams__members")
        if my_team
        else Project.objects.none()
    )

    context = {
        "my_tasks": my_tasks[:5],
        "upcoming_tasks": upcoming_tasks[:5],
        "my_team": my_team_members,
        "projects": projects,
    }

    return render(request, "task_manager/index.html", context=context)


class WorkerCreateView(CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/registration.html"

    def get_success_url(self):
        return reverse("task_manager:index")


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("position")
    paginate_by = 20

    def get_queryset(self):
        queryset = Worker.objects.all().select_related("position")
        query = self.request.GET.get("query")

        if query:
            queryset = queryset.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET)
        return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    queryset = (
        Worker.objects.all()
        .prefetch_related("assignees__task_type")
        .select_related("position")
    )


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy("")


class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    queryset = Project.objects.all().prefetch_related("teams")
    paginate_by = 20

    def get_queryset(self):
        queryset = Project.objects.all().prefetch_related("teams")
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = ProjectSearchForm(self.request.GET)
        return context


class ProjectsCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/project_form.html"

    def get_success_url(self):
        return reverse("task_manager:project-detail", kwargs={"pk": self.object.pk})


class ProjectsDetailView(LoginRequiredMixin, DetailView):
    model = Project
    queryset = Project.objects.prefetch_related("tasks").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress"] = self.object.progress()
        return context


class ProjectsUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = "__all__"
    template_name = "task_manager/project_form.html"
    success_url = reverse_lazy("task_manager:projects-list")


class ProjectsDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:projects-list")


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    queryset = Position.objects.all().prefetch_related("worker_set")
    paginate_by = 20


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDetailView(LoginRequiredMixin, DetailView):
    model = Position


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    fields = "__all__"


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    paginate_by = 20
    template_name = "task_manager/task_type_list.html"


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDetailView(LoginRequiredMixin, DetailView):
    model = TaskType
    queryset = TaskType.objects.prefetch_related("task_set")
    template_name = "task_manager/task_type_detail.html"


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")
    template_name = "task_manager/task_type_confirm_delete.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    queryset = Task.objects.all().prefetch_related("assignees")
    paginate_by = 20

    def get_queryset(self):
        queryset = Task.objects.all().prefetch_related("assignees")
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(self.request.GET)
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        if self.kwargs.get("project_pk"):
            return reverse("task_manager:project-detail", args=[self.kwargs["project_pk"]])
        return reverse("task_manager:task-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project_locked"] = bool(self.kwargs.get("project_pk"))
        return kwargs

    def form_valid(self, form):
        if not form.instance.project and self.kwargs.get("project_pk"):
            form.instance.project = get_object_or_404(
                Project, pk=self.kwargs["project_pk"]
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get("project_pk"):
            context["project_locked"] = True
            context["project_pk"] = self.kwargs["project_pk"]
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    queryset = Task.objects.all()


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task


class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user in task.assignees.all():
            task.is_complete = True
            task.save()
        return redirect("task_manager:index")


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    queryset = Team.objects.all().prefetch_related("projects__teams")
    paginate_by = 20

    def get_queryset(self):
        queryset = Team.objects.all().prefetch_related("projects__teams")
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TeamSearchForm(self.request.GET)
        return context


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team-list")


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    queryset = Team.objects.all().prefetch_related("projects__teams")


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    fields = "__all__"


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")
