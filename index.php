<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<title>Twitter Tracker</title>

<style type="text/css">
      html { height: 100% }
      body { height: 100%; margin: 0; padding: 0 }
      #map_canvas { height: 100% }
</style>
<script type="text/javascript" src="jsrefresh.js#js,notify"></script>
<script type="text/javascript" src="map.js?<?php echo time();?>"></script>
<script type="text/javascript">
function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&' +
      'callback=initialize';
  document.body.appendChild(script);
}

window.onload = loadScript;
</script>

</head>
<body>
	<div id="map_canvas"></div>
</body>
</html>
