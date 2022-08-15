from typing import Dict, List

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import TrackedItem
from .forms import AddTrackedItem


def dashboard_view(request):
    """View that render the dashboard of the user, displays the tracked items
    """

    error: str = None
    
    form = AddTrackedItem(request.POST or None)
    
    if request.method == "POST":
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "Echec lors de l'extraction des données du produit :/"
        except: # pylint: disable=bare-except
            error = "Un problème inattendu est survenu"

    form = AddTrackedItem()

    query_set: List[TrackedItem] = TrackedItem.objects.all() # pylint: disable=no-member
    no_tracked_items = query_set.count()
    
    discounted_items: List[TrackedItem] = list(
        item for item in query_set
        if item.current_price <= item.target_price
    )
    no_discounted_items: int = len(discounted_items)
    
    context: Dict = {
        "query_set": query_set,
        "no_tracked_items": no_tracked_items,
        "no_discounted_items": no_discounted_items,
        "form": form,
        "error": error
    }
    
    return render(request, 'items/dashboard.html', context)


def update_prices(request):
    """View to update the prices of the tracked items
    """
    
    query_set: List[TrackedItem] = TrackedItem.objects.all() # pylint: disable=no-member
    for item in query_set:
        item.save()
    return redirect('items.dashboard')


class ItemDeleteView(DeleteView):
    """Class based view to delete an item from the watch list
    """
    
    model = TrackedItem
    template_name: str = "items/confirm_del.html"
    success_url = reverse_lazy('items.dashboard')