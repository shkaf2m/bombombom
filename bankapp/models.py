from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    course = {
        (1, '1 курс (бакалавр)'),
        (2, '2 курс (бакалавр)'),
        (3, '3 курс (бакалавр)'),
        (4, '4 курс (бакалавр)'),
        (5, '1 курс (магистр)'),
        (6, '2 курс (магистр)'),
    }
    course = models.IntegerField('Курс', choices = course, blank = False, null=True)
    money = models.IntegerField('Деньги', default = 0, null=True)
    account_number = models.IntegerField('Номер счёта', default = 0, null=True)

class MoneyOrder(models.Model):
    sender_number = models.IntegerField('Отправитель')
    recipient_number = models.IntegerField('Получатель')
    money_sum = models.IntegerField('Количество денег')