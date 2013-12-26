{% load l10n %}

{% block vars %}var {{ module }} = {};
{{ module }}.map = null; {{ module }}.controls = null; {{ module }}.panel = null; {{ module }}.bounds = null; {{ module }}.layers = {};
{% endblock %}

var info = $('#{{ module }}_info');
info.tooltip({
  animation: false,
  trigger: 'manual'
});


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

var displayFeatureInfo = function(pixel) {
  info.css({
    left: pixel[0] + 'px',
    top: (pixel[1] - 15) + 'px'
  });
  {{ module }}.map.getFeatures({
    pixel: pixel,
    layers: [{% for layer in map_layers %}, {{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}],
    success: function(layerFeatures) {
      var feature = layerFeatures[0][0];
      console.debug("test");
      if (feature) {
        info.tooltip('hide')
            .attr('data-original-title', feature.get('name'))
            .tooltip('fixTitle')
            .tooltip('show');
      } else {
        info.tooltip('hide');
      }
    }
  });
};

//$({{ module }}.map.getViewport()).on('mousemove', function(evt) {
//  var pixel = map.getEventPixel(evt.originalEvent);
//  displayFeatureInfo(pixel);
//});


{{ module }}.map.on('click', function(evt) {
    var pixel = evt.getPixel();
    displayFeatureInfo(pixel);
});

}
