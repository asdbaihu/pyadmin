def application(environ, start_response):
	import cgi,os,sys
	from datetime import datetime
	from webob import Request, Response
	request = Request(environ)
	
	import redis
	r = redis.StrictRedis(host='localhost', port=6379, db=1)
	y = datetime.today().year
	m = datetime.today().month
	d = datetime.today().day	
	post = request.POST
	#for row in range(int(len(post.getall('changes[value][]')))):
		#r.set("%s_%s"%(post.getall('changes[value][]')[int(row)].split("<#>")[1],post['changes[account]'].split('<#>')[3]),"%s"%post.getall('changes[value][]')[int(row)].split("<#>")[2],57600)
			
	#cur.execute("""create table if not exists omnivore_question_%s_%s_%s
	#						(
	#						id serial8 primary key,
#no text,agent text, module text,domain text,title text,link text, quest text, answer text, time timestamp default now(), process_time numeric,img_id text,
#							update_time timestamp default now() )"""%(y,m,d))

							
	#cur.execute("""insert into  example (agent,module,domain,title,link,quest,answer) values(%s,%s,%s,%s,%s,%s,%s) """,(post['agent'],module,post['domain'],post['title'],post['link'],post['value'],post['answer']+'ask'))
	#page ="test"
	#if post['value'] =='long sleeve':
	#	quest ="<h5>Tay dài</h5>"
	#else:
	#	quest =""
	page ="""document.getElementById('guide').innerHTML="low heel ko lay outdoor shoes<button id='sanluong'>$</button><button id='trangt'>?</button>".fontsize(2);"""
	
	page +="""
			//var buttongt = document.createElement('button');
			//buttongt.id='trangt';
			//buttongt.style.zIndex = 1000;
			//title.style.position = "fixed";
			//buttongt.style.position = "absolute";
			//buttongt.style.top = "1%";
			//buttongt.style.left= "80%";
			//buttongt.style.font='30px bold';
			//buttongt.innerHTML='test';	
			//document.body.appendChild(buttongt);	
	//document.getElementById('log_all').innerHTML= "<img src='http://172.16.29.6/Gray.png' />;
	document.getElementById('trangt').onclick= function(){
	window.open("http://172.16.29.6");}
	document.getElementById('sanluong').onclick= function(){
	window.open("https://172.16.29.6/wsgi/omnivore/demo/report_quantity_module_by_day");}"""
	response = Response(body = page,
                      content_type = "text/javascript",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


