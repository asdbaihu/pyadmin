from beaker.middleware import SessionMiddleware
import importlib


def application(environ, start_response):
    from webob import Request, Response
    # from datetime import datetime
    # request = Request(environ)
    # post = request.POST
    import importlib, pyadmin.login
    importlib.reload(pyadmin.login)
    from pyadmin import login


    # Get the session object from the environ
    session = environ['beaker.session']

    # Check to see if a value is in the session
    user = 'username' in session
    passwd = 'password' in session

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

        import psycopg2, hashlib, pyadmin.conn
        importlib.reload(pyadmin.conn)
        from pyadmin.conn import conn
        try:
            con = psycopg2.connect(conn)
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
            import pyadmin.module
            importlib.reload(pyadmin.module)
            from pyadmin.module import head, headlink, menuadmin, menuuser, menuhead, menufoot


            page = ""
            page += head + headlink
            page += "<title>home page</title>"
            page += \
                """
                    </head>
                    <body>
                """
            page += menuhead
            if int(ps[0][2]) == 2:
                page += menuadmin
            else:
                page += menuuser
            page += menufoot
            page += """						
            <br />
            <br />
            <br />
            <br />"""

            page += """<p> You are successfully logged in !</p>
            <div class="container">
    <div class="row">
        <div class="col-lg-12">
            <div class="panel panel-default">
                <div class="panel-heading">Dashboard</div>

                <div class="panel-body">
                    <canvas id="line-chart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>
<script type="text/javascript">
    window.onload = function () {
        Chart.defaults.global.defaultFontColor = '#000000';
        Chart.defaults.global.defaultFontFamily = 'Arial';
        var lineChart = document.getElementById('line-chart');
        var myChart = new Chart(lineChart, {
            type: 'line',
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "June"],
                datasets: [
                    {
                        label: 'PHP Activities',
                        data: [80, 30, 63, 20, 110, 3],
                        backgroundColor: 'rgba(0, 128, 128, 0.3)',
                        borderColor: 'rgba(0, 128, 128, 0.7)',
                        borderWidth: 1
                    },
                    {
                        label: 'Ruby Activities',
                        data: [18, 72, 10, 39, 19, 75],
                        backgroundColor: 'rgba(0, 128, 128, 0.7)',
                        borderColor: 'rgba(0, 128, 128, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        }
                    }]
                },
            }
        });
    };
</script>
            
            """

        con.commit()
        cur.close()
        con.close()
    response = Response(body=page,
        content_type="text/html",
        charset="utf8",
        status="200 OK")

    return response(environ, start_response)

# Configure the SessionMiddleware
import pyadmin.sess

importlib.reload(pyadmin.sess)
session_opts = pyadmin.sess.session_opts
application = SessionMiddleware(application, session_opts)
