from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.models import Position


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")
        self.user_model = get_user_model()

    def test_str_representation(self):
        user = self.user_model.objects.create_user(
            username="worker123", password="testpass", position=self.position
        )
        self.assertEqual(str(user), "worker123")

    def test_verbose_names(self):
        self.assertEqual(self.user_model._meta.verbose_name, "Worker")
        self.assertEqual(self.user_model._meta.verbose_name_plural, "Workers")

    def test_position_relation(self):
        user = self.user_model.objects.create_user(
            username="reltest", password="123", position=self.position
        )
        self.assertEqual(user.position.name, "Tester")
