from dataclasses import fields
from pyexpat import model
from django import forms
from .models import *
from django.conf import settings
class AddClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__"
        widgets = {
            'subject':forms.SelectMultiple(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':' '}),
            'classteacher':forms.TextInput(attrs={'class':'form-control','placeholder':' '})
        }
class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':' '}),
            'abbr':forms.TextInput(attrs={'class':'form-control','placeholder':' '}),   
        }
class AddProgrammeForm(forms.Form):
    klass = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control','placeholder':' '}))
    subject = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control','placeholder':' '}))
    def __init__(self,*args, **kwargs):
        super(). __init__(*args, **kwargs)
        queryset1 = Class.objects.all()
        queryset2 = Subject.objects.all()
        self.fields['klass'].queryset = queryset1
        self.fields['subject'].queryset = queryset2
class StudentAddForm(forms.ModelForm):
    klass = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control','placeholder':' '}))
    class Meta:
        model = Student
        exclude = ['_class']
    def __init__(self,*args, **kwargs):
        super(). __init__(*args, **kwargs)
        queryset1 = Class.objects.all()
        self.fields['klass'].queryset = queryset1

class StaffAddForm(forms.ModelForm):
    # klass = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control','placeholder':' '}),required=False)
    # subject = forms.ModelChoiceField(queryset=None,widget=forms.Select(attrs={'class':'form-control','placeholder':' '}),required=False)
    email= forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput,required = False,min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, required = False)
    class Meta:
        model = Staff
        exclude = ['programme','user','status']
    def clean(self):
        if self.cleaned_data.get('staff_type') == 't':
            email = self.cleaned_data.get('email')
            if not email:
                self.add_error('email','Email is required for teaching staffs')
            if not self.cleaned_data.get('password'):
                self.add_error('password','Password is required for teaching staffs')
            if User.objects.filter(email = email).exists():
                self.add_error('email','User already Exists')
            if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
                self.add_error('password2',"Passwords deos not match")
            return self.cleaned_data
        return self.cleaned_data


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':' '}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':' '}),
            'date':forms.DateInput(attrs={'class':'form-control','placeholder':' '}),
            'time':forms.TimeInput(attrs={'class':'form-control','placeholder':' '}),
        }
    
class AddMailForm(forms.ModelForm):
    # receivers = forms.ModelChoiceField(queryset=None,widget=forms.SelectMultiple(attrs={'class':'form-control'}),required=True)
    class Meta:
        model = Mail
        fields = ['subject','message','flag','attachment']
        widgets={
            'flag':forms.Select(attrs={'class':'form-control','placeholder':' '}),
        }
    # def __init__(self,*args, **kwargs):
    #     super(). __init__(*args, **kwargs)
    #     queryset1 = User.objects.all()
    #     self.fields['receivers'].queryset = queryset1
