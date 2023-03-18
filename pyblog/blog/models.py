from django.db import models
import textwrap
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self) -> str:
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/')
    vip = models.BooleanField(default=False)

    @property
    def intro(self):
        return textwrap.shorten(self.content, width=300, placeholder="...")

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)