from django.db import models
from django.utils import timezone

# Create your models here.
class course(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    course_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    template = models.ImageField(upload_to='course_img', null=False, blank=False)


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        now = timezone.now()
        time_elapsed = now - self.created_at
        return time_elapsed.total_seconds() > 600