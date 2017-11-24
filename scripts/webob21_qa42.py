def application(environment, start_response):
	from webob import Request, Response
	from datetime import datetime
	#from pymongo import MongoClient
	#client = MongoClient('localhost',27017)
	#dbmongo = client.test
	import psycopg2
	import psycopg2.extras
	import psycopg2.extensions
	import redis
    #import json	
	r = redis.StrictRedis(host='localhost',port=6379,db=0)
	conn = psycopg2.connect("dbname=Google_qc user=postgres password=12345678")
	cur = conn.cursor()
	#import postgresql.driver as pg_driver
	#db = pg_driver.connect(host='localhost',user='postgres',password='12345678',database='Google_qc',port=5432)
	request = Request(environment)
	#params = request.params
	post = request.POST
	#y = datetime.today().year
	#m = datetime.today().month
	#d = datetime.today().day
	
	#counter = 	post['counter']
	date_time = post['date_time']
	agent = post['agent']
	link = post['link']
	title = post['title']
	variant_check = post['variant_check']
	correct_check = post['correct_check']
	status = post['status']
	price = post['price']
	currency = post['currency']
	condition = post['condition']
	availability = post['availability']
	process_time = post['process_time'].replace("NaN","10")
	cds_key = post['cds_key']
	merchant_page = post['merchant_page']
	render_method = post['render_method']
	av = post['av']
	co = post['co']
	country = post['country']
	language = post['language']
	customer = post['customer']
	month = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').month)
	year = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').year)
	day = int(datetime.strptime(post['date_time'],'%a %b %d %Y %H:%M:%S').day)
	#month = int(4)
	#year = int(2015)
	#day= int(30)
	cur.execute("""create table if not exists qc_project%s%s%s
				(id serial8 primary key,
				no text,
				date_time timestamp without time zone,
				agent text,
				link text,
				title text,
				variant_check text,
				correct_check text,
				status text,
				price text,
				currency text,
				condition text,
				availability text,
				process_time numeric,
				cds_key text,
				merchant_page text,
				render_method text,
				av text,
				co text,
				country text,
				language text,
				customer text,
				mistake text,
				right_choice text,
				update_time timestamp default now())""",(year,month,day))
	#qc_project_post = {"date_time":datetime.today(),"agent":agent,"link":link,"title":title,"correct_check":correct_check[:7],"status":status[:1],"price":price,"currency":currency,"condition":condition.replace("Yes","Y").replace("No info","I").replace("No","N"),"availability":availability[:1],"cds_key":cds_key,"merchant_page":merchant_page}

	# #insert into postgresql	
	# #db.execute("delete from qc_project%s%s%s where link ='%s' and confirm='N' and agent='%s'"%(year,month,day,link,agent))
	cur.execute("""insert into qc_project%s%s%s(date_time,agent,link,title,variant_check,correct_check,status,price,currency,condition,availability,process_time,cds_key,merchant_page,render_method,av,co,country,language,customer) values (nullif(%s,'')::timestamp,nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,'')::int,nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,''),nullif(%s,'')) """,(year,month,day,date_time,agent,link,title,variant_check,correct_check,status,price,currency,condition,availability,process_time,cds_key,merchant_page,render_method,av,co,country,language,customer))
    #images = [{'agent':'agent'}]
	#images ="""%s<#>%s<#>%s<#>%s<#>%s<#>%s<#>%s<#>%s<#>%s"""%(agent,variant_check,correct_check,status,price,currency,condition,availability,datetime.today())
	images ="""%s %s %s %s %s %s %s %s"""%(variant_check,correct_check,status,price,currency[:5],condition,availability[:5],agent.split('@')[0])
	r.sadd("%s"%link.split('stringQuestionId')[1],"%s"%images)
	r.expire("%s"%link.split('stringQuestionId')[1],259200)
	
	r2 = redis.StrictRedis(host='localhost',port=6379,db=1)	
	r2.hset("""%s%s"""%(title.split('</span><span>')[1].split('</span>')[0] , title.split('</span><span>')[4].split('</span>')[0]),"var%s"%variant_check,"%s"%variant_check)
	r2.hset("""%s%s"""%(title.split('</span><span>')[1].split('</span>')[0] , title.split('</span><span>')[4].split('</span>')[0]),"cor%s"%correct_check,"%s"%correct_check)
	r2.hset("""%s%s"""%(title.split('</span><span>')[1].split('</span>')[0] , title.split('</span><span>')[4].split('</span>')[0]),"sta%s"%status[:7] , "%s"%status[:7])	
	r2.hset("""%s%s"""%(title.split('</span><span>')[1].split('</span>')[0] , title.split('</span><span>')[4].split('</span>')[0]),"cur%s"%currency[:5] , "%s"%currency[:5])
	r2.hset("""%s%s"""%(title.split('</span><span>')[1].split('</span>')[0] , title.split('</span><span>')[4].split('</span>')[0]),"con%s"%currency[:5] , "%s"%condition)
	r2.hset("""%s%s"""%(title.split('</span><span>')[1].split('</span>')[0] , title.split('</span><span>')[4].split('</span>')[0]),"ava%s"%currency[:5] , "%s"%availability[:5])
	#images=[{'agent':agent}]#,'variant_check':'%s'%variant_check,'correct_check':'%s'%correct_check,'status':'%s'%status,'price':'%s'%price,'currency':'%s'%currency,'condition':'%s'%condition,'availability':'%s'%availability}]
    #json_images=json.dumps(images)
    #r.set('link','link')	
	#dbmongo['qc_project%s%s%s'%(year,month,day)].insert(qc_project_post)
	
	# dbmongo.qc_project.insert(qc_project_post)
	# # dbmongo.qc_project.remove({'link':link,'agent':agent,'confirm':'N'})
	# # dbmongo['qc_project%s%s%s'%(year,month,day)].remove({'link':link,'agent':agent,'confirm':'N'})
	# # if int(counter.split('/')[0]) == 1:
		# # db.execute("delete from qc_project%s%s%s where confirm='N' and agent='%s'"%(year,month,day,agent))
		# # db.execute("""insert into qc_project%s%s%s(counter,date_time,agent,link,title,correct_check,status,price,currency,condition,availability,process_time,cds_key,merchant_page) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') """%(year,month,day,counter,date_time,agent,link,title.replace("'","''"),correct_check,status.replace("'","''"),price,currency,condition,availability,process_time,cds_key,merchant_page.replace("'","''")))
		# # dbmongo.qc_project.remove({"agent":agent,"confirm":"N"})
		# # dbmongo['qc_project%s%s%s'%(year,month,day)].remove({"agent":agent,"confirm":"N"})
		# # dbmongo.qc_project.insert(qc_project_post)
		# # dbmongo['qc_project%s%s%s'%(year,month,day)].insert(qc_project_post)
	# # elif int(counter.split('/')[0]) == int(counter.split('/')[1]):
		# # db.execute("""insert into qc_project%s%s%s(counter,date_time,agent,link,title,correct_check,status,price,currency,condition,availability,process_time,cds_key,merchant_page) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') """%(year,month,day,counter,date_time,agent,link,title.replace("'","''"),correct_check,status.replace("'","''"),price,currency,condition,availability,process_time,cds_key,merchant_page.replace("'","''")))
		# # db.execute("""update qc_project%s%s%s set confirm='Y' where confirm='N' and agent='%s'"""%(year,month,day,agent))
		# # dbmongo.qc_project.insert(qc_project_post)
		# # dbmongo['qc_project%s%s%s'%(year,month,day)].insert(qc_project_post)
		# # dbmongo.qc_project.update(
			# # {"confirm":"N","agent":agent},
			# # {"$set":{"confirm" : "Y"}},
			# # upsert = False,
			# # multi =True
		# # )
		# # dbmongo['qc_project%s%s%s'%(year,month,day)].update(
			# # {"confirm":"N","agent":agent},
			# # {"$set":{"confirm" : "Y"}},
			# # upsert = False,
			# # multi =True
		# # )		
	# # else:
		# # db.execute("""insert into qc_project%s%s%s(counter,date_time,agent,link,title,correct_check,status,price,currency,condition,availability,process_time,cds_key,merchant_page) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') """%(year,month,day,counter,date_time,agent,link,title.replace("'","''"),correct_check,status.replace("'","''"),price,currency,condition,availability,process_time,cds_key,merchant_page.replace("'","''")))
		# # dbmongo.qc_project.insert(qc_project_post)						
		# # dbmongo['qc_project%s%s%s'%(year,month,day)].insert(qc_project_post)	
	conn.commit()
	cur.close()
	conn.close()
	
	# # qc_project_post = {"counter":counter,"date_time":date_time,"agent":agent,"link":link,"title":title,"correct_check":correct_check,"status":status,"price":price,"currency":currency,"condition":condition,"availability":availability,"process_time":process_time,"cds_key":cds_key,"merchant_page":merchant_page,"confirm":"N"}
	
	# # #insert into mongo date_time
	# # dbmongo.qc_project.remove({'link':link,'agent':agent,'confirm':'N'})
	# # if int(counter.split('/')[0]) == 1:
		# # dbmongo.qc_project.remove({"agent":agent,"confirm":"N"})
		# # dbmongo.qc_project.insert(qc_project_post)
	# # elif int(counter.split('/')[0]) == int(counter.split('/')[1]):
		# # dbmongo.qc_project.insert(qc_project_post)
		# # dbmongo.qc_project.update(
			# # {"confirm":"N","agent":agent},
			# # {"$set":{"confirm" : "Y"}},
			# # upsert = False,
			# # multi =True
		# # )
	# # else:
		# # dbmongo.qc_project.insert(qc_project_post)
	
	
	
	
	
	#page =  """post: %s \n\n  \n\n    """%post
	page ="ok"
	response = Response(body = page,
                      content_type = "text/plain",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environment, start_response)
