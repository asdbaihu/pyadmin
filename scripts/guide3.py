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
	if post['agent'] =='bpo3khuatquanghuy@gmail.com':
		dog ='bấm phím e để tăng tốc độ dàn trang'
	elif post['agent'] =='bpo3nguyenthiphuongdung@gmail.com':
		dog ='bấm phím e để tăng tốc độ dàn trang'
	else:
		dog =''
		
	if post['value'] =='low heel':
		quest ="""PASS thể thao đế xuồng thấp(21/04),có gót, dốc, dạng dress shoes.SKIP ko đế ,Athletic (ngoại trừ fashion Sneaker có lấy),Outdoor shoes; Men's shoes (27/04) <a href='https://172.16.29.6/wsgi/omnivore/demo/LOW_%20HEEL_%20KH_%20traloi_27-Apr-16.htm' target='_blank'>update</a> """
	elif post['value']== 'flat':
		quest ="SKIP sneaker,athletic,low heel, wedges, platform. Pass:đế <=1.5cm, men(1-3cm),sliper,Slip on (trừ đế trắng giống sneaker),bale,Mokassins <a href='https://172.16.29.6/wsgi/omnivore/demo/FLAT_%20KH_%20traloi_28-Apr-16.htm' target='_blank'>update</a> "
	elif post['value'] =='tunic':
		quest ='Tunic lấy váy thụng có buộc eo như váy xanh trong hướng dẫn'
	elif post['value'] =='sheath':
		quest ='váy bó sát thật là bó'		
	elif post['value'] =='high heel':
		quest ='PASS (high heel) thể thao, giầy giấu đế(25/04/16)'	
	elif post['value'] =='wedge heel':
		quest ="""PASS(de xuong) thể thao, cách điệu, giấu đế;Chụp sai hướng nhìn giống wedge heel tham khảo title (25/04/16) <a href='https://172.16.29.6/wsgi/omnivore/demo/WEDGE_HEEL_KH_traloi_26-Apr-16.htm' target='_blank'>update</a> """		
	elif post['value']=='tstrap':
		quest =""" <a href='https://172.16.29.6/wsgi/omnivore/demo/image/7.SilhouettesTrainingHarveyNash_17Jul15_tran.htm#id.uu9d4xfk7yvi' target='_blank' > Xem tai lieu</a>"""
	elif post['value']=='full coverage':
		quest ="""<a href='https://172.16.29.6/wsgi/omnivore/demo/image/7.SilhouettesTrainingHarveyNash_17Jul15_tran.htm#id.x3rlx0j13gbs' target='_blank'> xem tai lieu</a> = full back coverage """
	elif post['value']=='slingback':
		quest ="""<a href='https://172.16.29.6/wsgi/omnivore/demo/image/7.SilhouettesTrainingHarveyNash_17Jul15_tran.htm#id.2quqatydm8td' target='_blank'> xem tai lieu</a>"""
	elif post['value']=='black':
		quest ="""nero=noir=schwarz= black """
	elif post['value']=='purple':
		quest ="""Lilac =lila=lavender = violet = purple """
	elif post['value']=='gray':
		quest ="""gris=grau(tieng duc)=gray """	
	elif post['value']=='brown':
		quest ="""braun=brown """		
	elif post['value']=='red':
		quest ="""rosso(tieng italy)=rouge=rot=red """	
	elif post['value']=='pink':
		quest ="""rosa=pink """		
	elif post['value']=='green':
		quest ="""olive=Grün=green """		
	elif post['value']=='white':
		quest ="""blank=weiß=white, ivory chap nhan duoc la white """
	elif post['value']=='yellow':
		quest ="""jaune=yellow """		
	elif post['value']=='blue':
		quest ="""navy=bleu=blue """	
	elif post['value']=='vneck':
		quest ="""cổ ngũ giác không lấy,áo con ko lấy """	
	elif post['value']=='round neck':
		quest ="""cổ tau = tron"""			
	else:
		quest=''
	#items = [1, 2, 3, 4, 5, 6, 7]
	#a= random.sample(items,1)[0]
	#random.sample([1, 2, 3, 4, 5],  3)  # Choose 3 elements http://emojipedia-us.s3.amazonaws.com/cache/c2/91/c2918417595a77f6e2257eb6ea996a2d.png

	#	quest ="<img src='http://www.anglaisfacile.com/cgi2/myexam/images/21961.gif'>" + quest
	page ="""document.getElementById('guide').innerHTML="%s<span id='trangt'></span>%s<a href='https://172.16.29.6/wsgi/omnivore/demo/consensus_cu' target='_blank'>$</a>  <a href='https://172.16.29.6' target='_blank'>?</a> Yamaha,comming soon,not image=Placeholder | Youth có lấy".fontsize(1);
			 if (document.getElementById('attributetype').innerHTML != 'color'){
			 document.getElementById('log_all').innerHTML =(document.getElementById('value').innerHTML).fontcolor('red') +"<br /><span='test'>%s</span>".fontsize(0.1).fontcolor('green');}"""%(dog,quest,quest)
	
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
	
	//document.getElementById('trangt').onclick= function(){
	//window.open("http://172.16.29.6");}
	//document.getElementById('sanluong').onclick= function(){
	//window.open("https://172.16.29.6/wsgi/omnivore/demo/report_quantity_module_by_day");}"""
	response = Response(body = page,
                      content_type = "text/javascript",
                      charset = "utf8",
                      status = "200 OK")
 
	return response(environ, start_response)


