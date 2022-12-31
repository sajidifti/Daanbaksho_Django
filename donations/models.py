from django.db import models
from django.contrib.auth.models import User

from donations.decorators import donor_only

# Create your models here.

# Money Donation Model


class money_donation(models.Model):
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
    amount = models.FloatField(null=True)
    p_method = models.CharField(max_length=10, null=True, choices=P_METHOD)
    phone = models.CharField(max_length=11, null=True)
    txid = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=15, null=True,
                              choices=STATUS, default='Pending')
    date_donated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-date_donated',)

    # def __str__(self):
    #     return f'{self.donor.first_name}\'s Money Donation'


# Food Donation Model
class food_donation(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Picked', 'Picked'),
        ('About to Be Picked', 'About to Be Picked'),
        ('Received', 'Received'),
        ('Delivered', 'Delivered'),
        ('Declined', 'Declined'),
    )

    d_user = models.ManyToManyField(User)
    quantity = models.IntegerField(null=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=20, null=True,
                              choices=STATUS, default='Pending')
    date_donated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-date_donated',)

    # def __str__(self):
    #     return f'{self.d_user}\'s Food Donation'


# Cloth Donation Model
class cloth_donation(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Picked', 'Picked'),
        ('About to Be Picked', 'About to Be Picked'),
        ('Received', 'Received'),
        ('Delivered', 'Delivered'),
        ('Declined', 'Declined'),
    )

    d_user = models.ManyToManyField(User)
    total_items = models.IntegerField(null=True)
    items_description = models.TextField(null=True)
    status = models.CharField(max_length=20, null=True,
                              choices=STATUS, default='Pending')
    date_donated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-date_donated',)




class clothInventory(models.Model):
    shirt = models.IntegerField(null=True)
    pant = models.IntegerField(null=True)
    t_shirt = models.IntegerField(null=True)
    vest = models.IntegerField(null=True)
    lungi = models.IntegerField(null=True)
    salwar = models.IntegerField(null=True)
    pajama = models.IntegerField(null=True)
    saree = models.IntegerField(null=True)
    panjabi = models.IntegerField(null=True)
    blanket = models.IntegerField(null=True)



class foodInventory(models.Model):
    for_people = models.IntegerField(null=True)