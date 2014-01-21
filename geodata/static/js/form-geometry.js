// MapWidget init
var map_options = {
    maxExtend: new OpenLayers.Bounds(-20037508,-20037508,20037508,20037508),
    maxResolution: 156543.0339,
    numZoomLevels: 20,
    units: 'm'
};
var options = {
    geom_name: 'Point',
    id: 'id_geometry',
    map_id: 'id_geometry_map',
    map_options: map_options,
    map_srid: 3857,
    name: 'geodjango_geometry'
};
options['scale_text'] = true;
options['mouse_position'] = true;
options['base_layer'] = new OpenLayers.Layer.OSM.Mapnik("OpenStreetMap (Mapnik)");
var geodjango_geometry = new MapWidget(options);


// spin
$.fn.spin = function(opts) {
  this.each(function() {
    var $this = $(this),
    spinner = $this.data('spinner');
    if (spinner) spinner.stop();
    if (opts !== false) {
      opts = $.extend({color: $this.css('color')}, opts);
      spinner = new Spinner(opts).spin(this);
      $this.data('spinner', spinner);
    }
  });
  return this;
};

$(function() {
  $(".spinner-link").bind('click change',function() {
    var opts = {
      lines: 12, // The number of lines to draw
      length: 7, // The length of each line
      width: 5, // The line thickness
      radius: 10, // The radius of the inner circle
      color: '#fff', // #rbg or #rrggbb
      speed: 1, // Rounds per second
      trail: 66, // Afterglow percentage
      shadow: true // Whether to render a shadow
    };
    $("#spin").show().spin(opts);
  });
});

// searchNominatim
function searchNominatim(search_terms) {
  var nominatimSearchUrl = "https://open.mapquestapi.com/nominatim/v1/search.php?";
  var format = "json";
  var addressdetails = 1;
  var limit = 5;
  var params = "&format=" + format + "&addressdetails=" + addressdetails + "&limit=" + limit;
  var url = nominatimSearchUrl + params + '&q=' + search_terms;

  $.ajax({
    url: url,
    dataType: "json",
    type: 'GET',
    success: function (resp) {
        var items = [];
        $.each(resp, function(key, val) {
          items.push('<option value=' + val.display_name + ' lat=' + val.lat + ' lon=' + val.lon + ' minlat=' + val.boundingbox[0] + ' maxlat=' + val.boundingbox[1] + ' minlon=' + val.boundingbox[2] + ' maxlon=' + val.boundingbox[3] + '>' + val.display_name + ' ' + val.lat + ':' + val.lon + '</option>');
        });
        $('#search_results').html(items.join(''));
        $("#spin").spin(false);
    },
    error: function(e) {
        alert('Error: '+e);
    }  
  });
}

function updatePoint(lat,lon) {
  var point = "POINT(" + lon + " " + lat + ")";
  var wkt = geodjango_geometry.read_wkt(point);
  //geodjango_geometry.write_wkt(wkt);
  geodjango_geometry.write_wkt(wkt);
  geodjango_geometry.layers.vector.addFeatures([wkt]);
}

function panToLatLonZoom(lat, lon, zoom) {
  var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), geodjango_geometry.map.getProjectionObject());
  updatePoint(lonLat.lat,lonLat.lon);
  if (zoom != geodjango_geometry.map.getZoom())
    geodjango_geometry.map.setCenter(lonLat, zoom);
  else
    geodjango_geometry.map.panTo(lonLat, 10);
}

function panToLatLonBoundingBox(lat,lon,minlat,maxlat,minlon,maxlon,wkt) {
  var proj_EPSG4326 = new OpenLayers.Projection("EPSG:4326");
  var proj_map = geodjango_geometry.map.getProjectionObject();
  geodjango_geometry.map.zoomToExtent(new OpenLayers.Bounds(minlon,minlat,maxlon,maxlat).transform(proj_EPSG4326, proj_map));
  //var lonLat = new OpenLayers.LonLat(lon, lat).transform(proj_EPSG4326, proj_map);
  var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), geodjango_geometry.map.getProjectionObject());
  geodjango_geometry.map.panTo(lonLat, 2);

  updatePoint(lonLat.lat,lonLat.lon);
}

function selectEntry(lat, lon, minlat, maxlat, minlon, maxlon) {
  $('#latitude').html(lat);
  $('#longitude').html(lon);
  panToLatLonBoundingBox(lat, lon, minlat, maxlat, minlon, maxlon);
}
