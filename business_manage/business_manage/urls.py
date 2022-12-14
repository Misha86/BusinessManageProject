"""Business_manage URL Configuration.

For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, reverse_format=None):
    """Add links of all lists to API Home page."""
    return Response(
        {
            "specialists": reverse(
                "api:specialists-list-create",
                request=request,
                format=reverse_format,
            ),
            "locations": reverse(
                "api:locations-list-create",
                request=request,
                format=reverse_format,
            ),
            "appointments": reverse(
                "api:appointments-list-create",
                request=request,
                format=reverse_format,
            ),
            "schedules": reverse(
                "api:schedules-list-create",
                request=request,
                format=reverse_format,
            ),
        },
    )


urlpatterns = [
    path("", api_root),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    # path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
