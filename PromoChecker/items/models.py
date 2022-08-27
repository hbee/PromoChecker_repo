from re import T
from typing import Dict, List
from unicodedata import name

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .utils import get_item_data


class AppUser(AbstractBaseUser):
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
    
    full_name = models.CharField(max_length=48, null=True)
    email = models.EmailField(max_length=32, null=True, unique=True)
    referral_route = models.CharField(
        max_length=12, null=True, blank=True, choices=REFERRAL_ROUTE
    )
    
    USERNAME_FIELD: str = 'email'
    EMAIL_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['email']
    

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

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        item_name, item_price = get_item_data(url=self.url, store=self.store)
        
        if not self.current_price:
            self.initial_price = item_price
        
        self.current_price = item_price
        self.name = item_name
        
        super().save(*args, **kwargs)