def application(environ, start_response):
	import cgi,os,sys
	from datetime import datetime
	from webob import Request, Response
	request = Request(environ)
	
	import psycopg2
	import psycopg2.extras
	import psycopg2.extensions
	conn = psycopg2.connect("dbname=omnivore user=postgres password=12345678")
	cur = conn.cursor()
	y = datetime.today().year
	m = datetime.today().month
	d = datetime.today().day	

	post = request.POST
	
	if post['attributetype']=='domain':
		module = "DE"
	elif post['attributetype']=='color':
		module = 'COLOR'
	elif post['attributetype']=='silhouette':
		module = 'SILHOUETTE'
	elif post['attributetype']=='image_quality':
		module = 'IMQ'
	else:
		module = 'SS'	
			
	#cur.execute("""create table if not exists omnivore_question_%s_%s_%s
	#						(
	#						id serial8 primary key,
#no text,agent text, module text,domain text,title text,link text, quest text, answer text, time timestamp default now(), process_time numeric,img_id text,
#							update_time timestamp default now() )"""%(y,m,d))

							
	cur.execute("""insert into  example (agent,module,domain,title,link,quest,answer) values(%s,%s,%s,%s,%s,%s,'ask') """,(post['agent'],module,post['domain'],post['title'],post['link'],post['value']))
	conn.commit()
	table = post["domain"].split(".")[-1].replace("&amp;","").replace(" ","").replace("-","") + post["value"].replace(" ","")
	update = """update """ + table + """ set answer='' where link='%s'; insert into """%(post['link']) + table + """ (link,answer,gio) select '%s','',now()
where not exists (select 1 from """%(post['link']) + table + """ where link='%s');"""%(post['link'])
	cur.execute(update)
	conn.commit()	
	cur.close()
	conn.close()			
	#page ='%s,%s'%(post['attributetype'],post['trao'])
	page =''
	page ='ok men'
	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


