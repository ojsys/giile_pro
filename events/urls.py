from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('category/<slug:slug>/', views.EventCategoryView.as_view(), name='category'),
    path('registration-thank-you/<slug:event_slug>/', views.RegistrationThankYouView.as_view(), name='registration_thank_you'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
]