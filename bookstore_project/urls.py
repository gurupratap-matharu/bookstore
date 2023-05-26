from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from books.sitemaps import BookSitemap
from pages.sitemaps import StaticViewSitemap

sitemaps = {"books": BookSitemap, "static": StaticViewSitemap}


urlpatterns = [
    path("anything-but-admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("books/", include("books.urls")),
    path("orders/", include("orders.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("pages.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
