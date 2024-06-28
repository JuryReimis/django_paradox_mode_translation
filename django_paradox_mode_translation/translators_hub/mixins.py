from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

from auth_app.models import UserProfile
from translators_hub.models import Translation


# class AddCommentMixin(generic.edit.ModelFormMixin):
#
#     target = None
#     author = None
#
#     def get_comment_form(self):
#         self.object = self.get_object()
#         if isinstance(self.object, UserProfile):
#             self.form_class = AddProfileCommentForm
#             self.target = self.object
#             self.success_url = self.object.get_absolute_url()
#         elif isinstance(self.object, Translation):
#             self.form_class = AddProjectCommentForm
#             self.target = self.object
#             self.success_url = self.object.get_absolute_url()
#
#     def get_context_data(self, **kwargs):
#         if 'comment_form' not in kwargs:
#             kwargs['comment_form'] = self.get_form()
#         return super(AddCommentMixin, self).get_context_data(**kwargs)
#
#     def post(self, request, *args, **kwargs):
#         self.get_comment_form()
#         delete_id = request.POST.get('comment_id')
#         if delete_id:
#             current_object = self.get_object()
#             if isinstance(current_object, UserProfile):
#                 comment = get_object_or_404(ProfileComments, pk=delete_id)
#                 comment.visible = False
#             elif isinstance(current_object, Translation):
#                 comment = get_object_or_404(ProjectComments, pk=delete_id)
#                 comment.visible = False
#             try:
#                 comment.save()
#             except Exception as error:
#                 error_text = f'Ошибка удаления\n{error}'
#                 messages.add_message(request, level=messages.ERROR, message=error_text)
#             else:
#                 message_text = "Комментарий удален!"
#                 messages.add_message(request, level=messages.SUCCESS, message=message_text)
#         else:
#             form: AddProfileCommentForm | AddProjectCommentForm = self.get_form()
#             form.instance.target = self.target
#             form.instance.author = request.user
#             form.save()
#
#         return redirect(self.get_object().get_absolute_url())
#
#     def get_form_kwargs(self):
#         kwargs = {
#             "initial": self.get_initial(),
#             "prefix": self.get_prefix(),
#         }
#
#         if self.request.method in ("POST", "PUT"):
#             kwargs.update(
#                 {
#                     "data": self.request.POST,
#                     "files": self.request.FILES,
#                 }
#             )
#         return kwargs


# def comment_reaction_mixin(request):
#     comment = None
#     reaction = None
#     created = None
#     comment_object = request.POST.get('page_data')
#     comment_pk = request.POST.get('comment_pk')
#     if comment_object == 'Translation':
#         comment = ProjectComments.objects.filter(pk=comment_pk).first()
#         reaction, created = ProjectCommentsReaction.objects.get_or_create(target=comment, author=request.user)
#     elif comment_object == 'UserProfile':
#         comment = ProfileComments.objects.filter(pk=comment_pk).first()
#         reaction, created = ProfileCommentsReaction.objects.get_or_create(target=comment, author=request.user)
#
#     return comment, reaction, created
