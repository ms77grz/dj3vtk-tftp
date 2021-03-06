from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                    args=[self.publish.year,
    #                          self.publish.month,
    #                          self.publish.day, self.slug])

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                    kwargs={'year': self.publish.year,
    #                           'month': self.publish.month,
    #                           'day': self.publish.day,
    #                           'slug': self.slug})

    def get_absolute_url(self):
        kwargs={
            'pk': self.pk,
            'slug': self.slug,
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day,
        }
        return reverse('blog:post_detail', kwargs=kwargs)

    # auto generate slug
    def save(self, *args, **kwargs):
        title = self.title
        self.slug = slugify(title, allow_unicode=True)
        super().save(*args, **kwargs)
