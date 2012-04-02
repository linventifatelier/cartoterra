import idios.views
import geodata.views

class ProfileDetailView(idios.views.ProfileDetailView):

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['map'] = geodata.views.get_profilemap(context['profile'])
        return context

