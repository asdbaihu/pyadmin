from beaker.middleware import SessionMiddleware
import importlib
def application(environ, start_response):
	from webob import Request, Response
	#from datetime import datetime
	#request = Request(environ)
	#post = request.POST
	import importlib,pyad.login
	importlib.reload(pyad.login)
	from pyad import login


	# Get the session object from the environ
	session = environ['beaker.session']

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

		import psycopg2,hashlib,pyad.conn
		importlib.reload(pyad.conn)
		from pyad.conn import conn
		try:
			con = psycopg2.connect(conn)
		except:
			page ="Can not access databases"

		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = pyad.login.login_again
		else:
			import pyad.module
			importlib.reload(pyad.module)
			from pyad.module import head,headlink,menuadmin,menuuser,menuhead,menufoot


			page =""
			page += head + headlink
			page +="<title>home page</title>"
			page +="""
			</head>
			<body>"""
			page += menuhead
			if int(ps[0][2]) == 2:
				page += menuadmin
			else:
				page += menuuser

			saveurl ="""'%s/save_account_backup'"""%pyad.module.save
			loadurl = """%s/load.json"""%pyad.module.load
			page += menufoot
			page += """						
						<br />
						<br />
						<br />
						<br />"""

			page +="""
<div class="wrapper">
  <div class="wrapper-row">
    <div id="global-menu-clone">
      <h1><a href="../index.html">Handsontable</a></h1>

    </div>

    <div id="container">
      <div class="columnLayout">

        <div class="rowLayout">
      <div class="descLayout">
        <div class="pad" data-jsfiddle="example1">
          <h2>PHP example</h2>

          <p>This page loads and saves data on server. In this example, client side uses <b>$.ajax</b>. Server side uses
            <b>PHP with PDO (SQLite)</b>.</p>

          <p>Please note. This page and the PHP scripts are a work in progress. They are not yet configured on GitHub.
            Please run it on your own localhost.</p>

          <p>
            <button name="load">Load</button>
            <button name="save">Save</button>
            <button name="reset">Reset</button>
            <!--<label><input type="checkbox" name="autosave" checked="checked" autocomplete="off"> Autosave</label>-->
            <label><input type="checkbox" name="autosave"  autocomplete="off"> Autosave</label>
          </p>

          <div id="exampleConsole" class="console">Click "Load" to load data from server</div>

          <div id="example1"></div>

          <p>
            <button name="dump" data-dump="#example1" data-instance="hot" title="Prints current data source to Firebug/Chrome Dev Tools">
              Dump data to console
            </button>
          </p>
        </div>
      </div>

      <div class="codeLayout">
        <div class="pad">
          <script>
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
              rowHeaders: true,
              //colHeaders: ['Manufacturer', 'Year', 'Price'],
              colHeaders: true,
              //columns: [{},{},{}],
              minSpareCols: 1,
              minSpareRows: 1,
              contextMenu: true,
              afterChange: function (change, source) {
                var data;

                if (source === 'loadData' || !$parent.find('input[name=autosave]').is(':checked')) {
                  return;
                }
                data = change[0];

                // transform sorted row to original row
                data[0] = hot.sortIndex[data[0]] ? hot.sortIndex[data[0]][0] : data[0];

                clearTimeout(autosaveNotification);
                $.ajax({
                  url: 'php/save.php',
                  dataType: 'json',
                  type: 'POST',
                  data: {changes: change}, // contains changed cells' data
                  success: function () {
                    $console.text('Autosaved (' + change.length + ' cell' + (change.length > 1 ? 's' : '') + ')');

                    autosaveNotification = setTimeout(function () {
                      $console.text('Changes will be autosaved');
                    }, 1000);
                  }
                });
              }
            });

            $parent.find('button[name=load]').click(function () {
              $.ajax({
                url: '""" + loadurl + """',
                dataType: 'json',
                type: 'GET',
                success: function (res) {
                  var data = [], row;

                  for (var i = 0, ilen = res.cars.length; i < ilen; i++) {
                    row = [];
                    row[0] = res.cars[i].manufacturer;
                    row[1] = res.cars[i].year;
                    row[2] = res.cars[i].price;
                    data[res.cars[i].id - 1] = row;
                  }
                  $console.text('Data loaded');
                  hot.loadData(data);
                }
              });
            }).click(); // execute immediately

            $parent.find('button[name=save]').click(function () {
              $.ajax({
                url: 'php/save.php',
                data: {data: hot.getData()}, // returns all cells' data
                dataType: 'json',
                type: 'POST',
                success: function (res) {
                  if (res.result === 'ok') {
                    $console.text('Data saved');
                  }
                  else {
                    $console.text('Save error' );
                  }
                },
                error: function () {
                  $console.text('Save error' + JSON.stringify(hot.getData()) );
                }
              });
            });

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
          </script>
        </div>
      </div>
    </div>

        <div class="footer-text">
        </div>
      </div>

    </div>

  </div>
</div>

<div id="outside-links-wrapper"></div>

</body>
</html>
		"""

		con.commit()
		cur.close()
		con.close()
	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")

	return response(environ, start_response)

# Configure the SessionMiddleware
import pyad.sess
importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts
application = SessionMiddleware(application, session_opts)
