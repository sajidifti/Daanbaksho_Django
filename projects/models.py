from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# Create your models here.
class project(models.Model):
    title = models.CharField(max_length=200, null=True)
    short_desc = models.CharField(max_length=300, null=True)
    content = models.TextField(null=True)
    image = models.ImageField(default='default_post.jpg', upload_to='project_images')
    post_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default='True')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        output_size = (1600, 900)
        img.thumbnail(output_size)
        img.save(self.image.path)

    class Meta:
        ordering = ('-date_posted',)

    def get_absolute_url(self):
        return reverse('projects-detail', kwargs={'pk': self.pk})




class projectDonation(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Declined', 'Declined'),
    )

    P_METHOD = (
        ('Bkash', 'Bkash'),
        ('Nagad', 'Nagad'),
        ('Rocket', 'Rocket'),
    )

    donor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(project, null=True, on_delete=models.SET_NULL) #, related_name="prodons"
    amount = models.FloatField(null=True)
    p_method = models.CharField(max_length=10, null=True, choices=P_METHOD)
    phone = models.CharField(max_length=11, null=True)
    txid = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=15, null=True,
                              choices=STATUS, default='Pending')
    date_donated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-date_donated',)