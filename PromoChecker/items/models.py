from typing import Dict, List

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .utils import get_item_data


class AppUserManager(BaseUserManager):
    """Custom user manager for the AppUser model
    """
    
    def create_user(self, email, full_name, password=None):
        """Function to create a user account

        Args:
            email (str): email address of the new account
            password (str, optional): password for the new account
        """
        
        if not email:
            raise ValueError(
                "No email provided for account creation"
            )
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None):
        """Function to create a super user account
        """
        
        user = self.create_user(
            self.normalize_email(email),
            full_name,
            password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
        

class AppUser(PermissionsMixin, AbstractBaseUser):
    """Class for the app users profiles

    Attributes:
        full_name (str): name of the user
        email (str): email of the user
        referral_route (str): referral route of the user
    """
    
    REFERRAL_ROUTE: Dict = {
        ('social', 'social'),
        ('search', 'search'),
        ('friends', 'friends'),
        ('other', 'other'),
    }
    
    full_name = models.CharField(verbose_name="full name", max_length=48, null=True)
    email = models.EmailField(verbose_name="email", max_length=48, null=True, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    referral_route = models.CharField(
        max_length=12, null=True, blank=True, choices=REFERRAL_ROUTE
    )
    
    objects = AppUserManager()
    
    USERNAME_FIELD: str = 'email'
    EMAIL_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['full_name']
    
    def __str__(self) -> str:
        return str(self.full_name)
    
    

class TrackedItem(models.Model):
    """Class for the tracked items

    Attributes:
        url (str): link to the item's webpage
        name (str): name of the product
        media_url (str): link to the media asset of the product
        store (str): name of the store website
        initial_price (float): initial price of the product
        current_price (float): current price of the product
        target_price (float): price wanted by the user
        target_discount (integer): discount wanted by the user
        user_notified (boolean): if the user has been notified
        app_user (AppUser): User profile tracking this item
    """
    
    STORE: dict = {
        ('zalando', 'zalando'),
        ('asos', 'asos')
    }
    
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100, null=True, blank=True)
    media_url = models.URLField(max_length=200, blank=True)
    store = models.CharField(
        max_length=12, null=True, blank=True, choices=STORE
    )
    initial_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True
    )
    current_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True
    )
    target_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    target_discount = models.IntegerField(blank=True, null=True)
    user_notified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    app_user = models.ForeignKey(
        AppUser, null=True, on_delete=models.CASCADE, blank=True
    )
    
    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        item_name, item_price = get_item_data(url=self.url, store=self.store)
        
        if not self.current_price:
            self.initial_price = item_price
        
        self.current_price = item_price
        self.name = item_name
        
        super().save(*args, **kwargs)