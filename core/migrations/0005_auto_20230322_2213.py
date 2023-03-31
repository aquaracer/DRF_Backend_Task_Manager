# Generated by Django 3.2.4 on 2023-03-22 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
       # ('django_celery_results', '0009_auto_20230322_2213'),
        ('core', '0004_alter_notification_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='error_text',
            field=models.CharField(blank=True, max_length=3000, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='notification',
            name='result',
            field=models.OneToOneField(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_results.taskresult', verbose_name='Результат выполнения задачи'),
        ),
        migrations.AddField(
            model_name='profile',
            name='fca_token',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Токен для отправки уведомления через Firebase'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('planned', 'Запланировано'), ('completed', 'Выполнено'), ('error', 'Ошибка')], default='planned', max_length=30, verbose_name='Статус'),
        ),
    ]