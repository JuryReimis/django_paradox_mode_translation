from django.contrib.auth import views, login, authenticate, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import generic

import translators_hub.models
from .forms import UpdateProfileForm, RegistrationForm, AddPageForm, ServiceForm, ProfileFormForApply, InviteUserForm
from .models import ModTranslation, UserProfile, ProfileComments, Roles, Invites

User = get_user_model()
User: translators_hub.models.User


class HomeView(generic.ListView):
    template_name = 'translators_hub/home.html'
    context_object_name = 'latest_pages_list'

    def get_queryset(self):
        return ModTranslation.objects.order_by('-created_date')[:10]


class DetailView(generic.DetailView):
    model = ModTranslation
    template_name = 'translators_hub/detail_page.html'
    context_object_name = 'current_page'

    @staticmethod
    def post(request, slug, *args, **kwargs):
        current_page = ModTranslation.objects.get(slug=slug)
        if not request.user.is_authenticated:
            form = ServiceForm()
            form.add_error(field=None, error="Необходимо авторизоваться")
            context = {
                'form': form,
                'current_page': current_page,
            }
            return render(request=request, template_name='translators_hub/detail_page.html', context=context)
        elif current_page.authors.filter(user=request.user):
            form = ServiceForm()
            form.add_error(field=None, error="Вы уже являетесь членом команды!")
            context = {
                'form': form,
                'current_page': current_page,
            }
            return render(request=request, template_name='translators_hub/detail_page.html', context=context)
        else:
            return redirect(reverse_lazy('translators_hub:apply_for', kwargs={'slug': slug}))

    def get(self, request, *args, **kwargs):
        if self.get_object().authors.get(user=request.user).role in [Roles.ORGANISER, Roles.MODERATOR]:
            self.extra_context = {'moderator': True}
        return super(DetailView, self).get(request, args, kwargs)


class ProfileView(generic.edit.FormMixin, generic.DetailView):
    model = UserProfile
    template_name = 'translators_hub/profile_page.html'
    context_object_name = 'profile_data'
    form_class = UpdateProfileForm
    success_url = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.userprofile == self.object:
            self.initial = model_to_dict(self.object)
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            context = {
                'profile_data': self.object,
            }
            return render(request=request, template_name='translators_hub/profile_page.html', context=context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile = request.user.userprofile
            self.success_url = reverse_lazy('translators_hub:profile', kwargs={'slug': kwargs['slug']})
            form = self.get_form()
            print(model_to_dict(user_profile))
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.pk = user_profile.pk
                form_data.user = request.user
                form_data.slug = kwargs['slug']
                form_data.image = user_profile.profile_image
                form_data.reputation = user_profile.reputation
                form_data.save()
                form.save_m2m()
                return redirect(self.success_url)


class LogInView(views.LoginView):
    template_name = 'translators_hub/login.html'


class LogOutView(views.LogoutView):
    pass


class RegistrationView(generic.FormView):
    template_name = 'translators_hub/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('translators_hub:home')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, slug=slugify(user.username))
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request=request, user=user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AddPageView(generic.FormView):
    template_name = 'translators_hub/add_page.html'
    form_class = AddPageForm
    success_url = None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            current_page = form.save(commit=False)
            current_page.slug = slugify(current_page.title)
            self.success_url = reverse_lazy('translators_hub:detail_page', kwargs={'slug': current_page.slug})
            current_page.save()
            new_organiser = Roles.objects.get_or_create(user=request.user, role=Roles.ORGANISER)
            current_page.authors.add(new_organiser[0])
            form.save_m2m()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MyProjectsView(generic.ListView):
    template_name = 'translators_hub/my_projects.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        user = self.request.user
        if user is not AnonymousUser:
            projects = ModTranslation.objects.filter(authors__user=user).prefetch_related('authors', 'game')

            roles = {project.id: project.authors__role for project in
                     projects.values_list('id', 'authors__role', named=True)}
            for project in projects:
                project.role = Roles(role=roles.get(project.pk)).get_role_display()
            return projects

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user_slug = request.user.userprofile.slug
        if user_slug == slug:
            super_method = super(MyProjectsView, self).get(request, args, kwargs)
            return super_method
        else:
            return redirect('translators_hub:my_projects', slug=user_slug)


class InvitesView(generic.ListView):
    template_name = 'translators_hub/invites.html'
    context_object_name = 'invites'

    def get_queryset(self):
        invites = self.request.user.target_name.filter(status=None).prefetch_related('sender', 'mod_translation')
        self.extra_context = {'slug': self.kwargs.get('slug')}
        return invites

    def post(self, request, slug, *args, **kwargs):
        accepted = request.POST.get('accept')
        declined = request.POST.get('decline')
        if accepted:
            invites = Invites.objects.filter(Q(pk__in=accepted) | Q(pk=accepted))
            for invite in invites:
                invite.mod_translation.authors.add(Roles.objects.get_or_create(user=invite.target, role=invite.role)[0])
                invite.status = Invites.ACCEPTED
                invite.save()
        elif declined:
            invites = Invites.objects.filter(pk__in=declined)
            for invite in invites:
                invite.status = Invites.DECLINED
                invite.save()
        else:
            self.extra_context = {
                'errors': ['Ошибка чтения значения кнопки, повторите попытку']
            }
        return redirect(reverse('translators_hub:invites', kwargs={'slug': slug}))

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user_slug = request.user.userprofile.slug
        if user_slug == slug:
            return super(InvitesView, self).get(request, args, kwargs)
        else:
            return redirect('translators_hub:invites', slug=user_slug)


class SendInvitesView(generic.ListView):
    template_name = 'translators_hub/invite_user.html'
    context_object_name = 'free_users'

    def __init__(self, **kwargs):
        super(SendInvitesView, self).__init__(**kwargs)
        self.active_authors = []
        self.moderators = []
        self.invited_authors = None
        self.current_data = None

    def get_queryset(self):
        slug = self.request.resolver_match.kwargs['slug']
        self.current_data = ModTranslation.objects.get(slug=slug)
        for author in self.current_data.authors.all():
            if author.role in [Roles.ORGANISER, Roles.MODERATOR]:
                self.moderators.append(author.user)
            else:
                self.active_authors.append(author.user)
        self.invited_authors = [invite.target for invite in Invites.objects.filter(mod_translation=self.current_data)]
        free_users = User.objects.exclude(username__in=self.active_authors + self.invited_authors + self.moderators)
        return free_users

    def get(self, request, *args, **kwargs):
        form = InviteUserForm()
        self.extra_context = {'form': form, 'slug': kwargs.get('slug')}
        super_method = super(SendInvitesView, self).get(request, args, kwargs)
        moderators = [author.user if author.role in [Roles.ORGANISER, Roles.MODERATOR] else '' for author in
                      self.current_data.authors.all()]
        print(moderators)
        if request.user not in moderators:
            context = {
                'current_page': self.current_data,
                'errors': ["У вас нет прав на приглашение новых людей в этот проект", ],
            }
            return render(request=request, template_name='translators_hub/detail_page.html', context=context)
        else:
            return super_method

    @staticmethod
    def post(request, slug, *args, **kwargs):
        form = InviteUserForm(request.POST)
        mod_translation = ModTranslation.objects.get(slug=slug)
        if form.is_valid():
            data = form.save(commit=False)
            role = data.role
            data.mod_translation = mod_translation
            data.sender = request.user
            data.target_id = request.POST.get('target_user_id')
            data.role = None if role == '' else role
            data.save()
            form.save_m2m()
        return redirect(reverse('translators_hub:invite_authors', kwargs={'slug': slug}))


class ApplyForView(generic.FormView):
    template_name = 'translators_hub/apply_form_page.html'
    form_class = ProfileFormForApply
    success_url = None
    initial = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            current_user_profile = get_object_or_404(UserProfile, user=request.user)
            self.initial = current_user_profile.get_fields_in_dict()
            self.extra_context = {'reputation': current_user_profile.reputation}
        return super(ApplyForView, self).get(request=request, *args, **kwargs)
