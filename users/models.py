from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse



# Create your models here.
# 拓展默认的user模型
class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True,verbose_name='昵称')
    headshot = models.ImageField(upload_to='avatar/%Y/%m/%d', default='default.jpg',verbose_name='头像')
    signature = models.CharField(max_length=128,verbose_name='个性签名', default='This guy is too lazy to leave anything here!')

    def get_absolute_url(self):
        return reverse('users:edit',kwargs={'pk':self.pk})

    class Meta(AbstractUser.Meta):
        pass
