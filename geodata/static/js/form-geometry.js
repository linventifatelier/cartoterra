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
  var nominatimSearchUrl = "https://nominatim.openstreetmap.org/search?";
  var format = "json";
  var addressdetails = 1;
  var limit = 5;
  var params = "&format=" + format + "&addressdetails=" + addressdetails + "&limit=" + limit;
  var url = nominatimSearchUrl + 'q=' + search_terms + params;

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

function selectEntry(lat, lon, minlat, maxlat, minlon, maxlon) {
  $('#latitude').html(lat);
  $('#longitude').html(lon);
  panToLatLonBoundingBox(lat, lon, minlat, maxlat, minlon, maxlon);
}
