import importlib,pyad.module
importlib.reload(pyad.module)

data = "%s/login_form"%pyad.module.project
again = "%s/login_form_again"%pyad.module.project
loginform = """<!doctype html>
		<html>
			<head>
			<meta http-equiv="refresh" content="0; url=%s"/>
                <title> redirect login </title>
            </head>	
		<body>
		</body>
	</html>"""%data

login_again = """<!doctype html>
		<html>
			<head>
			<meta http-equiv="refresh" content="0; url=%s"/>
                <title> redirect login </title>
            </head>	
		<body>
		</body>
	</html>"""%again
