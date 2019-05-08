from django.db import models
from django.conf import settings
# from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='defaul.jpg', upload_to='profile_pictures')
    bio = models.TextField(max_length=500, blank=True, default='Update your bio')
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
