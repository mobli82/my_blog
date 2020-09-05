from django.db import models
from django.contrib.auth.models import User

from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.profile_img.path)

        if image.height > 120 and image.width > 120:
            size = (120, 120)
            image.thumbnail(size)
            image.save(self.profile_img.path)