from django import forms
from django.contrib import auth
from django.urls import reverse_lazy
from django.views import generic
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=_('Username'))
    password = forms.CharField(required=True, label=_("Password"))


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('schemas')

    def form_valid(self, form):
        if form.is_valid():
            print('valid')
            user = auth.authenticate(form, username=form.data.get('username'), password=form.data.get('password'))
            auth.login(self.request, user)
        return super().form_valid(form)
