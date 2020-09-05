from django.db import models
from django.contrib.auth.models import User

from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()
        size = (120, 120)
        image = Image.open(self.img.path)

        if image.height > 120 and image.width > 120:
            image.thumbnail(size)
            image.save(self.img.path)