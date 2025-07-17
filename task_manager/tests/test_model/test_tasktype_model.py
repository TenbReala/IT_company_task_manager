from django.test import TestCase
from task_manager.models import TaskType


class TaskTypeModelTest(TestCase):
    def test_str_representation(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), "Bug")
