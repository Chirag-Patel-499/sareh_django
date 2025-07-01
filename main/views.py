from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.views.generic.detail import DetailView
from .models import PortfolioItem

from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Blog, Tag, Category, Comment
from .forms import CommentForm
from django.db.models import Q

# HomeView for homepage
from .models import (
    Hero, InstagramPost, Video,
    PortfolioItem, BookSection,
    Stat, Testimonial
)

class HomeView(TemplateView):
    # template_name = 'edited_chi_final_rajil copy.html'
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

class PortfolioDetailView(DetailView):
    model = PortfolioItem
    # template_name = 'portfolio_detail.html'
    template_name = 'blog-details_2.html'
    context_object_name = 'item'



def blog_list(request):
    query = request.GET.get('search')
    tag = request.GET.get('tag')
    category = request.GET.get('category')

    blogs = Blog.objects.all()

    if query:
        blogs = blogs.filter(Q(title__icontains=query) | Q(content__icontains=query))

    if tag:
        blogs = blogs.filter(tags__name=tag)

    if category:
        blogs = blogs.filter(category__name=category)

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,
        'tags': Tag.objects.all(),
        'categories': Category.objects.all(),
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, slug):

    blog = get_object_or_404(Blog, slug=slug)
    

    return render(request, 'blog-details.html', {'blog': blog,'tags': Tag.objects.all(),
    'categories': Category.objects.all(), 'blogs' : Blog.objects.all(),})




def post_comment(request, post_id):
    blog = get_object_or_404(Blog, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent = Comment.objects.filter(id=parent_id).first() if parent_id else None

            comment = form.save(commit=False)
            comment.blog = blog
            comment.parent = parent  # Support replies
            comment.save()

    return redirect('blog-details', slug=blog.slug)
