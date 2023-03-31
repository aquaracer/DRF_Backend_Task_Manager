# Generated by Django 3.2.4 on 2023-03-19 19:58

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.EmailField(max_length=255, unique=True, verbose_name='Логин')),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Название')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Описание')),
                ('status', models.CharField(blank=True, choices=[('in_progress', 'В процессе'), ('completed', 'Выполнена'), ('deleted', 'Удалена')], default='low', max_length=30, verbose_name='Статус')),
                ('priority', models.CharField(blank=True, choices=[('low', 'Низкий'), ('medium', 'Средний'), ('high', 'Высокий')], default='low', max_length=30, verbose_name='Приоритет')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='Категория')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='TaskTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Название')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Популярная задача')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Шаблоны задач',
                'verbose_name_plural': 'Шаблон задачи',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('in_progress', 'В процессе'), ('completed', 'Выполнена'), ('deleted', 'Удалена')], default='in_progress', max_length=30, verbose_name='Статус')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Изменение задачи',
                'verbose_name_plural': 'Изменения задачи',
            },
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Название')),
                ('status', models.CharField(blank=True, choices=[('in_progress', 'В процессе'), ('completed', 'Выполнена'), ('deleted', 'Удалена')], default='in_progress', max_length=30, verbose_name='Статус')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Подзадача',
                'verbose_name_plural': 'Подзадачи',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('sex', models.CharField(blank=True, choices=[('Муж', 'Мужской'), ('Жен', 'Женский')], default='Муж', max_length=30, verbose_name='Пол')),
                ('company', models.CharField(blank=True, max_length=300, null=True, verbose_name='Компания')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Сайт')),
                ('social_account', models.URLField(blank=True, null=True, verbose_name='Ссылка на аккаунт в соц. сетях')),
                ('occupation', models.URLField(blank=True, null=True, verbose_name='Профессия')),
                ('user', models.OneToOneField(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='Название')),
                ('status', models.CharField(blank=True, choices=[('planned', 'Запланировано'), ('completed', 'Выполнено')], default='planned', max_length=30, verbose_name='Статус')),
                ('launch_time', models.DateTimeField(blank=True, null=True, verbose_name='Время запуска')),
                ('task', models.OneToOneField(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
    ]
