#session
import importlib,agora.module
importlib.reload(agora.module)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires':3000000, #True hoac 300 3000 ..v.v..v
#	'session.data_dir': './data',
	'session.data_dir': '/tmp',
#'session.domain' = '.domain.com',
'session.path' : '%s'%agora.module.project,	
	'session.auto': True    
}
