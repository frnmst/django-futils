from django import template
import decimal

register = template.Library()


@register.filter
def filter_primary(self, element):
    return element.filter(is_primary=True).first()


@register.filter
def filter_money_decimal_places(self, money):
    return str(
        money.amount.quantize(decimal.Decimal('.01'),
                              rounding=decimal.ROUND_UP))
