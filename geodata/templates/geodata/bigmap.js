{% extends "geodata/map_base.js" %}
{% load l10n %}
{% load i18n %}
{% load staticfiles %}

{% block cluster_layer %}
var clusterlayer{{ module }} = new L.markerClusterGroup();
var declusterlayer{{ module }} = new L.layerGroup();
{% endblock %}

{% block layers_getson_extra %}
    clusterlayer{{ module }}.addLayer(geojsonlayer{{ module }});
    map{{ module }}.addLayer(clusterlayer{{ module }});
    declusterlayer{{ module }}.addLayer(geojsonlayer{{ module }});
{% endblock %}


{% block extra_layers %}
var datacontrol{{ module }} = '';

function closegeodatacontrol{{ module }} () {
    $('#{{ module }}_map').removeClass('col-md-9 col-sm-8 col-xs-6');
    $('#{{ module }}_toolbox').removeClass('col-md-3 col-sm-4 col-xs-6');
    $('#{{ module }}_toolbox').css("display", "none");
    $('.geodata-toolbox-tool').css("display", "none");
    datacontrol{{ module }} = '';
};

function togglegeodatacontrol{{ module }} (control) {
    return function () {
        if (datacontrol{{ module }} == control) {
            closegeodatacontrol{{ module }}();
        } else if (datacontrol{{ module }} == '') {
            $('#{{ module }}_map').addClass('col-md-9 col-sm-8 col-xs-6');
            $('#{{ module }}_toolbox').addClass('col-md-3 col-sm-4 col-xs-6');
            $('#{{ module }}_toolbox').css("display", "block");
            $(control).css("display", "block");
            datacontrol{{ module }} = control;
        } else {
            $('.geodata-toolbox-tool').css("display", "none");
            $(control).css("display", "block");
            datacontrol{{ module }} = control;
        };
    };
};

L.Control.Data{{ module }} = L.Control.extend(
{
    options:
    {
        position: 'topright',
    },
    onAdd: function (map) {
        var controlDiv = L.DomUtil.create('div', 'leaflet-control-toolbar leaflet-bar');
        var controlDataDiv = L.DomUtil.create('a', 'leaflet-control-data', controlDiv);
        controlDataDiv.title = '{% trans "Select data to show" %}';
        controlDataDiv.href = '#';
        L.DomEvent
            .addListener(controlDataDiv, 'click', L.DomEvent.stopPropagation)
            .addListener(controlDataDiv, 'click', L.DomEvent.preventDefault)
            .addListener(controlDataDiv, 'click', togglegeodatacontrol{{ module }}('#{{ module }}_toolbox_filter'));
        var controlAddDiv = L.DomUtil.create('a', 'leaflet-control-add', controlDiv);
        controlAddDiv.title = '{% trans "Add a geodata" %}';
        controlAddDiv.href = '#';
        L.DomEvent
            .addListener(controlAddDiv, 'click', L.DomEvent.stopPropagation)
            .addListener(controlAddDiv, 'click', L.DomEvent.preventDefault)
            .addListener(controlAddDiv, 'click', togglegeodatacontrol{{ module }}('#{{ module }}_toolbox_add'));
        return controlDiv;
    }
});
var dataControl{{ module }} = new L.Control.Data{{ module }}();
map{{ module }}.addControl(dataControl{{ module }});

var cluster{{ module }} = true;

L.Control.Decluster{{ module }} = L.Control.extend(
{
    options:
    {
        position: 'topright',
    },
    onAdd: function (map) {
        var controlDiv = L.DomUtil.create('div', 'leaflet-control-toolbar leaflet-bar');
        L.DomEvent
            .addListener(controlDiv, 'click', L.DomEvent.stopPropagation)
            .addListener(controlDiv, 'click', L.DomEvent.preventDefault)
        .addListener(controlDiv, 'click', function () {
            if (cluster{{ module }}) {
                map{{ module }}.removeLayer(clusterlayer{{ module }});
                map{{ module }}.addLayer(declusterlayer{{ module }});
                cluster{{ module }} = false;
            } else {
                map{{ module }}.removeLayer(declusterlayer{{ module }});
                map{{ module }}.addLayer(clusterlayer{{ module }});
                cluster{{ module }} = true;
            };
        });

        var controlUI = L.DomUtil.create('a', 'leaflet-control-cluster', controlDiv);
        controlUI.title = 'Cluster ON/OFF';
        controlUI.href = '#';
        return controlDiv;
    }
});
var declusterControl{{ module }} = new L.Control.Decluster{{ module }}();
map{{ module }}.addControl(declusterControl{{ module }});

var hasclustercontrol{{ module }} = true;

function initFilter () {
    if (hasclustercontrol{{ module }}) {
        map{{ module }}.removeControl(declusterControl{{ module }});
        hasclustercontrol{{ module }} = false;
    }
    if (cluster{{ module }}) {
        map{{ module }}.removeLayer(clusterlayer{{ module }});
        map{{ module }}.addLayer(declusterlayer{{ module }});
        cluster{{ module }} = false;
    };
};

function geodataCheckbox (id, markerclassname) {
    $(id).change(function(event) {
        initFilter();
        var checkbox = event.target;
        $('.' + markerclassname).each(function () {
            var valhide = $(this).data("geodata-marker-hide") || 0;
            var valdatehide = $(this).data("geodata-marker-date-hide") || 0;
            if (checkbox.checked) {
                valhide--;
            } else {
                valhide++;
            };
            $(this).data("geodata-marker-hide", valhide);
            if (valhide + valdatehide > 0) {
                $(this).css("display", "none");
            } else {
                $(this).css("display", "");
            };
        });
    });
};

function dateFromString (str) {
    if (str) {
        var datearray = str.split("-");
        var date = new Date(datearray[0], datearray[1] - 1, datearray[2]);
        return date;
    } else {
        return null;
    }
};

function geodataDateCheckbox (id, start, end) {
    $(id).add(start).add(end).change(function(event) {
        initFilter();
        var checkboxchecked = $('#dateCheckbox').is(':checked');
        var startdate = dateFromString($(start).val());
        var enddate = dateFromString($(end).val());

        $('.geodata-marker-nodate').each(function () {
            var valdatehide = 0;
            var valhide = $(this).data("geodata-marker-hide") || 0;
            if (checkboxchecked) {
                valdatehide = 1;
            };
            $(this).data("geodata-marker-date-hide", valdatehide);
            if (valhide + valdatehide > 0) {
                $(this).css("display", "none");
            } else {
                $(this).css("display", "");
            };
        });

        $('[class^=geodata-marker-date-],[class*= geodata-marker-date-]').each(function () {
            var valdatehide = 0;
            var valhide = $(this).data("geodata-marker-hide") || 0;
            if (checkboxchecked && startdate && enddate) {
                var datematch = $(this).attr('class').match(/geodata-marker-date-([0-9-]+)/);
                var date = dateFromString(datematch[1]);
                if (!(date >= startdate && date <= enddate)) {
                    valdatehide = 1;
                };
            };
            $(this).data("geodata-marker-date-hide", valdatehide);
            if (valhide + valdatehide > 0) {
                $(this).css("display", "none");
            } else {
                $(this).css("display", "");
            };
        });
    });
};

geodataDateCheckbox('#dateCheckbox', '#dateStart', '#dateEnd');

{% for type in types %}
geodataCheckbox('#{{ type.name|lower|escapejs }}TypeCheckbox', 'geodata-marker-type-{{ type.name|lower|escapejs }}');
{% if type.subtypes %}
{% for subtype in type.subtypes %}
geodataCheckbox('#{{ type.name|lower|escapejs }}{{ subtype.ident_name|lower|escapejs }}SubTypeCheckbox', 'geodata-marker-subtype-{{ type.name|lower|escapejs }}-{{ subtype.ident_name|lower|escapejs }}');
{% endfor %}
{% endif %}
{% endfor %}

{% for technique in techniques %}
geodataCheckbox('#{{ technique.name|lower|escapejs }}TechniqueCheckbox', 'geodata-marker-technique-{{ technique.name|lower|escapejs }}');
{% endfor %}
geodataCheckbox('#techniqueNoneCheckbox', 'geodata-marker-notechnique');
{% endblock %}
