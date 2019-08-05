from django import template
from users.forms import *
from django.contrib.auth.forms import User

register = template.Library()


@register.simple_tag(takes_context=True)
def profile_made(context):
    request = context['request']
    userprof = Profile.objects.filter(
        username=User.objects.get(username=request.user.username))
    profile_made = (len(userprof) > 0)
    return profile_made
