from django import forms
from. models import *

class foodDonationForm(forms.ModelForm):
    class Meta:
        model = food_donation
        fields = ['quantity', 'description']


class clothDonationForm(forms.ModelForm):
    class Meta:
        model = cloth_donation
        fields = ['total_items', 'items_description']