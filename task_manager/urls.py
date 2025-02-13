from django.urls import path

from task_manager.views import index, WorkerCreateView, ProjectsCreateView, ProjectsListView, ProjectsUpdateView, \
    ProjectsDeleteView, ProjectsDetailView

urlpatterns = [
    path("", index, name="index"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker_create"),
    path("projects/", ProjectsListView.as_view(), name="projects_list"),
    path("projects/create/", ProjectsCreateView.as_view(), name="project_create"),
    path("projects/<int:pk>/detail/", ProjectsDetailView.as_view(), name="project_detail"),
    path("projects/<int:pk>/update/", ProjectsUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", ProjectsDeleteView.as_view(), name="project_delete"),
    ]

app_name = "task_manager"
