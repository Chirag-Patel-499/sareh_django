from django.db import models
from django.db.models.signals import post_delete, pre_save, pre_delete
from django.dispatch import receiver
import os
from tinymce.models import HTMLField
from django.utils.text import slugify



class Hero(models.Model):
    title        = models.CharField(max_length=200, default="Hi, I’m Sareeh Far")
    subtitle     = models.CharField(max_length=300, blank=True, default="Actress. Author. Dancer.")
    btn_text     = models.CharField(max_length=50, default="Explore ↓")
    desktop_img  = models.ImageField(upload_to="hero/", blank=True)
    mobile_img   = models.ImageField(upload_to="hero/", blank=True)

    def __str__(self):
        return "Hero Section"


# --- IMAGE DELETE HELPERS ---

def delete_file_if_exists(file_field):
    if file_field and file_field.name:
        file_path = file_field.path
        if os.path.isfile(file_path):
            file_field.delete(save=False)

# --- SIGNALS ---

@receiver(post_delete, sender=Hero)
def delete_hero_images(sender, instance, **kwargs):
    delete_file_if_exists(instance.desktop_img)
    delete_file_if_exists(instance.mobile_img)

@receiver(pre_save, sender=Hero)
def delete_old_hero_images_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object; nothing to delete

    try:
        old_instance = Hero.objects.get(pk=instance.pk)
    except Hero.DoesNotExist:
        return

    if old_instance.desktop_img and old_instance.desktop_img != instance.desktop_img:
        delete_file_if_exists(old_instance.desktop_img)

    if old_instance.mobile_img and old_instance.mobile_img != instance.mobile_img:
        delete_file_if_exists(old_instance.mobile_img)


class InstagramPost(models.Model):
    permalink = models.URLField()

    def _str_(self):
        return self.permalink

class Video(models.Model):
    youtube_id = models.CharField(max_length=20)

    def _str_(self):
        return self.youtube_id

class PortfolioItem(models.Model):
    image = models.ImageField(upload_to="portfolio/")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    typed1 = models.CharField(max_length=20, blank=True, default="Actress. Author. Dancer.")
    typed2 = models.CharField(max_length=20, blank=True, default="Painting the world with words.")
    typed3 = models.CharField(max_length=20, blank=True, default="Let’s create something magical.")
    content = HTMLField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BookSection(models.Model):
    quote       = models.TextField(default="“Every choice we make shapes our path.”")
    description = models.TextField(default="Dive into decisions, destiny, and self-awareness in my debut book.")
    link        = models.URLField(default="https://www.amazon.in/dp/9370925740")

    def _str_(self):
        return "Book Section"

class Stat(models.Model):
    label = models.CharField(max_length=50)
    value = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.value} {self.label}"

class Testimonial(models.Model):
    avatar   = models.ImageField(upload_to="testimonials/")
    rating   = models.PositiveSmallIntegerField(default=5)  # 1–5
    quote    = models.TextField()
    author   = models.CharField(max_length=100)
    details  = models.TextField(blank=True)

    def _str_(self):
        return f"{self.author} ({self.rating}★)"