# -*- coding: utf-8 -*-
import mitmproxy.http
import json
import mitmproxy
import os
# # image = sys.argv[1]
# runlist = [
#     request.HandleRequest().modify_request(),
#     response.HandleResponse().get_response()
# ]

def get_response(flow: mitmproxy.http.HTTPFlow):
    url = 'http://'+ flow.request.host + '/kssearch/submit/oralevaluatesearch'
    if flow.request.url.startswith(url):
        print("================================正确的呀=========================================")

        #读取测试图片
        # imagepath = open(r"../util/testimage.txt", 'rU').readlines()
        # path = os.path.dirname(os.path.realpath(__file__))
        # complete_path = os.path.join(path, imagepath)
        # picname = os.path.basename(complete_path)
        # file = open(complete_path, 'rb')
        # files = {'image': (picname, file, "application/octet-stream", {"Content-Transfer-Encoding": "8bit"})}
        # flow.request.query.update({"image": files})
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" + flow.request.query)
        # print("request" + imagepath)
        # print(type(imagepath))

        #写入接口返回的图片信息
        text = flow.response.text
        data_json = json.loads(text)
        print("脚本")
        if data_json.get('data'):
            imginfo = data_json.get('data').get('imageInfo')
            with open('.\\util\\queryinfo.txt', 'a+') as f:
                f.truncate()
                print("image")
                print(str(imginfo))
                f.write(str(imginfo)+'\n')
                f.close()

        #写入接口返回的框选坐标
        if data_json.get('data').get('questionList'):
            datas = data_json.get('data').get('questionList')
            with open('.\\util\\coordinate.txt','w') as f:
                f.truncate()
                for data in datas:
                    exptype = data.get('expType')
                    questionType = data.get('questionType')
                    if ((questionType == 1) and (exptype == 2)) or questionType == 2:
                        print(type(data.get('coordinate')))
                        print(data.get('coordinate'))
                        coordinate = data.get('coordinate')
                        f.write(str(coordinate)+'\n')
            f.close()

        #data = json.dumps(text)

        #ctx.log.info(str(result))
    else:
        print("else la else la else la else la else la else la else la else la else la else la else la ")

