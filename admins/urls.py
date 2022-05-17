from django.urls import path
from .views import *

app_name = 'admins'

urlpatterns = [
    path('',home),
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('staff/',StaffListView.as_view(),name="staff"),
    path('staff/add/',StaffAddFormView.as_view(),name="staff-add"),
    path('staff/<int:pk>/',StaffDetailView.as_view(),name="staff-details"),
    path('staff/<int:id>/get-schedule/',scheduleGetView),
    path('staff/<int:id>/toggle-status/',StaffStatusToggle.as_view(),name="staff-toggle"),
    path('staff/<int:id>/delete/',StaffDeleteView.as_view(),name="staff-delete"),
    path('student/',StudentListView.as_view(),name="student"),
    path('student/add/',StudentAddFormView.as_view(),name="student-add-form"),
    path('student/<int:pk>/',StudentDetailView.as_view(),name="student-details"),
    path('student/<int:id>/toggle-status/',StudentStatusToggle.as_view(),name="student-toggle"),
    path('student/<int:id>/delete/',StudentDeleteView.as_view(),name="student-delete"),
    path('mail/',InboxView.as_view(),name="inbox"),
    path('mail/received/',InboxReceivedView.as_view(),name="inbox-received"),
    path('mail/sent/',InboxSentView.as_view(),name="inbox-sent"),
    path('mail/create/',InboxFormView.as_view(),name="inbox-create"),
    path('event/',EventView.as_view(),name="event"),
    path('event/add/',EventFormView.as_view(),name="event-add"),
    path('event/<int:id>/',EventDetailsView.as_view(),name="event"),
    path('programme/',ProgrammeView.as_view(),name="programme"),
    path('programme/add-class',ProgrammeClassFormView.as_view(),name="programme-add-class"),
    path('programme/add-subject',ProgrammeSubjectFormView.as_view(),name="programme-add-subject"),
    path('programme/add-topic',ProgrammeTopicFormView.as_view(),name="programme-add-topic"),
    path('programme/class/<int:pk>/edit',ProgrammeUpdateClassView.as_view(),name="programme-edit-class"),
    path('programme/subject/<int:pk>/edit',ProgrammeUpdateSubjectView.as_view(),name="programme-edit-subject"),
    path('settings/',SettingsView.as_view(),name="settings"),
    path('settings/password',SettingsPasswordChangeView.as_view(),name="settings-password"),
    path('logout/',LogoutView.as_view(),name="logout"),
]