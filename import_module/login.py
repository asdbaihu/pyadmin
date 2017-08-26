import importlib,agora.module
importlib.reload(agora.module)

data = "%s/login_form"%agora.module.project
again = "%s/login_form_again"%agora.module.project
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
