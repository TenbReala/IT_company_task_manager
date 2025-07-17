from django.test import TestCase
from django.contrib import admin
from task_manager.admin import WorkerAdmin
from task_manager.models import Worker, Position, TaskType, Project, Task, Team


class AdminRegistrationTest(TestCase):

    def test_worker_model_registered(self):
        self.assertIn(Worker, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Worker], WorkerAdmin)

    def test_other_models_registered(self):
        for model in [Team, Project, Task, Position, TaskType]:
            self.assertIn(model, admin.site._registry)
