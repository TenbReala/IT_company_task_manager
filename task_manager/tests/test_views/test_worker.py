from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, Worker


class TestWorkerCreateView(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")
        self.create_url = reverse("task_manager:worker-create")

    def test_worker_create_get_accessible(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_worker_create_post_success(self):
        data = {
            "username": "new_user",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "position": self.position.id,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="new_user").exists())

    def test_worker_create_invalid_password(self):
        data = {
            "username": "bad_user",
            "password1": "123",
            "password2": "321",
            "position": self.position.id,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)


class TestWorkerListView(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")
        self.user = Worker.objects.create(
            username="worker1",
            position=self.position,
            password="Test123",
            first_name="John",
            last_name="Doe",
        )
        self.unmatched_user = Worker.objects.create(
            username="worker2",
            position=self.position,
            password="Test123",
            first_name="Not",
            last_name="Matching",
        )

        self.query_to_user = {
            "worker1": self.user,
            "John": self.user,
            "Doe": self.user,
        }

        self.client.force_login(self.user)

    def test_get_queryset(self):
        for query, expected_user in self.query_to_user.items():
            url = reverse("task_manager:worker-list")
            response = self.client.get(url, {"query": query})
            self.assertEqual(response.status_code, 200)
            workers = response.context["worker_list"]
            self.assertIn(expected_user, workers)
            self.assertNotIn(self.unmatched_user, workers)

    def test_get_context_data(self):
        response = self.client.get(
            reverse("task_manager:worker-list"), {"query": "test"}
        )
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].data.get("query"), "test")
        self.assertTrue(response.context["search_form"].is_bound)
