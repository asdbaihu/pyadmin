# -*- coding: utf-8 -*-
import requests, json, random
import logging,time,pymysql.cursors
# from pyquery import PyQuery as pq
# from lxml import etree
# import urllib


logging.basicConfig(
    filename='/var/log/pyadmin/runtime.log',
    format='%(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s',
    level=logging.DEBUG
)
logging.info('testting')

def getConnection():
    # You can change value connection.
    connection = pymysql.connect(host='192.168.0.118',
                                 port=3306,
                                 user='docker',
                                 password='docker',
                                 db='docker',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection

connection = getConnection()
try:
    with connection.cursor() as cursor:
        sql = "select cookies from fbcrawler_service_account where cookies like '%%facebook.com%%' and  cookies is not null and homepage like '%%https://m.facebook.com%%' and homepage not like '%%checkpoint/block%%'"
        cursor.execute(sql)
        rs = cursor.fetchall()
        connection.commit()
finally:
    connection.close()

time_waits = [2,3,5]



for row in rs:
    cs = row['cookies']
    #print(row['cookies'])

    j = json.loads(cs)
    s = requests.Session()
    for cookie in j:
        #logging.info(cookie['name'])
        s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'],
                      path=cookie['path'])

    r = s.get('https://www.facebook.com/pinkypinky.trang')

    # d = pq(r.content)
    from bs4 import BeautifulSoup

    #print(d('#toolbarContainer'))
    soup = BeautifulSoup(r.content,'html.parser')
    #print(s.cookies.get_dict()['c_user'])
    logging.info(s.cookies.get_dict())
    time.sleep(random.choice(time_waits))

cs = """[  
{
    "domain": ".facebook.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "act",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "1522396174558%2F3",
    "id": 1
},
{
    "domain": ".facebook.com",
    "expirationDate": 1530171177.947926,
    "hostOnly": false,
    "httpOnly": false,
    "name": "c_user",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": "true",
    "session": "false",
    "storeId": "0",
    "value": "100022700031597",
    "id": 2
},
{
    "domain": ".facebook.com",
    "expirationDate": 1572508081.213666,
    "hostOnly": false,
    "httpOnly": true,
    "name": "datr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "qyr4WR9Ez1nWorA_JZ_gWZ4e",
    "id": 3
},
{
    "domain": ".facebook.com",
    "expirationDate": 1530171177.947977,
    "hostOnly": false,
    "httpOnly": true,
    "name": "fr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "03f31XtHmTnhcxGxt.AWVbLI0j4vZbeBOWC_2ltLcS9ZU.BZ-Cqr.88.Fq9.0.0.Bavegp.AWWn-NPS",
    "id": 4
},
{
    "domain": ".facebook.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "presence",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "EDvF3EtimeF1522396563EuserFA21B227B31597A2EstateFDutF1522396563503Et3F_5b_5dElm3FnullEutc3F0CEchFDp_5f1B227B31597F3CC",
    "id": 5
},
{
    "domain": ".facebook.com",
    "expirationDate": 1572508088.996946,
    "hostOnly": false,
    "httpOnly": true,
    "name": "sb",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "qyr4WWKRT2rk0TZFezrAeC4B",
    "id":6
},
{
    "domain": ".facebook.com",
    "expirationDate": 1523001449,
    "hostOnly": false,
    "httpOnly": false,
    "name": "wd",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1235x987",
    "id": 7
},
{
    "domain": ".facebook.com",
    "expirationDate": 1530171177.94796,
    "hostOnly": false,
    "httpOnly": true,
    "name": "xs",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "16%3AxgYlXQxrcmh3VA%3A2%3A1509436088%3A-1%3A-1",
    "id": 8
}
]"""

cs1= """[
{
    "domain": ".facebook.com",
    "expirationDate": 1530412457.536839,
    "hostOnly": false,
    "httpOnly": false,
    "name": "c_user",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "100024046030935",
    "id": 1
},
{
    "domain": ".facebook.com",
    "expirationDate": 1579481568.225913,
    "hostOnly": false,
    "httpOnly": true,
    "name": "datr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "4JJiWjbfCFsdy6WTE64wSKDa",
    "id": 2
},
{
    "domain": ".facebook.com",
    "expirationDate": 1522921585,
    "hostOnly": false,
    "httpOnly": false,
    "name": "dpr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1.100000023841858",
    "id": 3
},
{
    "domain": ".facebook.com",
    "expirationDate": 1530412457.536998,
    "hostOnly": false,
    "httpOnly": true,
    "name": "fr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "0oA9PPSe75jOlUxPk.AWXEecAjwDGb0stgKzeRfOWKDps.BaYpLg.AW.Fq8.0.0.BawZap.AWX4w8KB",
    "id": 4
},
{
    "domain": ".facebook.com",
    "expirationDate": 1524185670.408991,
    "hostOnly": false,
    "httpOnly": true,
    "name": "pl",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "n",
    "id": 5
},
{
    "domain": ".facebook.com",
    "expirationDate": 1579481670.408812,
    "hostOnly": false,
    "httpOnly": true,
    "name": "sb",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "4JJiWn6Y0OcEtg2lXNM6Mivz",
    "id": 6
},
{
    "domain": ".facebook.com",
    "expirationDate": 1523243897,
    "hostOnly": false,
    "httpOnly": false,
    "name": "wd",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1685x897",
    "id": 7
},
{
    "domain": ".facebook.com",
    "expirationDate": 1530412457.536927,
    "hostOnly": false,
    "httpOnly": true,
    "name": "xs",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "32%3AkGOlKJQnlJj0ZQ%3A2%3A1516409671%3A-1%3A-1",
    "id": 8
}
]
"""



#print(s.cookies.get_dict())


#print(soup.prettify())
# print(soup.find_all('div'))
#print(soup.find_all("id='contentArea'"))
#print(soup.prettify())
#print(list(soup.children))
#print([type(item) for item in list(soup.children)])
# html = list(soup.children)[2]
# #print(list(html.children))
# body = list(html.children)
# print(body)
#print(soup.find_all('div',class_='_li'))

