from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from .manager import UserManager

class Customer(AbstractBaseUser,PermissionsMixin):
    username           =   models.CharField(unique=True, null=True, blank=True, max_length=50)
    email              =   models.EmailField(unique=True)
    profile_photo      =   models.ImageField(upload_to='products', null=True, blank=True)
    is_staff           =   models.BooleanField(default=False)
    is_superuser       =   models.BooleanField(default=False)
    is_active          =   models.BooleanField(default=False)
   
    objects = UserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
   
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# class Customer(AbstractBaseUser, PermissionsMixin):
#     name = models.CharField(unique=True, null=True, blank=True, max_length=50)
#     email = models.EmailField(unique=True)
#     is_verified = models.BooleanField(default=False)
#     email_token = models.CharField(max_length=100, null=True, blank=True)
#     profile_photo = models.ImageField(upload_to='products', null=True, blank=True)

#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     is_staff = models.BooleanField(
#         default=False,
#         help_text='Designates whether the user can log into this admin site.'
#     )

#     def __str__(self):
#         return self.email
