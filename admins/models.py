# from distutils.command.upload import upload
# from email.mime import image
# from email.policy import default
# from secrets import choice
# from turtle import position
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
def numeric_validator(value):
    if not value.isnumeric():
        raise ValidationError(_("This field should only contain numbers"))
def phone_validator(value):
    if not value.isnumeric():
        raise ValidationError(_("The phone number is not a number"))
    if len(value) != 11:
        raise ValidationError(_("The phone number should be 11 digits"))
    phone_start_number = ['081','080','090','091','070']
    if value[:3]  in phone_start_number:
        pass
    else:
        raise ValidationError(_("Enter a valid nigerian number"))

def alpha_validator(value):
    if not value.isalpha():
        raise ValidationError(_("This field should only contain alphabets"))

class BaseManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class User(AbstractUser):
    username = None
    email = models.EmailField(
        _('Email'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    is_teacher = models.BooleanField(default=False)
    objects = BaseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=55,validators=[alpha_validator])
    lastname = models.CharField(max_length=55,validators=[alpha_validator])
    
    image = models.ImageField(upload_to = 'admin-images',blank = True)
    phonenumber = models.CharField(
        _('Phone Number'),
        max_length=11,
        validators = [phone_validator],
        help_text=_('Required. 11 Nigeria Phone Numbers.'),
        error_messages={
            'max_length': _("11 Numbers required."),
        },
        unique=True,
    )

    def __str__(self):
        return self.firstname+" "+self.lastname

class Subject(models.Model):
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=100,unique=True)
    classteacher = models.CharField(max_length=50,blank = True)
    subject = models.ManyToManyField(Subject,blank=True)

    def __str__(self):
        return self.name
    def student_number(self):
        return self.student_set.all().count()

class TeacherProgramme(models.Model):
    _class = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    report = models.FileField(upload_to="programme-reports",blank = True)

    def __str__(self):
        return str(self._class.name)+" - "+str(self.subject.name)
class Staff(models.Model):
    staff_type_choices = (('t','TEACHING'),('n','NON-TEACHING'))
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank = True,null = True)
    firstname = models.CharField("First Name",max_length=55,validators=[alpha_validator])
    lastname = models.CharField("Last Name",max_length=55,validators=[alpha_validator])
    dob = models.DateField("Date of Birth")
    sex = models.CharField(max_length=10,choices=(('M','Male'),('F','Female')))
    phonenumber = models.CharField(_('Phone Number'),max_length=11,validators = [phone_validator],
        help_text=_('Required. 11 Nigeria Phone Numbers.'),error_messages={
            'max_length': _("11 Numbers required."),
        },unique=True)
    state = models.CharField(max_length=20)
    lga = models.CharField("Local Government Area",max_length=50)
    hometown = models.CharField("Home Town",max_length=50)
    residential_address = models.TextField(default="Prefer not to say",blank=True,max_length=1000)
    image = models.ImageField(upload_to = "teacher-images",blank = True,null = True)
    accountnumber = models.CharField(max_length=10,validators=[numeric_validator],blank = True)
    accountname = models.CharField(max_length=255,blank = True)
    bank = models.CharField(max_length=100, blank = True)
    staff_type = models.CharField(max_length = 2,choices = staff_type_choices)
    programme = models.ManyToManyField(TeacherProgramme,blank = True)
    status = models.BooleanField(default = True)
    position = models.CharField(max_length=30)

    def __str__(self):
        return self.firstname +" "+self.lastname

class Student(models.Model):
    firstname = models.CharField("First Name",max_length=55,validators=[alpha_validator])
    lastname = models.CharField("Last Name",max_length=55,validators=[alpha_validator])
    dob = models.DateField("Date of Birth")
    sex = models.CharField(max_length=10,choices=(('M','Male'),('F','Female')))
    state = models.CharField(max_length=20)
    lga = models.CharField("Local Government Area",max_length=50)
    hometown = models.CharField("Home Town",max_length=50)
    residential_address = models.TextField(default="Prefer not to say",max_length=1000)
    image = models.ImageField(upload_to = "student-images",blank = True,null = True)
    guardianname = models.CharField("Guardian Name",max_length=55)
    guardianphonenumber = models.CharField(_('Phone Number'),max_length=11,validators = [phone_validator],
        help_text=_('Required. 11 Nigeria Phone Numbers.'),error_messages={
            'max_length': _("11 Numbers required."),
        })
    guardianemail = models.EmailField()
    _class = models.ForeignKey(Class,null = True,on_delete=models.SET_NULL)
    subjects = models.ManyToManyField(Subject,blank = True)
    classaverage = models.FloatField(blank =  True,null = True)
    classposition = models.IntegerField(blank = True,null = True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.firstname +' '+self.lastname

class Schedule(models.Model):
    teacher = models.ForeignKey(Staff,on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    _class = models.ForeignKey(Class,on_delete=models.SET_NULL,null = True,blank = True)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.teacher.firstname +' '+self.teacher.lastname

class Event(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length=1500)
    date = models.DateField()
    time = models.TimeField()
    # session = models.CharField(max_length = 20)

    def __str__(self):
        return self.name
    
class EventImage(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'event-images')

    def __str__(self):
        return self.event.name

class Mail(models.Model):
    flag_choices = (('u','URGENT'),('i','INFO'))
    _from = models.ForeignKey(User,on_delete=models.SET_NULL,blank = True,null = True,related_name="_from")
    to = models.ForeignKey(User,blank = True,null = True,on_delete = models.SET("deleted user"))
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length = 1500)
    attachment = models.FileField(upload_to = 'mail',blank = True)
    read = models.BooleanField(default = False)
    flag = models.CharField(max_length=2,choices = flag_choices)
    date = models.DateField(auto_now_add = True)
    time = models.TimeField(auto_now_add = True)

    def __str__(self):
        return self.subject

class SiteSetting(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.name

