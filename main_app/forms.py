from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Reservation

class ReservationForm(ModelForm):
  class Meta:
    model = Reservation
    fields = ['start_date', 'end_date', 'gear_item', 'qty']

# class UserCreationFormWithName(UserCreationForm):
#     first_name = forms.CharField(max_length=100, required=True)
#     last_name = forms.CharField(max_length=100, required=True)
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "username", "email", "password1", "password2")

#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user