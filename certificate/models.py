from django.db import models

from course.models import course

import hashlib
import math
import datetime


# Create your models here.
class certificate(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today, null=False, blank=False)
    unique_code = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self.generate_unique_id()
        super(certificate, self).save(*args, **kwargs)

    def generate_unique_id(self):
        base = 36
        hash_input = f"{self.id}{self.course}{self.name}{self.date}{self.pk}".encode('utf-8')
        hashed_value = hashlib.sha256(hash_input).hexdigest()
        idnum = int(hashed_value, 16)
        t = int(math.log(idnum, base))
        uid = ''
        while idnum > 0:
            t = max(t, 0)
            bcp = base ** t
            dgt = idnum // bcp
            uid += 'a1b2c3d4e5fghijklmnopqrstuvwxyzA6B7C8D9E0FGHIJKLMNOPQRSTUVWXYZ'[dgt]
            idnum -= dgt * bcp
            t -= 1
        return uid.zfill(10)