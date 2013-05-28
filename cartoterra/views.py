import account.views
import cartoterra.forms


class SignupView(account.views.SignupView):
    form_class = cartoterra.forms.SignupForm
