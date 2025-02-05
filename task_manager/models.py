from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "URGENT", "Urgent"
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=6,
        choices=Priority,
        default=Priority.LOW,
    )
    task_type = models.ForeignKey(
        "TaskType",
        on_delete=models.CASCADE,
    )
    assignees = models.ManyToManyField("Worker", related_name="assignees")


class Project(models.Model):
    name = models.CharField(max_length=100)
    tasks = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
    )
    description = models.TextField()


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
    )


class Position(models.Model):
    name = models.CharField(max_length=100)


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ForeignKey(
        "Worker",
        on_delete=models.CASCADE,
    ),
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
    )
