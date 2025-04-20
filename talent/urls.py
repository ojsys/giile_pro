from django.urls import path
from . import views

app_name = 'talent'

urlpatterns = [
    # Public talent views
    path('', views.TalentListView.as_view(), name='talent_list'),
    
    # Talent dashboard views - moved before the detail view with slug
    path('dashboard/', views.TalentDashboardView.as_view(), name='talent_dashboard'),
    path('dashboard/profile/create/', views.TalentProfileCreateView.as_view(), name='talent_profile_create'),
    path('dashboard/profile/edit/', views.TalentProfileEditView.as_view(), name='talent_profile_edit'),
    path('dashboard/portfolio/add/', views.PortfolioItemCreateView.as_view(), name='portfolio_item_create'),
    path('dashboard/portfolio/edit/<int:pk>/', views.PortfolioItemEditView.as_view(), name='portfolio_item_edit'),
    path('dashboard/booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('dashboard/booking/<int:pk>/accept/', views.BookingAcceptView.as_view(), name='booking_accept'),
    path('dashboard/booking/<int:pk>/decline/', views.BookingDeclineView.as_view(), name='booking_decline'),
    
    # Other public views
    path('category/<slug:slug>/', views.TalentCategoryView.as_view(), name='talent_category'),
    path('skill/<slug:slug>/', views.TalentSkillView.as_view(), name='talent_skill'),
    path('booking-thank-you/<slug:talent_slug>/', views.BookingThankYouView.as_view(), name='booking_thank_you'),
    
    # Detail view with slug - moved to the end so it doesn't catch other URLs
    path('<slug:slug>/', views.TalentDetailView.as_view(), name='talent_detail'),
]