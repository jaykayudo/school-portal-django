from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.home,name = "home"),
    path('dashboard/', views.DashboardView.as_view(),name = "dashboard"),
    path('dashboard/get-schedule/', views.scheduleGetView),
    path('profile/', views.ProfileView.as_view(),name = "profile"),
    path('profile/edit/', views.EditProfileView.as_view(),name = "edit-profile"),
    path('profile/change-password/', views.UserPasswordChangeView.as_view(),name = "change-password"),
    path('classes/', views.ClassListView.as_view(),name = "class"),
    path('students/', views.StudentListView.as_view(),name = "student-list"),
    path('students/<int:id>', views.StudentDetailsView.as_view(),name = "student-details"),
    path('inbox/', views.InboxListView.as_view(),name = "inbox-list"),
    path('inbox/<int:id>', views.InboxDetailsView.as_view(),name = "inbox-details"),
    path('inbox/<int:id>/delete', views.InboxDeleteView.as_view(),name = "inbox-delete"),
    path('uploads/', views.UploadView.as_view(),name = "uploads"),
    path('logout/', views.LogoutView.as_view(),name = "logout"),
]