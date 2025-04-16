# Create your models here.

from django.db import models


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    language = models.CharField(max_length=255, blank=True, null=True)
    remote_host = models.CharField(max_length=255, blank=True, null=True)
    device_name = models.CharField(max_length=255, blank=True, null=True)
    first_visit = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    blocked_at = models.DateTimeField(null=True, blank=True)
    operating_system = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.device_name or 'Inconnu'}"
