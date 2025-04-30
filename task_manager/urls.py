from django.contrib.auth import views
from django.urls import path

from task_manager.views import (
    index,
    WorkerCreateView,
    ProjectsCreateView,
    ProjectsListView,
    ProjectsUpdateView,
    ProjectsDeleteView,
    ProjectsDetailView,
    PositionListView,
    PositionCreateView,
    PositionDetailView,
    PositionUpdateView,
    PositionDeleteView,
    WorkerListView,
    WorkerUpdateView,
    WorkerDetailView,
    WorkerDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeDetailView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TeamListView,
    TeamCreateView,
    TeamDetailView,
    TeamUpdateView,
    TeamDeleteView,
    TaskCompleteView,
)

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", WorkerCreateView.as_view(), name="register"),
    path("", index, name="index"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/detail/", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("projects/", ProjectsListView.as_view(), name="projects-list"),
    path("projects/create/", ProjectsCreateView.as_view(), name="project-create"),
    path(
        "projects/<int:pk>/detail/", ProjectsDetailView.as_view(), name="project-detail"
    ),
    path(
        "projects/<int:pk>/update/", ProjectsUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/", ProjectsDeleteView.as_view(), name="project-delete"
    ),
    path(
        "projects/<int:project_pk>/tasks/create/",
        TaskCreateView.as_view(),
        name="project-task-create",
    ),
    path("position/", PositionListView.as_view(), name="position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path(
        "position/<int:pk>/detail/",
        PositionDetailView.as_view(),
        name="position-detail",
    ),
    path(
        "position/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "position/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path("task-type/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-type/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path(
        "task-type/<int:pk>/detail/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail",
    ),
    path(
        "task-type/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task-type/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path("task/", TaskListView.as_view(), name="task-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/detail/", TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/complete/", TaskCompleteView.as_view(), name="task-complete"),
    path("team/", TeamListView.as_view(), name="team-list"),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path("team/<int:pk>/detail/", TeamDetailView.as_view(), name="team-detail"),
    path("team/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("team/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
]

app_name = "task_manager"
