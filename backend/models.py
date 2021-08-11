from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Airticle(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    img = models.ImageField(upload_to='AirticleImages')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.title
