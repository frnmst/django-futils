from django import template
import decimal
import urllib
import pathlib

register = template.Library()


@register.filter
def filter_primary(self, element):
    return element.filter(is_primary=True).first()


@register.filter
def filter_money_decimal_places(self, money):
    return str(
        money.amount.quantize(decimal.Decimal('.01'),
                              rounding=decimal.ROUND_UP))


@register.filter
def filter_url_last_path_component(self, element):
    return pathlib.Path(urllib.parse.urlsplit(element).path).name


# Got directly from the source code but
# modified to work with dicts.
# See
# https://github.com/django/django/blob/5fcfe5361e5b8c9738b1ee4c1e9a6f293a7dda40/django/contrib/admin/templatetags/admin_urls.py#L12
@register.filter
def admin_urlname_as_dict(value: dict, arg):
    return 'admin:%s_%s_%s' % (value['app_label'], value['model_name'], arg)
