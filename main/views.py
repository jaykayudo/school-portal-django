from django.shortcuts import render
from django.urls import reverse

from django.views.generic import FormView
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import login
# Create your views here.
def indexview(request):
    return render(request,'main/index.html')
def contactview(request):
    return render(request,'main/contact.html')
def newsview(request):
    return render(request,'main/news.html')
def newsdetailview(request,id):
    return render(request,'main/news-details.html')
def aboutview(request):
    return render(request,'main/about.html')

class LoginView(FormView):
    form_class = LoginForm
    template_name = "main/login.html"
    success_url = '/'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request,user = user)
        if form.cleaned_data.get('staff_type') == 'admin':
            messages.success(self.request,"Login Successful")
            self.success_url = reverse('admins:dashboard')
        elif form.cleaned_data.get('staff_type') == 'staff':
            messages.success(self.request,"Login Successful")
            self.success_url = reverse('staff:dashboard')
        return super().form_valid(form)
