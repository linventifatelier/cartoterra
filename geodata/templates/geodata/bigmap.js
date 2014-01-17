{% load l10n %}

{% block vars %}var {{ module }} = {};
{{ module }}.map = null; {{ module }}.controls = null; {{ module }}.panel = null; {{ module }}.bounds = null; {{ module }}.layers = {}; {{ module }}.info = null; {{ module }}.popoverTopLimit = 120; {{ module }}.popup = null;
{% endblock %}

{{ module }}_init = function(){
    var base_layer = new ol.layer.Tile({
        source: new ol.source.OSM(),
    });

    {% for layer in map_layers %}
    {{ module }}.layers[{{ forloop.counter0 }}] = new ol.layer.Vector({
        source: new ol.source.Vector({
            parser: new ol.parser.GeoJSON(),
            url: '{{ layer.url }}'
        }),
        style: new ol.style.Style({
            symbolizers: [
                new ol.style.Icon({
                    url: '{{ layer.external_graphic }}',
                })
            ]
        }),
        transformFeatureInfo: function(features) {
            if (features.length > 0) {
                var content = {};
                content.name = features[0].get('name');
                content.url = features[0].get('url');
                content.image = features[0].get('image');
                content.geometry = features[0].getGeometry();
                content.coordinates = features[0].getGeometry().getCoordinates();
                return content;
            };
        }
    });
    {% endfor %}

    {{ module }}.map = new ol.Map({
        target: '{{ module }}_map',
        layers: [
            base_layer{% for layer in map_layers %}, {{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}
        ],
        renderer: ol.RendererHint.CANVAS,
        view: new ol.View2D({
          center: [0, 0],
          zoom: 2
        })
    });

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

    $({{ module }}.map.getViewport()).on('mousemove', function(evt) {
      var pixel = {{ module }}.map.getEventPixel(evt.originalEvent);
      var position = {{ module }}.map.getEventCoordinate(evt.originalEvent);
      {{ module }}.map.getFeatureInfo({
        pixel: pixel,
        layers: [{% for layer in map_layers %}{% if forloop.first %}{% else %}, {% endif %}{{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}],
        success: function(layerFeatures) {
          var flattenFeatures = [];
          for (i = 0; i < layerFeatures.length; i++ ) {
              if (layerFeatures[i]) {
                 flattenFeatures = flattenFeatures.concat(layerFeatures[i]);
              }
          }
          var feature = flattenFeatures[0];
          if (feature) {
            {{ module }}.popup.setPosition([feature.coordinates[0], feature.coordinates[1] - 150000]);
            var content = "";
            if (feature.image) {
                content = "<a href=\"" + feature.url + "\"><img src=\""  + feature.image + "\"></a>"
            };
            {{ module }}.info.popover('hide')
                .attr('data-original-title', "<a href=\"" + feature.url + "\">"  + feature.name + "</a>")
                .attr('data-content', content)
                .popover('show');
          } else {
            {{ module }}.info.popover('hide');
          }
        }
      });
    });

    $({{ module }}.map.getViewport()).on('click', function(evt) {
      var pixel = {{ module }}.map.getEventPixel(evt.originalEvent);
      {{ module }}.map.getFeatures({
        pixel: pixel,
        layers: [{% for layer in map_layers %}{% if forloop.first %}{% else %}, {% endif %}{{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}],
        success: function(layerFeatures) {
          var flattenFeatures = [].concat.apply([], layerFeatures);
          var feature = flattenFeatures[0];
          if (feature) {
            window.location.href = feature.e.url;
          } else {
          }
        }
      });
    });
}
