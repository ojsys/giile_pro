from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.db.models import Count, Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Talent, TalentCategory, Skill, BookingRequest, PortfolioItem, Testimonial
from .forms import BookingRequestForm, TalentProfileForm, PortfolioItemForm, TestimonialForm, AvailabilityForm
from core.models import SiteSettings

class TalentListView(ListView):
    model = Talent
    template_name = 'talent/talent_list.html'
    context_object_name = 'talents'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Talent.objects.filter(status__in=['active', 'featured'])
        
        # Filter by category if provided
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Filter by skill if provided
        skill_slug = self.request.GET.get('skill')
        if skill_slug:
            queryset = queryset.filter(skills__slug=skill_slug)
        
        # Search query
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(short_bio__icontains=search_query) |
                Q(categories__name__icontains=search_query) |
                Q(skills__name__icontains=search_query)
            ).distinct()
        
        # Sort options
        sort_by = self.request.GET.get('sort', 'featured')
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'experience':
            queryset = queryset.order_by('-years_of_experience')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:  # Default: featured first
            queryset = queryset.order_by('-is_featured', 'name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['categories'] = TalentCategory.objects.annotate(talent_count=Count('talents'))
        context['skills'] = Skill.objects.annotate(talent_count=Count('talents')).order_by('-talent_count')[:20]
        
        # Get featured talents
        context['featured_talents'] = Talent.objects.filter(is_featured=True, status__in=['active', 'featured']).order_by('?')[:4]
        
        # Get filter parameters
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_skill'] = self.request.GET.get('skill', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['sort_by'] = self.request.GET.get('sort', 'featured')
        
        return context

class TalentDetailView(DetailView):
    model = Talent
    template_name = 'talent/talent_detail.html'
    context_object_name = 'talent'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        
        # Get portfolio items
        context['portfolio_items'] = self.object.portfolio_items.all().order_by('order')
        
        # Get testimonials
        context['testimonials'] = self.object.testimonials.all().order_by('-date')
        
        # Booking form
        context['booking_form'] = BookingRequestForm()
        
        # Similar talents (same categories)
        talent_categories = self.object.categories.all()
        similar_talents = Talent.objects.filter(
            categories__in=talent_categories,
            status__in=['active', 'featured']
        ).exclude(id=self.object.id).distinct()
        context['similar_talents'] = similar_talents.order_by('?')[:3]
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = BookingRequestForm(request.POST)
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.talent = self.object
            booking.status = 'pending'
            booking.save()
            messages.success(request, "Your booking request has been submitted successfully!")
            return redirect('talent:booking_thank_you', talent_slug=self.object.slug)
        
        context = self.get_context_data(object=self.object)
        context['booking_form'] = form
        return render(request, self.template_name, context)

class TalentCategoryView(ListView):
    template_name = 'talent/talent_category.html'
    context_object_name = 'talents'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(TalentCategory, slug=self.kwargs['slug'])
        return Talent.objects.filter(
            categories=self.category,
            status__in=['active', 'featured']
        ).order_by('-is_featured', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['categories'] = TalentCategory.objects.annotate(talent_count=Count('talents'))
        context['category'] = self.category
        return context

class TalentSkillView(ListView):
    template_name = 'talent/talent_skill.html'
    context_object_name = 'talents'
    paginate_by = 12
    
    def get_queryset(self):
        self.skill = get_object_or_404(Skill, slug=self.kwargs['slug'])
        return Talent.objects.filter(
            skills=self.skill,
            status__in=['active', 'featured']
        ).order_by('-is_featured', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['skills'] = Skill.objects.annotate(talent_count=Count('talents')).order_by('-talent_count')[:20]
        context['skill'] = self.skill
        return context

class BookingThankYouView(TemplateView):
    template_name = 'talent/booking_thank_you.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        talent_slug = self.kwargs.get('talent_slug')
        context['talent'] = get_object_or_404(Talent, slug=talent_slug)
        return context

class TalentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'talent/talent_dashboard.html'
    
    def get(self, request, *args, **kwargs):
        # Check if user has a talent profile
        try:
            talent = Talent.objects.get(user=self.request.user)
        except Talent.DoesNotExist:
            messages.warning(self.request, "You don't have a talent profile yet. Please create one.")
            return redirect('talent:talent_profile_create')
        
        # If talent exists, proceed with normal template view behavior
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        
        # Get the talent profile for the current user
        talent = Talent.objects.get(user=self.request.user)
        context['talent'] = talent
        
        # Get booking requests
        context['pending_bookings'] = BookingRequest.objects.filter(
            talent=talent, 
            status='pending'
        ).order_by('-created_at')
        
        context['confirmed_bookings'] = BookingRequest.objects.filter(
            talent=talent, 
            status='confirmed'
        ).order_by('start_date')
        
        context['completed_bookings'] = BookingRequest.objects.filter(
            talent=talent, 
            status='completed'
        ).count()
        
        # Get portfolio items
        context['portfolio_items'] = PortfolioItem.objects.filter(
            talent=talent
        ).order_by('order')
        
        # Get testimonials
        context['testimonials'] = Testimonial.objects.filter(
            talent=talent
        ).order_by('-date')
        
        # Profile stats
        context['profile_views'] = talent.view_count
        
        # Calculate profile completion percentage
        completion_fields = [
            talent.name, talent.short_bio, talent.biography, 
            talent.profile_image, talent.years_of_experience,
            talent.categories.exists(), talent.skills.exists()
        ]
        completed_fields = sum(1 for field in completion_fields if field)
        context['profile_completion'] = int((completed_fields / len(completion_fields)) * 100)
        
        return context

class TalentProfileCreateView(LoginRequiredMixin, CreateView):
    model = Talent
    form_class = TalentProfileForm
    template_name = 'talent/talent_profile_form.html'
    success_url = reverse_lazy('talent:talent_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['is_create'] = True
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'pending'
        messages.success(self.request, "Your talent profile has been created and is pending approval.")
        return super().form_valid(form)

class TalentProfileEditView(LoginRequiredMixin, UpdateView):
    model = Talent
    form_class = TalentProfileForm
    template_name = 'talent/talent_profile_form.html'
    success_url = reverse_lazy('talent:talent_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['is_create'] = False
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(Talent, user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Your talent profile has been updated successfully.")
        return super().form_valid(form)

class PortfolioItemCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'talent/portfolio_item_form.html'
    success_url = reverse_lazy('talent:talent_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['is_create'] = True
        return context
    
    def form_valid(self, form):
        talent = get_object_or_404(Talent, user=self.request.user)
        form.instance.talent = talent
        messages.success(self.request, "Portfolio item has been added successfully.")
        return super().form_valid(form)

class PortfolioItemEditView(LoginRequiredMixin, UpdateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = 'talent/portfolio_item_form.html'
    success_url = reverse_lazy('talent:talent_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['is_create'] = False
        return context
    
    def get_queryset(self):
        talent = get_object_or_404(Talent, user=self.request.user)
        return PortfolioItem.objects.filter(talent=talent)
    
    def form_valid(self, form):
        messages.success(self.request, "Portfolio item has been updated successfully.")
        return super().form_valid(form)

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = BookingRequest
    template_name = 'talent/booking_detail.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        talent = get_object_or_404(Talent, user=self.request.user)
        return BookingRequest.objects.filter(talent=talent)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        return context

class BookingAcceptView(LoginRequiredMixin, UpdateView):
    model = BookingRequest
    fields = []
    http_method_names = ['post']
    
    def get_queryset(self):
        talent = get_object_or_404(Talent, user=self.request.user)
        return BookingRequest.objects.filter(talent=talent, status='pending')
    
    def form_valid(self, form):
        booking = self.object
        booking.status = 'confirmed'
        booking.save()
        messages.success(self.request, f"Booking for '{booking.project_title}' has been accepted.")
        return redirect('talent:talent_dashboard')

class BookingDeclineView(LoginRequiredMixin, UpdateView):
    model = BookingRequest
    fields = []
    http_method_names = ['post']
    
    def get_queryset(self):
        talent = get_object_or_404(Talent, user=self.request.user)
        return BookingRequest.objects.filter(talent=talent, status='pending')
    
    def form_valid(self, form):
        booking = self.object
        booking.status = 'declined'
        booking.save()
        messages.success(self.request, f"Booking for '{booking.project_title}' has been declined.")
        return redirect('talent:talent_dashboard')
