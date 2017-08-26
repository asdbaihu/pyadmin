def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import importlib
	import pyad.module
	importlib.reload(pyad.module)
	bootstrap = pyad.module.bootstrap
	js = pyad.module.js
	page = """
	<!doctype html>
		<html>
			<head>
                <title> Login </title>
                <script src="%s/jquery.min.js"></script>
				<script src="%s/js/bootstrap.min.js"></script>
				<link rel="stylesheet" href="%s/css/bootstrap.min.css">
            </head>	

		<body>

			<p>Có thể bạn đăng nhập sai password hoặc username. Bạn cần phải đăng nhập lại</p>
					<div class="modal-dialog">
						<div class="modal-content">
							<div class="modal-header">
							<h4 class="modal-title">Login</h4>
						</div>
						<div class="modal-body">
						<form class="form-horizontal" role="form" action = 'login.py' method='post'>
							<div class="form-group">
								<label for="inputEmail1" class="col-lg-4 control-label">User name</label>
								<div class="col-lg-5">
									<input type="text" class="form-control" id="inputuser1" name='username' placeholder="test">
								</div>
							</div>
								<div class="form-group">
									<label for="inputPassword1" class="col-lg-4 control-label">Password</label>
									<div class="col-lg-5">
										<input type="password" class="form-control" id="inputPassword1" name='password' placeholder="123">
									</div>
								</div>
								<div class="form-group">
								<div class="col-lg-offset-4 col-lg-5">
									<div class="checkbox">
										<label>
											<input type="checkbox"> Remember me
										</label>
									</div>
								</div>
							</div>
							<div class="form-group">
								<div class="col-lg-offset-4 col-lg-5">
									<button type="submit" class="btn btn-default">Sign in</button>
								</div>
							</div>
						</form>
					</div>
					<div class="modal-footer">

					</div>
				</div><!-- /.modal-content -->
			</div><!-- /.modal-dialog -->		

		</body>
	</html>"""%(js,bootstrap,bootstrap)

	response = Response(body = page,
	content_type = "text/html",
	charset = "utf8",
	status = "200 OK")

	return response(environment, start_response)
