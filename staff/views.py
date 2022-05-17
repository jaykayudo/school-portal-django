from django.shortcuts import render, redirect,reverse,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from django.views.generic import FormView, ListView
from django.contrib.auth import logout
import datetime

from pytz import timezone

from staff.forms import ScheduleForm,EditProfileForm,UploadForm
from .forms import *
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, JsonResponse,Http404

# Create your views here.
from admins.models import *

def home(request):
    return redirect(reverse('staff:dashboard'))

class StaffRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_teacher

class DashboardView(StaffRequiredMixin,View):
    def get(self,request):
        context = {}
        students = []
        all_students = []
        subjects = []
        classes = []
        completed_uploads = []
        schedule_form  = ScheduleForm()
        
        staff = request.user.staff.id
        teacher_programme = Staff.objects.get(id = staff).programme.all()
        
        if teacher_programme:
            for programme in teacher_programme:
                class_student = Student.objects.filter(_class = programme._class,status = True)
                if class_student:
                    for sub in class_student:
                        if programme.subject in sub.subjects.all():
                            students.append(sub)
            for x in students:
                if x not in all_students:
                    all_students.append(x)
            
            for data in teacher_programme:
                if data.subject not in subjects:
                    subjects.append(data.subject)
            for data in teacher_programme:
                if data._class not in classes:
                    classes.append(data._class)
            for data in teacher_programme:
                if data.report:
                    completed_uploads.append(data)

        today_schedule = Schedule.objects.filter(teacher = request.user.staff,date = date.today())
        valid_inbox = False
        mail_checker = Mail.objects.filter(to = request.user,read = False)
        if mail_checker:
            valid_inbox = True
        
        context['unread'] = valid_inbox
        context['form'] = schedule_form
        context['student_no'] = len(all_students)
        context['subject_no'] = len(subjects)
        context['class_no'] = len(classes)
        context['schedule'] = today_schedule
        context['upload'] = len(teacher_programme)
        context['completed_upload'] = completed_uploads
        context['formclass'] = schedule_form['_class']  
    

        return render(request,'staff/index.html',context)
    
    def post(self,request):
        form = ScheduleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.teacher = request.user.staff
            obj.save()
            messages.success(request,"Schedule Created")
            return redirect(reverse('staff:dashboard'))
        return redirect(reverse('staff:dashboard'))
            



def scheduleGetView(request):
    if not request.is_ajax():
        return redirect(reverse('staff:dashboard'))
    date = request.GET.get('date')
    if date:
        date = date.split('/')
        date = datetime.date(year = int(date[2]),month = int(date[0]),day = int(date[1]))
        schedule = Schedule.objects.filter(teacher = request.user.staff,date = date).values('description','_class__name','time')
        schedule = list(schedule)
        return JsonResponse({'schedule':schedule},safe = False)
    else:
        raise ValueError('Date not Specified')

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

class ProfileView(StaffRequiredMixin,View):
    def get(self,request):
        context = {
        }
        subjects = []
        classes = []
        data = Staff.objects.get(id = request.user.staff.id )
        for dat in data.programme.all():
            if dat.subject not in subjects:
                subjects.append(dat.subject)
        for dat in data.programme.all():
            if dat._class not in classes:
                classes.append(dat._class)
        context['data'] = data
        context['subjects'] = subjects
        context['classes'] = classes
        return render(request,'staff/profile.html',context)

class EditProfileView(StaffRequiredMixin,View):
    def get(self,request):
        details = request.user.staff.id
        staff = Staff.objects.get(id = details)
        dictstaff = staff.__dict__
        dictstaff['email'] = request.user.email
        dictstaff['phonenumber'] = request.user.staff.phonenumber
        form = EditProfileForm(dictstaff)
        return render(request,'staff/edit-profile.html',{'form':form})
    def post(self,request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            obj = form.cleaned_data
            staff = Staff.objects.get(id = request.user.staff.id)
            # staff.update(**obj) #error has no attr email
            updated_model = update_attrs(staff,**obj)
            # user = User.objects.get(id=request.user.id)
            # user.email = form.cleaned_data['email']
            # user.save()
            messages.success(request,"Profile Edited Successfully")
            return redirect(reverse('staff:profile'))
        print(form)
        return render(request,'staff/edit-profile.html',{'form':form})

class UserPasswordChangeView(StaffRequiredMixin,PasswordChangeView):
    template_name = "staff/change-password.html"
    success_url = reverse_lazy("staff:profile")
    def form_valid(self,form):
        messages.success(self.request,_("Password changed."))
        return super().form_valid(form)

def class_name_sort(obj):
    return obj.name
def student_name_sort(obj):
    return obj.firstname

class ClassListView(StaffRequiredMixin,View):
    def get(self,request):
        staff = request.user.staff
        teacher_programme = staff.programme.all()
        classes = []

        for data in teacher_programme:
                if data._class not in classes:
                    classes.append(data._class)
        classes.sort(key = class_name_sort)
        return render(request,'staff/class.html',{'classes':classes})
class ClassDetailsView(StaffRequiredMixin,View):
    def get(self,request,id):
        pass

class StudentListView(StaffRequiredMixin,ListView):
    paginate_by = 12
    template_name = 'staff/student.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        classes = []
        subjects = []
        staff = self.request.user.staff
        teacher_programme = staff.programme.all()
        classes = []

        for data in teacher_programme:
            if data._class not in classes:
                classes.append(data._class)
        for data in teacher_programme:
            if data.subject not in subjects:
                subjects.append(data.subject)
        context['classes'] = classes
        context['subjects'] = subjects
        return context
        
    def get_queryset(self):
        students = []
        all_students = []
        staff = self.request.user.staff.id
        teacher_programme = Staff.objects.get(id = staff).programme.all()
        
        if teacher_programme:
            for programme in teacher_programme:
                class_student = Student.objects.filter(_class = programme._class,status = True)
                if class_student:
                    for sub in class_student:
                        if programme.subject in sub.subjects.all():
                            students.append(sub)
            for x in students:
                if x not in all_students:
                    all_students.append(x)
        all_students.sort(key = student_name_sort)
        return all_students
        
class StudentDetailsView(StaffRequiredMixin,View):
    def get(self,request,id):
        student = get_object_or_404(Student,id = id)
        students = []
        staff = self.request.user.staff.id
        teacher_programme = Staff.objects.get(id = staff).programme.all()
        
        if teacher_programme:
            for programme in teacher_programme:
                class_student = Student.objects.filter(_class = programme._class, status = True)
                if class_student:
                    for sub in class_student:
                        if programme.subject in sub.subjects.all():
                            students.append(sub)
        if student in students:
            return render(request,'staff/student-details.html',{'object':student})
        else:
            messages.error(request,"Unauthorized Access")
            return redirect(reverse('staff:student-list'))

class InboxListView(StaffRequiredMixin,ListView):
    paginate_by = 15
    template_name = 'staff/inbox.html'
    def get_queryset(self):
        to_user = self.request.user
        if self.request.GET.get('date'):
            inbox = Mail.objects.filter(to = to_user,date = self.request.GET['date'])
            return inbox.order_by('-time')
        else:
            inbox = Mail.objects.filter(to = to_user)
            return inbox.order_by("-date")

class InboxDetailsView(StaffRequiredMixin,View):
    def get(self,request,id):
        try:
            letter = Mail.objects.get(to = request.user,id = id)
        except:
            messages.error(request,"Mail does not Exist")
            return redirect(reverse('staff:inbox-list'))
        
        letter.read = True
        letter.save()
        
        context = {'object':letter}
        return render(request,'staff/inbox-details.html',context)


class InboxDeleteView(StaffRequiredMixin,View):
    def get(self,request,id):
        try:
            letter = Mail.objects.get(to = request.user,id = id)
        except:
            messages.error(request,"Mail does not Exist")
            return redirect(reverse('staff:inbox-list'))
        
        letter.to = None
        letter.save()
        messages.success(request,"Mail deleted")
        return redirect(reverse('staff:inbox-list'))


class UploadView(StaffRequiredMixin,FormView):
    form_class = UploadForm
    template_name = "Staff/upload.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.request.user.staff
        context_data = []
        teacher_programme = staff.programme.all()
        for x in teacher_programme:
            if not x.report:
                context_data.append(x)
        context['programmes'] = context_data
        return context
    def form_valid(self,form):
        response = super().form_valid(form)
        data = form.cleaned_data
        programme = TeacherProgramme.objects.get(id = data['category'])
        programme.report = data['file']
        programme.save()
        messages.success(self.request,"Upload Successful")
        return response

class LogoutView(StaffRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logout Successful")
        return redirect(reverse('login'))

         

