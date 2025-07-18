from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

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
    deadline = models.DateTimeField()
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
        blank=True,
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks", null=True, blank=True
    )

    class Meta:
        ordering = ["is_complete"]

    def __str__(self):
        return f"{self.name} {self.deadline} {self.priority} {self.is_complete}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(
        max_length=500,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def progress(self):
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(is_complete=True).count()
        return int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

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
        ordering = ["username"]

    def __str__(self):
        return f"{self.username}"


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        Worker,
        related_name="members",
        blank=True,
    )
    projects = models.ManyToManyField(
        "Project",
        related_name="teams",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
