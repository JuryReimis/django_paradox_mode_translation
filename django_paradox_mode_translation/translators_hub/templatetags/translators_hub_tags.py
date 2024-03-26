from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, Case, When, Value, IntegerField, CharField
from django.template import Library

from translators_hub.models import Invites, ProfileComments, UserProfile, Translation, ProjectComments
from translators_hub.utils.custom_paginator import CustomPaginator

register = Library()


@register.inclusion_tag(takes_context=True, filename='translators_hub/nav-bar.html')
def get_nav_bar(context):
    user = context['user']
    if isinstance(user, AnonymousUser):
        return {'button_name': "Авторизоваться", 'login_status': "Войти", 'registration_status': "Регистрация",
                'user': user}
    else:
        active_invites = user.target_name.filter(status=None)
        active_team_invites = user.team_target_name.filter(status='no_resp')
        active_projects = user.roles.all()
        return {'button_name': f'{user}', 'login_status': f'{user}', 'registration_status': "Выйти",
                'user_logged': user.userprofile,
                'user': user,
                'active_invites': active_invites,
                'active_team_invites': active_team_invites,
                'active_projects': active_projects
                }


@register.inclusion_tag(filename='translators_hub/pagination.html')
def get_pagination_block(page_obj):
    context = {
        'page_obj': page_obj,
    }
    return context


@register.simple_tag()
def get_role_display(role):
    display = Invites(role=role).get_role_display()
    return display


@register.simple_tag(takes_context=True)
def get_comments(context, target):
    user = context.get('user')
    object_list = []
    if isinstance(target, UserProfile):
        object_list = ProfileComments.objects.filter(target=target, visible=True).select_related('author').annotate(
            likes=Count(
                Case(When(profile_comment_reactions__reaction=True, then=Value(1)), output_field=IntegerField())),
            dislikes=Count(
                Case(When(profile_comment_reactions__reaction=False, then=Value(1)), output_field=IntegerField())),
            like_class=Case(When(profile_comment_reactions__reaction=True, profile_comment_reactions__author=user,
                                 then=Value('btn-success')),
                            default=Value('btn-outline-success'),
                            output_field=CharField()
                            ),
            dislike_class=Case(When(profile_comment_reactions__reaction=False, profile_comment_reactions__author=user,
                                    then=Value('btn-danger')),
                               default=Value('btn-outline-danger'),
                               output_field=CharField()
                               ),
        ).order_by('-pub_date')
    elif isinstance(target, Translation):
        object_list = ProjectComments.objects.filter(target=target, visible=True).select_related('author').annotate(
            likes=Count(
                Case(When(project_comment_reactions__reaction=True, then=Value(1)), output_field=IntegerField())),
            dislikes=Count(
                Case(When(project_comment_reactions__reaction=False, then=Value(1)), output_field=IntegerField())),
            like_class=Case(When(project_comment_reactions__reaction=True, project_comment_reactions__author=user,
                                 then=Value('btn-success')),
                            default=Value('btn-outline-success'),
                            output_field=CharField()
                            ),
            dislike_class=Case(When(project_comment_reactions__reaction=False, project_comment_reactions__author=user,
                                    then=Value('btn-danger')),
                               default=Value('btn-outline-danger'),
                               output_field=CharField()
                               ),
        ).order_by('-pub_date')
    if object_list:
        paginator = CustomPaginator(object_list, per_page=5)
    else:
        paginator = None
    current_page = context.request.GET.get('page', 1)
    page_obj = paginator.get_page(current_page) if paginator else None
    return page_obj
