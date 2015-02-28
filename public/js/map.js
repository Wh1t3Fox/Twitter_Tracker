function initialize() {
	var centerlatlng = new google.maps.LatLng(35.650000, -97.466700);
	var myOptions = {
		zoom: 5,
		center: centerlatlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

	var latlng = new google.maps.LatLng(35.6500, -97.4667);
	var img = new google.maps.MarkerImage('http://chart.apis.google.com/chart?cht=mm&chs=12x16&chco=FFFFFF,FF0000,000000&ext=.png');
	var marker = new google.maps.Marker({
	title: "@USERNAME",
	icon: img,
	position: latlng
	});
	marker.setMap(map);

	var latlng = new google.maps.LatLng(40.6500, -80.4667);
	var img = new google.maps.MarkerImage('http://chart.apis.google.com/chart?cht=mm&chs=12x16&chco=FFFFFF,FF0000,000000&ext=.png');
	var marker = new google.maps.Marker({
	title: "@USERNAME",
	icon: img,
	position: latlng
	});
	marker.setMap(map);

	

	var PolylineCoordinates = [
		new google.maps.LatLng(35.6500, -97.4667),
		new google.maps.LatLng(40.6500, -80.4667),
	];

	var lineSymbol = { 
		path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW 
	}; 
	var Path = new google.maps.Polyline({
		clickable: false,
		geodesic: true,
		path: PolylineCoordinates,
		icons: [{ 
			icon: lineSymbol,
			offset: "100%"
		}],
		strokeColor: "#0000FF",
		strokeOpacity: 1.000000,
		strokeWeight: 2
	});

	Path.setMap(map);


}
