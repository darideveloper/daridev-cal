from django.contrib import admin
from django.urls import path, include
from django.conf import settings
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
    # Admin Interface
    path("admin/", tenant_admin_site.urls),
    
    # Root Redirect to Admin
    path("", RedirectView.as_view(url="/admin/"), name="home-redirect-admin"),
    
    # API Endpoints
    path("api/", include(router.urls)),
]

# Serve Media Files in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
