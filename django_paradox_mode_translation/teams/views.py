from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from teams.forms import InviteUserForm
from teams.models import Teams, TeamInvites, TeamMembers
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


class TeamInvitesHandler(generic.View):

    def post(self, request, *args, **kwargs):
        accepted = request.POST.get('accept')
        declined = request.POST.get('decline')
        if accepted:
            invites = TeamInvites.objects.filter(Q(pk__in=accepted) | Q(pk=accepted))
            for invite in invites:
                member_note = TeamMembers.objects.get_or_create(team=invite.team, user=request.user)[0]
                member_note.save()
                invite.status = TeamInvites.ACCEPTED
                invite.save()
        elif declined:
            invites = TeamInvites.objects.filter(pk=declined)
            for invite in invites:
                invite.status = TeamInvites.DECLINED
                invite.save()
        else:
            error_message = "Ошибка чтения значения кнопки, повторите попытку"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
        return redirect(reverse('translators_hub:invites', kwargs={'slug': request.user.userprofile.slug}))
