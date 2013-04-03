function searchNominatim(search_terms) {
  var nominatimSearchUrl = "http://nominatim.openstreetmap.org/search?q=";
  var format = "json";
  var acceptlanguage = "en";
  var addressdetails = 1;
  var limit = 5;
  var params = "&format=" + format + "&accept-language=" + acceptlanguage + "&addressdetails=" + addressdetails + "&limit=" + limit;
  var url = nominatimSearchUrl + search_terms + params;

  $.ajax({
    url: url,
    dataType: "json",
    type: 'GET',
    success: function (resp) {
        var items = [];
        $.each(resp, function(key, val) {
          items.push('<option value=' + val.display_name + ' lat=' + val.lat + ' lon=' + val.lon + ' minlat=' + val.boundingbox[0] + ' maxlat=' + val.boundingbox[1] + ' minlon=' + val.boundingbox[2] + ' maxlon=' + val.boundingbox[3] + '>' + val.display_name + ' ' + val.lat + ':' + val.lon + '</option>');
        });
        console.debug(items);
        $('#search_results').html(items.join(''));
    },
    error: function(e) {
        alert('Error: '+e);
    }  
  });
}

function updatePoint(lat,lon) {
  var point = "POINT(" + lon + " " + lat + ")";
  var wkt = {{ module }}.read_wkt(point);
  {{ module }}.write_wkt(wkt);
  {{ module }}.layers.vector.addFeatures([wkt]);
}

function panToLatLon(lat,lon) {
  var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), {{ module }}.map.getProjectionObject());
  {{ module }}.map.panTo(lonLat, 2);

  updatePoint(lonLat.lat,lonLat.lon);
}

function panToLatLonZoom(lat, lon, zoom) {
  var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), {{ module }}.map.getProjectionObject());
  if (zoom != {{ module }}.map.getZoom())
    {{ module }}.map.setCenter(lonLat, zoom);
  else
    {{ module }}.map.panTo(lonLat, 10);
}

function panToLatLonBoundingBox(lat,lon,minlat,maxlat,minlon,maxlon,wkt) {
  var proj_EPSG4326 = new OpenLayers.Projection("EPSG:4326");
  var proj_map = {{ module }}.map.getProjectionObject();
  {{ module }}.map.zoomToExtent(new OpenLayers.Bounds(minlon,minlat,maxlon,maxlat).transform(proj_EPSG4326, proj_map));
  var lonLat = new OpenLayers.LonLat(lon, lat).transform(proj_EPSG4326, proj_map);
  {{ module }}.map.panTo(lonLat, 2);

  updatePoint(lonLat.lat,lonLat.lon);
}

function selectEntry(lat, lon, minlat, maxlat, minlon, maxlon) {
  $('#latitude').html(lat);
  $('#longitude').html(lon);
  panToLatLonBoundingBox(lat, lon, minlat, maxlat, minlon, maxlon);
}

