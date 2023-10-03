from django.contrib.auth.models import AnonymousUser
from django.template import Library

from translators_hub.models import Invites, Roles, ModTranslation, User

register = Library()


@register.inclusion_tag(takes_context=True, filename='translators_hub/nav-bar.html')
def get_nav_bar(context):
    user = context['user']
    if isinstance(user, AnonymousUser):
        return {'button_name': "Авторизоваться", 'login_status': "Войти", 'registration_status': "Регистрация", 'user': user}
    else:
        active_invites = user.target_name.filter(status=None)
        active_projects = user.roles.all()
        return {'button_name': f'{user}', 'login_status': f'{user}', 'registration_status': "Выйти", 'user_logged': user.userprofile,
                'user': user,
                'active_invites': active_invites,
                'active_projects': active_projects
                }


@register.simple_tag()
def get_role_display(role):
    display = Invites(role=role).get_role_display()
    return display
