from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ContactForm

# HomeView for homepage
from .models import (
    Hero, InstagramPost, Video,
    PortfolioItem, BookSection,
    Stat, Testimonial
)

class HomeView(TemplateView):
    template_name = 'home.html'
    

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['hero']        = Hero.objects.first()
        ctx['insta_posts'] = InstagramPost.objects.all()
        ctx['videos']      = Video.objects.all()
        ctx['portfolio']   = PortfolioItem.objects.all()
        ctx['booksec']     = BookSection.objects.first()
        ctx['stats']       = Stat.objects.all()
        ctx['testis']      = Testimonial.objects.all()
        return ctx

# AboutView for about page
class AboutView(TemplateView):
    template_name = 'about.html'

# ContactView with form
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    def form_valid(self, form):
        # You can save data or send email here
        form.save()  # Only if your form is linked to a model
        return super().form_valid(form)
    
class VideoView(TemplateView):
    template_name = 'videos-1.html'

class WorkView(TemplateView):
    template_name = 'work.html'        

class BlogView(TemplateView):
    template_name = 'blog.html' 

class BlogDetailsView(TemplateView):
    template_name = 'blog-details.html'     



