from django import forms
from django.forms import ValidationError
from admins.models import Schedule, Staff,phone_validator

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        # fields = '__all__'
        exclude = ['teacher']
        widgets = {
            '_class':forms.Select(attrs={'class':'form-control'})
        }

class UploadForm(forms.Form):
    message = forms.CharField(max_length=50)
    category = forms.ChoiceField()
    file = forms.FileField()
class EditProfileForm(forms.ModelForm):
    phonenumber = forms.CharField(validators=[phone_validator])
    class Meta:
        model = Staff
        exclude = ['programme','status','position','user','phonenumber',"staff_type"]