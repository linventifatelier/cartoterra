"""GeoData forms."""

from django import forms
from models import GeoDataAbstract, Building, Worksite, Event, Stakeholder, \
    Image, EarthTechnique, EarthGroup
from django.forms import ModelForm
from django.forms.models import ModelMultipleChoiceField, ModelChoiceIterator
from geodata.widgets import GeoDataWidget, BootstrapDatePicker, \
    EarthTechniqueMultiple, IsceahCheckboxInput
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.gis.forms.fields import PointField
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict
from pagedown.widgets import PagedownWidget


class EarthTechniqueChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (
            self.field.prepare_value(obj),
            self.field.label_from_instance(obj),
            obj
        )


class EarthTechniqueMultipleChoiceField(ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(EarthTechniqueMultipleChoiceField, self).__init__(
            *args, **kwargs
        )
        self.choices = EarthTechniqueChoiceIterator(self)


ImageFormSet = generic_inlineformset_factory(Image, extra=1, can_delete=True)


class GeoDataAbstractForm(ModelForm):
    geometry = PointField(widget=GeoDataWidget())
    techniques = EarthTechniqueMultipleChoiceField(
        required=False, queryset=EarthTechnique.objects.all(),
        widget=EarthTechniqueMultiple
    )

    class Meta:
        model = GeoDataAbstract
        exclude = ('creator', 'pub_date', )

    class Media:
        js = ('js/formset.js', )


# https://stackoverflow.com/questions/913589/django-forms-inheritance-and-order-of-form-fields/27493844#27493844
def reorder_fields(fields, order):
    """Reorder form fields by order, removing items not in order.

    >>> reorder_fields(
    ...     OrderedDict([('a', 1), ('b', 2), ('c', 3)]),
    ...     ['b', 'c', 'a'])
    OrderedDict([('b', 2), ('c', 3), ('a', 1)])
    """
    for key, v in fields.items():
        if key not in order:
            del fields[key]

    return OrderedDict(sorted(fields.items(), key=lambda k: order.index(k[0])))


class BuildingForm(GeoDataAbstractForm):
    detailed_description = forms.CharField(
        required=False, widget=forms.Textarea,
        help_text=_("Detailled description (major elements, present and past \
use, cultural affiliation, historical/cultural/architectural \
importance, period of construction, geographical scole, associated \
events, hybrid construction techniques if any)")
    )
    inauguration_date = forms.DateField(
        required=False, widget=BootstrapDatePicker,
        help_text=_("Put here the inauguration date for a contemporary \
building if known, ignore otherwise.")
    )
    construction_date = forms.CharField(
        required=False, help_text=_("If heritage site")
    )
    isceah = forms.BooleanField(
        required=False, widget=IsceahCheckboxInput,
        help_text=_("Tick here if you are member of ICOMOS-ISCEAH and want \
this entry to be referenced as ICOMOS-ISCEAH.")
    )
    stakeholder = forms.ModelMultipleChoiceField(
        required=False, queryset=Stakeholder.objects.all(),
        help_text=_("Select cartoterra.net stakeholders you want to link to \
this entry.")
    )

    def __init__(self, user=None, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        if not user.has_perm('profile.world_heritage'):
            self.fields['unesco'].widget.attrs['disabled'] = 'disabled'
        self._user = user
        # https://stackoverflow.com/questions/913589/django-forms-inheritance-and-order-of-form-fields/27493844#27493844
        key_order = [
            'name', 'geometry', 'heritage_status', 'isceah',
            'classification', 'use', 'cultural_landscape', 'unesco',
            'protection_status', 'property_status', 'techniques',
            'earth_quantity', 'description', 'detailed_description',
            'inauguration_date', 'construction_date', 'condition',
            'references', 'url', 'architects', 'stakeholder', 'contact',
            'credit_creator', 'image'
        ]
        self.fields = reorder_fields(self.fields, key_order)

        for f in [
            'detailed_description',
            'classification', 'use', 'cultural_landscape',
            'protection_status', 'property_status', 'construction_date',
            'condition', 'references'
        ]:
            self.fields[f].widget.attrs['class'] = 'geodata-isceah'
        self.fields['isceah'].widget.attrs['class'] = 'geodata-toggle-isceah'

    def clean_unesco(self):
        if self._user.has_perm('profile.world_heritage'):
            return self.cleaned_data.get('unesco')
        else:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                return instance.unesco
            else:
                return self.fields['unesco'].initial

    class Meta:
        model = Building
        exclude = ('creator', 'pub_date', )


class WorksiteForm(GeoDataAbstractForm):
    inauguration_date = forms.DateField(
        widget=BootstrapDatePicker, required=False
    )

    def __init__(self, user=None, *args, **kwargs):
        super(WorksiteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Worksite
        exclude = ('creator', 'pub_date', )


class EventForm(GeoDataAbstractForm):
    beginning_date = forms.DateField(widget=BootstrapDatePicker)
    end_date = forms.DateField(widget=BootstrapDatePicker)

    def __init__(self, user=None, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if not user.has_perm('profile.unesco_chair'):
            self.fields['unesco_chair'].widget.attrs['disabled'] = 'disabled'
        self._user = user

    def clean_unesco_chair(self):
        if self._user.has_perm('profile.unesco_chair'):
            return self.cleaned_data.get('unesco_chair')
        else:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                return instance.unesco_chair
            else:
                return self.fields['unesco_chair'].initial

    class Meta:
        model = Event
        exclude = ('creator', 'pub_date', )


class StakeholderForm(GeoDataAbstractForm):
    isceah = forms.BooleanField(
        required=False, help_text=_("Tick here if you are member of \
ICOMOS-ISCEAH and want this entry to be referenced as ICOMOS-ISCEAH.")
    )

    def __init__(self, user=None, *args, **kwargs):
        super(StakeholderForm, self).__init__(*args, **kwargs)
        if not user.has_perm('profile.unesco_chair'):
            self.fields['unesco_chair'].widget.attrs['disabled'] = 'disabled'
        self._user = user

    def clean_unesco_chair(self):
        if self._user.has_perm('profile.unesco_chair'):
            return self.cleaned_data.get('unesco_chair')
        else:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                return instance.unesco_chair
            else:
                return self.fields['unesco_chair'].initial

    class Meta:
        model = Stakeholder
        exclude = ('creator', 'pub_date', )


class EarthGroupForm(ModelForm):
    class Meta:
        model = EarthGroup
        exclude = ('pub_date', 'administrators', )
        widgets = {
            'description_markdown': PagedownWidget,
            'buildings': forms.CheckboxSelectMultiple,
            'worksites': forms.CheckboxSelectMultiple,
            'events': forms.CheckboxSelectMultiple,
            'stakeholders': forms.CheckboxSelectMultiple,
        }

    class Media:
        js = ('js/formset.js', )
