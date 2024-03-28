from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views import View
from django.views.generic import FormView

from moderators.forms import SendQueryForm


class ModeratorHomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='moderators/home.html')


class SendQueryView(FormView):

    template_name = 'moderators/send_query.html'
    form_class = SendQueryForm
    success_url = reverse_lazy('moderators:home')

    def get(self, request, *args, **kwargs):
        return super(SendQueryView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SendQueryView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.query_author = self.request.user
        form.instance.status = None
        form.save()
        return super(SendQueryView, self).form_valid(form)

