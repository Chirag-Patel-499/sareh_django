from django.contrib import admin, messages
from .models import PortfolioItem
from tinymce.widgets import TinyMCE
from django import forms
from .models import Hero, InstagramPost, Video, PortfolioItem, BookSection, Stat, Testimonial

# 🔁 Reusable Singleton Admin
class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def save_model(self, request, obj, form, change):
        if not change and self.model.objects.exists():
            messages.error(request, f"🚫 Only one {self.model.__name__} instance is allowed.")
        else:
            super().save_model(request, obj, form, change)



# ✅ Singleton model admins
@admin.register(Hero)
class HeroAdmin(SingletonModelAdmin):
    pass

@admin.register(BookSection)
class BookSectionAdmin(SingletonModelAdmin):
    pass

# ✅ Normal registrations
admin.site.register(InstagramPost)
admin.site.register(Video)
admin.site.register(PortfolioItem)
admin.site.register(Stat)
admin.site.register(Testimonial)



class PortfolioItemForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = PortfolioItem
        fields = '__all__'

class PortfolioItemAdmin(admin.ModelAdmin):
    form = PortfolioItemForm

admin.site.register(PortfolioItem, PortfolioItemAdmin)