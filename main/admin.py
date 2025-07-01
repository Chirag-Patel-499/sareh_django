from django.contrib import admin, messages
from .models import Hero, InstagramPost, Video, PortfolioItem, BookSection, Stat, Testimonial, Blog, Tag, Category


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
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Category)
