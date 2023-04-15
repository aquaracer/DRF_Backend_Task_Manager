from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from common.models import AbstarctBaseModel


class User(AbstractUser):
    """Пользователь"""

    username = models.EmailField(verbose_name='Логин', max_length=255, unique=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.id} | {self.username}'


class Profile(AbstarctBaseModel):
    """Профиль пользователя"""

    M = 'Муж'
    W = 'Жен'

    SEX = (
        (M, 'Мужской'),
        (W, 'Женский')
    )

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        default='',
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    sex = models.CharField(verbose_name='Пол', choices=SEX, max_length=30, default=M, blank=True)
    company = models.CharField(verbose_name='Компания', max_length=300, blank=True, null=True)
    website = models.URLField(verbose_name='Сайт', blank=True, null=True)
    social_account = models.URLField(verbose_name='Ссылка на аккаунт в соц. сетях', blank=True, null=True)
    occupation = models.URLField(verbose_name='Профессия', blank=True, null=True)
    fca_token = models.CharField(
        verbose_name='Токен для отправки уведомления через Firebase',
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        if self.user:
            return f'{self.id} | {self.user.first_name} | {self.user.last_name} |' f' {self.user.username}'


class Category(AbstarctBaseModel):
    """Категория"""

    name = models.CharField(verbose_name='Название', max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.id} {self.name}'


class Task(AbstarctBaseModel):
    """Задача"""

    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    DELETED = 'deleted'

    STATUS = (
        (IN_PROGRESS, 'В процессе'),
        (COMPLETED, 'Выполнена'),
        (DELETED, 'Удалена'),
    )

    LOW = 'low'
    MEDIUN = 'medium'
    HIGH = 'high'

    PRIORITY = (
        (LOW, 'Низкий'),
        (MEDIUN, 'Средний'),
        (HIGH, 'Высокий'),
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True)

    name = models.CharField(verbose_name='Название', max_length=300, blank=True, null=True)
    description = models.CharField(verbose_name='Описание', max_length=300, blank=True, null=True)
    status = models.CharField(verbose_name='Статус', choices=STATUS, max_length=30, default=LOW, blank=True)
    priority = models.CharField(verbose_name='Приоритет', choices=PRIORITY, max_length=30, default=LOW, blank=True)
    execution_date = models.DateField(verbose_name='Дата исполнения', default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.id} {self.name} {self.status} {self.user.username}'


class Subtask(AbstarctBaseModel):
    """Подзадача"""

    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE, null=True)

    name = models.CharField(verbose_name='Название', max_length=300, blank=True, null=True)
    status = models.CharField(
        verbose_name='Статус',
        choices=Task.STATUS,
        max_length=30,
        default=Task.IN_PROGRESS,
        blank=True,
    )

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'

    def __str__(self):
        return f'{self.id} {self.name} {self.status} | основная задача: {self.task.name}'


class TaskLog(AbstarctBaseModel):
    """История изменений задачи"""

    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE, null=True)

    status = models.CharField(
        verbose_name='Статус',
        choices=Task.STATUS,
        max_length=30,
        default=Task.IN_PROGRESS,
        blank=True,
    )

    class Meta:
        verbose_name = 'Изменение задачи'
        verbose_name_plural = 'Изменения задачи'

    def __str__(self):
        return f'{self.id} {self.created} {self.task.name} {self.status}'


class TaskTemplate(AbstarctBaseModel):
    """Шаблон задачи"""

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True)

    name = models.CharField(verbose_name='Название', max_length=300, blank=True, null=True)
    is_popular = models.BooleanField(verbose_name='Популярная задача', default=False)

    class Meta:
        verbose_name = 'Шаблоны задач'
        verbose_name_plural = 'Шаблон задачи'

    def __str__(self):
        return f'{self.id} {self.name} {self.category}'
