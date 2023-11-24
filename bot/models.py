from django.db import models


# Create your models here.
class TgUser(models.Model):
    tg_id = models.BigIntegerField(primary_key=True, unique=True,
                                   verbose_name='ID в Телеграм')
    user_name = models.CharField(max_length=150, null=True,
                                 blank=True, verbose_name='Username')


class Subscription(models.Model):
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"
