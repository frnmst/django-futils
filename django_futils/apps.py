from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class DjangoFutilsConfig(AppConfig):
    name = 'django_futils'
    verbose_name = 'django-futils'


class DjangoFutilsDefaultAdminConfig(AdminConfig):
    default_site = 'django_futils.default_admin.MyAdminSite'
