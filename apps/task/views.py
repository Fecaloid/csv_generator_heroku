from django import forms
from django.urls import reverse_lazy
from django.views import generic

from apps.task.models import Schema, Task, Column
from django.utils.translation import ugettext_lazy as _
from querystring_parser import parser


class SchemasView(generic.ListView):
    template_name = 'schema/schemas.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = Schema.objects.filter(user=None)
        else:
            queryset = Schema.objects.filter(user=self.request.user)
        return queryset


class SchemaUpdateView(generic.UpdateView):
    model = Schema
    template_name = 'schema/_update.html'
    fields = ['name', 'separator']
    template_name_suffix = 'schema'
    success_url = reverse_lazy('schemas')

    def form_valid(self, form):
        print(form.data)
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(SchemaUpdateView, self).form_valid(form)


class SchemaCreateView(generic.CreateView):
    model = Schema
    template_name = 'schema/_create.html'
    fields = ['name', 'separator']
    # template_name_suffix = 'schema'
    success_url = reverse_lazy('schemas')

    def form_valid(self, form):
        tasks = parser.parse(form.data.get('data_json'))
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        for item in tasks['data_rows'].values():
            Column.objects.create(
                schema=obj,
                name=item['name'],
                kind=item['kind'],
                start=int(item['start']) if item.get('start', None) else None,
                end=int(item['end']) if item.get('end', None) else None,
                order=int(item['order']),
            )
        return super(SchemaCreateView, self).form_valid(form)


class SchemaDeleteView(generic.DeleteView):
    model = Schema
    template_name = 'schema/_delete.html'
    fields = ['name']
    template_name_suffix = 'schema'
    success_url = reverse_lazy('schemas')


class SchemaDetailForm(forms.Form):
    rows = forms.IntegerField(required=True, label=_('Rows'))


class SchemaDetailView(generic.FormView):
    form_class = SchemaDetailForm
    template_name = 'schema/_detail.html'

    def get_success_url(self):
        return reverse_lazy('schema-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['tasks'] = Task.objects.filter(schema__user=self.request.user, schema_id=self.kwargs['pk'])
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            Task.objects.create(schema_id=self.kwargs['pk'], rows=form.data.get('rows'))
        return super().form_valid(form)
