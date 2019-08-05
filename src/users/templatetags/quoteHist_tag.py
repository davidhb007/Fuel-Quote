from django import template
from users.models import *
from users.forms import *
from Fuel_Quote.models import *
from django.contrib.auth.forms import User

register = template.Library()


@register.simple_tag(takes_context=True)
def has_quote_history(context):
    request = context['request']

    quoteList = Quote.objects.filter(
        profileId=Profile.objects.get(id=request.user.id))
    has_quote_history = (len(quoteList) > 0)
    return has_quote_history
