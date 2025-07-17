from django.test import TestCase
from task_manager.models import Team


class TeamModelTest(TestCase):
    def test_str_representation(self):
        team = Team.objects.create(name="Bravo Squad")
        self.assertEqual(str(team), "Bravo Squad")
