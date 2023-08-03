from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form

from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        excludes='user'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class RegForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']     