from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField('Permission', related_name='roles', blank=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.codename


class Users(AbstractUser):
    profile_image = models.IntegerField(null=True, blank=True)
    profile_image_crop_positions = models.TextField(null=True, blank=True)
    profile_image_thumbnail = models.TextField(null=True, blank=True)
    password_token = models.TextField(null=True, blank=True)
    profile_pic = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    username = None
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_password_change = models.DateTimeField(null=True, blank=True)

    
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name="Admin",  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="add_user",  
        blank=True,
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            old_user = Users.objects.get(pk=self.pk)
            if old_user.password != self.password:
                self.last_password_change = timezone.now()
        
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        return super().save(*args, **kwargs)

    def has_permission(self, codename):
        role_permissions = {
            perm.codename for perm in self.role.permissions.all()
        } if self.role else set()
        user_permissions = {perm.codename for perm in self.user_permissions.all()}
        return codename in role_permissions or codename in user_permissions
