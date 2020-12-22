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
