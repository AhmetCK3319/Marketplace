from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.fields.related import OneToOneField, ForeignKey
from django.utils.safestring import mark_safe


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password=None):

        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    VENDOR=1
    CUSTOMER=2
    ROLE_CHOICES = (
        (VENDOR,'vendor'),
        (CUSTOMER,'customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=20,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,blank=True,null=True)

    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'vendor'
        elif self.role == 2:
            user_role = 'customer'
        return user_role
    

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='users/profile_picture',blank=True,null=True)
    cover_picture = models.ImageField(upload_to='users/cover_picture',blank=True,null=True)
    address_line1 = models.CharField(max_length=50,blank=True)
    address_line2 = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=15,blank=True)
    state = models.CharField(max_length=15,blank=True)
    country = models.CharField(max_length=15,blank=True)
    pin_code = models.CharField(max_length=6,blank=True)
    latitude = models.CharField(max_length=20,blank=True)
    longitude = models.CharField(max_length=20,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
    
    def image_tag(self):
        if self.profile_picture:
            return mark_safe(f'<img src="{self.profile_picture.url}" height="50"/>')
        else:
            return ""
    image_tag.short_description = 'Image'

    def image_tag2(self):
        if self.cover_picture:
            return mark_safe(f'<img src="{self.cover_picture.url}" height="50"/>')
        else:
            return ""
    image_tag.short_description = 'Image'    