"""Module for project signals."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def cropper(sender, instance, created, **kwargs):
    """Make a square avatar image."""
    if instance.avatar.name != "default_avatar.jpeg":
        with Image.open(instance.avatar) as image:

            if image.width > image.height:
                crop_width_delta = (image.width - image.height) // 2
                crop_data = (crop_width_delta, 0, (crop_width_delta + image.height), image.height)
            else:
                crop_height_delta = (image.height - image.width) // 2
                crop_data = (0, crop_height_delta, image.width, (crop_height_delta + image.width))
            cropped_image = image.crop(crop_data)
            cropped_image.save(instance.avatar.path)
