from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# User model attribute group
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    nid = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=200)
    phone = models.CharField(blank=True, max_length=11)

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

