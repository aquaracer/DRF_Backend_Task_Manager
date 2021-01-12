from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from datetime import date


class Fields(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название поля')

    def __str__(self):
        return self.name


class Tasks(models.Model):
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


class TaskChanges(models.Model):
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
    changed_fields = models.ManyToManyField(Fields, verbose_name='Измененные поля')
    changed_task = models.ForeignKey(Tasks, verbose_name="Задача", on_delete=models.CASCADE, related_name='task_change')
