from django.db import models

# Create your models here.
class course(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    course_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    template = models.ImageField(upload_to='course_img', null=False, blank=False)