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

