from django import template

register = template.Library()

@register.filter
def mult(dayPrice, NumOfDays):
    return dayPrice * NumOfDays
