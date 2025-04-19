from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import AboutPage, SiteSettings

def home_view(request):
    """View for the home page."""
    settings = SiteSettings.get_settings()
    return render(request, 'core/home.html', {
        'settings': settings,
    })

def about_view(request):
    """View for the about page."""
    # Get the first about page or create one if it doesn't exist
    about_page, created = AboutPage.objects.get_or_create(pk=1)
    settings = SiteSettings.get_settings()
    
    # Get related content
    values = about_page.values.all().order_by('order')
    team_members = about_page.team_members.all().order_by('order')
    
    return render(request, 'core/about.html', {
        'page': about_page,
        'settings': settings,
        'values': values,
        'team_members': team_members,
    })

class ContactView(TemplateView):
    template_name = 'core/contact.html'


def privacy_policy(request):
    """Privacy policy page view."""
    context = {
        'title': 'Privacy Policy',
    }
    return render(request, 'core/privacy_policy.html', context)

def terms_of_service(request):
    """Terms of service page view."""
    context = {
        'title': 'Terms of Service',
    }
    return render(request, 'core/terms_of_service.html', context)
