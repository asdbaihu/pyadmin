from beaker.middleware import SessionMiddleware
import importlib


def application(environ, start_response):
  from webob import Request, Response
  # from datetime import datetime
  # request = Request(environ)
  # post = request.POST
  import importlib, pyad.login
  importlib.reload(pyad.login)
  from pyad import login

  # Get the session object from the environ
  session = environ['beaker.session']

  # Check to see if a value is in the session
  user = 'username' in session
  passwd = 'password' in session

  # Set some other session variable
  # session['user_id'] = 10
  # user_id = 'user_id' in session

  if not 'username' in session:
    page = pyad.login.loginform
  elif not 'password' in session:
    page = pyad.login.loginform
  else:
    user = session['username']
    passwd = session['password']

    import psycopg2, hashlib, pyad.conn
    importlib.reload(pyad.conn)
    from pyad.conn import conn
    try:
      con = psycopg2.connect(conn)
    except:
      page = "Can not access databases"

    cur = con.cursor()
    cur.execute(
      "select username,account_password,account_level from account where username=%s and account_password=%s ",
      (user, passwd,))
    ps = cur.fetchall()
    if len(ps) == 0:
      page = pyad.login.login_again
    else:
      import pyad.module
      importlib.reload(pyad.module)
      from pyad.module import head, headlink, menuadmin, menuuser, menuhead, menufoot

      page = ""
      page += head + headlink
      page += "<title>home page</title>"
      page += """
      <style>
.center {
    margin: auto;
    width: 60%;
    border: 3px solid #73AD21;
    padding: 10px;
}
</style>  
      </head>
      <body>"""
      page += menuhead
      if int(ps[0][2]) == 2:
        page += menuadmin
      else:
        page += menuuser
      page += menufoot
      page += """						
            <br />
            <br />
            <br />
            <br />"""

      page += """
      <div class="center">
      <button onclick="myFunction()">Try it</button>
      <p id="show"></p>
        Test:(khi dien input vao) , se check khi input chuyen tu trang thai khong co gi sang co value thi thong bao tren
        console log. Tuong tu doi anh load ra se bat dau do something <br />
        <input id ='test' name='test' type='text' /> <br />
        <p id ="step1">start 1</p>
        <p id ="step2">step 2</p>
        <p id ="step3">step 3t</p>
        </div>
      <script>
      var i =0; 
var stop = 0;
var check_step;
function count(){
var dem = setInterval(function(){
    document.getElementById("show").innerHTML=i;
    localStorage['count']= i;
    i++;
 },1000);
} 
count();
class_step1();


function class_step1(){
  step1 =  setInterval(function(){ 
    if($("#test").val().length > 0){
      clearInterval(step1);    
      check_step = "step1_finish";
      document.getElementById("step1").innerHTML= check_step+ "step1. Bat dau co value:" + $("#test").val() +". Do continue " ;
      console.log(check_step);
      console.log("Value xuat hien: " + $("#test").val());
      class_step2();
    };
  }, 500);
}  




function class_step2(){
  step2 =  setInterval(function(){ 
    if(i==10 && check_step=="step1_finish"){
      clearInterval(step2);    
      setTimeout(function(){
      check_step = "step2_finish";
      },10000);
      document.getElementById("step2").innerHTML= check_step+ "step2";
      console.log(check_step);
      class_step3();
    };
  }, 500);
}  

function class_step3(){
  step3 =  setInterval(function(){ 
    if(/*i==20 && */check_step=="step2_finish"){
      clearInterval(step3);    
      check_step = "step3_finish";
      document.getElementById("step3").innerHTML= check_step+ "step3";
      console.log(check_step);
      window.close();
      window.top.close();
    };
  }, 500);
} 
 
</script>
      """

    con.commit()
    cur.close()
    con.close()
  response = Response(body=page,
                      content_type="text/html",
                      charset="utf8",
                      status="200 OK")

  return response(environ, start_response)


# Configure the SessionMiddleware
import pyad.sess

importlib.reload(pyad.sess)
session_opts = pyad.sess.session_opts
application = SessionMiddleware(application, session_opts)
