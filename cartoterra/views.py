from django.views.generic.base import TemplateView
from django.conf import settings
import account.views
import cartoterra.forms


class HomeView(TemplateView):
    template_name = "home.html"


class SignupView(account.views.SignupView):
    form_class = cartoterra.forms.SignupForm


class DonateView(TemplateView):
    template_name = "donate.html"

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        context['donate_email'] = settings.GEODATA_PAYPAL_ID
        return context
