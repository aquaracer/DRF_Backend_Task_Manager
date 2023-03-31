from django.db import models

from common.models import AbstarctBaseModel

class Notification(AbstarctBaseModel):
    """Уведомление"""

    PLANNED = 'planned'
    COMPLETED = 'completed'
    ERROR = 'error'

    STATUS = (
        (PLANNED, 'Запланировано'),
        (COMPLETED, 'Выполнено'),
        (ERROR, 'Ошибка')

    )

    # Отношения
    task = models.OneToOneField('core.Task', verbose_name='Задача', on_delete=models.CASCADE, default='', null=True,
                                blank=True)

    # Поля
    name = models.CharField(verbose_name='Название', max_length=300, blank=True, null=True)
    status = models.CharField(verbose_name='Статус', choices=STATUS, max_length=30, default=PLANNED,
                              blank=True)
    launch_time = models.DateTimeField(verbose_name='Время запуска', blank=True, null=True)
    error_text = models.CharField(verbose_name='Текст ошибки', max_length=3000, blank=True, null=True)
    task_result_id = models.UUIDField(verbose_name='ID результата выполнения задачи', unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.id} {self.created}'