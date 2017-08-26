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
				key = 'Sicily'
			else:
				key = post['key']					

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
			
<div id='map'></div>

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
getLocation();
</script>			
			
					<br />
							<form method="post" action="">
							Key: <input class="input-mini-1" type="text" name="key" value = "%s" /> | 
							Row : <input class="input-mini" type="number" name ="display" value = %s />"""%(ip,key, display)		
			page += """		<input type="submit" value="Submit" />
							</form>

  <p>
	<button name="load" id="load_dog">Load</button>
	<!--<button name="save">Save</button>-->
	<button name="reset">Reset</button>
	<label><input type="checkbox" name="autosave" checked="checked" autocomplete="off"> Autosave</label>
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
	  localStorage['update_len'] = 0;
	  localStorage['insert_len']= 0;
	  hot = new Handsontable($container[0], {
	  columnSorting: true,
	  manualColumnResize: true,
	  startRows: 8,
	  startCols: 14,
	  rowHeaders: true,"""
			page +="""colHeaders: ["Key","Member","Lon","Lat"],"""
			page +="""
	  columns: [{},{}, {}, {}],
	  minSpareCols: 0,
	  minSpareRows: 1,
	  currentRowClassName: 'currentRow',
currentColClassName: 'currentCol',
autoWrapRow: true,
	  contextMenu: true,
 beforeChange: function(changes, source) {
    // [[row, prop, oldVal, newVal], ...]
    //changes[0] = null;
    //alert(changes);
    //alert(source);
    alert(hot.getData().length);
  },	  
beforeRemoveRow: function(index, amount) {
var dellist=[];
for(var i=0; i<amount; i++){
dellist.push(hot.getData()[index +i][1]);
}
	  $.ajax({
		url: '/wsgi/geo/save/save_geo',
		data: {delete:dellist,key:"%s"}, // returns all cells' data"""%key
			page +="""
		dataType: 'json',
		type: 'POST',
		success: function(res) {//alert(res);
if (res.result === 'ok') {
			$console.text('Data saved');
			document.getElementById("load_dog").click();
		  }
		  else {
			$console.text('Save error');
		  }
		},
		error: function () {
		  $console.text('Save error');
		}
	  });        
},
	  afterChange: function (change, source) {
		var data;
		if (source === 'loadData' || !$parent.find('input[name=autosave]').is(':checked')) {
		//them vao:
	  var colu = ["key","member","lon","lat"];  
	  var update = [],insert=[],rows=[],unique=[]; 	
if(change){							
							for (var i=0;i<change.length;i++){
								if (hot.getData()[change[i][0]][0]){
									localStorage['update'+ localStorage['update_len']+'key'] = hot.getData()[change[i][0]][0];
									localStorage['update'+ localStorage['update_len']+'member'] = hot.getData()[change[i][0]][1];
									localStorage['update'+ localStorage['update_len']+'lon'] = hot.getData()[change[i][0]][2];
									localStorage['update'+ localStorage['update_len']+'lat'] = hot.getData()[change[i][0]][3];
									localStorage['update_len'] = parseInt(localStorage['update_len']) + 1;
																	
								}
							}
		}
		  return;
		}

		data = change[0];
		//alert(hot.getData()[change[0][0]][0]);
		//alert(change[0][3]);
		
		//them vao:
		var colu = ["key","member", "lon", "lat"];

							var update = [],insert=[],rows=[],unique=[]; 
							
							for (var i=0;i<change.length;i++){
								if (hot.getData()[change[i][0]][0] == null){
									rows.push(change[i][0]);
								}
								else{
									//update.push({"key":hot.getData()[change[i][0]][0],"column":colu[change[i][1]],"value":change[i][3]});
									update.push({"key":hot.getData()[change[i][0]][0],"member":hot.getData()[change[i][0]][1],"lon":hot.getData()[change[i][0]][2],"lat":hot.getData()[change[i][0]][3]});
								}
							}
							if (rows.length >0) {	
								for(var i in rows){
									if(unique.indexOf(rows[i]) === -1){
										unique.push(rows[i]);
									}
								}                
							for (var i in unique){
								insert.push({"key":hot.getData()[unique[i]][0],
								"member":hot.getData()[unique[i]][1],
								"lon":hot.getData()[unique[i]][2],
								"lat":hot.getData()[unique[i]][3]
					
								})
							}
						}
	   
		// transform sorted row to original row
		data[0] = hot.sortIndex[data[0]] ? hot.sortIndex[data[0]][0] : data[0];
		//
		//alert(JSON.stringify(insert));
		clearTimeout(autosaveNotification);
		$.ajax({
		  url: '/wsgi/geo/save/save_geo',
		  dataType: 'json',
		  type: 'POST',
		  //data: {"changes": change}, // contains changed cells' data
		  data: {update:update,insert:insert,lenupdate:update.length,leninsert:insert.length,key:"%s"},"""%key
			page+="""
		  success: function (/*res*/) {
//alert(res);
			//$console.text('Autosaved (' + change.length + ' cell' + (change.length > 1 ? 's' : '') + ')');
document.getElementById("load_dog").click();
			autosaveNotification = setTimeout(function () {
			  $console.text('Changes will be autosaved');
			}, 1000);
			
		  }
		});
	  }
	});

	$parent.find('button[name=load]').click(function () {
	  $.ajax({
		url: '/wsgi/geo/load/load_geo',"""
			page += """	data: {"display":%s,key:"%s"},"""%(display,key)
			page += """	dataType: 'json',
						type: 'POST',					
			success: function (res) {
				var data = [], row;

				for (var i = 0, ilen = res.product.length; i < ilen; i++) {
					row = [];
					row[0] = res.product[i].key;
					row[1] = res.product[i].member;
					row[2] = res.product[i].lon;
					row[3] = res.product[i].lat;
	
			data[res.product[i].index - 1] = row;
		  }
		  $console.text('Data loaded');
		  hot.loadData(data);
		  $(".page2").html("<strong>Page 1/ "  + Math.round(res.sum_page)+"</strong>");
									$('.demo2').bootpag({
										total: res.sum_page,
										page: 1,
										maxVisible: 10,
										//href:'../demo/account_manager.py?page={{number}}',
										leaps: false,
											firstLastUse: true,
										first: '←',
										last: '→',
										wrapClass: 'pagination',
										activeClass: 'active',
										disabledClass: 'disabled',
										nextClass: 'next',
										prevClass: 'prev',
										lastClass: 'last',
										firstClass: 'first'
									}).on('page', function(event, num){
											$(".page2").html("<strong>Page " + num + '/' + Math.round(res.sum_page)+"</strong>");
						  $.ajax({
								url: "/wsgi/geo/load/load_geo","""
							
			page += """ 		data: {"page":num,"display":%s,key:"%s"},"""%(display,key)			
			page += """			dataType: 'json',
								type: 'POST',
								success: function (res) {
								var data = [], row;
								for (var i = 0, ilen = res.product.length; i < ilen; i++) {
									row = [];
									row[0] = res.product[i].key;
									row[1] = res.product[i].member;
									row[2] = res.product[i].lon;
									row[3] = res.product[i].lat;
	
									data[res.product[i].index - 1] = row;
									}
									$console.text('Data loaded');
									hot.loadData(data);

								}
						});
										});                  
		}
	  });
	}).click(); // execute immediately

	$parent.find('button[name=reset]').click(function () {
	  $.ajax({
		url: 'php/reset.php',
		success: function () {
		  $parent.find('button[name=load]').click();
		},
		error: function () {
		  $console.text('Data reset failed');
		}
	  });
	});
	$parent.find('button[name=save]').click(function () {
if(!$parent.find('input[name=autosave]').is(':checked')){	
		var update = [],insert=[],autosaveNotification;	
for (var i=0; i<localStorage['update_len'] ; i++){
update.push({"key":localStorage['update'+i+'key'],"member":localStorage['update'+i+'member'],"lon":localStorage['update'+i+'lat']});
}


	
for (var i=0; i<hot.getData().length-1 ; i++){
if(!hot.getData()[i][0]){
		insert.push({"key":hot.getData()[i][0],
		"member":hot.getData()[i][1],
		"lon":hot.getData()[i][2],
		"lat":hot.getData()[i][3]						
		})
}
}
alert(JSON.stringify(update));

if(update.length + insert.length >0){
		clearTimeout(autosaveNotification);
		$.ajax({
		  url: '/wsgi/apolo/save/save_geo',
		  dataType: 'json',
		  type: 'POST',
		  data: {update:update,insert:insert,lenupdate:update.length,leninsert:insert.length,key:"%s"},"""%key
			page+="""
		  success: function (/*res*/) {
//alert(res);
			//$console.text('Autosaved (' + change.length + ' cell' + (change.length > 1 ? 's' : '') + ')');
document.getElementById("load_dog").click();
			autosaveNotification = setTimeout(function () {
			  $console.text('Changes will be saved');
			}, 1000);
			
		  }
		});	
		
localStorage.clear();
localStorage['update_len']= 0;
}
else{
alert("Nothing gonna change");
}
}
else{
alert("You need to uncheck autosave first");
}



	
	});
	$parent.find('input[name=autosave]').click(function () {
	  if ($(this).is(':checked')) {
		$console.text('Changes will be autosaved');
	  }
	  else {
		$console.text('Changes will not be autosaved');
	  }
	});
				hot.selectCell(3,3);
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
import geo.sess
importlib.reload(geo.sess)
session_opts = geo.sess.session_opts

application = SessionMiddleware(application, session_opts)
