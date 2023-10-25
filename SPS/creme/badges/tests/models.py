from django.db import models


class PlayerStat(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="stats", on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    class Meta:
        app_label = "playerstat"
