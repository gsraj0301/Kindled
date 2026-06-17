from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    channel_name = models.CharField(max_length=255)
    curator_note = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    embed_disabled = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_added']



    def __str__(self):
        return self.title
    
class Suggestion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('added', 'Added'),
        ('not_a_fit', 'Not a Fit'),
    ]
    name = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    youtube_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion by {self.name or 'Anonymous'} - {self.status}"