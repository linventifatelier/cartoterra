{% load l10n %}

{% block vars %}var {{ module }} = {};
{{ module }}.map = null; {{ module }}.controls = null; {{ module }}.panel = null; {{ module }}.bounds = null; {{ module }}.layers = {}; {{ module }}.info = null;
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
        })
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
      placement: 'top',
      html: true,
      trigger: 'manual'
    });

    var displayFeatureInfo = function(pixel) {
      {{ module }}.info.css({
        left: pixel[0] + 'px',
        top: (pixel[1] - 5) + 'px'
      });
      {{ module }}.map.getFeatures({
        pixel: pixel,
        layers: [{% for layer in map_layers %}{% if forloop.first %}{% else %}, {% endif %}{{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}],
        success: function(layerFeatures) {
          var feature = layerFeatures[0][0];
          if (feature) {
            {{ module }}.info.popover('hide')
                .attr('data-original-title', feature.e.name)
                .attr('data-content', "<img src=\""  + feature.e.image + "\">")
                .popover('show');
          } else {
            {{ module }}.info.popover('hide');
          }
        }
      });
    };

    var goToFeature = function(pixel) {
      {{ module }}.map.getFeatures({
        pixel: pixel,
        layers: [{% for layer in map_layers %}{% if forloop.first %}{% else %}, {% endif %}{{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}],
        success: function(layerFeatures) {
          var feature = layerFeatures[0][0];
          if (feature) {
            window.location.href = feature.e.url;
          } else {
          }
        }
      });
    };

    $({{ module }}.map.getViewport()).on('mousemove', function(evt) {
      var pixel = {{ module }}.map.getEventPixel(evt.originalEvent);
      displayFeatureInfo(pixel);
    });

    $({{ module }}.map.getViewport()).on('click', function(evt) {
      var pixel = {{ module }}.map.getEventPixel(evt.originalEvent);
      goToFeature(pixel);
    });

}
