{% load staticfiles %}

{% block popup_detail %}
function gotoFeature (e) {
    var layer = e.target;
    var feature = layer.feature;

    var title = '<a href=\"' + feature.properties.url + '\"><span class=\"badge\"><span class="glyphicon glyphicon-star"></span><span>' + feature.properties.recommends + '</span></span> ' + feature.properties.name + '</a>'

    var image = ""
    if (feature.properties.image) {
        image = '<img class="img-thumbnail geodata-thumbnail" src=\"' + feature.properties.image + '\" alt=\"' + feature.properties.name + '\">';
    } else {
        image = '<div class="img-thumbnail geodata-thumbnail"><span class="glyphicon glyphicon-camera geodata-icon-empty"></span></div>'
    };
    {{ module }}info.find('.geodata-info-image').html(image);
    {{ module }}info.find('.modal-title').html(title);
    {{ module }}info.find('.geodata-info-content').html(feature.properties.summary);
    {{ module }}info.find('.geodata-info-detail').attr('href', feature.properties.url);
    {{ module }}info.modal();
};

function importFeature (feature, layer) {
    layer.on({
        click: gotoFeature
    });
};

{{ module }}info = $('#{{ module }}_info');
{% endblock %}

{% block map %}var map{{ module }} = L.map('{{ module }}_map', { zoomControl: false, attributionControl: false }){% block extra_map %}.setView([0, 0], 2){% endblock %};{% endblock %}

{% block zoom %}new L.control.zoom({ position: 'topright' }).addTo(map{{ module }});{% endblock %}

{% block attribution %}L.control.attribution().setPrefix('© <a href=\"{{ SITE_URL }}\">{{ SITE_NAME}}</a> contributors').addTo(map{{ module }});{% endblock %}

{% block cluster_layer %}{% endblock %}

{% block layers %}
{% for layer in map_layers %}
$.getJSON("{{ layer.url }}", function(data) {
    function getIconFromFeature (feature) {
        var size = [12, 12];
        var anchor = [6, 6];
        var classname = 'geodata-marker-type-' + feature.properties.type;

        if (feature.properties.simple) {
            size = [6, 6];
            anchor = [3, 3];
            classname = classname + ' geodata-marker-type-' + feature.properties.type + '-simple';
        };

        if (feature.properties.techniques.length > 0) {
            feature.properties.techniques.forEach(function(entry) {
                classname = classname + ' geodata-marker-technique-' + entry;
            });
        } else {
            classname = classname + ' geodata-marker-notechnique';
        };

        if (feature.properties.subtypes && feature.properties.subtypes.length > 0) {
            feature.properties.subtypes.forEach(function(entry) {
                classname = classname + ' geodata-marker-subtype-' + feature.properties.type + '-' + entry;
            });
        };

        if (feature.properties.date) {
            classname = classname + ' geodata-marker-date-' + feature.properties.date;
        } else {
            classname = classname + ' geodata-marker-nodate'
        };

        return L.icon({
            iconUrl: '{{ layer.external_graphic }}',
            iconSize: size,
            iconAnchor: anchor,
            className: classname,
        })
    };
    function placePointToLayer (feature, latlng) {
        return L.marker(latlng, { icon: getIconFromFeature(feature) });
    };
    var geojsonlayer{{ module }} = L.geoJson(data, {
        pointToLayer: placePointToLayer,
        onEachFeature: importFeature,
        className: 'geodata-layer-{{ layer.name|lower|escapejs }}',
    });
    {% block layers_getson_extra %}
    {% endblock %}
});
{% endfor %}
{% endblock %}

{% block extra_layers %}{% endblock %}

{% block osm_layer %}
// add an OpenStreetMap tile layer
var osmlayer{{ module }} = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors",
    minZoom: 2,
    maxZoom: 20
});

osmlayer{{ module }}.addTo(map{{ module }});
{% endblock %}
