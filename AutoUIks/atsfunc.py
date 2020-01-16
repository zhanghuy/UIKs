from zybats.ext.appext.dbUtil import Db
from zybats.ext.appext.redisUtil import RedisSingleNode
import os
import time
import random
import json
from urllib.parse import quote
import datetime

def get_picsearch_imgpath(imagepath):
    imagepath='image/yinshuati.jpg'
    path=os.path.dirname(os.path.realpath(__file__))
    picsearch_imgpath=os.path.join(path, imagepath)
    return picsearch_imgpath

def upload_file(request,imagepath):
    path=os.path.dirname(os.path.realpath(__file__))
    complete_path=os.path.join(path, imagepath)
    picname=os.path.basename(complete_path)
    file = open(complete_path, 'rb')
    files = {'image':(picname, file, "application/octet-stream", {"Content-Transfer-Encoding": "8bit"})}
    request["files"] = files

def get_user_identity():
    identity_list=[3,4,5]
    idenfity=random.choice(identity_list)
    return idenfity

def get_user_grade():
    grade_list=[9,11,12,13,14,15,16,21,22,23,31,32,33]
    grade=random.choice(grade_list)
    return grade

def get_session_base_url():
    url = os.environ['URL']
    if '.com' not in url:
        url='https://kousuan.zybang.com'
    return url

def get_base_url():
    url = os.environ['URL']
    return url

def get_base_time():
    sleeptime = os.environ['sleeptime']
    return int(sleeptime)

def teardown_hook_sleep_N_secs(response, n_secs):
    """ sleep n seconds after request
    """
    if response.status_code == 200:
        time.sleep(n_secs)
    else:
        time.sleep(10)

def query_mysql_one_result(sql_str):
    ip = "192.168.240.197"
    port = 8888
    user_name = "root"
    password = "root"
    db_name = "adx_admin"

    dbClient = Db(ip, port, user_name, password, db_name)
    result = dbClient.select(sql_str)
    return result[0][0]

def get_redis_str_value(key):
    ip = "192.168.240.98"
    port = 6379

    client = RedisSingleNode(ip, port)
    v = client.get(key)

    return v.decode()


def show_request_function(request_body, replace_app_id):
    print("You can do something here! for example:")
    request_body["json"]["appId"] = replace_app_id
    print("Replaced request body is:", request_body)

def show_response_function(response_body, id):
    print("You can do something here! for example:")
    print(response_body)

def get_list_len(lst):
    return len(lst)

def gen_random_cuid():
    num = random.randint(1000000,9999999)
    cuid = 'QAPerfTest9AC301AA91D1EB71C8C' + str(num)+'|0'
    return cuid


def get_openId():
    openidlist = ['orPQE5ufuNOGpwcZ_etEauSHNvjg','orPQE5t6t7gL7iXhdxXBCG7AJMvo','orPQE5nLS7hK8_CxRXpuUir0e1yc','orPQE5rpY6tp16At1JQu_W2B8Vj4','orPQE5oZRK2pO7oauSC95ak1N_zk','orPQE5t6R-Thv1NBhLZ_1n2cVLI0']
    hour=int(time.strftime('%H',time.localtime(time.time())))
    if 0 <= hour <= 3:
        openid=openidlist[0]
    if 4 <= hour <= 7:
        openid=openidlist[1]
    if 8 <= hour <= 11:
        openid=openidlist[2]
    if 12 <= hour <= 15:
        openid=openidlist[3]
    if 16 <= hour <= 19:
        openid=openidlist[4]
    if 20 <= hour <= 23:
        openid=openidlist[5]
    ExecScenario = os.environ['ExecScenario']
    if ExecScenario=='70' or ExecScenario=='8':
       openid='orPQE5o-3RWFN5dx42D3Lz7KZpDU'
    return openid

def get_openId_arith():
    openid='ox_mu4qDla2LdEMiqbNjJE6v0kS8'
    return openid

def update_url(request):
    num = random.randint(1000000000,9999999999)
    newurl=request["url"]+'&'+'logid='+str(num)
    request["url"] = newurl

def sleep():
    time.sleep(1)

def sleepocr():
    time.sleep(15)

def get_sidlist_json(sid,request):
    list = [{"sid": sid}]
    jlist = json.dumps(list)
    request["data"]["sidList"] = jlist

def get_qcontent_json(questionType,errorFormula,correctFormula,request):
    if(questionType == '200'):
        dict = {"errorFormula": errorFormula, "correctFormula": correctFormula, "style": 0, "question": "NULL"}
        jdict = json.dumps(dict)
        request["data"]["questionContent"] = jdict
    else:
        request["data"]["questionContent"] = ''

def get_content_json(sid,turl,twidth,theight,aurl,awidth,aheight,qtype,request):
    if(aurl == '' and awidth== '' and aheight==''):
        dict = [{"sid":sid,"imageInfo":{"url":turl,"width":twidth,"height":theight},"qType":qtype}]
    else:
        dict = [{"sid": sid,"imageInfo":{"url":turl,"width": twidth,"height":theight},"answerImage":{"url":aurl,"width":awidth,"height":aheight},"qType":qtype}]
    jdict = json.dumps(dict)
    request["data"]["content"] = jdict

def get_urlencode_data(data,request):
    request["data"]["value"]=quote(data)

def set_current_date(request):
    currentDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    request["data"]["startTime"]=currentDate
    request["data"]["endTime"] = currentDate

def login_scene(request):
    ExecScenario = os.environ['ExecScenario']
    if ExecScenario=='70' or ExecScenario=='8':
       request["data"]["phone"]=os.environ['phone_tips']
       request["data"]["password"]=os.environ['password_tips']
    else:
       request["data"]["phone"]=os.environ['phone']
       request["data"]["password"]=os.environ['password']

def getcookie_scene(request,sessionKey,sessionId):
    newcookie=sessionKey+"="+sessionId
    request["headers"]["Cookie"]=newcookie

def get_random_voice():
    a = chr(random.randint(0x4e00, 0x9fbf))
    b='来看十位十位我们需要计算1减1减1等于0最高位结果为0省略不写'
    c=random.choice(b)
    name=a+c
    e='[{"name":"%s","channel":1,"type":1,"code":0,"speed":4}]'%name
    return e

if __name__ =='__main__':
    a = chr(random.randint(0x4e00, 0x9fbf))
    b='来看十位十位我们需要计算1减1减1等于0最高位结果为0省略不写'
    c=random.choice(b)
    d=a+c
    e='[{"name":"%s","channel":1,"type":1,"code":0,"speed":4}]'%d
    print(e)