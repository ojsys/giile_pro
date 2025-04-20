from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import AboutPage, SiteSettings, HomePage
from blog.models import Post  
from events.models import Event
from django.utils import timezone

def home_view(request):
    """View for the home page."""
    home = HomePage.get_homepage()
    settings = SiteSettings.get_settings()
    
    # Get related content with safe empty defaults
    services = home.services.all().order_by('order') if hasattr(home, 'services') else []
    now = timezone.now()
    upcoming_events = Event.objects.filter(
            start_date__gte=now,
            status__in=['upcoming', 'ongoing']
        ).order_by('start_date')[:3]
    
    # Get the latest 3 published blog posts
    latest_posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    
    context = {
        'home': home,
        'settings': settings,
        'services': services,
        'events': upcoming_events,
        'latest_posts': latest_posts,  # Add latest posts to context
    }
    return render(request, 'core/home.html', context)

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


