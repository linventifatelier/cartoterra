{% load l10n %}
{% load staticfiles %}

var map{{ module }} = L.map('{{ module }}_map', { zoomControl: false }).setView([0, 0], 2);

new L.control.zoom({ position: 'topright' }).addTo(map{{ module }});

var clusterlayer{{ module }} = new L.MarkerClusterGroup();

{{ module }}info = $('#{{ module }}_info');

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
    console.debug(feature.properties);
    {{ module }}info.find('.geodata-info-detail').attr('href', feature.properties.url);
    {{ module }}info.modal();
}

function importFeature (feature, layer) {
    layer.on({
        click: gotoFeature
    });
};

{% for layer in map_layers %}
$.getJSON("{{ layer.url }}", function(data) {
    function getIconFromFeature (feature) {
        if (feature.properties.isceah) {
            return L.icon({
                shadowUrl: '{{ layer.external_graphic }}',
                shadowSize: [24, 24],
                shadowAnchor: [12,12],
                iconUrl: '{% static "img/isceah_blanc.png" %}',
                iconSize: [24, 24],
                iconAnchor: [12, 12],
            })
        } else {
            return L.icon({
                iconUrl: '{{ layer.external_graphic }}',
                iconSize: [24, 24],
                iconAnchor: [12, 12],
            })
        }
    };
    function placePointToLayer (feature, latlng) {
        return L.marker(latlng, { icon: getIconFromFeature(feature) });
    };
    var geojsonlayer{{ module }} = L.geoJson(data, {
        pointToLayer: placePointToLayer,
        onEachFeature: importFeature
    });
    clusterlayer{{ module }}.addLayer(geojsonlayer{{ module }});
    map{{ module }}.addLayer(clusterlayer{{ module }})
});
{% endfor %}

// add an OpenStreetMap tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors",
    minZoom: 2,
    maxZoom: 20
}).addTo(map{{ module }});
