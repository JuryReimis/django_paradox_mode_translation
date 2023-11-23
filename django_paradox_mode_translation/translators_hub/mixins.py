from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import generic

from translators_hub.forms import AddProfileCommentForm
from translators_hub.models import UserProfile, ProfileComments


class AddCommentMixin(generic.edit.ModelFormMixin):

    target = None
    author = None

    def get_comment_form(self):
        current_object = self.get_object()
        if isinstance(current_object, UserProfile):
            self.form_class = AddProfileCommentForm
            self.target = current_object
            self.success_url = current_object.get_absolute_url()

    def get_context_data(self, **kwargs):
        if 'comment_form' not in kwargs:
            kwargs['comment_form'] = self.get_form()
        return super(AddCommentMixin, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.get_comment_form()
        delete_id = request.POST.get('comment_id')
        if delete_id:
            current_object = self.get_object()
            if isinstance(current_object, UserProfile):
                comment = get_object_or_404(ProfileComments, pk=delete_id)
                comment.visible = False
                try:
                    comment.save()
                except Exception as error:
                    error_text = f'Ошибка удаления\n{error}'
                    messages.add_message(request, level=messages.ERROR, message=error_text)
                else:
                    message_text = "Комментарий удален!"
                    messages.add_message(request, level=messages.SUCCESS, message=message_text)
        else:
            form: AddProfileCommentForm = self.get_form()
            form.instance.target = self.target
            form.instance.author = request.user
            form.save()

        return redirect(self.get_object().get_absolute_url())
