from django.contrib import admin

from api.models import Tasks, TaskChanges


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskChanges)
class TaskChangesAdmin(admin.ModelAdmin):
    pass
