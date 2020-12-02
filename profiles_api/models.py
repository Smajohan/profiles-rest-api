from django.db import models

# Standard base classes -> needed, when customizing the default Django user model (see official docs)
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None): # CLI will use this when creating users with the command line tool; pw=None -> if pw not specified -> by default you have to specify a pw in Django!
        """Create a new user profile!"""
        if not email:
            raise ValueError('User must have an email address')

        # Normalize email address -> makes the second half of the email address all lowercase -> standardization!
        email = self.normalize_email(email)
        # Create user model
        user = self.model(email=email, name=name)

        # set password - to encrypth the password -> converted to a hash and not stored as plain text in the db
        user.set_password(password) # part of AbstractBaseUser
        user.save(using=self._db) # Django supports several db's -> see Django mkdocs

        return user

    # Create super user function
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True # part of PermissionsMixin
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True) # email column in the user profile db table; email field with max length 255 characters & unique
    name = models.CharField(max_length=255) # name column
    is_active = models.BooleanField(default=True) # to determine if a user's profile is activated or not -> default set as True -> allows us to deactivate users if we need to
    is_staff = models.BooleanField(default=False) # determines if a user is a staff user -> used to determine if the should have access to the Django admin; by default all users are not staff

    # specifies model manager for the objects -> needed because we need to use the custom user model with the Django CLI -> Django needs to have a custom model manager -> so it knows how to create users
    objects = UserProfileManager() # will contain manager class

    # work with Django admin & Django authentication system
    USERNAME_FIELD= 'email' # overwriting the default username field -> replaced by 'email' field
    REQUIRED_FIELDS = ['name'] # specification of the name by the User is required

    # Django interaction with custom user model
    def get_full_name(self): # self: when defining a function within a class
         """Retrieve full name of user"""
         return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    # Specifiy string representation of the model
    # the item we want to return, when we convert a user object to a string in Python
    def __str__(self):
        """Return string representation of the user"""
        return self.email
