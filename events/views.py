from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages
from .models import Event, EventCategory, EventRegistration
from .forms import EventRegistrationForm
from core.models import SiteSettings

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        else:
            # Default to showing upcoming and ongoing events
            queryset = queryset.filter(status__in=['upcoming', 'ongoing'])
        
        # Order by start date (upcoming first)
        return queryset.order_by('start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['categories'] = EventCategory.objects.annotate(event_count=Count('events'))
        
        # Get featured events
        context['featured_events'] = Event.objects.filter(is_featured=True, status__in=['upcoming', 'ongoing']).order_by('start_date')[:3]
        
        # Get filter parameters
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_status'] = self.request.GET.get('status', '')
        
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['categories'] = EventCategory.objects.annotate(event_count=Count('events'))
        
        # Get related events (same category)
        event_categories = self.object.categories.all()
        related_events = Event.objects.filter(categories__in=event_categories).exclude(id=self.object.id).distinct()
        context['related_events'] = related_events.order_by('start_date')[:3]
        
        # Registration form
        context['registration_form'] = EventRegistrationForm()
        
        # Check if registration is still open
        now = timezone.now()
        if self.object.registration_deadline and now > self.object.registration_deadline:
            context['registration_closed'] = True
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = EventRegistrationForm(request.POST)
        
        # Check if registration is still open
        now = timezone.now()
        if self.object.registration_deadline and now > self.object.registration_deadline:
            messages.error(request, "Registration for this event has closed.")
            return redirect('events:event_detail', slug=self.object.slug)
        
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = self.object
            registration.save()
            # Redirect to thank you page instead of the event detail page
            return redirect('events:registration_thank_you', event_slug=self.object.slug)
        
        context = self.get_context_data(object=self.object)
        context['registration_form'] = form
        return render(request, self.template_name, context)

# Add the new thank you page view
class RegistrationThankYouView(TemplateView):
    template_name = 'events/registration_thank_you.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        event_slug = self.kwargs.get('event_slug')
        context['event'] = get_object_or_404(Event, slug=event_slug)
        return context

class EventCategoryView(ListView):
    template_name = 'events/event_category.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(EventCategory, slug=self.kwargs['slug'])
        return Event.objects.filter(categories=self.category).order_by('start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['categories'] = EventCategory.objects.annotate(event_count=Count('events'))
        context['category'] = self.category
        return context
