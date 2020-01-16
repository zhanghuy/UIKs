# -*- coding: utf-8 -*-
import mitmproxy.http
import json


# # image = sys.argv[1]
# runlist = [
#     request.HandleRequest().modify_request(),
#     response.HandleResponse().get_response()
# ]

# def get_response(flow: mitmproxy.http.HTTPFlow):
#     url = 'http://' + flow.request.host + '/kssearch/submit/oralevaluatesearch'
#     if flow.request.url.startswith(url):
#         print("================================正确的呀=========================================")
#
#         # 读取测试图片
#         # imagepath = open(r"../util/testimage.txt", 'rU').readlines()
#         # path = os.path.dirname(os.path.realpath(__file__))
#         # complete_path = os.path.join(path, imagepath)
#         # picname = os.path.basename(complete_path)
#         # file = open(complete_path, 'rb')
#         # files = {'image': (picname, file, "application/octet-stream", {"Content-Transfer-Encoding": "8bit"})}
#         # flow.request.query.update({"image": files})
#         # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n" + flow.request.query)
#         # print("request" + imagepath)
#         # print(type(imagepath))
#
#         # 写入接口返回的图片信息
#         text = flow.response.text
#         data_json = json.loads(text)
#         print("脚本")
#         if data_json.get('data'):
#             imginfo = data_json.get('data').get('imageInfo')
#             with open('.\\query.txt', 'a+') as f:
#                 f.truncate()
#                 print("image")
#                 print(str(imginfo))
#                 f.write(str(imginfo) + '\n')
#                 f.close()
#
#         # 写入接口返回的框选坐标
#         if data_json.get('data').get('questionList'):
#             datas = data_json.get('data').get('questionList')
#             with open('.\\coordinate.txt', 'w') as f:
#                 f.truncate()
#                 for data in datas:
#                     exptype = data.get('expType')
#                     questionType = data.get('questionType')
#                     if ((questionType == 1) and (exptype == 2)) or questionType == 2:
#                         print(type(data.get('coordinate')))
#                         print(data.get('coordinate'))
#                         coordinate = data.get('coordinate')
#                         f.write(str(coordinate) + '\n')
#             f.close()
#
#         # data = json.dumps(text)
#
#         # ctx.log.info(str(result))
#     else:
#         print("else la else la else la else la else la else la else la else la else la else la else la ")

# 所有发出的请求数据包都会被这个方法所处理
# 所谓的处理，我们这里只是打印一下一些项；当然可以修改这些项的值直接给这些项赋值即可
#     def request(flow):
#         # 获取请求对象
#         request = flow.request
#         # 实例化输出类
#         info = ctx.log.info
#         # 打印请求的url
#         info(request.url)
#         # 打印请求方法
#         info(request.method)
#         # 打印host头
#         info(request.host)
#         # 打印请求端口
#         info(str(request.port))
#         # 打印所有请求头部
#         info(str(request.headers))
#         # 打印cookie头
#         info(str(request.cookies))

# 所有服务器响应的数据包都会被这个方法处理
# 所谓的处理，我们这里只是打印一下一些项
#     def response(flow):
#         # 获取响应对象
#         response = flow.response
#         # 实例化输出类
#         info = ctx.log.info
#         # 打印响应码
#         info(str(response.status_code))
#         # 打印所有头部
#         info(str(response.headers))
#         # 打印cookie头部
#         info(str(response.cookies))
#         # 打印响应报文内容
#         info(str(response.text))


# 设置上游代理
# def request(self, flow: mitmproxy.http.HTTPFlow):
#      if flow.request.method == "CONNECT":
#          return
#      if flow.live:
#          proxy = ('http://121.228.53.238', '9990')
#          print(flow.request.host)
#          flow.live.change_upstream_proxy_server(proxy)
# str = 'cmd.exe mitmdump -s ./pyscript.py - p 8080'
# d = os.system('mitmdump')
# print(d)
# mitmproxy.mitmdump(str)
# os.system('mitmweb -s proxyscript.py -p 8082')

def response(flow: mitmproxy.http.HTTPFlow):
    url = 'http://' + flow.request.host + '/kssearch/submit/oralevaluatesearch'
    if flow.request.url.startswith(url):
        print("正确的呀")
        text = flow.response.text
        data_json = json.loads(text)
        print("脚本")
        if data_json.get('data'):
            imginfo = data_json.get('data').get('imageInfo')
            with open('.\\util\\query.txt', 'w') as f:
                f.truncate()
                print("image")
                print(str(imginfo))
                f.write(str(imginfo) + '\n')
                f.close()
        if data_json.get('data').get('questionList'):
            datas = data_json.get('data').get('questionList')
            with open('.\\util\\coordinate.txt', 'w') as f:
                f.truncate()
                for data in datas:
                    exptype = data.get('expType')
                    questionType = data.get('questionType')
                    if ((questionType == 1) and (exptype == 2)) or questionType == 2:
                        print(type(data.get('coordinate')))
                        print(data.get('coordinate'))
                        coordinate = data.get('coordinate')
                        f.write(str(coordinate) + '\n')
            f.close()

        # data = json.dumps(text)

        # ctx.log.info(str(result))
    else:
        print("else la else la else la else la else la else la else la else la else la else la else la ")
