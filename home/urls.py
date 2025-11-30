from django.urls import path
from django.http import HttpResponseNotFound
from . import views

def make_view(name):
    """
    Return the view callable if present in views module,
    otherwise return a simple 404-returning view so Django doesn't crash.
    """
    view = getattr(views, name, None)
    if view is None:
        def _missing(request, *args, **kwargs):
            return HttpResponseNotFound(f"View '{name}' is not implemented.")
        return _missing
    return view

urlpatterns = [
    path('', make_view('home_view'), name='home'),
    path('about/', make_view('about_view'), name='about'),
    path('menu/', make_view('menu_view'), name='menu'),
    path('contact/', make_view('contact_view'), name='contact'),
    path('reservations/', make_view('reservations_view'), name='reservations'),
    path('feedback/', make_view('feedback_view'), name='feedback'),
    path('search/', make_view('search_view'), name='search'),
    # API endpoints
    path('api/menu/', make_view('menu_api_view'), name='menu-api'),
]
