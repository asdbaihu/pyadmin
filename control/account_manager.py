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

		import psycopg2,pyad.module
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

				from datetime import datetime,date
				year_today = date.today().year
				month_today = date.today().month
				day_today = date.today().day
				if not 'display' in post:
					display = 200
				else:
					display = post['display']

				if not 'table' in post:
					table = ''
				else:
					table = post['table']
				if table =="":
					cur.execute("select")
				else:
					cur.execute("select * from %s limit 0"%table)
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
					elif colname == 'account_level':
						columns.append({'type':'numeric'})
					else:
						columns.append({})



				saveurl ="""'%s/save_account'"""%save
				loadurl = """'%s/load_account_manager'"""%load
				page=""
				page +=head
				page +="<title>Account manager</title>"
				page +=headlink
				page +="""</head>
				<body>"""
				page +=menuhead
				if int(ps[0][2]) == 2:
					page += menuadmin

				else:
					page += menuuser
				page += menufoot
				page += """<br />
							<br />"""


				page += """<ul class="nav nav-tabs">
								<li class="active"><a href="%s/account_manager">%s</a></li>
							</ul>
							
									  <h2>Table  %s </h2> """%(pyad.module.control,table,table)

				page +=	"""		<br />
								<form method="post" action="">
								  <input list="table" name="table" value="%s" onchange='if(this.value != 0) { this.form.submit(); }'>
								  <datalist id="table">
									<option value="account">
									<option value="admin_first_menu">
									<option value="admin_second_menu">
									<option value="first_menu">
									<option value="second_menu">
								  </datalist>									
									
									
									
									
																								
								Row : <input class="input-mini" type="number" name ="display" value = %s />"""%(table,display)
				page += """		<input type="submit" value="Chon" />
								</form>

	  <p>
		<button name="load" id="load_dog">Load</button>
		<button name="reset">Reset</button>
		<label><input id="autosave" type="checkbox" name="autosave" checked="checked" autocomplete="off"> Autosave</label>
		<input class="toggle" data-column="0" type="button" value="show/hide col 0">
<input class="toggle" data-column="1" type="button" value="show/hide col 1">
<input class="toggle" data-column="2" type="button" value="show/hide col 2">
	  </p>
	  <p>
		Instruction:Username must be unique, not duplicate. Should input account level column first, account level must be integer and not empty please. Do not forget input account level . Account level 2 is admin user and 1 is normal user.After insert new row, should update password last. Password always update last
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
$$ = function(id) {
  return document.getElementById(id);
},
autosave = $$('autosave'),
		 $container = $("#example1"),
		  $console = $("#exampleConsole"),
		  $parent = $container.parent(),
		  autosaveNotification,
		  hot;

		  hot = new Handsontable($container[0], {
		  columnSorting: true,
		  startRows: 8,
		  startCols: 3,
			currentRowClassName: 'currentRow',
currentColClassName: 'currentCol',
autoWrapRow: true,
		  rowHeaders: true,"""
				page +="""			colHeaders: %s,
							columns: %s,"""%(str(colHeaders),str(columns))
				page +="""					
//colWidths: [0.1,50,200,50,50,50,50],		
manualColumnResize: true,		
autoColumnSize : true,
//stretchH: 'all',	
hiddenColumns: true,			
		  minSpareCols: 0,
		  minSpareRows: 1,
		  contextMenu: true,
			beforeRemoveRow: function(index, amount) {
			var dellist=[];
			for(var i=0; i<amount; i++){
			dellist.push(hot.getData()[index +i][0]);
			}
			//alert(dellist);
				  $.ajax({
					url: """ + saveurl +""",
					data: {delete:dellist,table:"%s"}, // returns all cells' data
					dataType: 'json',
					type: 'POST',
					success: function(res) {//alert(res);
					if (res.result === 'ok') {
						$console.text('Data saved');
						//document.getElementById("load_dog").click();
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
			  return;
			}
		   
			data = change[0];"""%table
				page +="""				var update = [],insert=[],rows=[],unique=[];
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
			  url: """ + saveurl + """,
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
			url: """%table + loadurl + ""","""
				page += """	data: {"display":%s,table:"%s"},"""%(display,table)
				page += """	dataType: 'json',
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
												$(".page2").html("<strong>Page " + num + '/' + Math.round(res.sum_page)+"</strong>" );
							  $.ajax({
									url: """+ loadurl +""","""

				page += """ 		data: {"page":num,"display":%s,table:"%s"},"""%(display,table)
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

//hot.updateSettings({columns: [{data:1},{data:2,type:"password"},{data:3},{data:4},{data:5},{data:6}] });
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
