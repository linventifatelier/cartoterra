{% load l10n %}

{% block vars %}var {{ module }} = {};
{{ module }}.map = null; {{ module }}.panel = null; {{ module }}.layers = {}; {{ module }}.layerstyle = {}; {{ module }}.info = null; {{ module }}.popup = null;
{% endblock %}

var base_layer = new ol.layer.Tile({
    source: new ol.source.OSM(),
});

{% for layer in map_layers %}
{{ module }}.layerstyle[{{ forloop.counter0 }}] = [new ol.style.Style({
        image: new ol.style.Icon(({
                src: '{{ layer.external_graphic }}',
              }))
    })];

{{ module }}.layers[{{ forloop.counter0 }}] = new ol.layer.Vector({
    source: new ol.source.GeoJSON({
        projection: 'EPSG:3857',
        url: '{{ layer.url }}'
    }),
    style: function(feature, resolution) {
        return {{ module }}.layerstyle[{{ forloop.counter0 }}];
    }
});
{% endfor %}

{{ module }}.map = new ol.Map({
    layers: [
        base_layer{% for layer in map_layers %}, {{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}
    ],
    renderer: 'canvas',
    target: document.getElementById('{{ module }}_map'),
    view: new ol.View2D({
      center: [-2400000, 3000000],
      zoom: 2
    }),
    controls: [new ol.control.Attribution(), new ol.control.Logo()]
});

{{ module }}.map.addControl(new ol.control.Zoom({target : document.getElementById('{{ module }}_controls')}));

{{ module }}.info = $('#{{ module }}_info');

{{ module }}.info.popover({
  animation: false,
  placement: 'bottom',
  container: '#{{ module }}_map',
  html: true,
  trigger: 'manual'
});

{{ module }}.popup = new ol.Overlay({
    element: document.getElementById('{{ module }}_info')
});
{{ module }}.map.addOverlay({{ module }}.popup);

{{ module }}.map.on('mousemove', function(evt) {
  var allFeaturesAtPixel = [];
  {{ module }}.map.forEachFeatureAtPixel(evt.pixel, function(feature) {
    allFeaturesAtPixel.push(feature);
  });

  if (allFeaturesAtPixel.length > 0) {
    var feature = allFeaturesAtPixel[0];
    var coordinates = feature.getGeometry().getCoordinates();
    var pixel = {{ module }}.map.getPixelFromCoordinate(coordinates);
    {{ module }}.popup.setPosition({{ module }}.map.getCoordinateFromPixel([pixel[0], pixel[1] + 5]));
    var content = "";
    if (feature.get('image')) {
        content = "<a href=\"" + feature.get('url') + "\"><img src=\""  + feature.get('image') + "\"></a>"
    };
    {{ module }}.info.popover('hide')
        .attr('data-original-title', "<a href=\"" + feature.get('url') + "\">"  + feature.get('name') + "</a>")
        .attr('data-content', content)
        .popover('show');
  } else {
    {{ module }}.info.popover('hide');
  }
});

{{ module }}.map.on('click', function(evt) {
  var allFeaturesAtPixel = [];
  {{ module }}.map.forEachFeatureAtPixel(evt.pixel, function(feature) {
    allFeaturesAtPixel.push(feature);
  });

  if (allFeaturesAtPixel.length > 0) {
    var feature = allFeaturesAtPixel[0];
    window.location.href = feature.get('url');
  }
});
