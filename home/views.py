from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
from .models import (
    Restaurant, Feedback, RestaurantConfig, MenuItem,
    RestaurantLocation, ContactSubmission, AboutContent
)
from .forms import FeedbackForm, ContactForm
from .serializers import MenuItemSerializer
from django.utils import timezone

logger = logging.getLogger(__name__)


def _get_restaurant_instance():
    """Return the main Restaurant instance (create default if missing)."""
    try:
        restaurant = Restaurant.objects.first()
        if not restaurant:
            restaurant = Restaurant.objects.create(
                name=getattr(settings, "RESTAURANT_NAME", "Gourmet Delight"),
                description=getattr(settings, "RESTAURANT_DESCRIPTION", "Welcome to our restaurant!"),
                phone=getattr(settings, "RESTAURANT_PHONE", "+1 (555) 123-4567"),
            )
        return restaurant
    except Exception as e:
        logger.exception("Failed to get/create Restaurant instance: %s", e)
        return None


def _base_context():
    """Common context used by several templates."""
    restaurant = _get_restaurant_instance()
    restaurant_config = RestaurantConfig.objects.first()
    restaurant_location = RestaurantLocation.objects.first()
    return {
        "restaurant": restaurant,
        "restaurant_config": restaurant_config,
        "restaurant_location": restaurant_location,
        "opening_hours": {
            "weekdays": getattr(settings, "RESTAURANT_HOURS", {}).get("weekdays", "Mon - Fri: 11:00 AM - 9:00 PM"),
            "weekend": getattr(settings, "RESTAURANT_HOURS", {}).get("weekend", "Sat - Sun: 10:00 AM - 10:00 PM"),
        },
        "current_year": timezone.now().year,
    }


def home_view(request):
    """
    Home page. Handles optional contact form POST and renders the home template.
    """
    context = _base_context()

    # Contact form handling
    if request.method == "POST" and "contact_submit" in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message! We will get back to you soon.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    context.update({
        "form": form,
    })
    return render(request, "home/home.html", context)


def contact_view(request):
    """
    Dedicated contact page using the same ContactForm logic as the homepage.
    """
    context = _base_context()
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thank you for your message! We will get back to you soon.")
        return redirect("contact")
    elif request.method == "POST":
        messages.error(request, "Please correct the errors below.")

    context.update({"form": form})
    return render(request, "home/contact.html", context)


def about_view(request):
    """
    About page: use active AboutContent if present, otherwise fall back to a default.
    """
    about = AboutContent.objects.filter(is_active=True).first()
    if not about:
        # Keep a safe fallback instance (don't crash if DB missing)
        about = AboutContent(
            title="About Gourmet Delight",
            mission="To provide exceptional dining experiences through authentic cuisine and warm hospitality.",
            history="Founded in 2010, Gourmet Delight has been serving the community with passion and dedication for over a decade."
        )

    context = _base_context()
    context.update({
        "about": about,
    })
    return render(request, "home/about.html", context)


def custom_404(request, exception):
    """Custom 404 handler"""
    ctx = _base_context()
    return render(request, "home/404.html", ctx, status=404)


def menu_view(request):
    """
    Render menu grouped by category from DB (MenuItem model).
    """
    try:
        menu_items = MenuItem.objects.filter(is_available=True).order_by("category", "name")
        menu_by_category = {}
        for item in menu_items:
            menu_by_category.setdefault(item.category, []).append(item)

        context = _base_context()
        context.update({
            "menu_items": menu_items,
            "menu_by_category": menu_by_category,
        })
        return render(request, "home/menu.html", context)
    except Exception as e:
        logger.exception("Error in menu_view: %s", e)
        return render(request, "home/error.html", {
            "error_message": "Unable to load menu at the moment. Please try again later."
        }, status=500)


def reservations_view(request):
    """Placeholder for reservations page"""
    context = _base_context()
    return render(request, "home/reservations.html", context)


def feedback_view(request):
    """Feedback form view"""
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect("feedback")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeedbackForm()

    context = _base_context()
    context.update({"form": form})
    return render(request, "home/feedback.html", context)


def search_view(request):
    """Simple search placeholder"""
    query = request.GET.get("q", "").strip()
    context = _base_context()
    context.update({
        "query": query,
        "results": [],  # future: run a query over MenuItem, Restaurant, etc.
    })
    return render(request, "home/search.html", context)


@api_view(["GET"])
def menu_api_view(request):
    """
    API endpoint to return serialized MenuItem model instances (DB-backed).
    Use query params ?category=&vegetarian=true|false
    """
    qs = MenuItem.objects.filter(is_available=True)
    category = request.GET.get("category")
    vegetarian = request.GET.get("vegetarian")
    if category:
        qs = qs.filter(category__iexact=category)
    if vegetarian is not None:
        veg_flag = vegetarian.lower() in ("1", "true", "yes")
        qs = qs.filter(is_vegetarian=veg_flag)

    serializer = MenuItemSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
