def application(environ, start_response):
	from webob import Request, Response
	request = Request(environ)
	post = request.POST
	import redis
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	if r.get("%s"%post['find']) is None:
		page ="None"
	else:
		#page ="%s_%s"%((r.get("%s"%post['find'])).decode('utf-8'),post['id'].decode('utf-8'))
		#if str(environment[ 'REMOTE_ADDR']) !='172.16.29.49':
		page ="%s"%(r.get("%s"%post['find'])).decode('utf-8')
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


