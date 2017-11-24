def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	post = request.POST
	import redis
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	if r.get("%s"%post['find']) is None:
		page ="None"
	else:
		#if str(environment[ 'REMOTE_ADDR']) !='172.16.29.49':
		page ="b'%s'"%str((r.get("%s"%post['find'])).decode('utf-8','ignore')).split('_')[0]
	#page ="%s'"%str(r.get("%s"%post['find'])).split('_')[0]
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


