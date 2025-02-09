from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "URGENT", "Urgent"
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
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
    assignees = models.ManyToManyField(
        "Worker",
        related_name="assignees",
        blank=True
    )

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.name} {self.deadline} {self.priority} {self.is_complete}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        max_length=500,
        blank=True,
    )
    tasks = models.ManyToManyField(
        "Task",
        related_name="projects",
        blank=True
    )

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

    def __str__(self):
        return f"{self.username}({self.first_name} {self.last_name}) {self.position}"


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        Worker,
        related_name="members",
        blank=True,
    )
    projects = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
