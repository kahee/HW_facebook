from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


# Create your models here.
class User(AbstractUser):
    # 이름. 메일주소, 비밀번호, 비밀번호 확인,  프로필 이미지(페이스북 로그인시)
    email = models.EmailField(
        verbose_name='이메일주소',
        max_length=255,
        unique=True,
    )

    img_profile = models.ImageField(
        verbose_name='프로필 사진',
        upload_to='user',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
