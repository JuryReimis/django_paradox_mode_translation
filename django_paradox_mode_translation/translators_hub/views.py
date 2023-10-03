import django.core.paginator
from django.contrib.auth import views, login, authenticate, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.forms import model_to_dict, modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import generic

import translators_hub.models
from . import models
from .forms import UpdateProfileForm, RegistrationForm, AddPageForm, ServiceForm, ProfileFormForApply, InviteUserForm, \
    UpdateUserForm, ChangeUserRoleForm, ChangeDescriptionForm
from .models import ModTranslation, UserProfile, ProfileComments, Roles, Invites, Game

User = get_user_model()
User: translators_hub.models.User


class HomeView(generic.ListView):
    template_name = 'translators_hub/home.html'
    context_object_name = 'latest_pages_list'
    paginate_by = 4

    def __init__(self, *args, **kwargs):
        self.extra_filter = None
        super(HomeView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.extra_filter:
            return ModTranslation.objects.filter(game__in=self.extra_filter.get('selected_game')).order_by(
                '-created_date')
        return ModTranslation.objects.order_by('-created_date')

    def get(self, request, *args, **kwargs):
        selected_category = request.GET.get('game')
        games = Game.objects.all()
        selected_game = Game.objects.filter(game_name=selected_category) if selected_category is not None else None

        self.extra_filter = {
            'selected_game': selected_game if selected_game is not None else games
        }
        self.extra_context = {
            'games': games,
            'selected_game': selected_game
        }
        return super(HomeView, self).get(request, *args, **kwargs)


class SearchProjectView(generic.ListView):
    template_name = 'translators_hub/search_results.html'
    context_object_name = 'search_results'
    paginate_by = 5

    def get_queryset(self):
        def add_model_name(obj):
            obj_name = obj._meta.model_name
            obj.model_name = obj_name
            return obj
        search_query = self.extra_context.get('search_query')
        if search_query:
            search_vector_for_projects = SearchVector('title', 'mode_name', 'description')
            search_vector_for_users = SearchVector('user__username', 'user__first_name', 'user__last_name')
            searched_projects = ModTranslation.objects.annotate(search=search_vector_for_projects).filter(
                search=search_query)
            searched_users = UserProfile.objects.annotate(search=search_vector_for_users).filter(
                search=search_query)
            search_results = list(map(add_model_name, list(searched_projects) + list(searched_users)))
            self.extra_context['total_objects'] = len(search_results)
            return search_results
        else:
            self.extra_context['search_query'] = '---'
            search_results = list(map(add_model_name, list(ModTranslation.objects.all()) + list(UserProfile.objects.all())))
            self.extra_context['total_objects'] = len(search_results)
            return search_results
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchProjectView, self).get_context_data(object_list=object_list, **kwargs)
        paginator: django.core.paginator.Paginator = context['paginator']
        return context

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query')
        self.extra_context = {
            'search_query': search_query,
        }
        return super(SearchProjectView, self).get(request, args, kwargs)


class DetailView(generic.DetailView):
    model = ModTranslation
    template_name = 'translators_hub/detail_page.html'
    context_object_name = 'current_page'

    def post(self, request, slug, *args, **kwargs):
        current_page = self.get_object()
        if not request.user.is_authenticated:
            form = ServiceForm()
            error_message = "Необходимо авторизоваться"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            context = {
                'form': form,
                'current_page': current_page,
            }
            return render(request=request, template_name='translators_hub/detail_page.html', context=context)
        elif current_page.authors.filter(user=request.user):
            form = ServiceForm()
            error_message = "Вы уже являетесь членом команды!"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            context = {
                'form': form,
                'current_page': current_page,
            }
            return render(request=request, template_name='translators_hub/detail_page.html', context=context)
        else:
            return redirect(reverse_lazy('translators_hub:apply_for', kwargs={'slug': slug}))

    def get(self, request, *args, **kwargs):
        try:
            if not isinstance(request.user, AnonymousUser):
                role_object = self.get_object().authors.get(user=request.user)
                if role_object.role in [Roles.ORGANISER, Roles.MODERATOR]:
                    self.extra_context = {'moderator': True}
            return super(DetailView, self).get(request, args, kwargs)
        except models.models.ObjectDoesNotExist:
            return super(DetailView, self).get(request, args, kwargs)


class ManagementView(generic.View):
    template_name = 'translators_hub/project_management.html'

    def get(self, request, slug, *args, **kwargs):
        project = ModTranslation.objects.get(slug=slug)
        project_authors = None
        project_moderator = None
        description_form = ChangeDescriptionForm(instance=project)
        if not isinstance(request.user, AnonymousUser):
            project_authors = project.authors.all().prefetch_related('user', 'user__userprofile')
            project_moderator = project.authors.filter(role__in=[Roles.ORGANISER, Roles.MODERATOR],
                                                       user=request.user)
        if project_moderator:
            context = {
                'slug': slug,
                'user': request.user,
                'authors': project_authors,
                'form': description_form,
            }
            return render(request=request, template_name='translators_hub/project_management.html', context=context)
        else:
            error_message = "У вас недостаточно прав для захода на эту страницу"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            context = {
                'current_page': project,
            }
            return render(request=request, template_name='translators_hub/detail_page.html', context=context)

    def post(self, request, slug, *args, **kwargs):
        project = ModTranslation.objects.get(slug=slug)
        if request.POST.get('fired'):
            fired_users = Roles.objects.filter(user_id__in=request.POST.get('fired'))
            for author in fired_users:
                project.authors.remove(author)
                project.save()
            return redirect('translators_hub:management', slug=slug)
        elif request.POST.get('save_description'):
            change_description_form = ChangeDescriptionForm(request.POST, request.FILES, instance=project)
            change_description_form.save()
            return redirect('translators_hub:management', slug=slug)
        else:
            return redirect('translators_hub:management', slug=slug)


class ChangeRoleView(generic.edit.FormView):
    form_class = ChangeUserRoleForm
    template_name = 'translators_hub/change_user_role.html'
    success_url = ''

    def get(self, request, *args, **kwargs):
        userprofile = User.objects.get(username=kwargs.get('username')).userprofile
        self.extra_context = {'changing_user': kwargs.get('username'), 'userprofile': userprofile}
        return super(ChangeRoleView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=kwargs.get('username'))
        mod_translation = ModTranslation.objects.get(slug=kwargs.get('slug'))
        old_role = user.roles.get(modtranslation=mod_translation)
        new_role = Roles.objects.get_or_create(user=user, role=request.POST.get('role'))[0]
        mod_translation.authors.remove(old_role)
        mod_translation.authors.add(new_role)
        return redirect('translators_hub:management', slug=kwargs.get('slug'))


class ProfileView(generic.edit.FormMixin, generic.DetailView):
    model = UserProfile
    template_name = 'translators_hub/profile_page.html'
    context_object_name = 'profile_data'
    form_class = UpdateProfileForm
    success_url = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if isinstance(request.user, AnonymousUser):
            error_message = "Для просмотра профилей наших пользователей - авторизуйтесь!"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            return redirect('translators_hub:home')
        if request.user.userprofile == self.object:
            self.initial = model_to_dict(self.object)
            user_form = UpdateUserForm(data=request.POST if request.POST != {} else None,
                                       initial=model_to_dict(request.user))
            self.extra_context = {'user_form': user_form}
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
            self.kwargs['instance'] = user_profile
            form = self.get_form()
            user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)

            if form.is_valid() and user_form.is_valid():
                form.save(commit=True)
                user_form.save()
                return redirect(self.success_url)
            else:
                return self.get(request=request, form_errors=user_form.errors, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        instance = self.kwargs.get('instance')
        if instance:
            kwargs.update({'instance': instance})
        return kwargs


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

    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            error_message = "Зарегистрируйтесь или войдите для этого действия"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            return redirect('translators_hub:home')
        else:
            return super(AddPageView, self).get(args, kwargs)

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
            error_message = "Ошибка чтения значения кнопки, повторите попытку"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
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
        self.current_authors = None

    def get_queryset(self):
        slug = self.request.resolver_match.kwargs['slug']
        self.current_data = ModTranslation.objects.get(slug=slug)
        self.current_authors = self.current_data.authors.all().prefetch_related('user')
        for author in self.current_authors:
            if author.role in [Roles.ORGANISER, Roles.MODERATOR]:
                self.moderators.append(author.user)
            else:
                self.active_authors.append(author.user)
        self.invited_authors = [invite.target for invite in Invites.objects.filter(mod_translation=self.current_data)]
        free_users = User.objects.exclude(
            username__in=self.active_authors + self.invited_authors + self.moderators).prefetch_related('userprofile',
                                                                                                        'userprofile__titles')
        return free_users

    def get(self, request, *args, **kwargs):
        form = InviteUserForm()
        self.extra_context = {'form': form, 'slug': kwargs.get('slug')}
        super_method = super(SendInvitesView, self).get(request, args, kwargs)
        moderators = [author.user if author.role in [Roles.ORGANISER, Roles.MODERATOR] else '' for author in
                      self.current_authors]
        if request.user not in moderators:
            error_message = "У вас нет прав на приглашение новых людей в этот проект"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            context = {
                'current_page': self.current_data,
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
        slug = kwargs.get('slug')
        current_page = ModTranslation.objects.get(slug=slug)

        if not request.user.is_authenticated:
            error_message = "Необходимо авторизоваться"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            return redirect('translators_hub:detail_page', slug=slug)
        elif current_page.authors.filter(user=request.user):
            error_message = "Вы уже являетесь членом команды!"
            messages.add_message(request=request, level=messages.ERROR, message=error_message)
            return redirect('translators_hub:detail_page', slug=slug)
        elif request.user.is_authenticated:
            current_user_profile = get_object_or_404(UserProfile, user=request.user)
            self.initial = current_user_profile.get_fields_in_dict()
            self.extra_context = {'reputation': current_user_profile.reputation}
            return super(ApplyForView, self).get(request=request, *args, **kwargs)
