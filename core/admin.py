from django.contrib import admin

from .models import User, Profile, Category, Task, Subtask, TaskLog, TaskTemplate


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    pass
