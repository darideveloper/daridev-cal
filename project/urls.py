from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import routers
from project.admin import tenant_admin_site
from scheduler.views import EventViewSet, BookingViewSet, BusinessHoursViewSet

# Initialize DRF Router
router = routers.DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"business-hours", BusinessHoursViewSet, basename="business-hours")

urlpatterns = [
    # API Endpoints (Not prefixed by language)
    path("api/", include(router.urls)),
    
    # Language Switcher
    path("i18n/", include("django.conf.urls.i18n")),
]

# Prefixed UI Patterns
urlpatterns += i18n_patterns(
    # Admin Interface
    path("admin/", tenant_admin_site.urls),
    
    # Root Redirect to Admin (Language Aware)
    path("", RedirectView.as_view(pattern_name="admin:index"), name="home-redirect-admin"),
)

# Serve Media Files in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
