from django.db import models
from django.core.validators import RegexValidator


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(
        max_length=2,
        validators=[RegexValidator(
            r'^[0-9A-Z]{2}$',
            message='The sequence must contain uppercase characters'
        )],
        blank=False,
        null=False
    )
    version = models.CharField(
        max_length=2,
        validators=[RegexValidator(
            r'^[0-9A-Z]{2}$',
            message='The sequence must contain uppercase characters'
        )],
        blank=False,
        null=False
    )
    created = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.serial
