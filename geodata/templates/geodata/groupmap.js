{% extends "geodata/map_base.js" %}
{% load l10n %}
{% load staticfiles %}

{% block extra_map %}{% endblock %}

{% block layers_getson_extra %}
    var bounds = geojsonlayer{{ module }}.getBounds();
    if (bounds.isValid()) {
        if (map{{ module }}._loaded) {
            map{{ module }}.fitBounds(map{{ module }}.getBounds().extend(bounds));
        } else {
            map{{ module }}.fitBounds(bounds);
        };
    };
    map{{ module }}.addLayer(geojsonlayer{{ module }});
{% endblock %}
