from beaker.middleware import SessionMiddleware
import importlib
def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	
	import agora.conn,agora.login
	importlib.reload(agora.conn)
	importlib.reload(agora.login)

	# Get the session object from the environ
	session = environment['beaker.session']

	# Set some other session variable
	#session['user_id'] = 10
	#user_id = 'user_id' in session

	if not 'username' in session:
		page = agora.login.loginform
	elif not 'password' in session:
		page = agora.login.loginform
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,psycopg2.extras,psycopg2.extensions,agora.module
		try:
			con = psycopg2.connect(agora.conn.conn)
		except:
			page ="Can not access databases"
		
		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = agora.login.login_again
		else:
			importlib.reload(agora.module)
			from agora.module import head,headlink,menuadmin,menuuser,load,save,menuhead,menufoot					
			
			from datetime import datetime,date
			year_today = date.today().year
			month_today = date.today().month
			day_today = date.today().day
			if not 'agent' in params:
				if not 'agent' in post:
					agent = user
				else:
					agent = post['agent']
			else:
				if not 'agent' in post:
					agent = params['agent']
				else:
					agent = post['agent']				
				
			if not 'display' in post:
				display = 1
			else:
				display = post['display']
			if not 'date' in params:					
				if not 'date_time' in post:
					date_time = '%s/%s/%s'%(month_today,day_today,year_today)
				else:
					date_time = post['date_time']
					date_time_input = datetime.strptime(date_time, '%m/%d/%Y')	
					month_input = date_time_input.month
					day_input = date_time_input.day
					year_input = date_time_input.year				
			else:
				if not 'date_time' in post:
					date_time = params['date']
				else:
					date_time = post['date_time']
					date_time_input = datetime.strptime(date_time, '%m/%d/%Y')	
					month_input = date_time_input.month
					day_input = date_time_input.day
					year_input = date_time_input.year
			page=""
			page +=head
			page +="<title>Check online</title>"
			page +=headlink
			page +="""</head>
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
						<br />
						<br /><ul class="nav nav-tabs">
								<li><a href="../demo/check_online_text_quick">Quick check text</a></li>
								<li><a href="../demo/check_online">Check text</a></li>
								<li  class="active"><a href="../demo/check_online_anh">Check with images</a></li>
								<li><a href="../demo/check_online_anh_quick">Quick check with images</a></li>
								<li><a href="../demo/report_quantity_by_day">SL ngay</a></li>
								<li><a href="../demo/report_quantity_by_month">SL thang</a></li>
								<li><a href="../demo/report_quantity_by_month_detail">SL chi tiet thang</a></li>                                    

							</ul>"""
			try:
				cur.execute("""Select link,date_time from qc_project%s%s%s where id=(select max(id) from qc_project%s%s%s) """%(year_today,month_today,day_today,year_today,month_today,day_today))
				ps2 = cur.fetchone()
				page +="""<p>Token key moi nhat: %s <br /> lay luc :%s </p>"""%(ps2[0],ps2[1])	

			except:
				page +=""" <p>Token key moi nhat: <font color="red">Loi Can kiem tra xem bang du lieu co ton tai khong</font></p>"""	
				con.rollback()
				
							
			page += """<p> Link bat dong , 1 anh nhung co nhieu ket qua khac nhau """
			page += """Ngay <b>%s %s</b>  """%(date_time,agent)
			page +=	"""		<br />
							<form method="post" action="">
								Ngay : <input type="text" id="datepicker" name ="date_time" size="30" value = '%s' required>
								Agent : <input list="agent_list" name="agent">
												<datalist id="agent_list">
													<option value="%s">"""%(date_time,agent)
			cur.execute("select gmail from user_report order by id")
			ps_list_agent = cur.fetchall()
			for row in ps_list_agent:
				page +="""                          <option value="%s">"""%row
			page += """							</datalist>
								Row: <input type="number" name ="display" value = %s size ="2" /> """%(display)
			page +="""			<input type="submit" value="Tim kiem" />
							</form><button name="load">Load</button>
														<div class="page2">No page selected</div>
						<div class="demo2"></div>
													
						<div id="example1"></div>	
						"""

			page += """	<label><input type="checkbox" name="autosave" checked="checked" autocomplete="off"> Autosave</label>
						
						<div id="exampleConsole" class="console">Click "Load" to load data from server</div>

						<script>
						function strip_tags(input, allowed) {
						  // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
						  allowed = (((allowed || "") + "").toLowerCase().match(/<[a-z][a-z0-9]*>/g) || []).join(''); // making sure the allowed arg is a string containing only tags in lowercase (<a><b><c>)
						  var tags = /<\\/?([a-z][a-z0-9]*)\\b[^>]*>/gi,
							commentsAndPhpTags = /<!--[\\s\\S]*?-->|<\\?(?:php)?[\\s\\S]*?\\?>/gi;
						  return input.replace(commentsAndPhpTags, '').replace(tags, function ($0, $1) {
							return allowed.indexOf('<' + $1.toLowerCase() + '>') > -1 ? $0 : '';
						  });
						}

						var safeHtmlRenderer = function (instance, td, row, col, prop, value, cellProperties) {
						  var escaped = Handsontable.helper.stringify(value);
						  escaped = strip_tags(escaped, '<em><b><strong><a><big>'); //be sure you only allow certain HTML tags to avoid XSS threats (you should also remove unwanted HTML attributes)
						  td.innerHTML = escaped;
						  return td;
						};

						var coverRenderer = function (instance, td, row, col, prop, value, cellProperties) {
						  var escaped = Handsontable.helper.stringify(value);
						  if (escaped.indexOf('http') === 0) {
							var $img = $('<img>');
							$img.attr('src', value);
							$img.on('mousedown', function (event) {
							  event.preventDefault(); //prevent selection quirk
							});
							$(td).empty().append($img); //empty is needed because you are rendering to an existing cell
						  }
						  else {
							Handsontable.renderers.TextRenderer.apply(this, arguments); //render as text
						  }
						  return td;
						};		
						var $container = $("#example1");
						var $console = $("#exampleConsole");
						var $parent = $container.parent();
						var autosaveNotification;
						$container.handsontable({
						//startRows: 9,
						//startCols: 18,
						rowHeaders: true,
						colHeaders: ['','Link'],"""
			page +="""columns: [{renderer:"html"}
								],
						//fixedColumnsLeft: 1,
						colWidths: [200],
						minSpareCols: 0,
						minSpareRows: 0,
						//contextMenu: true,
						manualColumnMove: true,
						manualColumnResize: true,
						manualRowResize: true,
						persistentState: true,
						afterChange: function (change, source) {
							if (source === 'loadData') {
								return; //don't save this change
							}
							if ($parent.find('input[name=autosave]').is(':checked')) {
								clearTimeout(autosaveNotification);
								$.ajax({
								url: "php/save.php",
								dataType: "json",
								type: "POST",
								data: {changes: change}, //contains changed cells' data
								success: function () {
									$console.text('Autosaved (' + change.length + ' cell' + (change.length > 1 ? 's' : '') + ')');
									autosaveNotification = setTimeout(function () {
									$console.text('Changes will be autosaved');
									}, 1000);
								}
								});
							}
						}
						});
						var handsontable = $container.data('handsontable');

						$parent.find('button[name=load]').click(function () {
						  $.ajax({
								url: "%s/load_check_online_anh2new","""%load
							
			page += """ 		data: {"date_time": "%s","display":%s,"agent":"%s"},	"""%(date_time,display,agent)
			page += """			dataType: 'json',
								type: 'POST',
								success: function (res) {
								var data = [], row;
								for (var i = 0, ilen = res.product.length; i < ilen; i++) {
									row = [];
									//row[0] = res.product[i].check; 
									row[0] = res.product[i].link;
									/*if (res.product[i].title == 'null' || res.product[i].title == '' || res.product[i].title == null) {
										row[2] = '';}
									else{
										row[2] = res.product[i].title;}

									if (res.product[i].answer == 'null' || res.product[i].answert == '' || res.product[i].answer == null) {
										row[3] = '';}
									else{
										row[3] = res.product[i].answer;}*/
							
									data[res.product[i].index - 1] = row;
									}
									$console.text('Data loaded');
									handsontable.loadData(data);
									$(".page2").html("<strong>Page 1/ "  + res.sum_page+"</strong>. Tong so dong: "+ res.sum_row);
									$('.demo2').bootpag({
										total: res.sum_page,
										page: 1,
										maxVisible: 10,
										//href:'../demo/account_manager.py?page={{number}}',
										leaps: false,
									}).on('page', function(event, num){
											$(".page2").html("<strong>Page " + num + '/' + res.sum_page+"</strong>. Tong so dong: "+ res.sum_row);
						  $.ajax({
								url: "%s/load_check_online_anh2new","""%load
							
			page += """ 		data: {"date_time": "%s","page":num,"display":%s,"agent":"%s"},	"""%(date_time,display,agent)			

			page += """		dataType: 'json',
								type: 'POST',
								success: function (res) {
								var data = [], row;
								for (var i = 0, ilen = res.product.length; i < ilen; i++) {
									row = [];
									//row[0] = res.product[i].check; 
									row[0] = res.product[i].link;
									/*if (res.product[i].title == 'null' || res.product[i].title == '' || res.product[i].title == null) {
										row[2] = '';}
									else{
										row[2] = res.product[i].title;}

									if (res.product[i].answer == 'null' || res.product[i].answert == '' || res.product[i].answer == null) {
										row[3] = '';}
									else{
										row[3] = res.product[i].answer;}*/
										
									data[res.product[i].index - 1] = row;
									}
									$console.text('Data loaded');
									handsontable.loadData(data);

								}
						});
										});
								}
						});
						}).click(); //execute immediately
						
						</script>
						<script type="text/javascript">
						  (function(){
							var HOT = $('#example1').handsontable('getInstance');

							$('.reset-state1').on('click', function(){

							  HOT.runHooks('persistentStateReset');

							  HOT.updateSettings({
								manualColumnResize: true,
								manualRowResize: true
							  });

							  $(".state-loaded.example1").fadeOut(300, function () {
								// render table after hidden state-loaded alert
								HOT.render();
							  });
							});


							var storedData = {};

							HOT.runHooks('persistentStateLoad', '_persistentStateKeys', storedData);

							var savedKeys = storedData.value;

							if(savedKeys && savedKeys.length > 0){
							  $(".state-loaded.example1").show();
							  HOT.render();
							}
						  })();
						</script>						
						"""
			
			page +="""</body></html>"""

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
import agora.sess
importlib.reload(agora.sess)
session_opts = agora.sess.session_opts
application = SessionMiddleware(application, session_opts)
