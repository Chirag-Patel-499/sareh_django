from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Hero, Testimonial, PortfolioItem
import os

# Generic function to delete image files
def delete_file_if_exists(file_field):
    if file_field and os.path.isfile(file_field.path):
        file_field.delete(save=False)

def delete_empty_folders(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            for item in os.listdir(path):
                delete_empty_folders(os.path.join(path, item))
            if not os.listdir(path):
                os.rmdir(path)


@receiver(post_delete, sender=Hero)
def delete_hero_images(sender, instance, **kwargs):
    delete_file_if_exists(instance.desktop_img)
    delete_file_if_exists(instance.mobile_img)

@receiver(post_delete, sender=Testimonial)
def delete_testimonial_avatar(sender, instance, **kwargs):
    delete_file_if_exists(instance.avatar)

@receiver(post_delete, sender=PortfolioItem)
def delete_portfolio_image(sender, instance, **kwargs):
    delete_file_if_exists(instance.image)

