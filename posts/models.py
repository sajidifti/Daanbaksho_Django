# import imp
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# Create your models here.

class post(models.Model):
    title = models.CharField(max_length=200, null=True)
    short_desc = models.CharField(max_length=300, null=True)
    content = models.TextField(null=True)
    image = models.ImageField(default='default_post.jpg', upload_to='post_images')
    post_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        output_size = (900, 1600)
        img.thumbnail(output_size)
        img.save(self.image.path)

    class Meta:
        ordering = ('-date_posted',)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



class postMedia(models.Model):
    image = models.ImageField(default='default_post.jpg', upload_to='media_images')
    post_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.date_posted}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        output_size = (1600, 900)
        img.thumbnail(output_size)
        img.save(self.image.path)

    class Meta:
        ordering = ('-date_posted',)

    def get_absolute_url(self):
        return reverse('media-detail', kwargs={'pk': self.pk})