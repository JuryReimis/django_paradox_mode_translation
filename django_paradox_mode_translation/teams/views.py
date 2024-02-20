from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from teams.forms import InviteUserForm
from teams.models import Teams, TeamInvites
from translators_hub.models import User


class TeamsView(generic.ListView):
    template_name = 'teams/home.html'
    context_object_name = 'teams'

    def get_queryset(self):
        teams = self.request.user.membership.all()
        queryset = Teams.objects.filter(team_members__in=teams).prefetch_related('team_members')
        return queryset
    
    def get(self, request, *args, **kwargs):
        return super(TeamsView, self).get(request, *args, **kwargs)


class TeamPageView(generic.DetailView):
    model = Teams
    template_name = 'teams/team_page.html'
    context_object_name = 'team_data'

    def get_object(self, queryset=None):
        obj = self.model.objects.filter(slug=self.kwargs.get('slug')).prefetch_related('team_members__user')[0]
        return obj

    def get(self, request, *args, **kwargs):
        return super(TeamPageView, self).get(request, *args, **kwargs)


class SendInviteView(generic.ListView):
    template_name = 'teams/invite_user.html'
    context_object_name = 'free_users'

    def get_queryset(self):
        team = Teams.objects.get(slug=self.kwargs.get('slug'))
        free_users = User.objects.exclude(Q(membership__team=team) | Q(team_target_name__status=TeamInvites.NO_RESPONSE))
        return free_users

    def get(self, request, *args, **kwargs):
        form = InviteUserForm()
        self.extra_context = {'form': form, 'slug':kwargs.get('slug')}
        return super(SendInviteView, self).get(request, *args, **kwargs)

    def post(self, request, slug, *args, **kwargs):
        form = InviteUserForm(request.POST)
        data = form.save(commit=False)
        data.sender = request.user
        data.target_id = request.POST.get('target_user_id')
        data.team = Teams.objects.get(slug=slug)
        data.status = TeamInvites.NO_RESPONSE
        data.save()
        form.save_m2m()
        return redirect(reverse('teams:invite_user', kwargs={'slug': slug}))
