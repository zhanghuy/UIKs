# -*- coding: utf-8 -*-
import mitmproxy.http
import json

class HandleResponse:
    def get_response(flow: mitmproxy.http.HTTPFlow):
        url = 'http://'+ flow.request.host + '/kssearch/submit/oralevaluatesearch'
        if flow.request.url.startswith(url):
            print("正确的呀")
            text = flow.response.text
            data_json = json.loads(text)
            print("脚本")
            if data_json.get('data'):
                imginfo = data_json.get('data').get('imageInfo')
                with open('.\\queryinfo.txt', 'a+') as f:
                    f.truncate()
                    print("image")
                    print(str(imginfo))
                    f.write(str(imginfo)+'\n')
                    f.close()
            if data_json.get('data').get('questionList'):
                datas = data_json.get('data').get('questionList')
                with open('.\\coordinate.txt','w') as f:
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
        # else:
        #     print("else la else la else la else la else la else la else la else la else la else la else la ")

