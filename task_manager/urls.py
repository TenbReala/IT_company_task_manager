from django.urls import path

from task_manager.views import index, WorkerCreateView

urlpatterns = [
    path("", index, name="index"),
    path("worker/create", WorkerCreateView.as_view(), name="worker_create"),
    ]

app_name = "task_manager"
