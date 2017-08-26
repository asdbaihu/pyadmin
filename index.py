from beaker.middleware import SessionMiddleware
import importlib


def application(environ, start_response):
    from webob import Request, Response
    # from datetime import datetime
    # request = Request(environ)
    # post = request.POST
    import importlib, pyad.login
    importlib.reload(pyad.login)
    from pyad import login


    # Get the session object from the environ
    session = environ['beaker.session']

    # Check to see if a value is in the session
    user = 'username' in session
    passwd = 'password' in session

    # Set some other session variable
    # session['user_id'] = 10
    # user_id = 'user_id' in session

    if not 'username' in session:
        page = pyad.login.loginform
    elif not 'password' in session:
        page = pyad.login.loginform
    else:
        user = session['username']
        passwd = session['password']

        import psycopg2, hashlib, pyad.conn
        importlib.reload(pyad.conn)
        from pyad.conn import conn
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
            page = pyad.login.login_again
        else:
            import pyad.module
            importlib.reload(pyad.module)
            from pyad.module import head, headlink, menuadmin, menuuser, menuhead, menufoot


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

            page += "<p> You are successfully logged in !</p>"

        con.commit()
        cur.close()
        con.close()
    response = Response(body=page,
        content_type="text/html",
        charset="utf8",
        status="200 OK")

    return response(environ, start_response)

# Configure the SessionMiddleware
import pyad.sess

importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts
application = SessionMiddleware(application, session_opts)
