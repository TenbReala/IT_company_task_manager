from django.urls import path

from task_manager.views import (
    index,
    WorkerCreateView,
    ProjectsCreateView,
    ProjectsListView,
    ProjectsUpdateView,
    ProjectsDeleteView,
    ProjectsDetailView, PositionListView, PositionCreateView, PositionDetailView, PositionUpdateView,
    PositionDeleteView, WorkerListView, WorkerUpdateView, WorkerDetailView, WorkerDeleteView, TaskTypeListView,
    TaskTypeCreateView, TaskTypeDetailView, TaskTypeUpdateView, TaskTypeDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/detail/", WorkerDetailView.as_view(), name="worker-detail"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),


    path("projects/", ProjectsListView.as_view(), name="projects-list"),
    path("projects/create/", ProjectsCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/detail/", ProjectsDetailView.as_view(), name="project-detail"),
    path("projects/<int:pk>/update/", ProjectsUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", ProjectsDeleteView.as_view(), name="project-delete"),

    path("position/", PositionListView.as_view(), name="position-list"),
    path("position/create/", PositionCreateView.as_view(), name="position-create"),
    path("position/<int:pk>/detail/", PositionDetailView.as_view(), name="position-detail"),
    path("position/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("position/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),

    path("task-type/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-type/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-type/", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("task-type/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-type/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    ]

app_name = "task_manager"
