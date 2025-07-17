from django.test import TestCase
from task_manager.models import Position


class PositionModelTest(TestCase):
    def test_str_representation(self):
        position = Position.objects.create(name="DevOps")
        self.assertEqual(str(position), "DevOps")
