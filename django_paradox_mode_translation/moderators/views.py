from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views import View
from django.views.generic import FormView, ListView

from moderators.forms import SendQueryForm
from moderators.models import Query
from translators_hub.utils.custom_paginator import CustomPaginator


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


class MyQueriesView(ListView):

    model = Query
    paginator_class = CustomPaginator
    paginate_by = 10
    context_object_name = 'queries'
    template_name = 'moderators/my_queries.html'

    def get_queryset(self):
        my_queries = Query.objects.filter(query_author=self.request.user).select_related('topic')
        return my_queries


class QueryBookingView(ListView):
    model = Query
    paginator_class = CustomPaginator
    paginate_by = 10
    context_object_name = 'queries'
    template_name = 'moderators/query_booking.html'

    def get_queryset(self):
        queries = Query.objects.filter(status=None).select_related('query_author', 'topic').order_by('pub_date')
        return queries

    def post(self, request, *args, **kwargs):
        query = Query.objects.get(pk=request.POST.get('query_pk'))
        query.query_author = request.user
        query.status = Query.IN_WORK
        query.save()
        return render(request, template_name=self.template_name)
