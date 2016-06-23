{% load l10n %}
{% load geodata %}

var map{{ module }} = L.map('{{ module }}_map', { zoomControl: false, attributionControl: false }).setView({{ geodata.geometry.coords | to_leaflet }}, 5);

new L.control.zoom({ position: 'topright' }).addTo(map{{ module }});

L.control.attribution().setPrefix('© <a href=\"{{ SITE_URL }}\">{{ SITE_NAME}}</a> contributors').addTo(map{{ module }});

{% for layer in map_layers %}
$.getJSON("{{ layer.url }}", function(data) {
    var icon{{ module }} = L.icon({
        iconUrl: '{{ layer.external_graphic }}',
        iconSize: [24, 24],
        iconAnchor: [12, 12],
    });
    function placePointToLayer (feature, latlng) {
        return L.marker(latlng, { icon: icon{{ module }} });
    };

    var geojsonlayer{{ module }} = L.geoJson(data, {
        pointToLayer: placePointToLayer,
    });
    map{{ module }}.addLayer(geojsonlayer{{ module }})
});
{% endfor %}

// add an OpenStreetMap tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© <a href=\"http://osm.org/copyright\">OpenStreetMap</a> contributors",
    minZoom: 2,
    maxZoom: 20
}).addTo(map{{ module }});
