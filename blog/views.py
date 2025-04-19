from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import Post, Category, Tag
from .forms import CommentForm
from core.models import SiteSettings

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.annotate(post_count=Count('posts'))
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-published_at')[:5]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.annotate(post_count=Count('posts'))
        context['recent_posts'] = Post.objects.filter(status='published').exclude(id=self.object.id).order_by('-published_at')[:5]
        
        # Comments
        comments = self.object.comments.filter(active=True)
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        
        # Related posts
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        related_posts = Post.objects.filter(status='published', tags__in=post_tags_ids).exclude(id=self.object.id)
        context['related_posts'] = related_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published_at')[:3]
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return self.get(request, *args, **kwargs)
        
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return render(request, self.template_name, context)

class CategoryPostListView(ListView):
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', categories=self.category).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['category'] = self.category
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.annotate(post_count=Count('posts'))
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-published_at')[:5]
        return context

class TagPostListView(ListView):
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', tags=self.tag).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = SiteSettings.get_settings()
        context['tag'] = self.tag
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.annotate(post_count=Count('posts'))
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-published_at')[:5]
        return context
