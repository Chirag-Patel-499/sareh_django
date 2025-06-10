from django.db import models

class Hero(models.Model):
    title        = models.CharField(max_length=200, default="Hi, I’m Sareeh Far")
    subtitle     = models.CharField(max_length=300, blank=True, default="Actress. Author. Dancer.")
    btn_text     = models.CharField(max_length=50, default="Explore ↓")
    desktop_img  = models.ImageField(upload_to="hero/", blank=True)
    mobile_img   = models.ImageField(upload_to="hero/", blank=True)

    def _str_(self):
        return "Hero Section"

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

    def _str_(self):
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