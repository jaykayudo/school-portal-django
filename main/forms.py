from django import forms
from django.contrib.auth import authenticate
from admins.models import User,Admin,Staff
class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput, strip =False)
    staff_type = forms.CharField()
    def __init__(self,request = None,*args,**kwargs):
        self.request = request
        self.user = None
        super().__init__(*args,**kwargs)
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user  = authenticate(self.request,email = email,password=password)
        if user:
            if self.cleaned_data.get('staff_type') == 'admin':
                if Admin.objects.filter(user = user):
                    self.user = user
                else:
                    raise forms.ValidationError("Unregistered Admin Account")
            elif self.cleaned_data.get('staff_type') == 'staff':
                if Staff.objects.filter(user = user):
                    self.user = user
                else:
                    raise forms.ValidationError("Unregistered Staff Account")
            else:
                raise forms.ValidationError("Unauthorized user")
        if not self.user:
            raise forms.ValidationError("Incorrect Credentials")
        return self.cleaned_data
    def get_user(self):
        return self.user