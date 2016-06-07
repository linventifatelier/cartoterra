import itertools
from django.views.generic.base import TemplateView
from django.conf import settings
import account.views
import cartoterra.forms
from geodata.models import Building, Worksite, Event, Stakeholder


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        last_entries = list(itertools.chain(
            Building.objects.filter(image__isnull=False).distinct().order_by('-pub_date')[:10],
            Worksite.objects.filter(image__isnull=False).distinct().order_by('-pub_date')[:10],
            Event.objects.filter(image__isnull=False).distinct().order_by('-pub_date')[:10],
            Stakeholder.objects.filter(image__isnull=False).distinct().order_by('-pub_date')[:10]
        ))
        context['last_entries'] = sorted(last_entries, key=lambda x: x.pub_date, reverse=True)[:10]
        return context


class SignupView(account.views.SignupView):
    form_class = cartoterra.forms.SignupForm


class DonateView(TemplateView):
    template_name = "donate.html"

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        context['donate_email'] = settings.GEODATA_PAYPAL_ID
        return context
