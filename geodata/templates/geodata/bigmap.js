{% extends "geodata/map_base.js" %}
{% load l10n %}
{% load staticfiles %}

{% block cluster_layer %}var clusterlayer{{ module }} = new L.MarkerClusterGroup();{% endblock %}

{% block layers_getson_extra %}
    clusterlayer{{ module }}.addLayer(geojsonlayer{{ module }});
    map{{ module }}.addLayer(clusterlayer{{ module }})
{% endblock %}
