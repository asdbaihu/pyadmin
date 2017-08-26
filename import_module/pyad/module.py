project ="/wsgi/pyad"
control = "%s/control"%project
js ="http://192.168.0.136/pyad/js"
bootstrap = "http://192.168.0.136/pyad/bootstrap"
load = "%s/load"%project 
save = "%s/save"%project    

csshead ="""
          <style data-jsfiddle="common">
            .handsontable .currentRow {
              background-color: #E7E8EF;
            }

            .handsontable .currentCol {
              background-color: #F9F9FB;
            }
            						#ui-datepicker-div{z-index:9000;}
									#datepicker{z-index:9000;}
									#example1{z-index:1;}
          </style>"""          
head ="""<!doctype html>
			<html>
				<head>
					<meta charset='utf-8'>"""

csscheckbox =""".multiselect-container>li>a>label {
  padding: 4px 20px 3px 20px;
}"""



headlink ="""<script type="text/javascript" src="%s/jquery.min.js"></script>"""%js
headlink+="""<script type="text/javascript" src="%s/js/bootstrap.js"></script>
<script type="text/javascript" src="%s/js/dropdowns-enhancement.js"></script>
<script type="text/javascript" src="%s/js/bootstrap-multiselect.js"></script>

"""%(bootstrap,bootstrap,bootstrap)
headlink+="""<link rel="stylesheet" href="%s/css/bootstrap.css" type="text/css">
<link rel="stylesheet" href="%s/css/dropdowns-enhancement.css" type="text/css">
<link rel="stylesheet" href="%s/css/bootstrap-multiselect.css" type="text/css"/>
			"""%(bootstrap,bootstrap,bootstrap)
headlink+="""<script type="text/javascript" src="%s/jquery.bootpag.min.js"></script>"""%js			
headlink+="""<script type="text/javascript" data-jsfiddle="common" src="%s/handsontable.full.js"></script>"""%js
headlink+="""<link data-jsfiddle="common" rel="stylesheet" media="screen" href="%s/handsontable.full.css" type="text/css">"""%js
headlink+="""<!-- the below is only needed for DateCell (uses jQuery UI Datepicker) -->"""
headlink+="""<script type="text/javascript" src="%s/jquery-ui.js"></script>"""%js
headlink+="""<link rel="stylesheet" href="%s/jquery-ui.css" type="text/css">"""%js
headlink+="""						
			<style data-jsfiddle="common">
			.handsontable .currentRow {
			background-color: #E7E8EF;
			}

			.handsontable .currentCol {
			background-color: #F9F9FB;
			}
			#ui-datepicker-div{z-index:9000;}
			#datepicker{z-index:9000;}
			#example1{z-index:1;}


			</style>
			
			
			<script>
			$("#datepicker").datepicker();
			$("#format").change(function() {
			$("#datepicker").datepicker( "option", "dateFormat", $( this ).val());
			});
    </script>"""
    
import importlib,pyad.conn
importlib.reload(pyad.conn)    
from pyad.conn import conn
import psycopg2
import psycopg2.extras
import psycopg2.extensions 

con = psycopg2.connect(conn)
cur = con.cursor()

menuhead ="""<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
						<div class="container">
						<div class="navbar-collapse collapse">
							<ul class="nav navbar-nav">"""
menuadmin =""

cur.execute("""Select fid,menu1,link from admin_first_menu order by id""")
ps_admin_menu1 = cur.fetchall()
cur.execute("""Select fid,menu1,link from first_menu order by id""")
ps_menu1 = cur.fetchall()

for row_admin1 in ps_admin_menu1:
	cur.execute("""Select menu2,link from admin_second_menu where first_menu_id = %s order by id """%row_admin1[0])
	ps_admin_menu2 = cur.fetchall()
	if len(ps_admin_menu2)>0:
		menuadmin +="""<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href='%s'>%s<b class="caret"></b></a>"""%(row_admin1[2],row_admin1[1])
		menuadmin +="""<ul class="dropdown-menu">"""
		for row_admin2 in ps_admin_menu2:
			menuadmin +="""<li><a href='%s'>%s</a></li>"""%(row_admin2[1],row_admin2[0])
		menuadmin +="""</ul></li>"""
	else:
		menuadmin +="""<li><a href='%s'>%s</a></li>"""%(row_admin1[2],row_admin1[1])
for row1 in ps_menu1:
	cur.execute("""Select menu2,link from second_menu where first_menu_id = %s order by id """%row1[0])
	ps_menu2 = cur.fetchall()
	if len(ps_menu2)>0:
		menuadmin +="""<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href='%s'>%s<b class="caret"></b></a>"""%(row1[2],row1[1])
		menuadmin +="""<ul class="dropdown-menu">"""
		for row2 in ps_menu2:
			menuadmin +="""<li><a href='%s'>%s</a></li>"""%(row2[1],row2[0])
		menuadmin +="""</ul></li>"""
	else:
		menuadmin +="""<li><a href='%s'>%s</a></li>"""%(row1[2],row1[1])

menuuser =""

cur.execute("""Select fid,menu1,link from first_menu order by id""")
ps_menu1 = cur.fetchall()
for row1 in ps_menu1:
	cur.execute("""Select menu2,link from second_menu where first_menu_id = %s order by id """%row1[0])
	ps_menu2= cur.fetchall()
	if len(ps_menu2)>0:
		menuuser +="""<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href='%s'>%s<b class="caret"></b></a>"""%(row1[2],row1[1])
		menuuser +="""<ul class="dropdown-menu">"""
		for row2 in ps_menu2:
			menuuser +="""<li><a href='%s'>%s</a></li>"""%(row2[1],row2[0])
		menuuser +="""</ul></li>"""
	else:
		menuuser +="""<li><a href='%s'>%s</a></li>"""%(row1[2],row1[1])
		
menufoot ="""</ul>
				</div>
					</div>
						</nav>"""		

con.commit()
cur.close()
con.close()	

