from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Worker, Position, TaskType, Team, Project, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display


admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Position)
admin.site.register(TaskType)
