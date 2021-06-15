from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User,Fan,Customer
from django import forms


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    

    class Meta(UserCreationForm.Meta):
        model = User



    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer=True
        user.first_name= self.cleaned_data.get('first_name')
        user.last_name= self.cleaned_data.get('first_name')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number= self.cleaned_data.get('phone_number')
        customer.save()
        return user


class FanSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    city = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    

    class Meta(UserCreationForm.Meta):
        model = User



    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_fan=True
        user.first_name= self.cleaned_data.get('first_name')
        user.last_name= self.cleaned_data.get('last_name')
        user.save()
        fan = Fan.objects.create(user=user)
        fan.phone_number= self.cleaned_data.get('phone_number')
        fan.city= self.cleaned_data.get('city')
        fan.save()
        return user