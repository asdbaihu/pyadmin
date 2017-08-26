from beaker.middleware import SessionMiddleware
import importlib
def application(environment, start_response):
	from webob import Request, Response
	request = Request(environment)
	params = request.params
	post = request.POST
	res = Response()
	import pyad.login
	importlib.reload(pyad.login)

	# Get the session object from the environ
	session = environment['beaker.session']

	# Check to see if a value is in the session
	#user = 'username' in session

	if not 'username' in session:
		page = pyad.login.loginform
		response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
	elif not 'password' in session:
		page = pyad.login.loginform
		response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
	else:
		user = session['username']
		passwd = session['password']

		import psycopg2,pyad.conn
		importlib.reload(pyad.conn)


		try:
			con = psycopg2.connect(pyad.conn.conn)
		except:
			page ="Can not access databases"

		cur = con.cursor()
		cur.execute("select username,account_password,account_level from account where username=%s and account_password=%s ",(user,passwd,))
		ps = cur.fetchall()
		if len(ps) == 0:
			page = pyad.login.login_again
			response = Response(body = page,content_type = "text/html",charset = "utf8", status = "200 OK")
		else:

			from datetime import datetime,date

			if not 'date_time' in post:
				month_input = date.today().month
				day_input = date.today().day
				year_input = date.today().year
				date_time ='%s/%s/%s'%(month_input,day_input,year_input)
			else:
				date_time = post['date_time']
				date_time_input = datetime.strptime(date_time, '%m/%d/%Y')
				month_input = date_time_input.month
				day_input = date_time_input.day
				year_input = date_time_input.year


			if not 'display' in post:
				display = 1
			else:
				display = int(post['display'])
			if not 'page' in post:
				page = 1
			else:
				page = post['page']
			start = (int(page)-1)*display
			#db.execute("""delete from qc_project%s%s%s where id in (select b.id from (select agent,link from qc_project%s%s%s group by agent,link having count(*)>1 ) as a left join (select id,agent,link from qc_project%s%s%s where id not in (select min(id) from qc_project%s%s%s group by agent,link having count(*)>1)) as b on  a.agent=b.agent and a.link=b.link )"""%(year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input))
			#ps2 = db.prepare("select count(*) from qc_project%s%s%s where process_time='NaN'"%(year_input,month_input,day_input))
			#ps3 = db.prepare("select count(*) from qc_project_csv%s%s where process_time='NaN'"%(year_input,month_input))
			#if int(ps2()[0][0]) > 0:
			#	db.execute("""update qc_project%s%s%s set process_time='10' where process_time='NaN'"""%(year_input,month_input,day_input))
			#if int(ps3()[0][0]) > 0:
			#	db.execute("""update qc_project_csv%s%s set process_time='10' where process_time='NaN'"""%(year_input,month_input))
			if not 'agent' in post:
				query_count = """select count(*) from (select split_part(link,'stringQuestionId',2)as link, title,array_to_string(array_agg(distinct   COALESCE(variant_check,'null') || ' ' || COALESCE(correct_check,'null') || ' '|| COALESCE(status,'null') || ' ' || COALESCE(price,'null') || ' '|| COALESCE(currency,'null') || ' ' || COALESCE(condition,'null') || ' ' || COALESCE(availability,'null') || ' '|| COALESCE(split_part(agent,'@',1),'null') || ' ' || id || ' ' || date_time  ),' ; \n ') as answer  from (select d.id,d.date_time,d.agent,d.link,d.title,d.variant_check,d.correct_check,d.status,d.price,d.currency,d.condition,d.availability,d.process_time,d.cds_key from 
(select a.idv from  
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2)  having count(*)>1) as a left join
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2) ,variant_check,correct_check,status,price,currency,condition,availability having count(*)>1) as b on a.idv = b.idv and a.count = b.count where a.idv !='undefined' and b.idv is null) as c inner join
(select *from qc_project%s%s%s ) as d on c.idv = split_part(d.link,'stringQuestionId',2) order by split_part(link,'stringQuestionId',2) ) as aa group by split_part(link,'stringQuestionId',2), title) as dd"""%(year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input)
				query_rows= """select split_part(link,'stringQuestionId',2)as link, title,array_to_string(array_agg(distinct   COALESCE(variant_check,'null') || ' ' || COALESCE(correct_check,'null') || ' '|| COALESCE(status,'null') || ' ' || COALESCE(price,'null') || ' '|| COALESCE(currency,'null') || ' ' || COALESCE(condition,'null') || ' ' || COALESCE(availability,'null') || ' '|| COALESCE(split_part(agent,'@',1),'null') || ' ' || id|| ' ' || date_time  ),' ; \n ') as answer ,max(id) as id from (select d.id,d.date_time,d.agent,d.link,d.title,d.variant_check,d.correct_check,d.status,d.price,d.currency,d.condition,d.availability,d.process_time,d.cds_key from 
(select a.idv from  
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2)  having count(*)>1) as a left join
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2) ,variant_check,correct_check,status,price,currency,condition,availability having count(*)>1) as b on a.idv = b.idv and a.count = b.count where a.idv !='undefined' and b.idv is null) as c inner join
(select *from qc_project%s%s%s ) as d on c.idv = split_part(d.link,'stringQuestionId',2) ) as aa group by split_part(link,'stringQuestionId',2), title order by id asc limit %s offset %s """%(year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input,display,start)
			else:
				agent = post['agent']
				if agent=='admin' or agent =='':
					query_count = """select count(*) from (select split_part(link,'stringQuestionId',2)as link, title,array_to_string(array_agg(distinct   COALESCE(variant_check,'null') || ' ' || COALESCE(correct_check,'null') || ' '|| COALESCE(status,'null') || ' ' || COALESCE(price,'null') || ' '|| COALESCE(currency,'null') || ' ' || COALESCE(condition,'null') || ' ' || COALESCE(availability,'null') || ' '|| COALESCE(split_part(agent,'@',1),'null') || ' ' || id|| ' ' || date_time ),' ; \n ') as answer  from (select d.id,d.date_time,d.agent,d.link,d.title,d.variant_check,d.correct_check,d.status,d.price,d.currency,d.condition,d.availability,d.process_time,d.cds_key from 
(select a.idv from  
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2)  having count(*)>1) as a left join
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2) ,variant_check,correct_check,status,price,currency,condition,availability having count(*)>1) as b on a.idv = b.idv and a.count = b.count where a.idv !='undefined' and b.idv is null) as c inner join
(select *from qc_project%s%s%s ) as d on c.idv = split_part(d.link,'stringQuestionId',2) order by split_part(link,'stringQuestionId',2) ) as aa group by split_part(link,'stringQuestionId',2), title ) as dd"""%(year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input)
					query_rows= """select split_part(link,'stringQuestionId',2)as link, title,array_to_string(array_agg(distinct   COALESCE(variant_check,'null') || ' ' || COALESCE(correct_check,'null') || ' '|| COALESCE(status,'null') || ' ' || COALESCE(price,'null') || ' '|| COALESCE(currency,'null') || ' ' || COALESCE(condition,'null') || ' ' || COALESCE(availability,'null') || ' '|| COALESCE(split_part(agent,'@',1),'null') || ' ' || id || ' ' || date_time ),' ; \n ') as answer, max(id) as id  from (select d.id,d.date_time,d.agent,d.link,d.title,d.variant_check,d.correct_check,d.status,d.price,d.currency,d.condition,d.availability,d.process_time,d.cds_key from 
(select a.idv from  
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2)  having count(*)>1) as a left join
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2) ,variant_check,correct_check,status,price,currency,condition,availability having count(*)>1) as b on a.idv = b.idv and a.count = b.count where a.idv !='undefined' and b.idv is null) as c inner join
(select *from qc_project%s%s%s ) as d on c.idv = split_part(d.link,'stringQuestionId',2) ) as aa group by split_part(link,'stringQuestionId',2), title order by id asc limit %s offset %s """%(year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input,display,start)
				else:
					query_count = """select count(*) from (select split_part(link,'stringQuestionId',2)as link, title,array_to_string(array_agg(distinct   COALESCE(variant_check,'null') || ' ' || COALESCE(correct_check,'null') || ' '|| COALESCE(status,'null') || ' ' || COALESCE(price,'null') || ' '|| COALESCE(currency,'null') || ' ' || COALESCE(condition,'null') || ' ' || COALESCE(availability,'null') || ' '|| COALESCE(split_part(agent,'@',1),'null') || ' ' || id || ' ' || date_time ),' ; \n ') as answer, max(id) as id  from (select d.id,d.date_time,d.agent,d.link,d.title,d.variant_check,d.correct_check,d.status,d.price,d.currency,d.condition,d.availability,d.process_time,d.cds_key from 
(select a.idv from  
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2)  having count(*)>1) as a left join
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2) ,variant_check,correct_check,status,price,currency,condition,availability having count(*)>1) as b on a.idv = b.idv and a.count = b.count where a.idv !='undefined' and b.idv is null) as c inner join
(select *from qc_project%s%s%s ) as d on c.idv = split_part(d.link,'stringQuestionId',2) ) as aa group by split_part(link,'stringQuestionId',2), title order by id asc) as cbb where answer ilike '%%%s%%' """%(year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input,agent.split('@')[0])
					query_rows= """select *from (select split_part(link,'stringQuestionId',2)as link, title,array_to_string(array_agg(distinct   COALESCE(variant_check,'null') || ' ' || COALESCE(correct_check,'null') || ' '|| COALESCE(status,'null') || ' ' || COALESCE(price,'null') || ' '|| COALESCE(currency,'null') || ' ' || COALESCE(condition,'null') || ' ' || COALESCE(availability,'null') || ' '|| COALESCE(split_part(agent,'@',1),'null') || ' ' || id || ' ' || date_time ),' ; \n ') as answer, max(id) as id  from (select d.id,d.date_time,d.agent,d.link,d.title,d.variant_check,d.correct_check,d.status,d.price,d.currency,d.condition,d.availability,d.process_time,d.cds_key from 
(select a.idv from  
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2)  having count(*)>1) as a left join
(select split_part(link,'stringQuestionId',2) as idv,count(*) from qc_project%s%s%s group by split_part(link,'stringQuestionId',2) ,variant_check,correct_check,status,price,currency,condition,availability having count(*)>1) as b on a.idv = b.idv and a.count = b.count where a.idv !='undefined' and b.idv is null) as c inner join
(select *from qc_project%s%s%s ) as d on c.idv = split_part(d.link,'stringQuestionId',2) ) as aa group by split_part(link,'stringQuestionId',2), title order by id asc) as cbb where answer ilike '%%%s%%'  limit %s offset %s """%(year_input,month_input,day_input,year_input,month_input,day_input,year_input,month_input,day_input,agent.split('@')[0],display,start)
			try:
				cur.execute(query_count)
			except:
				page ='{"product":"ok"}'
				con.rollback()
			rows_count= cur.fetchone()
			try:
				cur.execute(query_rows)
			except:
				page ='{"product":"ok"}'
				con.rollback()
			rows= cur.fetchall()
			sum_page = (int(rows_count[0])/display)+1
			#print(rows)
			row = []
			for ro in rows:
				row.append(list(ro))
			#print(row)
			page = '{"product":'
			objects_list = []
			try:
				cur.execute("""Select link,date_time from qc_project%s%s%s where id=(select max(id) from qc_project%s%s%s) """%(date.today().year,date.today().month,date.today().day ,date.today().year,date.today().month,date.today().day))
			except:
				page ='{"product":"ok"}'
				con.rollback()
			ps5 = cur.fetchone()
			token = ps5[0].split('stringQuestionId')

			import json,collections
			for i in range(len(row)):
				d = collections.OrderedDict()
				d['index'] = i+1 #row[0]
				#d['check'] = ""    #d.update({'isActive':'no'})
				#d['link'] = "<div>" +row[i][1] + row[i][2] + "</div>" + """<img src='"""+'https://www.thesun.co.uk/wp-content/uploads/2016/06/nintchdbpict000248155659-e1467125427889.jpg'+ """'/>"""
				d['link'] = "<div>" +row[i][1] + row[i][2] + "</div>" + """<img src='"""+token[0]+ "stringQuestionId" + row[i][0] + """'/>"""
				#d['link'] = """<img src='"""+'/'.join(token[:6]) +'/'+row[i][0] +'/' + '/'.join(token[7:])+ "/>" + "<div>" +row[i][1] + row[i][2] + "</div>"
				#d['title'] = row[i][1].replace("</span><span>",":").replace("<p>"," ").replace("</p>","").replace("<span>","").replace("</span>"," ")
				#d['answer'] = row[i][2]

				objects_list.append(d)

			#print(objects_list)
			page += json.dumps(objects_list)
			page +=""","sum_page":%s,"sum_row":%s}"""%(int(sum_page),rows_count[0])
			response = Response(body = page, content_type = "application/json", charset = "utf8", status = "200 OK")
		con.commit()
		cur.close()
		con.close()
	return response(environment, start_response)
import pyad.sess
importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts

application = SessionMiddleware(application, session_opts)


