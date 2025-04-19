from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.conf import settings  # Import settings instead of User directly

class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, max_length=100)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])

class Tag(models.Model):
    name = models.CharField(_("Tag Name"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, max_length=50)
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:tag', args=[self.slug])

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use AUTH_USER_MODEL instead of User
        on_delete=models.CASCADE, 
        related_name='blog_posts', 
        verbose_name=_("Author")
    )
    featured_image = models.ImageField(_("Featured Image"), upload_to='blog/images/', blank=True, null=True)
    excerpt = models.TextField(_("Excerpt"), help_text=_("A short description of the post"))
    content = RichTextField(_("Content"))
    categories = models.ManyToManyField(Category, related_name='posts', verbose_name=_("Categories"))
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True, verbose_name=_("Tags"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    published_at = models.DateTimeField(_("Published At"), blank=True, null=True)
    status = models.CharField(_("Status"), max_length=10, choices=STATUS_CHOICES, default='draft')
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    @property
    def formatted_date(self):
        """Return a formatted date string for display"""
        if self.published_at:
            return self.published_at.strftime("%B %d, %Y")
        return self.created_at.strftime("%B %d, %Y")

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Post"))
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    content = models.TextField(_("Comment"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=True)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
