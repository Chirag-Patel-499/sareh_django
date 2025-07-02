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
    



class Contact(models.Model):
    name    = models.CharField(max_length=100)
    email   = models.EmailField()
    phone   = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


    


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='blogs/')
    author = models.CharField(max_length=100, default="Admin")
    date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", blank=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)

    content = HTMLField(default="""<div class='jo-inner-blog-img jo-blog-details-img'>
<img src='/static/assets/img/fbl5.png' alt='Blog cover'>
</div>
<div class='jo-blog-details-txt'>
<div class='jo-inner-blog-infos'>
<div class='author'>Written by: <span class='name'>Sareh Far</span></div>
<div class='date'>14 March 2024</div>
</div>
<h3 class='jo-inner-blog-title'>Creative Partnerships That Shape the Future</h3>
<p>Over the years, I’ve had the privilege to collaborate with brands that value vision, storytelling, and design. These partnerships go beyond simple promotion — they represent shared values and mutual growth. Here's a glimpse into the creative journey that brings those stories to life.</p>
<p>Every collaboration begins with a story — a mood, a palette, a vibe. Whether it's conceptualizing a shoot or developing visuals for campaigns, I focus on merging brand identity with creative freedom.</p>
<ul>
<li>Launched a wellness product series with immersive lifestyle visuals.</li>
<li>Directed a fashion short for an emerging label featured in Elle India.</li>
<li>Created visual branding campaigns that boosted engagement by 3x.</li>
</ul>
<p>Collaboration is not just about output; it's about chemistry. When the brand and the creator align, magic happens. From ideation to delivery, I ensure the journey is just as meaningful as the result.</p>
<div class='jo-blog-details-inner-imgs'>
<img src='/static/assets/img/fbl6.png' alt='Creative session'>
<img src='/static/assets/img/fbl7.png' alt='Behind the scenes'>
</div>
<p>Behind every reel, every campaign, there’s a lot of brainstorming, experimentation, and care. These images represent more than work — they capture energy, connection, and style.</p>
<blockquote>“I believe authenticity is the strongest brand message. If it feels real, it resonates.”<img src='/static/assets/img/quotation-icon-2.svg' alt='quotation icon' class='quotation-icon'></blockquote>
<p>If you're a brand looking to build a story around values, emotion, and experience — I’m always open to co-creating something impactful.</p>
</div>
<div class='jo-blog-details-actions'>
<div class='tags-wrapper'>
<h4 class='title'>Tags:</h4>
<div class='tags'>
<a href='#'>Creative</a>
<a href='#'>Collaboration</a>
<a href='#'>Branding</a>
</div>
</div>
<div class='share'>
<h4 class='title'>Share:</h4>
<div class='share-options'>
<a href='#'><i class='flaticon-facebook-1'></i></a>
<a href='#'><i class='flaticon-twitter'></i></a>
<a href='#'><i class='flaticon-instagram-2'></i></a>
</div>
</div>
</div>""")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug
    
    
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    # models.py

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_reply(self):
        return self.parent is not None
    
    def __str__(self):
        return self.name

    


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

    def __str__(self):
        return self.permalink

class Video(models.Model):
    youtube_id = models.CharField(max_length=300)

    def __str__(self):
        return self.youtube_id


class PortfolioItem(models.Model):
    image = models.ImageField(upload_to="portfolio/")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    typed1 = models.CharField(max_length=50)
    typed2 = models.CharField(max_length=50)
    typed3 = models.CharField(max_length=50)
    content = HTMLField(default="""
        <div class=\"jo-blog-details\">
            <div class=\"jo-inner-blog-img jo-blog-details-img\">
                <img src=\"/static/assets/img/fbl5.png\" alt=\"\">
            </div>
            <div class=\"jo-blog-details-txt\">
                <div class=\"jo-inner-blog-infos\">
                    <div class=\"author\">Written by: <span class=\"name\">Marry biden</span></div>
                    <div class=\"date\">14/03/2024</div>
                </div>
                <h3 class=\"jo-inner-blog-title\"><a href=\"#\">Life won's one Beast air Over above all</a></h3>
                <p class=\"jo-inner-blog-descr\">Consectetur adipisicing elit...<br><br>Vivamus condimentum a sem nec vehicula...</p>
                <ul>
                    <li>Technology Support Allows Erie non-profit to Serve.</li>
                    <li>Web design done Delightful Visualization</li>
                    <li>Software Makes Your Profit Double if You Scale Properly.</li>
                </ul>
                <div class=\"jo-blog-details-inner-imgs\">
                    <img src=\"/static/assets/img/fbl6.png\" alt=\"Inner Image\">
                    <img src=\"/static/assets/img/fbl7.png\" alt=\"Inner Image\">
                </div>
                <blockquote>Pellentesque sollicitudin congue dolor...<img src=\"/static/assets/img/quotation-icon-2.svg\" class=\"quotation-icon\"></blockquote>
            </div>
            <div class=\"jo-blog-details-actions\">
                <div class=\"tags-wrapper\">
                    <h4 class=\"title\">Tags:</h4>
                    <div class=\"tags\">
                        <a href=\"#\">My Profile</a>
                        <a href=\"https://www.amazon.in/dp/9370925740\">My Book</a>
                        <a href=\"https://sarehfar.com/contact/\">Contact me</a>
                    </div>
                </div>
                <div class=\"share\">
                    <h4 class=\"title\">Share:</h4>
                    <div class=\"share-options\">
                        <a href=\"#\"><i class=\"flaticon-facebook-1\"></i></a>
                        <a href=\"#\"><i class=\"flaticon-twitter\"></i></a>
                        <a href=\"#\"><i class=\"flaticon-social-media\"></i></a>
                        <a href=\"#\"><i class=\"flaticon-youtube-1\"></i></a>
                    </div>
                </div>
            </div>
        </div>
    """)

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