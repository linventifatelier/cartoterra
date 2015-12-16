from __future__ import unicode_literals

from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.widgets import DateInput, CheckboxChoiceInput, \
    CheckboxSelectMultiple, ChoiceFieldRenderer, CheckboxInput
from leaflet.forms.widgets import LeafletWidget

class GeoDataWidget(LeafletWidget):
    include_media = True
    template_name = 'geodata/geodata_form_geometry_widget.html'
    map_width = '500px'
    map_height = '250px'

    class Media:
        js = [
            'js/spin.min.js',
            'js/form-geometry.js',
        ]


class BootstrapDatePicker(DateInput):
    def __init__(self, attrs=None):
        if attrs is not None:
            if 'class' in attrs:
                attrs['class'] = 'form-datepicker ' + attrs['class']
            else:
                attrs['class'] = 'form-datepicker'
        else:
            attrs = {'class': 'form-datepicker', }
        super(BootstrapDatePicker, self).__init__(attrs)

    class Media:
        js = (
            'js/bootstrap-datepicker.min.js',
            'js/form-datepicker.js',
        )
        css = {
            'all': (
                'css/bootstrap-datepicker3.min.css',
            )
        }


class EarthTechniqueCheckboxChoiceInput(CheckboxChoiceInput):
    def __init__(self, name, value, attrs, choice, index):
        self.name = name
        self.value = value
        self.attrs = attrs
        self.choice_value = force_text(choice[0])
        self.choice_label = force_text(choice[1])
        self.choice_obj = choice[2]
        self.index = index
        if 'id' in self.attrs:
            self.attrs['id'] += "_%d" % self.index

    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        help_text = """\
<a href="#" data-toggle="modal" data-target="#geodata-modal-techniques-%(pk)s">
    <span class="glyphicon glyphicon-question-sign"></span>
</a>
<div class="modal fade" id="geodata-modal-techniques-%(pk)s">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">%(name)s</h4>
            </div>
            <div class="modal-body">
                %(description)s</br>
                <a href="%(url)s">%(url)s</a>
            </div>
        </div>
    </div>
</div>
""" % {'name': self.choice_obj.name, 'url': self.choice_obj.url, 'pk': self.choice_obj.pk, 'description': self.choice_obj.description}
        return format_html(
            '<label{}>{} {}</label>{}', label_for, self.tag(attrs),
            self.choice_label, mark_safe(help_text)
        )


class CheckboxFieldRenderer(ChoiceFieldRenderer):
    choice_input_class = EarthTechniqueCheckboxChoiceInput

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id', None)
        output = []
        for i, choice in enumerate(self.choices):
            choice_value, choice_label, _ = choice
            # ^ HACK: use (value, label, obj) choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{}'.format(i)
                sub_ul_renderer = CheckboxFieldRenderer(name=self.name,
                                                        value=self.value,
                                                        attrs=attrs_plus,
                                                        choices=choice_label)
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html(self.inner_html, choice_value=choice_value,
                                          sub_widgets=sub_ul_renderer.render()))
            else:
                w = self.choice_input_class(self.name, self.value,
                                            self.attrs.copy(), choice, i)
                output.append(format_html(self.inner_html,
                                          choice_value=force_text(w), sub_widgets=''))
        return format_html(self.outer_html,
                           id_attr=format_html(' id="{}"', id_) if id_ else '',
                           content=mark_safe('\n'.join(output)))


class EarthTechniqueMultiple(CheckboxSelectMultiple):
    renderer = CheckboxFieldRenderer


class IsceahCheckboxInput(CheckboxInput):
    class Media:
        js = ['js/geodata-hide-isceah.js']
        css = {
            'all': ['css/geodata-hide-isceah.css']
        }
