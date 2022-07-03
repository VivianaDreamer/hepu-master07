# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from design.urls import design_patterns
from pages.urls import pages_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin route
    path('admin/', admin.site.urls),
    # Auth routes - login / register
    path("", include("apps.authentication.urls")),
    # Design routes
    path("design/", include(design_patterns)),
    # Pages paths
    path("terms/", include(pages_patterns)),
    # UI Kits Html files
    path("", include("apps.home.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    pass
else:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error handlers
handler403 = "apps.home.views.error_403"
handler404 = "apps.home.views.error_404"
handler500 = "apps.home.views.error_500"