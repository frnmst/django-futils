from django.contrib import admin
from django.urls import path, re_path, reverse_lazy, include
# See https://overiq.com/django-1-10/handling-media-files-in-django/
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# See https://stackoverflow.com/a/55723121
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
]
