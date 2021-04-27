from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Overriding the BaseUserManager to ask for email and password rather the
    default username & password during-
    user/superuser creation.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.Also
        sets default permissions to the superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Creating a custom User class MyUser that subclasses AbstractUser,
    extending the default fields and
    setting the new unique identifier for the user model to 'email'.
    """
    username = None
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)

    date_of_birth = models.DateField(null=True, default=None, blank=True)
    image = models.ImageField(
        null=True, upload_to='profile_pics', blank=True)
    nickname = models.CharField(max_length=200, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def image_tag(self):
        """
        A method to display the user image on the admin list_display.
        """
        if self.image:
            return format_html('<img src="{}" width="100px" height="100px" />'.
                               format(self.image.url))

    image_tag.allow_tags = True
    image_tag.short_description = 'Image'
