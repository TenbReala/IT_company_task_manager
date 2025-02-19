from django.urls import path

from task_manager.views import (
    index,
    WorkerCreateView,
    ProjectsCreateView,
    ProjectsListView,
    ProjectsUpdateView,
    ProjectsDeleteView,
    ProjectsDetailView, PositionListView, PositionCreateView, PositionDetailView, PositionUpdateView,
    PositionDeleteView, WorkerListView, WorkerUpdateView, WorkerDetailView, WorkerDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker_create"),
    path("worker/", WorkerListView.as_view(), name="worker_list"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker_update"),
    path("worker/<int:pk>/detail/", WorkerDetailView.as_view(), name="worker_detail"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker_delete"),


    path("projects/", ProjectsListView.as_view(), name="projects_list"),
    path("projects/create/", ProjectsCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/detail/", ProjectsDetailView.as_view(), name="project_detail"),
    path("projects/<int:pk>/update/", ProjectsUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", ProjectsDeleteView.as_view(), name="project_delete"),

    path("position/", PositionListView.as_view(), name="position_list"),
    path("position/create/", PositionCreateView.as_view(), name="position_create"),
    path("position/<int:pk>/detail/", PositionDetailView.as_view(), name="position_detail"),
    path("position/<int:pk>/update/", PositionUpdateView.as_view(), name="position_update"),
    path("position/<int:pk>/delete/", PositionDeleteView.as_view(), name="position_delete"),
    ]

app_name = "task_manager"
