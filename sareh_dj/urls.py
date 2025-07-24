
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from main.views import post_comment,HomeView, AboutView, ContactView, VideoView, WorkView, BlogView, PortfolioDetailView, blog_detail
from main import views
from main.admin import custom_admin_site




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'), 
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('videos-1/', VideoView.as_view(), name='videos-1'),
    path('videos-2/', VideoView.as_view(), name='videos-2'),
    path('videos-3/', VideoView.as_view(), name='videos-3'),
    path('video-details/', VideoView.as_view(), name='video-details'),
    path('work/', WorkView.as_view(), name='work'),
    # path('blog/', BlogView.as_view(), name='blog'),
    path('tinymce/', include('tinymce.urls')),
    path('portfolio/<slug:slug>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog-details'),
    path('comment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('admin/', custom_admin_site.urls),






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
