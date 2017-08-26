from beaker.middleware import SessionMiddleware
import importlib
def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()

	import pyad.conn,pyad.login
	importlib.reload(pyad.conn)
	importlib.reload(pyad.login)

	# Get the session object from the environ
	session = environment['beaker.session']

	# Check to see if a value is in the session
	user = 'username' in session
	passwd = 'password' in session

	# Set some other session variable
	#session['user_id'] = 10
	#user_id = 'user_id' in session

	if not 'username' in session:
		page = pyad.login.loginform
	elif not 'password' in session:
		page = pyad.login.loginform
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,psycopg2.extras,psycopg2.extensions,pyad.module
		try:
			con = psycopg2.connect(pyad.conn.conn)
		except:
			page ="Can not access databases"

		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = pyad.login.login_again
		else:
			if int(ps[0][2]) == 2:
				importlib.reload(pyad.module)
				from pyad.module import head,headlink,menuadmin,menuuser,load,save,menuhead,menufoot

				if not 'table' in post:
					table = 'admin_first_menu'
				else:
					table = post['table']
				if not 'display' in post:
					display = 200
				else:
					display = post['display']

				#if table == 'admin_first_menu' or table =='first_menu':
				#	cur.execute("""select id,menu1,link from %s limit 0 """%(table))
				#elif table == 'admin_second_menu' or table == 'second_menu' :
				#	cur.execute("""select id,first_menu_id,menu2,link from %s limit 0"""%(table))

				cur.execute("""select * from %s limit 0"""%(table))
				colHeaders = [desc[0].title().replace("_"," ") for desc in cur.description]
				cols = [desc[0] for desc in cur.description]
				columns =[]
				for colname in cols:
					if colname == 'id':
						columns.append({'readOnly':'true'})
					elif colname == 'account_password':
						columns.append({"type":"password"})
					elif colname == 'update_time':
						columns.append({'readOnly':'true'})
					else:
						columns.append({})


				page =""
				page += head + headlink
				page +="<title>Edit menu</title>"
				page +="""
				</head>
				<body>"""
				page +=menuhead
				if int(ps[0][2]) == 2:
					page += menuadmin
				else:
					page += menuuser
				page += menufoot
				page += """						
							<br />
					<br />								
									  <h2>Edit menu %s</h2> 
						<br />
								<form method="post" action="">
									<select name="table" onchange='if(this.value != 0) { this.form.submit(); }' >
										<option value="%s">%s</option>
										<option value="admin_first_menu">admin first menu level</option>
										<option value="admin_second_menu">admin second menu level</option>
										<option value="first_menu">user first menu level</option>
										<option value="second_menu">user second menu level</option>
									</select>									
								Row : <input class="input-mini" type="number" name ="display" value = %s />"""%(table, table, table,display)
				page += """		<input type="submit" value="Chon" />
								</form>

		<p>
		<button name="load" id="load_dog">Load</button>
		<button name="save">Save</button>
		<button name="reset">Reset</button>
		<label><input type="checkbox" name="autosave" checked="checked" autocomplete="off"> Autosave</label>
		</p>
		<div>
		<span id="exampleConsole" class="console">Click "Load" to load data from server </span> | 
							<span class="page2">No page selected</span> 
		</div>
		<div id="example1" style="width:100%; height: 500px; overflow: hidden"></div>
		<div class="demo2"></div>

		<script>"""
				page +="""
			var colu = %s;"""%cols
				page +="""
		  var
		  $container = $("#example1"),
		  $console = $("#exampleConsole"),
		  $parent = $container.parent(),
		  autosaveNotification,
		  hot;

		  hot = new Handsontable($container[0], {
		  columnSorting: true,
		  startRows: 8,
		  startCols: 3,
							rowHeaders: true,"""

				page += """
							colHeaders: %s,
							columns: %s,"""%(colHeaders,columns)
				page += """	fixedColumnsLeft: 1,
		  minSpareCols: 0,
		  minSpareRows: 1,
						  currentRowClassName: 'currentRow',
		currentColClassName: 'currentCol',
		autoWrapRow: true,
		  contextMenu: true,
		beforeRemoveRow: function(index, amount) {
		var dellist=[];
		for(var i=0; i<amount; i++){
		dellist.push(hot.getData()[index +i][0]);
		}
		//alert(dellist);
		  $.ajax({
			url: '%s/save_menu',
			data: {delete:dellist,table:"%s"}, // returns all cells' data
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
			error: function (res) {
			  $console.text('Save error: ' + JSON.stringify(res));
			}
		  });        
		},              
		  
		  afterChange: function (change, source) {
			var data;

			if (source === 'loadData' || !$parent.find('input[name=autosave]').is(':checked')) {
			  return;
			}
			data = change[0];
		  
			"""%(save,table)

				page +="""var update = [],insert=[],rows=[],unique=[];
								for (var i=0;i<change.length;i++){
									if (hot.getData()[change[i][0]][0] == null){
										rows.push(change[i][0]);
									}
									else{
										update.push({"id":hot.getData()[change[i][0]][0],"column":colu[change[i][1]],"value":change[i][3]});
									}
								}
								if (rows.length >0) {	
									for(var i in rows){
										if(unique.indexOf(rows[i]) === -1){
											unique.push(rows[i]);
										}
									}                
								for (var i in unique){
									var son = {};
									for (var k in colu){
										son[colu[k]] = hot.getData()[unique[i]][k]
									}
									
									insert.push(son);
								}
							}
			// transform sorted row to original row
			data[0] = hot.sortIndex[data[0]] ? hot.sortIndex[data[0]][0] : data[0];

			clearTimeout(autosaveNotification);
			$.ajax({
			  url: '%s/save_menu',
			  dataType: 'json',
			  type: 'POST',
			  //data: {"changes": change}, // contains changed cells' data
			  data: {update:update,insert:insert,lenupdate:update.length,leninsert:insert.length,table:"%s"},
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
									url: "%s/load_admin_first_menu","""%(save,table,load)

				page += """ 		data: {display:%s,table:"%s"},"""%(display,table)
				page += """			dataType: 'json',
									type: 'POST',
									success: function (res) {
					var data = [], row;
					for (var i = 0, ilen = res.product.length; i < ilen; i++) {
						row = [];
						for(var m in colu){
						row[m] = res.product[i][colu[m]];
						}
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
									url: "%s/load_admin_first_menu","""%load

				page += """ 		data: {"page":num,"display":%s,"table":"%s"},"""%(display,table)
				page += """			dataType: 'json',
									type: 'POST',
									success: function (res) {					var data = [], row;
					for (var i = 0, ilen = res.product.length; i < ilen; i++) {
						row = [];
						for(var m in colu){
						row[m] = res.product[i][colu[m]];
						}
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
			else:
				page=pyad.login.login_again

		con.commit()
		cur.close()
		con.close()
			#request.headers['Cookie']
	response = Response(body = page,
	content_type = "text/html",
	charset = "utf8",
	status = "200 OK")

	return response(environment, start_response)

# Configure the SessionMiddleware
import pyad.sess
importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts
application = SessionMiddleware(application, session_opts)
