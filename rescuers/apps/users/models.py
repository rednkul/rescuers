from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from .managers import CustomUserManager


# Authentification
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('логин', max_length=50, unique=True)

    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Администратор', default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = (
                        ('can_everything', 'Все возможные действия'),
                        ('can_add_workers_and_vacancies_read_reports', 'Можно добавлять/редактировать сотрудников и вакансии, скачивать отчеты'),
                        ('can_read_reports', 'Можно скачивать отчеты'),
                        ('only_viewing', 'Можно только просматривать')
                        )








