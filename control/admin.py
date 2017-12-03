from beaker.middleware import SessionMiddleware
import importlib
from datetime import datetime

def application(environment, start_response):
    from webob import Request, Response
    request = Request(environment)
    params = request.params
    post = request.POST
    res = Response()

    import pyadmin.conn, pyadmin.login
    importlib.reload(pyadmin.conn)
    importlib.reload(pyadmin.login)

    # Get the session object from the environ
    session = environment['beaker.session']

    # Set some other session variable
    # session['user_id'] = 10
    # user_id = 'user_id' in session

    if not 'username' in session:
        page = pyadmin.login.loginform
    elif not 'password' in session:
        page = pyadmin.login.loginform
    else:
        user = session['username']
        passwd = session['password']

        import psycopg2, pyadmin.module, re
        try:
            con = psycopg2.connect(pyadmin.conn.conn)
        except:
            page = "Can not access databases"

        cur = con.cursor()
        cur.execute(
            "select username,account_password,account_level from account where username=%s and account_password=%s ",
            (user, passwd,))
        ps = cur.fetchall()
        if len(ps) == 0:
            page = pyadmin.login.login_again
        else:
            if int(ps[0][2]) == 2:
                importlib.reload(pyadmin.module)
                from pyadmin.module import head, headlink, menuadmin, menuuser, load, save, menuhead, menufoot

                from datetime import datetime, date
                year_today = date.today().year
                month_today = date.today().month
                day_today = date.today().day
                if not 'display' in post:
                    display = 200
                else:
                    display = post['display']

                if not 'hidecols' in post:
                    hidecols = []
                else:
                    hidecols = post.getall('hidecols')

                if not 'hidefils' in post:
                    hidefils = []
                else:
                    hidefils = post.getall('hidefils')

                if not 'orderby' in post:
                    orderby = ['1']
                else:
                    orderby = post.getall('orderby')

                if not 'by' in post:
                    by = 'asc'
                else:
                    by = post['by']
                que = ""
                if 'table' in post:
                    if post['table'] != "":
                        table = post['table']
                        cur.execute(
                            "select count(*) from information_schema.tables where table_name='%s' " % post['table'])
                        check = cur.fetchone()
                        if check[0] > 0:
                            # table exists in database
                            cur.execute("select count(*) from %s limit 1" % table)
                            que = "select *from " + table
                            countrows = cur.fetchone()
                            if countrows[0] == 0:  # no records in table, table is empty
                                cur.execute(
                                    "select column_name, data_type from information_schema.columns where table_name = '" +
                                    post['table'] + "'")
                                rws = cur.fetchall()
                                cols = [desc[0] for desc in rws if desc[0] not in hidecols]
                                # colHeaders =[co.title().replace("_"," ") for co in cols]
                                data_types = [desc[1] for desc in rws if desc[0] not in hidecols]

                                colslist = [desc[0] for desc in cur.description]
                                filcols = [fils for fils in cols if fils not in hidefils]

                                if 'movecols' in post:
                                    if len(post.getall('movecols')) != 0:
                                        movecols = ",movecols:%s" % str(post.getall('movecols'))
                                        cols = [co for co in post.getall('movecols') if co not in hidecols]
                                        que = "select " + ",".join(cols) + " from " + table

                                else:
                                    movecols = ""

                            # records in table, table is not empty
                            else:
                                cur.execute("select * from %s limit 1" % table)
                                que = "select *from " + table
                                cols = [desc[0] for desc in cur.description if desc[0] not in hidecols]

                                daty = cur.fetchone()
                                data_types = [type(val).__name__ for index, val in enumerate(daty)]

                                colslist = [desc[0] for desc in cur.description]
                                filcols = [fils for fils in cols if fils not in hidefils]

                                if 'movecols' in post:
                                    if len(post.getall('movecols')) != 0:
                                        movecols = ",movecols:%s" % str(post.getall('movecols'))
                                        cols = [co for co in post.getall('movecols') if co not in hidecols]

                                        cur.execute("select " + ",".join(cols) + " from %s limit 1" % table)
                                        que = "select " + ",".join(cols) + " from " + table
                                        colslist = [desc[0] for desc in cur.description]
                                        filcols = [fils for fils in cols if fils not in hidefils]

                                else:
                                    movecols = ""


                        else:  # table does not exits in database, only for query sql
                            table = post['table']
                            cur.execute("select count(*) from settings where tablename='" + table + "'")
                            check2 = cur.fetchone()
                            if check2[0] > 0:
                                cur.execute("select query from settings where tablename='" + table + "' limit 1")
                                check3 = cur.fetchone()
                                cur.execute("select count(*) from (" + check3[0] + ") as jotikaandmendaka")
                                check5 = cur.fetchone()
                                if check5[0] > 0:
                                    cur.execute("select * from (" + check3[0] + ") as jotikaandmendaka limit 1")

                                    que = check3[0]

                                    cols = [desc[0] for desc in cur.description if desc[0] not in hidecols]
                                    daty = cur.fetchone()
                                    data_types = [type(val).__name__ for index, val in enumerate(daty)]

                                    colslist = [desc[0] for desc in cur.description]
                                    filcols = [fils for fils in cols if fils not in hidefils]

                                    if 'movecols' in post:
                                        if len(post.getall('movecols')) > 0:
                                            movecols = ",movecols:%s" % str(post.getall('movecols'))
                                            cols = [co for co in post.getall('movecols') if co not in hidecols]

                                            cur.execute("select " + ",".join(cols) + " from (" + check3[
                                                0] + ") as jotikaandmendaka limit 1")
                                            que = check3[0]
                                            colslist = [desc[0] for desc in cur.description]
                                            filcols = [fils for fils in cols if fils not in hidefils]

                                    else:  # no row in query
                                        movecols = ""
                                else:
                                    cols = []
                                    data_types = []
                                    table = ""
                                    colslist = []
                                    filcols = []
                                    movecols = ""
                                    que = ""
                            else:
                                cols = []
                                data_types = []
                                table = ""
                                colslist = []
                                filcols = []
                                movecols = ""
                                que = ""



                    else:  # table =""

                        cols = []
                        data_types = []
                        table = ""
                        colslist = []
                        filcols = []
                        movecols = ""
                        que = ""
                else:  # no table in post
                    cols = []
                    data_types = []
                    table = ""
                    colslist = []
                    filcols = []
                    movecols = ""
                    que = ""

                if 'table' in params:
                    table = params.getall('table')[0]

                colHeaders = [co.title().replace("_", " ") for co in cols]

                cur.execute("select tablename,query from settings order by id")
                lst = cur.fetchall()
                ops = ""
                for l in lst:
                    # ops += "<option value='%s'>"%l[0]
                    if l[0] == table:
                        ops += """<option value="%s" selected="selected">%s</option>""" % (l[0], l[0])
                    else:
                        ops += """<option value="%s">%s</option>""" % (l[0], l[0])

                types = {}
                for i in range(len(cols)):
                    types[cols[i]] = data_types[i]
                data = []
                grofil = ""
                for fil in filcols:

                    if types[fil] == 'int':
                        grofil += fil.title().replace("_",
                                                      " ") + """ > <input class="input-mini" name='mor""" + fil + """' value=''/> and """
                        grofil += fil.title().replace("_",
                                                      " ") + """ < <input class="input-mini" name='les""" + fil + """' value=''/> || """
                    elif types[fil] == 'datetime' or types[fil] == 'date':
                        grofil += fil.title().replace("_",
                                                      " ") + """ > <input class="input-mini" name='mor""" + fil + """' value=''/> and """
                        grofil += fil.title().replace("_",
                                                      " ") + """ < <input class="input-mini" name='les""" + fil + """' value=''/> || """
                    else:
                        grofil += fil.title().replace("_",
                                                      " ") + """ ilike <input class="input-mini" name='fil""" + fil + """' value=''/>|| """
                        grofil += fil.title().replace("_",
                                                      " ") + """ not ilike <input class="input-mini" name='notfil""" + fil + """' value=''/>|| """

                    grofil += fil.title().replace("_", " ") + """ <select name="%snull">
  <option value=""></option>
    <option value="null">Empty</option>
  <option value="not_null">not empty</option>
</select> """ % fil

                    if 'mor%s' % fil in post:
                        data.append(""" mor%s:"%s" """ % (fil, post["mor%s" % fil]))
                    if 'les%s' % fil in post:
                        data.append(""" les%s:"%s" """ % (fil, post["les%s" % fil]))
                    if 'fil%s' % fil in post:
                        data.append(""" fil%s:"%s" """ % (fil, post["fil%s" % fil]))
                    if '%snull' % fil in post:
                        data.append(""" %snull:"%s" """ % (fil, post["%snull" % fil]))

                if len(data) > 0:
                    send_data = "," + ",".join(data)
                else:
                    send_data = ""

                hidefilter = ""
                hidefilter += """
				<div class="btn-group">
				  <button data-toggle="dropdown" class="btn dropdown-toggle"  data-placeholder="Hide filter">
					Hide filter <span class="caret"></span>
				  </button>
					<ul id="sortable3" class="connectedSortable dropdown-menu">
					"""
                for colsname in colslist:
                    if colsname in hidefils:
                        hidefilter += """<li class="ui-state-default"><input type="checkbox" id="fil%s" name="hidefils" value="%s"><label for="fil%s" name="hidefils" value="%s" checked>%s</label></li>""" % (
                            colsname, colsname, colsname, colsname, colsname.title().replace("_", " "))
                    else:
                        hidefilter += """<li class="ui-state-default"><input type="checkbox" id="fil%s" name="hidefils" value="%s"><label for="fil%s" name="hidefils" value="%s" >%s</label></li>""" % (
                            colsname, colsname, colsname, colsname, colsname.title().replace("_", " "))
                hidefilter += """
					  <!-- Other items -->
					</ul>
				</div>"""
                columns = []
                for colname in cols:
                    if colname == 'id':
                        columns.append({'readOnly': 'true'})
                    elif colname == 'account_password':
                        columns.append({"type": "password"})
                    elif colname == 'update_time':
                        columns.append({'readOnly': 'true'})
                    elif colname == 'account_level':
                        columns.append({'type': 'numeric', 'allowEmpty': 'false'})
                    elif colname == 'username':
                        columns.append({'allowEmpty': 'false'})
                    elif colname == 'fid':
                        columns.append({'type': 'numeric', 'allowEmpty': 'false'})

                    else:
                        columns.append({})
                saveurl = """'%s/save_admin'""" % save
                loadurl = """'%s/load_admin'""" % load
                page = ""
                page += head
                page += "<title>Account manager</title>"
                page += headlink
                page += """
			
				
				
				</head>
				<body>"""
                page += menuhead
                if int(ps[0][2]) == 2:
                    page += menuadmin

                else:
                    page += menuuser
                page += menufoot
                
                # for in this case need add more filter duplicate row in table home;
                
                if 'year' in params:
                    year = params.getone('year')
                else:
                    year = datetime.today().year
                if table == 'home_%s'%year:
                    cur.execute("delete from "+table +" where id not in (select max(id) from " + table + " group by report_date,agent)")
                page += """<br /><br />"""
                page += """<ul class="nav nav-tabs">
								<li class="active"><a href="%s/account_manager">%s</a></li>
							</ul>""" % (pyadmin.module.control, table)
                page += """<h2>Table  %s </h2>""" % (table)
                page += """Order by: %s. Sort by: %s. Hide columns: %s	| Hide filter: %s + %s  <br />
				<nav class='navbar navbar-default'>
								<form method="post" action="">								
								<div class="btn-group col-sm-2">
								<label>Table:
								<input list="table" name="table" value="%s"  onchange='if(this.value != 0) { this.form.submit(); }'>
								  <datalist id="table">
									%s
								  </datalist>
								</label> 
								 </div> 	
<select id="example-single-selected">
 <option value="">test</option>
 <option value="">test</option>
</select>
						 
<div class="btn-group">
  <button data-toggle="dropdown" class="btn dropdown-toggle"  data-placeholder="Move columns">
	Move columns <span class="caret"></span>
  </button>
    <ul id="sortable6" class="connectedSortable dropdown-menu">""" % (
                    ",".join(orderby), by, ",".join(hidecols), ",".join(hidefils), movecols, table, ops)
                for colsname in colslist:
                    page += """<li class="ui-state-default"><input type="checkbox" id="move%s" name="movecols" value="%s"><label for="move%s" name="movecols" value="%s" >%s</label></li>""" % (
                        colsname, colsname, colsname, colsname, colsname.title().replace("_", " "))
                page += """
      <!-- Other items -->
    </ul>
</div>									 								
<div class="btn-group">
  <button data-toggle="dropdown" class="btn dropdown-toggle"  data-placeholder="Hide column">
	Hide columns <span class="caret"></span>
  </button>
    <ul id="sortable1" class="connectedSortable dropdown-menu">"""
                for colsname in colslist:
                    page += """<li class="ui-state-default"><input type="checkbox" id="%s" name="hidecols" value="%s"><label for="%s" name="hidecols" value="%s" >%s</label></li>""" % (
                        colsname, colsname, colsname, colsname, colsname.title().replace("_", " "))
                page += """
      <!-- Other items -->
    </ul>
</div>	
<div class="btn-group">
  <button data-toggle="dropdown" class="btn dropdown-toggle"  data-placeholder="Order by">
	Order by <span class="caret"></span>
  </button>
    <ul id="sortable2" class="connectedSortable dropdown-menu">"""
                for colsname in colslist:
                    page += """<li class="ui-state-default"><input type="checkbox" id="by%s" name="orderby" value="%s"><label for="by%s" name="orderby" value="%s" >%s</label></li>""" % (
                        colsname, colsname, colsname, colsname, colsname.title().replace("_", " "))
                page += """
      <!-- Other items -->
    </ul>
</div>	
<div class="btn-group">
  <button data-toggle="dropdown" class="btn dropdown-toggle"  data-placeholder="Sort by">
	Sort by <span class="caret"></span>
  </button>
    <ul class="dropdown-menu">
    <li class="ui-state-default"><input type="radio" id="asc" name="by" value="asc"><label for="asc" name="by" value="asc" >asc</label></li>
    <li class="ui-state-default"><input type="radio" id="desc" name="by" value="desc"><label for="desc" name="by" value="desc" >desc</label></li>
      <!-- Other items -->
    </ul>
</div>"""
                page += "<div id='filadv' style='display:none'>"
                page += hidefilter
                page += grofil
                page += "</div>"
                page += """Show filter <input class="btn-group" type="checkbox" onclick="myFunction()"/>"""
                page += """
			<div class="btn-group col-sm-1">
				<input class="btn-group form-control col-sm-1" type="number" name ="display" value = %s />
				</div>
				""" % (display)
                page += """		<input type="submit" id ="chon" value="Chon" />
					
				</div>
								</form>
								</nav>

	  <p>
		<button name="load" id="load_dog">Load</button>
		<button name="reset">Reset</button>
		<label><input id="autosave" type="checkbox" name="autosave" checked="checked" autocomplete="off"> Autosave</label>
	  </p>
		<div>
	  <span id="exampleConsole" class="console">Click "Load" to load data from server </span> | 
							<span class="page2">No page selected</span> 
	  </div>
	  <div id="example1" style="width:100%; height: 500px; overflow: hidden"></div>
	  <div class="demo2"></div>

	  <script>"""
                for hids in hidefils:
                    page += """$("#fil%s").click();""" % hids
                # for c in cols:
                # page +="""$("#move%s").click();"""%c

                page += """
				
    $(document).ready(function() {
        $('#example-dropDown, #example-single-selected').multiselect({
            enableFiltering: true,
            includeSelectAllOption: false,
            disableIfEmpty: true,
            multiple:false,
            maxHeight: 400,
            dropDown: true
        });
    });
			
function myFunction() {
    var x = document.getElementById('filadv');
    if (x.style.display === 'none') {
        x.style.display = 'inline';
    } else {
        x.style.display = 'none';
    }
}			
	  
  $( function() {
    $( "#sortable1, #sortable2,#sortable3,#sortable5 ,#sortable6").sortable({
      connectWith: ".connectedSortable"
    }).disableSelection();
$( "ul, li" ).disableSelection();

    
  } );
  
 

	  """
                page += """
			var colu = %s;""" % cols
                page += """
  emailValidator = function (value, callback) {
    setTimeout(function(){
      if (/.+@.+/.test(value)) {
        callback(true);
      }
      else {
        callback(false);
      }
    }, 1000);
  };				
emptyValidator = function(value, callback) {
    setTimeout(function(){
    if (isEmpty(value)) { // isEmpty is a function that determines emptiness, you should define it
        callback(true);
    } else {
        callback(fasle);
    }
    }, 1000);    
}	    
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
                page += """			colHeaders: %s,
							columns: %s,""" % (str(colHeaders), str(columns))
                page += """					
//colWidths: [0.1,50,200,50,50,50,50],		
manualColumnResize: true,
manualRowResize: true,		
autoColumnSize : true,
//stretchH: 'all',	
hiddenColumns: true,			
		  minSpareCols: 0,
		  minSpareRows: 1,
		  contextMenu: true,
		  
			beforeRemoveRow: function(index, amount) {
			var dellist=[];
			for(var i=0; i<amount; i++){
			dellist.push(hot.getData()[index +i][colu.indexOf("id")]);
			}
			//alert(dellist);
				  $.ajax({
					url: """ + saveurl + """,
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
		   
			data = change[0];""" % table
                page += """				var update = [],insert=[],rows=[],unique=[];
								for (var i=0;i<change.length;i++){
									if (hot.getData()[change[i][0]][colu.indexOf("id")] == null){
										rows.push(change[i][0]);
									}
									else{
										update.push({"id":hot.getData()[change[i][0]][colu.indexOf("id")],"column":colu[change[i][1]],"value":change[i][3]});
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
			  data: {update:update,insert:insert,lenupdate:update.length,leninsert:insert.length,table:"%s",cols:%s},
			  success: function (res) {
			  					if (res.result === 'ok') {
//alert(res);
				//$console.text('Autosaved (' + change.length + ' cell' + (change.length > 1 ? 's' : '') + ')');
document.getElementById("load_dog").click();
				autosaveNotification = setTimeout(function () {
				  $console.text('Changes will be autosaved ');
				}, 1000);
}else{$console.html("<font color='red'>Data save error</font>");}
			  },
			error: function (res) {
							autosaveNotification = setTimeout(function () {
			  $console.html("<font color='red'>Data save error:</font>");
				}, 1000);

			}
			});
			   
		  }
		});
		
		
		$parent.find('button[name=load]').click(function () {
		  $.ajax({
			url: """ % (table, str(cols)) + loadurl + ""","""
                page += """	data: JSON.parse(JSON.stringify({types:%s,"display":%s,table:"%s",cols:%s,orderby:%s,by:"%s",filcols:%s%s%s,que:"%s"})),""" % (
                    str(types), display, table, str(cols), str(orderby), by, str(filcols), send_data, movecols,
                    re.sub('\s+', ' ', que.replace('"', '\\"')))
                page += """	dataType: 'json',
							type: 'POST',					
				success: function (res) {
					var data = [], row;
					for (var i = 0, ilen = res.product.length; i < ilen; i++) {
						row = [];
						for(var m in colu){
						row[m] = res.product[i][colu[m]];
						}
				data[res.product[i].idha - 1] = row;
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
												$(".page2").html("<strong>Page " + num + '/' + Math.round(res.sum_page)+"</strong>"/* + res.test */);
							  $.ajax({
									url: """ + loadurl + ""","""

                page += """ 		data: JSON.parse(JSON.stringify({types:%s,"page":num,"display":%s,table:"%s",cols:%s,orderby:%s,by:"%s",filcols:%s%s%s,que:"%s"})),""" % (
                    str(types), display, table, str(cols), str(orderby), by, str(filcols), send_data, movecols,
                    re.sub('\s+', ' ', que.replace('"', '\\"')))
                page += """			dataType: 'json',
									type: 'POST',
									success: function (res) {
					var data = [], row;

					for (var i = 0, ilen = res.product.length; i < ilen; i++) {
						row = [];
						for(var m in colu){
						row[m] = res.product[i][colu[m]];
						
						}
					
				data[res.product[i].idha - 1] = row;
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
                page = pyadmin.login.login_again

        con.commit()
        cur.close()
        con.close()
    # request.headers['Cookie']
    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")

    return response(environment, start_response)


# Configure the SessionMiddleware
import pyadmin.sess

importlib.reload(pyadmin.sess)
session_opts = pyadmin.sess.session_opts
application = SessionMiddleware(application, session_opts)
