import email
from typing import Dict, List

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import AppUser, TrackedItem
from .forms import AddTrackedItem
from .forms import RegistrationForm


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """Class based view to delete an item from the watch list
    """
    
    model = TrackedItem
    template_name: str = "items/confirm_del.html"
    success_url = reverse_lazy('items.dashboard')
    login_url = reverse_lazy('items.dashboard')


def register_view(request):
    """View that renders and processes the registration page
    """
    
    if request.user.is_authenticated:
        return redirect('items.dashboard')
    else:
        context =  {}
        form: RegistrationForm = RegistrationForm(request.POST or None)
        if request.POST:
            if form.is_valid():
                form.save()
                email: str = form.cleaned_data.get("email")
                password: str = form.cleaned_data.get("password1")
                messages.success(
                    request=request,
                    message=(
                        f"{form.cleaned_data.get('full_name')}, "
                        "votre compte a été créé !"
                    )
                )
                return redirect('items.login')
            else:
                context["form"] = form
        else:
            context["form"] = form
        
        return render(request, 'items/register.html', context)


def login_view(request):
    """View function that renders and proccesses the login page
    """
    if request.user.is_authenticated:
        return redirect('items.dashboard')
    else:
        context: Dict = {}
        if request.POST:
            email: str = request.POST.get('email')
            password: str = request.POST.get('password')
            user: AppUser = authenticate(request=request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('items.dashboard')
            else:
                messages.error(request, "Email ou mot de passe incorrect")
    
        return render(request, 'items/login.html', context)


@login_required(login_url='items.login')
def logout_view(request):
    """View function to logout a logged in user
    """
    
    logout(request)
    return redirect('items.login')
    

@login_required(login_url='items.login')
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
            error = "Echec de l'extraction des données du produit :/"
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


@login_required(login_url='items.login')
def update_prices(request):
    """View to update the prices of the tracked items
    """
    
    query_set: List[TrackedItem] = TrackedItem.objects.all() # pylint: disable=no-member
    for item in query_set:
        item.save()
    return redirect('items.dashboard')
