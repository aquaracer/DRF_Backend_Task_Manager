from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from datetime import date


class Tasks(models.Model):
    """Задачи"""

    STATUSES = (
        ('new', 'NEW'),
        ('planned', 'PLANNED'),
        ('in work', 'IN WORK'),
        ('finished', 'FINISHED'),
    )

    name = models.CharField("Название задачи", max_length=256)
    description = models.TextField("Описание задачи")
    created = models.DateTimeField("Дата создания", auto_now=True)
    status = models.CharField("Статус задачи", max_length=8, choices=STATUSES)
    planned_finish = models.DateField("Планируемая дата завершения",
                                      validators=[validators.MinValueValidator(date.today())])
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaskChanges(models.Model):
    """Изменения в задаче"""

    STATUSES = (
        ('new', 'NEW'),
        ('planned', 'PLANNED'),
        ('in work', 'IN WORK'),
        ('finished', 'FINISHED'),
    )

    task_name = models.CharField("Название задачи", max_length=256)
    task_description = models.TextField("Описание заадчи")
    task_status = models.CharField("Статус задачи", max_length=8, choices=STATUSES)
    task_planned_finish = models.DateField("Планируемая дата завершения",
                                           validators=[validators.MinValueValidator(date.today())])
    change_created = models.DateTimeField("Дата и время изменения задачи", auto_now_add=True)
    changed_task = models.ForeignKey(Tasks, verbose_name="Задача", on_delete=models.CASCADE, related_name='task_change')

    def __str__(self):
        return self.task_name
