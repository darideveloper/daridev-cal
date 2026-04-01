from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from project.admin import public_admin_site

urlpatterns = [
    # Admin Interface
    path("admin/", public_admin_site.urls),
    
    # Root Redirect to Admin
    path("", RedirectView.as_view(url="/admin/"), name="home-redirect-admin"),
]

# Serve Media Files in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
