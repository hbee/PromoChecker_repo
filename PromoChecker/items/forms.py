from django import forms
from .models import TrackedItem


class AddTrackedItem(forms.ModelForm):
    """class representing the form for adding a product to the tracked items
    """

    class Meta:
        """class helps configuring the AddTrackedItem ModelForm in relation to the TrackedItem model
        """

        model = TrackedItem
        fields = ('url', 'target_price', 'store')