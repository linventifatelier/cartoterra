from django.views.generic.base import TemplateView
import account.views
import cartoterra.forms


class SignupView(account.views.SignupView):
    form_class = cartoterra.forms.SignupForm


class DonateView(TemplateView):
    template_name = "donate.html"
