{% load l10n %}

{% block vars %}var {{ module }} = {};
{{ module }}.map = null; {{ module }}.controls = null; {{ module }}.panel = null; {{ module }}.bounds = null; {{ module }}.layers = {};
{% endblock %}

get_popup_content = function(feature){
    if (feature.attributes.image) {
        return "<a href=" + feature.attributes.url + ">" + "<h1>" + feature.attributes.name + "</h1></a>" + "<p><a href=" + feature.attributes.url + "><img src=\""  + feature.attributes.image + "\"></a></p>"
    } else {
        return "<a href=" + feature.attributes.url + ">" + "<h1>" + feature.attributes.name + "</h1></a>" + "<p>no photo</p>"
    };
}

{{ module }}_init = function(){
    {{ module }}.bounds = new OpenLayers.Bounds();
    
    {{ module }}.map = new OpenLayers.Map('{{ module }}_map', {theme: null});
    
    {{ module }}.base_layer = new OpenLayers.Layer.OSM("OpenStreetMap (Mapnik)");

    LOADED_LAYERS = 0;

    {% for layer in map_layers %}

    {{ module }}.layers[{{ forloop.counter0 }}] = new OpenLayers.Layer.Vector("{{ layer.name }}", {
        style: {
            externalGraphic: '{{ layer.external_graphic }}',
            graphicWidth: '{{ layer.graphic_width }}',
            graphicHeight: '{{ layer.graphic_height }}',
            fillColor: '{{ layer.fill_color }}',
            strokeColor: '{{ layer.stroke_color }}',
        },
        strategies: [new OpenLayers.Strategy.BBOX()],
        eventListeners: {           
            'loadend': function (evt) {
                LOADED_LAYERS++;
                {{ module}}.bounds.extend({{ module }}.layers[{{ forloop.counter0 }}].getDataExtent());
                if (LOADED_LAYERS == {{ map_layers|length }}) {
                    {{ module }}.map.zoomToExtent({{ module }}.bounds);
                };
            },
            'featureselected':function(evt){
                var feature = evt.feature;
                console.log(feature);
                var popup = new OpenLayers.Popup.Anchored("popup",
                    OpenLayers.LonLat.fromString(feature.geometry.toShortString()),
                    null,
                    get_popup_content(feature),
                    null,
                    true,
                    null
                );
                popup.autoSize = true;
                popup.maxSize = new OpenLayers.Size(400,800);
                popup.fixedRelativePosition = true;
                feature.popup = popup;
                {{ module }}.map.addPopup(popup);
            },
            'featureunselected':function(evt){
                var feature = evt.feature;
                {{ module }}.map.removePopup(feature.popup);
                feature.popup.destroy();
                feature.popup = null;
            }
        },
        protocol: new OpenLayers.Protocol.HTTP({
           url: '{{ layer.url }}',
           format: new OpenLayers.Format.GeoJSON()
        })
    });
    {% endfor %}

    {{ module }}.map.addLayers([{{ module }}.base_layer{% for layer in map_layers %}, {{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}]);

    var select = new OpenLayers.Control.SelectFeature([{% for layer in map_layers %}{% if forloop.first %}{% else %}, {% endif %}{{ module }}.layers[{{ forloop.counter0 }}]{% endfor %}], {'toggle' : true, 'clickout' : true});
    {{ module }}.map.addControl(select);
    select.activate();

    {{ module }}.panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});

    {{ module }}.map.addControl(new OpenLayers.Control.LayerSwitcher());

    {{ module }}.map.zoomIn();
}
