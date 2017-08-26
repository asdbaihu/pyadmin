from beaker.middleware import SessionMiddleware

import importlib
def application(environ, start_response):
  from webob import Request, Response

