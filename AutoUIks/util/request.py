# -*- coding: utf-8 -*-
import mitmproxy.http
import os

class HandleRequest:

    def modify_request(flow: mitmproxy.http.HTTPFlow):
        url = 'http://'+ flow.request.host + '/kssearch/submit/oralevaluatesearch'
        if flow.request.url.startswith(url):
            print("正确的呀")
            imagepath = open(r"../util/testimage.txt", 'rU').readlines()
            path = os.path.dirname(os.path.realpath(__file__))
            complete_path = os.path.join(path, imagepath)
            picname = os.path.basename(complete_path)
            file = open(complete_path, 'rb')
            files = {'image': (picname, file, "application/octet-stream", {"Content-Transfer-Encoding": "8bit"})}
            flow.request.query.update({"image": files})
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"+ flow.request.query)
            print("request" + imagepath)
            print(type(imagepath))
            #data = json.dumps(text)
            #ctx.log.info(str(result))
        # else:
        #     print("else la else la else la else la else la else la else la else la else la else la else la ")

