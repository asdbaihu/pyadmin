from beaker.middleware import SessionMiddleware
import importlib
def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import geo.login
	importlib.reload(geo.login)

	from geo import login
	

	# Get the session object from the environ
	session = environment['beaker.session']

	# Check to see if a value is in the session
	user = 'username' in session
	passwd = 'password' in session

	# Set some other session variable
	#session['user_id'] = 10
	#user_id = 'user_id' in session

	if not 'username' in session:
		page = login.loginform
	elif not 'password' in session:
		page = login.loginform
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,psycopg2.extras,psycopg2.extensions,importlib,geo.module,geo.conn
		importlib.reload(geo.conn)
		importlib.reload(geo.module)
		
		from geo.conn import conn

		try:
			con = psycopg2.connect(conn)
		except:
			page ="Can not access databases"
		
		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = login.login_again
		else:
			#if int(ps[0][2]) == 2:
			importlib.reload(geo.module)
			from geo.module import head,headlink,menuadmin,menuuser
			from requests import get
			ip = get('https://api.ipify.org').text

			if not 'display' in post:
				display = 1200
			else:
				display = post['display']	
			if not 'key' in post:
				key = 'Lastvisited'
			else:
				key = post['key']					
			
			if not 'member' in post:
				member = ''
			else:
				member = post['member']
				
			if not 'lon' in post:
				lon = ''
			else:
				lon = post['lon']
			if not 'lat' in post:
				lat = ''
			else:
				lat = post['lat']
			if not 'unit' in post:
				unit =''
			else:
				unit = post['unit']	
			if not 'radius' in post:
				radius = 0
			else:
				radius = post['radius']
			
			page=""
			page += head
			page += """<title>Edit%s</title>"""%key.upper()
			page += headlink
			page += """
		
			</head>
			<body>
			<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
				<div class="container">
				<div class="navbar-collapse collapse">
					<ul class="nav navbar-nav">"""

			if int(ps[0][2]) == 2:
				page += menuadmin
			else:
				page += menuuser
				
			page += """</ul>
						</div></div>
						</nav>								
						<br />
						<br />
"""

			page += """<ul class="nav nav-tabs">
							<li class="active"><a href="/wsgi/geo/control/geo">Edit <span class="uppercase">%s</span></a></li>
						</ul>
						
								  """%(key)
			page +=	"""
			
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD0p8hcMhiLWNOXQEOlQBbEqmL7qYRZ7e4&callback=initMap" async defer></script>

<section id="result"></section>
<section id="gMap"></section>

<script>
var result = document.querySelector('#result');
navigator.geolocation.getCurrentPosition(geoFunc, errFunc)
			
function geoFunc(e){
          console.log(e);
				var lati = e.coords.latitude;
				var loti = e.coords.longitude;
				var accu = e.coords.accuracy;
				result.innerHTML = 'Latitude: '+lati+'<br>Longitude: '+loti+'<br>Accuracy: '+accu;
				// Google Map
				var mapcanvas = document.createElement('div');
				mapcanvas.id = 'mapcontainer';
				mapcanvas.style.height = '400px';
				mapcanvas.style.width = '600px';
				document.querySelector('#gMap').appendChild(mapcanvas);
				var coords = new google.maps.LatLng(lati,loti);
				var options = {
					zoom: 15,
					center: coords,
					mapTypeControl: true,
					navigationControlOptions: {
						style: google.maps.NavigationControlStyle.SMALL
					},
					mapTypeId: google.maps.MapTypeId.ROADMAP
				};
				var map = new google.maps.Map(document.getElementById("mapcontainer"), options);
				var marker = new google.maps.Marker({
				    position: coords,
				    map: map,
				    title:"You are here!"
				});
				var infowindow = new google.maps.InfoWindow({
	          		content: 'Here your position. <br> Latitude: '+lati+'. Longitude: '+loti+'<br>',
	          		position: coords
        		});
        		infowindow.open(map);
			}
function errFunc(e){
				console.log(e);
				// PERMISSION_DENIED: 1
				// POSITION_UNAVAILABLE: 2
				// TIMEOUT: 3
}

</script>

<div id="handsontable">		

<p>Click to get your position</p>
<button onclick="getLocation()">Get your position</button>
<p> Your public ip: %s </p>
<div id='console5'></div>
<p id="demo5"></p>

<script>
/*$.getJSON('//freegeoip.net/json/?callback=?', function(data) {
  //console.log(JSON.stringify(data, null, 2));
  var $console  = $("#console5");
  $console.text(JSON.stringify(data, null, 2));
});*/
var x = document.getElementById("demo5");

function getLocation() {
if (navigator.geolocation) {
navigator.geolocation.getCurrentPosition(showPosition);
} else {
x.innerHTML = "Geolocation do not support your browser.";
}
}

function showPosition(position) {
x.innerHTML = "Latitude: <span id='lat'>" + position.coords.latitude +"</span><br>Longtitude: <span id='lon'>" + position.coords.longitude+"</span>";
}
//getLocation();
</script>			
			
					<br />
							<form method="post" action="">
							Key: <input class="input-mini-1" type="text" name="key" value = "%s" /> | 
							Member: <input class="input-mini-1" type="text" name="member" value = "%s" /> |
							Lon : <input class="input-mini-1" type="text" name="lon" value = "%s" /> |
							Lat : <input class="input-mini-1" type="text" name="lat" value = "%s" /> |
							Radius : <input class="input-mini-1" type="number" name = "radius" value ="%s" required /> |
							Unit of length : <input class="input-mini-1" type="text" name="unit" value ="%s" placeholder = 'km,m,ft,mile'/> """%(ip,key,member,lon,lat,radius,unit)		
			page += """
			<input type="submit" value="Submit" />
							</form>
 <p>
	<button name="load" id="load_dog">Load</button>
  </p>
	<div>
  <span id="exampleConsole" class="console">Click "Load" to load data from server </span> | 
						<span class="page2">No page selected</span> 
  </div>
  <div id="example1" style="width:100%; height: 500px; overflow: hidden"></div>
  <div class="demo2"></div>
</div> <!-- handsontable -->
  <script>
	  var
	  $container = $("#example1"),
	  $console = $("#exampleConsole"),
	  $parent = $container.parent(),
	  autosaveNotification,
	  hot;
	$parent.find('button[name=load]').click(function () {
	  $.ajax({
		url: '/wsgi/geo/load/load_radius',"""
			page+="""data: {key:"%s",member:"%s",lon:"%s",lat:"%s",radius:"%s",unit:"%s"},"""%(key,member,lon,lat,radius,unit)
			page += """	dataType: 'json',
						type: 'POST',					
			success: function (res) {
			$console.text(res);
										},
			error: function () {
			  $console.text('Data reset failed');
			}										

	  });
	}).click(); // execute immediately

  </script>


</body>
</html>
"""


		con.commit()
		cur.close()
		con.close()	
					
			#request.headers['Cookie']
	response = Response(body = page,
	content_type = "text/html",
	charset = "utf8",
	status = "200 OK")

	return response(environment, start_response)
session_opts = {
	'session.type': 'file',
	'session.cookie_expires': True,
	'session.data_dir': '/tmp',
	'session.path':'/wsgi/geo',
	#'session.domain':'domain.com',
	'session.auto': True
}

application = SessionMiddleware(application, session_opts)
