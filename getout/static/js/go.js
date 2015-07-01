(function (root) {

  "use strict";

  var go = root.GetOut = {};
  go.map = null;
  go.center = {lat: 0.0, lng: 0.0};

  // Design for the location marker.
  var loc_marker = [
    {
      offset: '0%',
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 8,
        fillColor: "steelblue",
        fillOpacity: 0.5,
        strokeWeight: 0
      }
    }, {
      offset: '0%',
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 4,
        fillColor: "steelblue",
        fillOpacity: 1,
        strokeColor: "white",
        strokeWeight: 1.5
      }
    }
  ];

  // The geolocation function.
  go.map_w_geo = function (map_id, old_lat, old_lng, callback) {
    var zoom = 8;
    if (typeof old_lat === "undefined" || typeof old_lng === "undefined") {
      old_lat = 0.0;
      old_lng = 0.0;
      zoom = 1;
    }
    go.center = {lat: old_lat, lng: old_lng};
    var opts = {
      center: go.center, zoom: zoom,
      disableDefaultUI: true, zoomControl: true,
      styles: [{featureType: "poi.business", stylers: [{ visibility: "off" }]}]
    };

    // Create the map.
    go.map_id = map_id;
    go.map = new google.maps.Map(document.getElementById(map_id), opts);

    // Fail immediately if there is no geolocation.
    if (!navigator.geolocation) {
      no_geo(false);
      return;
    }

    // A call back to handle the response from the geolocation call.
    function handle_pos (position) {
      var lat = position.coords.latitude,
          lng = position.coords.longitude,
          pos = new google.maps.LatLng(lat, lng);

      // Add the location marker.
      new google.maps.Polyline({path: [pos, pos], icons: loc_marker, map: go.map});
      go.center = pos;
      go.map.panTo(pos);
      go.map.setZoom(15);

      // Call the location callback.
      if (typeof callback !== "undefined") callback(lat, lng);
    }

    // Execute the geolocation call.
    navigator.geolocation.getCurrentPosition(handle_pos, function(){no_geo(true)});
  }

  // Handle errors in the geolocation.
  function no_geo(flg) {
    var content;
    if (flg) content = "Error: The Geolocation service failed.";
    else content = "Error: Your browser doesn't support geolocation.";
    var opts = {map: go.map, position: go.map.getCenter(), content: content},
        infowindow = new google.maps.InfoWindow(opts);
  }

})(this);
