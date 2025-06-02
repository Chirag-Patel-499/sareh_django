from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ContactForm

# HomeView for homepage
class HomeView(TemplateView):
    template_name = 'rajil.html'

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



