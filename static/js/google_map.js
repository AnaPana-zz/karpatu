function initialize() {
    var myLatLng = {lat: 48.6266963, lng: 24.2079893};

    var mapCanvas = document.getElementById('map');
    var mapOptions = {
        center: myLatLng,
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(mapCanvas, mapOptions)

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'Stara Huta'
    });

    marker.setMap(map);

}

google.maps.event.addDomListener(window, 'load', initialize);