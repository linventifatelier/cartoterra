from django import forms
import account.forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from cartoterra.settings import SITE_NAME


class SignupForm(account.forms.SignupForm):
    license = forms.BooleanField(required=False, label=mark_safe(_("""\
        I hereby agree:<br>
        Content I create on %s is automatically licensed according to the \
        Open Database License: \
        <a target="_blank" \
        href="http://opendatacommons.org/licenses/odbl/1.0/">\
        http://opendatacommons.org/licenses/odbl/1.0/</a>. Any rights in \
        individual contents of the database are licensed under the Database \
        Contents License: \
        <a target="_blank" \
        href="http://opendatacommons.org/licenses/dbcl/1.0/">\
        http://opendatacommons.org/licenses/dbcl/1.0/</a>""" % SITE_NAME)))

    def clean_license(self):
        license = self.cleaned_data['license']

        if not license:
            raise forms.ValidationError(_('You must approve the license'))
