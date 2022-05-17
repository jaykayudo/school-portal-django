from ast import For
import re
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from django.views.generic import FormView, ListView, DetailView, UpdateView
from django.contrib.auth import logout
import datetime
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, JsonResponse,Http404
from .models import *
from .forms import *
from django import forms
def update_attrs(instance, **kwargs):
    """
    Update multiple attrs of models
    """
    instance_pk = instance.pk
    for key, value in kwargs.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
    instance.save(force_update=True)
    return instance.__class__.objects.get(pk=instance_pk)

# Create your views here.
class AdminRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
def home(request):
    return redirect(reverse('admins:dashboard'))

class DashboardView(AdminRequiredMixin,View):
    def get(self,request):
        # students = []
        # subjects = []
        # classes = []
        # staffs = []
        recent_events = []
        recent_mail = []

        students  = Student.objects.all().count()
        subjects = Subject.objects.all().count()
        classes = Class.objects.all().count()
        staffs = Staff.objects.all().count()
        events = Event.objects.all().count()
        recent_events = Event.objects.all()[0:4]
        recent_mail = Mail.objects.filter(to = request.user)[0:4]
        context = {
            'student_no':students,
            'subject_no':subjects,
            'class_no':classes,
            'staff_no':staffs,
            'event_no': events,
            'recent_events':recent_events,
            'recent_mail':recent_mail
        }
        return render(request,'admins/index.html',context)

def getClassValues(x):
    """
    For getting all the class values of a set of programmes
    """
    classvalue = []
    for y in x:
        classvalue.append(y._class)
    return classvalue


def teacherClassFilter(_class):
     
    """
    For getting all the teachers of a particular class
    """
    teachers = []
    try:
        classValue = Class.objects.get(name = _class)
    except:
        return []
    staffs = Staff.objects.filter(staff_type = 't')
    for x in staffs:
        if classValue in getClassValues(x.programme.all()):
            teachers.append(x)
    return teachers
def getSubjectValue(x):
    classvalue = []
    for y in x:
        classvalue.append(y.subject)
    return classvalue


def teacherSubjectFilter(_class):
    teachers = []
    try:
        subjectValue = Subject.objects.get(name = _class)
    except:
        return []
    staffs = Staff.objects.filter(staff_type = 't')
    for x in staffs:
        if subjectValue in getSubjectValue(x.programme.all()):
            teachers.append(x)
    return teachers
def sortbyFirstname(object):
    def sort_func(value):
        return value.firstname

    objectlist = []
    for x in object:
        objectlist.append(x)
    return sorted(objectlist,key = sort_func)
class StaffListView(AdminRequiredMixin,ListView):
    paginate_by = 20
    template_name = "admins/staffs.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        classes = Class.objects.all()
        subjects = Subject.objects.all()
        context['classes'] = classes
        context['subjects'] = subjects
        return context
    # def get(self,request,*args,**kwargs):
    #     data = self.get_queryset()
    #     return HttpResponse(data)
    def get_queryset(self):
        staff = Staff.objects.all()
        if self.request.GET.get('class'):
            staff = teacherClassFilter(self.request.GET['class'])
        if self.request.GET.get('status'):
            if self.request.GET['status'].isnumeric():
                staff = staff.filter(status = bool(int(self.request.GET.get('status'))))
        if self.request.GET.get('staff_type'):
            if self.request.GET['staff_type'] in ['t','n']:
                staff = staff.filter(staff_type = self.request.GET['staff_type'])
        if self.request.GET.get('subject'):
            staff = teacherClassFilter(self.request.GET['subject'])
        return sortbyFirstname(staff)
class StaffDetailView(AdminRequiredMixin,DetailView):
    model = Staff
    template_name = 'admins/staff-details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objectdata = self.get_object()
        today_schedule = Schedule.objects.filter(teacher = objectdata,date = datetime.date.today())
        context['schedule'] = today_schedule
        subjects = []
        classes = []
        data = Staff.objects.get(id = context['object'].id )
        for dat in data.programme.all():
            if dat.subject not in subjects:
                subjects.append(dat.subject)
        for dat in data.programme.all():
            if dat._class not in classes:
                classes.append(dat._class)
        context['subjects'] = subjects
        context['classes'] = classes
        return context

def scheduleGetView(request,id):
    if not request.is_ajax():
        return redirect(reverse('staff:dashboard'))
    date = request.GET.get('date')
    if date:
        date = date.split('/')
        date = datetime.date(year = int(date[2]),month = int(date[0]),day = int(date[1]))
        try:
            staff = Staff.objects.get(id = id)
        except:
            raise ValueError('Staff does not exist')
        schedule = Schedule.objects.filter(teacher = staff,date = date).values('description','_class__name','time')
        schedule = list(schedule)
        return JsonResponse({'schedule':schedule},safe = False)
    else:
        raise ValueError('Date not Specified')
class StaffStatusToggle(AdminRequiredMixin,View):
    def get(self,request,id):
        try:
            staff = Staff.objects.get(id = id)
        except:
            messages.error(request,"Invalid Query")
            return redirect(reverse('admins:staff'))
        
        user = User.objects.get(id = staff.user.id)
        if staff.status:
            staff.status = False
            user.is_active = False
            messages.success(request,"Staff Blocked Successfully")
        else:
            staff.status = True
            user.is_active = True
            messages.success(request,"Staff Activated Successfully")
        staff.save()            
        user.save()

        return redirect(reverse('admins:staff-details',kwargs ={"pk":id}))
class StaffDeleteView(AdminRequiredMixin,View):
    def get(self,request,id):
        try:
            staff = Staff.objects.get(id = id)
        except:
            messages.error(request,"Invalid Query")
            return redirect(reverse('admins:staff'))
        
        return HttpResponse('Are you sure')
    
    def post(self,request,id):
        try:
            staff = Staff.objects.get(id = id)
        except:
            messages.error(request,"Invalid Query")
            return redirect(reverse('admins:staff'))
        staff.delete()
        messages.success(request,"Staff Deleted Successfully")
        return redirect(reverse('admins:staff'))
class StaffAddFormView(AdminRequiredMixin,FormView):
    form_class = StaffAddForm
    template_name = 'admins/forms/add-staff-form.html'
    success_url = reverse_lazy('admins:staff')
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        classes = Class.objects.all()
        context['classes'] = classes
        subjects = Subject.objects.all()
        context['subjects'] = subjects
        return context
    def form_valid(self,form):  
        if form.cleaned_data.get('staff_type') == 't':
            classes = self.request.POST.getlist('class')
            subjects = self.request.POST.getlist('subject')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(email = email, password = password)
            user.is_teacher = True
            user.save()
            obj = form.save(commit = False)
            obj.user = user
            obj.save()
            for x,y in zip(classes,subjects):
                _class = Class.objects.get(id = int(x))
                subject = Subject.objects.get(id = int(y))
                programme, created = TeacherProgramme.objects.get_or_create(_class = _class,subject = subject)
                obj.programme.add(programme)
                obj.save()
                print(programme)
        else:
            form.save()
        messages.success(self.request,"Staff Created")
        return super().form_valid(form)


class StudentListView(AdminRequiredMixin,ListView):
    paginate_by = 20
    template_name = "admins/students.html"
    # def get(self,request,*args,**kwargs):
    #     data = self.get_queryset()
    #     return HttpResponse(data)
    def get_queryset(self):
        student = Student.objects.all()
        if self.request.GET.get('class'):
            student = student.filter(_class__name = self.request.GET['class'])
        if self.request.GET.get('status'):
            if self.request.GET['status'].isnumeric():
                student = student.filter(status = bool(int(self.request.GET.get('status'))))
        if self.request.GET.get('sex'):
            student = student.filter(sex = self.request.GET['sex'])
        # if self.request.GET.get('subject'):
            
        return student.order_by('firstname')

class StudentDetailView(AdminRequiredMixin,DetailView):
    model = Student
    template_name = 'admins/students-profile.html'


class StudentStatusToggle(AdminRequiredMixin,View):
    def get(self,request,id):
        try:
            student = Student.objects.get(id = id)
        except:
            messages.error(request,"Invalid Query")
            return redirect(reverse('admins:student'))
        
        if student.status:
            student.status = False
            messages.success(request,"Student Blocked Successfully")
        else:
            student.status = True
            messages.success(request,"Student Activated Successfully")
        student.save()            
        

        return redirect(reverse('admins:student-details',kwargs ={"pk":id}))

class StudentDeleteView(AdminRequiredMixin,View):
    def get(self,request,id):
        try:
            student = Student.objects.get(id = id)
        except:
            messages.error(request,"Invalid Query")
            return redirect(reverse('admins:student'))
        
        return HttpResponse('Are you sure')
    
    def post(self,request,id):
        try:
            student = Student.objects.get(id = id)
        except:
            messages.error(request,"Invalid Query")
            return redirect(reverse('admins:student'))
        student.delete()
        messages.success(request,"Student Deleted Successfully")
        return redirect(reverse('admins:student'))
class StudentAddFormView(AdminRequiredMixin,FormView):
    form_class = StudentAddForm
    template_name = "admins/forms/add-student-form.html"
    success_url = reverse_lazy('admins:student')

    def form_valid(self, form):
        obj = form.save(commit = False)
        class_id = form.cleaned_data.get('klass')
        obj._class = class_id
        obj.save()
        messages.success(self.request,"Student Added")
        if self.request.GET.get('submit') == 'Save and Add Another':
            self.success_url = reverse('admins:student-add-form')
        return super().form_valid(form)
class InboxView(AdminRequiredMixin,View):
    def get(self,request):
        return redirect(reverse('admins:inbox-received'))
class InboxReceivedView(AdminRequiredMixin,ListView):
    paginate_by = 15
    template_name = 'admins/inbox.html'
    def get_queryset(self):
        to_user = self.request.user
        if self.request.GET.get('date'):
            inbox = Mail.objects.filter(to = to_user,date = self.request.GET['date'])
            return inbox.order_by('-time')
        else:
            inbox = Mail.objects.filter(to = to_user)
            return inbox.order_by("-date")
class InboxSentView(AdminRequiredMixin,ListView):
    paginate_by = 15
    template_name = 'admins/inbox-sent.html'
    def get_queryset(self):
        to_user = self.request.user
        if self.request.GET.get('date'):
            inbox = Mail.objects.filter(_from = to_user,date = self.request.GET['date'])
            return inbox.order_by('-time')

        else:
            inbox = Mail.objects.filter(_from = to_user)
            return inbox.order_by("-date")
class InboxFormView(AdminRequiredMixin,FormView):
    form_class = AddMailForm
    template_name = "admins/forms/send-mail-form.html"
    success_url = reverse_lazy('admins:inbox-sent')
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        users = User.objects.all()
        context['users'] = users
        return context
    def form_valid(self, form):
        receivers = self.request.POST.getlist('receivers')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        attachment = form.cleaned_data.get('attachment')
        flag = form.cleaned_data.get('flag')
        for x in receivers:
            user = User.objects.get(id = int(x))
            Mail.objects.create(_from = self.request.user,to = user,subject = subject,message = message,attachment = attachment,flag= flag)
        messages.success(self.request,"Mail Sent")
        return super().form_valid(form)
class InboxDetailsView(AdminRequiredMixin,View):
    def get(self,request,id):
        try:
            letter = Mail.objects.get(to = request.user,id = id)
        except:
            try:
                letter = Mail.objects.get(_from = request.user,id = id)
            except:
                messages.error(request,"Mail does not Exist")
                return redirect(reverse('staff:inbox-list'))
        if not letter.read and letter._from != request.user:
            letter.read = True
            letter.save()
        
        context = {'object':letter}
        return render(request,'admins/inbox-details.html',context)
class EventView(AdminRequiredMixin,ListView):
    paginate_by = 15
    template_name = 'admins/events.html'
    def get_queryset(self):
        if self.request.GET.get('date'):
            event = Event.objects.filter(date = self.request.GET['date'])
            return event.order_by('-time')
        else:
            event = Event.objects.all()
            return event.order_by("-date")
class EventFormView(AdminRequiredMixin,FormView):
    form_class = AddEventForm
    template_name = 'admins/forms/add-event.html'
    success_url = reverse_lazy('admins:event')
    def form_valid(self, form):
        obj = form.save()
        eventimages = self.request.FILES.getlist('image')
        for x in eventimages:
            EventImage.objects.create(event = obj,image = x)
        messages.success(self.request,"Event Created")
        return super().form_valid(form)
class EventDetailsView(AdminRequiredMixin,View):
    def get(self,request,id):
        event = get_object_or_404(Event,id=id)
        context = {'object':event}
        return render(request,'admins/event-details.html',context)
class ProgrammeView(AdminRequiredMixin,View):
    def get(self,request):
        subjects = Subject.objects.all().order_by('name')
        classes = Class.objects.all().order_by('name')
        context = {
            'classes':classes,
            'subjects':subjects
        }
        return render(request,'admins/programme.html',context)

class ProgrammeClassFormView(AdminRequiredMixin,FormView):
    form_class = AddClassForm
    template_name = 'admins/forms/add-class.html'
    success_url = reverse_lazy('admins:programme')
    extra_context = {'title':"Add Class",'btn_text':'Add'}

    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Class Created")
        return super().form_valid(form)
class ProgrammeSubjectFormView(AdminRequiredMixin,FormView):
    form_class = AddSubjectForm
    template_name = 'admins/forms/add-subject.html'
    success_url = reverse_lazy('admins:programme')
    extra_context = {'title':"Add Subject",'btn_text':'Add'}

    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Subject Created")
        return super().form_valid(form)
class ProgrammeTopicFormView(AdminRequiredMixin,FormView):
    form_class = AddProgrammeForm
    template_name = 'admins/forms/add-topic.html'
    success_url = reverse_lazy('admins:programme')

    def form_valid(self, form):
        messages.success(self.request,"Topic Added")
        return super().form_valid(form)
class ProgrammeUpdateClassView(AdminRequiredMixin,UpdateView):
    model = Class
    fields = '__all__'
    success_url = reverse_lazy('admins:programme')
    template_name = 'admins/forms/add-class.html'
    extra_context = {'title':'Edit Class','btn_text':'Update'}

    def get_success_url(self):
        messages.success(self.request,"Class Updated")
        return self.success_url
    # def get_context_data(self, **kwargs):
    #     form_class = self.get_form_class()
    #     if not 'form' in kwargs:
    #         kwargs['form'] = self.get_form(form_class)
    #     context = super().get_context_data(**kwargs)
    #     return context
    # def get_form_class(self):
    #     widgets = {
    #         'name':forms.TextInput(attrs={'class':'form-control','placeholder':' '}),
    #         'abbr':forms.TextInput(attrs={'class':'form-control','placeholder':' '}),   
    #     }
    #     self.form_class = super().get_form_class()
    #     self.form_class.Meta().widgets = widgets
    #     return self.form_class
    # def get_form(self, form_class):
       
    #     instance = super().get_form(form_class)
    #     # print(instance.__dict__['fields']['subject'].__dict__)
       
    #     return instance
class ProgrammeUpdateSubjectView(AdminRequiredMixin,UpdateView):
    model = Subject
    fields = '__all__'
    success_url = reverse_lazy('admins:programme')
    template_name = 'admins/forms/add-subject.html'
    extra_context = {'title':'Edit Subject','btn_text':'Update'}

    def get_success_url(self):
        messages.success(self.request,"Subject Updated")
        return self.success_url


class SettingsView(AdminRequiredMixin,View):
    def get(self,request):
        return render(request,'admins/settings/settings.html')
    def post(self,request):
        data = request.POST
        user = User.objects.get(id = request.user.id)
        admin = Admin.objects.get(user = user)
        update_attrs(user,**data)
        update_attrs(admin,**data)
        messages.success('Profile Updated')
        return redirect(reverse('admins:settings'))
class SettingsPasswordChangeView(AdminRequiredMixin,PasswordChangeView):
    template_name = "admins/settings/change-password.html"
    success_url = reverse_lazy("staff:profile")
    def form_valid(self,form):
        messages.success(self.request,_("Password changed."))
        return super().form_valid(form)
class SettingsAdminView(AdminRequiredMixin,View):
    def get(self,request):
        admin = Admin.objects.all()
        return render(request,'staff/Users.html',{'admin':admin})
class LogoutView(AdminRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logout Successful")
        return redirect(reverse('login'))