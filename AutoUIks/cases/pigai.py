#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Shengjie.Liu
# @Time    : 2019-06-03 14:47
# @File    : calculator_test.py
# @Desc    :

#导入unittest测试框架
import os
import unittest
from selenium import webdriver as seleniumdriver

#导入appium客户端库

from PIL import ImageFile, Image
from appium import webdriver

#导入time模块
import time
from time import sleep
#导入HtmlTestRunner
import HtmlTestRunner
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import re
import ast
import imagehash
import photohash


class CalculatorTest(unittest.TestCase):
    # pass
    # def __init__(self):
    #     self.deviceName = 'PD2717C'
    deviceName = 'PD2717C'
    relativeoffset = 358.5/2160
    #img_path = []  # 用来存放图片地址
    # 封用来判断元素标签是否存在
    # obj = subprocess.Popen("mitmdump -s mitmproxyscript.py -p 8811", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                        stderr=subprocess.PIPE, universal_newlines=True)
    # obj = subprocess.Popen("mitmdump -p 8085", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                       stderr=subprocess.PIPE, universal_newlines=True)
    # obj = subprocess.Popen("adb devices", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                        stderr=subprocess.PIPE, universal_newlines=True)

    def isElementPresent(self, by, value):
        try:
            self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True
    def get_image_path(self, filename, questionIndex, case= 'result'):
        file_path = os.path.dirname(os.path.abspath(".")) + '\\result_image\\'
        #now = time.strftime('%Y-%m-%d_%H_%M_%S_')
        screen_name = "%simage%s_%s_%s_%s.png" % (file_path, questionIndex, self.deviceName, filename, case)
        return screen_name

    def get_screent_img(self):
        """"页面截图功能"""
        screen_name = self.get_image_path()
        try:
            self.driver.get_screenshot_as_file(screen_name)
            #logger.info('页面截图 %s，截图路径在: /screenshots/目录下' % self.driver.get_screenshot_as_file(screen_name))
        except NameError as na:
            #logger.info("截图失败:%s" % na)
            #self.get_screent_img()
            print("截图失败-------------------------")


    def allways_allow(self, number=2):
        for i in range(number):
            try:
                # loc = ("xpath", "//*[@text='允许']")
                loc = ("xpath", "//*")
                #e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_all_elements_located(loc))
                while 1:
                    e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_all_elements_located(loc))
                    if not e:
                        break
                    if e:
                        self.driver.switch_to.alert.accept()
                        print('allow success')
                        sleep(1)
            except:
                pass

    def get_last_line(self, filename):
        """
        get last line of a file
        :param filename: file name
        :return: last line or None for empty file
        """
        try:
            filesize = os.path.getsize(filename)
            if filesize == 0:
                return None
            else:
                with open(filename, 'rb') as fp:  # to use seek from end, must use mode 'rb'
                    offset = -8  # initialize offset
                    while -offset < filesize:  # offset cannot exceed file size
                        fp.seek(offset, 2)  # read # offset chars from eof(represent by number '2')
                        lines = fp.readlines()  # read from fp to eof
                        if len(lines) >= 2:  # if contains at least 2 lines
                            return lines[-1]  # then last line is totally included
                        else:
                            offset *= 2  # enlarge offset
                    fp.seek(0)
                    lines = fp.readlines()
                    return lines[-1]
        except FileNotFoundError:
            print(filename + ' not found!')
            return None

    def get_img(self):
        imgfile = "../util/query.txt"
        line = ast.literal_eval(bytes.decode(self.get_last_line(imgfile)))
        queryurl = line.get('url')
        imgsize = {'width': line.get('width'), 'height': line.get('height')}
        return imgsize, queryurl


    # def get_img(self):
    #     imgsize = {}
    #     imgfile = "../util/query.txt"
    #     with open(imgfile, encoding='utf-8') as f:
    #         while 1:
    #             lines = f.readlines(100)
    #             if not lines:
    #                 break
    #             for line in lines:
    #                 line = ast.literal_eval(line)
    #                 queryurl = line.get('url')
    #                 imgsize = {'width': line.get('width'), 'height': line.get('height')}
    #             return imgsize, queryurl

    def get_loc(self, imgsize):
       coordinateList = []
       coordinatefile = "../util/coordinate.txt"
       with open(coordinatefile, encoding='utf-8') as f:
           while 1:
               lines = f.readlines(100)
               if not lines:
                   break
               for line in lines:
                   line = ast.literal_eval(line)
                   topLeftX = line['topLeftX']
                   topLeftY = line['topLeftY']
                   downLeftX = line['downLeftX']
                   downLeftY = line['downLeftY']
                   downRightX =line['downRightX']
                   downRightY = line['downRightY']
                   topRightX = line['topRightX']
                   topRightY = line['topRightY']
                   leftX = (topLeftX + downLeftX) / 2
                   rightX = (topRightX + downRightX) / 2
                   topY = (topLeftY + topRightY) / 2
                   downY = (downLeftY + downRightY) / 2
                   x = abs(rightX - leftX)/2 + leftX
                   y = abs(topY + downY)/2+ downY

                   #获取屏幕大小
                   el_x = self.driver.get_window_size()['width']
                   el_y = self.driver.get_window_size()['height']
                   # 获取图片大小
                   img_w = imgsize['width']
                   img_h = imgsize['height']

                   if (img_w/img_h) > (el_x/el_y):  #宽图
                       relative_h = el_x * (img_h/img_w)
                       relative_y = (el_y - relative_h)/2
                       coordinateList.append((x, y+relative_y))
                   elif (img_w/img_h) < (el_x/el_y): #长图
                       relative_w = el_y * (img_w / img_h)
                       relative_x = (el_x - relative_w) / 2
                       coordinateList.append((x +  + relative_x, y))


                   # 绝对坐标转换为相对坐标，假设当前分辨率为720x1280，绝对坐标为(x, y)
                   #xd_x = int((x / el_x) * el_x)
                   #xd_y = int((y / el_y) * el_y)
                   #coordinateList.append((xd_x,xd_y))

                   return coordinateList
    def joint_image(self, imagelist, width, sc_hight, i, filename, questionIndex):
        new_img = Image.new("RGB", (width, sc_hight * i))  # 创建一个新图片,大小为元素的大小
        k = 0
        for i in imagelist:
            tem_img = Image.open(i)
            new_img.paste(tem_img, (0, sc_hight * k))  # 把图片贴上去,间隔一个截图的距离
            k += 1
        else:
            new_img.save(self.get_image_path(filename, questionIndex))  # 保存
        print(str(i)+self.get_image_path(filename, questionIndex))

    def compare_image_with_hash(self, image1, image2, max_dif=0):
        """
        :param max_dif: 允许最大hash差值，越小越精确，最小为0
        """
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        with open(image1, 'rb') as fp:
            hash_1 = imagehash.average_hash(Image.open(fp))
        with open(image2, 'rb') as fp:
            hash_2 = imagehash.average_hash(Image.open(fp))
        distance = photohash.hash_distance(str(hash_1), str(hash_2))  #汉明距离 小于等于5时我们认为这两张图非常相似，大于10 则认为这两张图完全不一样
        # distance = 0:image1和image2完全不像；distance=1：image1和image2完全一样；distance=2：image1和image2部分重叠
        if distance < 0:
            distance = -distance
        if distance <= max_dif:
            return 1
        else:
            return 0
        #elif distance > 10:
        #     return 0
        # else:
        #     return 2

    def result_scroll(self, location, size, select, filename, questionIndex):
        img_path = []  # 用来存放图片地址
        start_higth = location["y"]  # 元素的初始高度
        sc_hight = size['height']
        screenPath = self.get_image_path(filename,"result_%s") % 0
        select.screenshot(screenPath)
        img_path.append(screenPath)
        i = 1
        imagelike = 0
        el_h = self.driver.get_window_size()['height']
        while imagelike is not 1:
            print(start_higth + sc_hight-0.1)
            print(start_higth)
            if imagelike is 0:
                #js = 'javascript:mobile.onGetWebContentHeight' # 用于移动滑轮，每次移动614px，初始值是元素的初始高度
                #self.driver.swipe(1, start_higth + sc_hight-0.1, 1, start_higth+49.5, 8000)  #每次向上滑动(sc_hight)px
                # 实现滑动的另一种方法,move_to里的坐标是相对于前一个坐标的偏移量

                TouchAction(self.driver).press(x=1,y=(start_higth + sc_hight-0.1)).wait(1000).move_to(x=1, y=start_higth + self.relativeoffset * el_h).release().perform()
            if imagelike is 2:
                self.driver.swipe(1, start_higth + sc_hight-0.1, 1, start_higth+300, 1000)  #每次向上滑动(sc_hight)px
            time.sleep(0.5)
            screenPath = self.get_image_path(filename,"result_%s") % i  # 图片地址，运行的话，改一下
            select.screenshot(screenPath)
            print(str(i) + screenPath)
            img_path.append(screenPath)  # 添加图片路径
            if len(img_path) > 1:
                imagelike = self.compare_image_with_hash(img_path[-1], img_path[-2])
            i = i + 1
            print("imagelike"+ str(imagelike))

        if len(img_path) > 1:
            self.joint_image(img_path[0:-1], size['width'], sc_hight, i-1, filename, questionIndex)
            for path in img_path:
                os.remove(path)
                print("remove "+ path + " success!")

    def answer_results(self):
        i = 1
        imagesize, imageurl = self.get_img()
        imagename = str(imageurl).split('/')[-1].split('.')[0]
        coordinateList = self.get_loc(imagesize)             #获取题目框坐标列表
        count = self.question_count()               #获取题目数目
        while i <= count:
            if i == 1:
                self.driver.tap([coordinateList[0]])    # 根据接口返回坐标点击框选
            elif i > 1:
                class_text = '//android.widget.TextView[@text="%s"]' % str(i)
                print(class_text)
                sign = self.driver.find_element_by_xpath(class_text)
                sign.click()
            sleep(2)
            scroll_view = self.driver.find_element_by_id("com.zybang.kousuan:id/scroll_view")
            query = self.driver.find_elements_by_id("com.zybang.kousuan:id/query_img")
            if len(query) is 0: self.scoll_to_top(scroll_view.location, scroll_view.size)
            self.result_scroll(scroll_view.location, scroll_view.size, scroll_view, imagename, i)
            print("第%s题的答案详情页========" % i)
            i = i+1
            sleep(2)

    def question_count(self):
        count = len(open(r"../util/coordinate.txt",'rU').readlines())
        return count

    def scoll_to_top(self, location, size):
        while 1:
            e = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "com.zybang.kousuan:id/query_img",)))
            if not e:
                start_higth = location["y"]  #元素的初始高度
                sc_hight = size['height']
                #self.driver.swipe(1, start_higth - 0.1, 1, start_higth + sc_hight - 0.1, 100)  # 每次向上滑动(sc_hight)px
                TouchAction(self.driver).press(x=1, y=(start_higth + 0.1)).wait(1000).move_to(x=1,y=start_higth + sc_hight - 0.1).release().perform()
            elif e:
                print('query is appear')
                break

    #SetUP，case运行前的环境初始化
    def setUp(self):
        #字典变量，初始化配置，提供建立session的所有必要信息：http://appium.io/docs/en/writing-running-appium/caps/index.html
        desired_caps = {}
        #被测应用平台：iOS/Android
        desired_caps['platformName'] = 'Android'
        #被测应用平台版本：adb shell getprop ro.build.version.release
        desired_caps['platformVersion'] = '9'
        #测试设备名：adb devices
        #desired_caps['deviceName'] = self.deviceName
        #desired_caps['deviceName'] = 'PD2717C'
        desired_caps['deviceName'] = 'PD12D1C'
        #被测应用包名
        desired_caps['appPackage'] = 'com.zybang.kousuan'
        #被测应用启动时的活动名
        desired_caps['appActivity'] = '.activity.InitActivity'
        #服务端等待客户端发送消息的超时时间
        desired_caps['newCommandTimeout'] = 150
        #在一个session开始前不重置被测程序的状态
        desired_caps['noReset'] = True
        #是否支持uicode的键盘（输入中文需设置）
        desired_caps['unicodeKeyboard'] = True
        desired_caps['Accept-Language']: 'zh-CN,zh;q=0.9'
        #desired_caps['automationName'] = 'uiautomator2'
        #以desired_caps作为参数初始化WebDriver连接,Appium服务器的IP：http://localhost 端口号：4723
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        sleep(3)
        self.wait = WebDriverWait(self.driver, 120)
        self.allways_allow()

    #TearDown，case运行后的环境恢复
    def tearDown(self):
        #退出driver，关闭被测应用所有的关联窗口
        self.driver.quit()

    #TestCase，测试用例1
    #def test_case_1(self):
        #pass

    # def start_mitmproxy(self):
    #     self.obj.stdin.write("mitmweb -s mitmproxyscript.py -p 8082")

    def get_response(self):
        obj = self.obj
        out, err = obj.communicate()
         #for line in out.splitlines():
        #     linestr = line.decode("gbk", "ignore")
        print(out)
        #out = out.decode("gbk", "ignore")
        pigai_re_compile = re.compile(r"/kssearch/submit/oralevaluatesearch")
        pigai_data = pigai_re_compile.findall(out)[-1]
        print(pigai_data)
    def get_testimage(self):
        images = []
        image_path = os.path.dirname(os.path.abspath(".")) + '\\image\\'
        for root, dirs, files in os.walk(image_path, topdown=False):
            for name in files:
                images.append(os.path.join(root, name))
        return images

    def test_plus(self):
        #self.setUp()
        #预期结果等于10
        #result = "10"
        #底部权限弹窗的允许按钮
        #bottom_alert_pass = self.driver.find_element_by_id("android:id/button1")
        self.allways_allow()
        #首页拍照按钮
        #button = self.wait.until(EC.presence_of_element_located((By.ID, idstr)))
        photo_correct = self.driver.find_element_by_id("com.zybang.kousuan:id/photo_correct")
        photo_correct.click()
        sleep(1)
        self.allways_allow()

        #示例关闭按钮
        camera_close_present = self.isElementPresent('id', "com.zybang.kousuan:id/demo_close")
        if camera_close_present:
            camera_close = self.driver.find_element_by_id("com.zybang.kousuan:id/demo_close")
            camera_close.click()
            sleep(2)
        # 相机页拍照按钮
        # camera_take_photo = self.driver.find_element_by_id("com.zybang.kousuan:id/camera_take_photo")
        # camera_take_photo.click()

        #拍照批改搜题
        # testimagelist = self.get_testimage()
        # for testimage in testimagelist:
        #     with open('../util/testimage.txt', 'w') as f:
        #         f.truncate()
        #         f.write(str(testimage) + '\n')
        #     f.close()
        #
        #     #相机页相册按钮
        #     camera_gallery = self.driver.find_element_by_id("com.zybang.kousuan:id/camera_gallery")
        #     camera_gallery.click()
        #     sleep(1)
        #     #相册图片
        #     media_thumbnail = self.driver.find_element_by_id("com.zybang.kousuan:id/media_thumbnail")
        #     media_thumbnail.click()
        #     sleep(6)
        #     self.answer_results()                   # 截图答案详情页

        #相机页相册按钮
        camera_gallery = self.driver.find_element_by_id("com.zybang.kousuan:id/camera_gallery")
        camera_gallery.click()
        sleep(2)

        #相册图片
        media_thumbnail = self.driver.find_element_by_id("com.zybang.kousuan:id/media_thumbnail")
        media_thumbnail.click()
        sleep(6)

        #答案详情页截图
        i = 1
        imagesize, imageurl = self.get_img()
        imagename = str(imageurl).split('/')[-1].split('.')[0]
        coordinateList = self.get_loc(imagesize)  # 获取题目框坐标列表
        count = self.question_count()  # 获取题目数目
        while i <= count:
            if i == 1:
                self.driver.tap([coordinateList[0]])  # 根据接口返回坐标点击框选
            elif i > 1:
                class_text = '//android.widget.TextView[@text="%s"]' % str(i)
                print(class_text)
                sign = self.driver.find_element_by_xpath(class_text)
                sign.click()
            sleep(2)
            scroll_view = self.driver.find_element_by_id("com.zybang.kousuan:id/scroll_view")
            query = self.driver.find_elements_by_id("com.zybang.kousuan:id/query_img")
            if len(query) is 0: self.scoll_to_top(scroll_view.location, scroll_view.size)
            self.result_scroll(scroll_view.location, scroll_view.size, scroll_view, imagename, i)
            print("第%s题的答案详情页========" % i)
            i = i + 1
            sleep(2)


        #断言结果是否相等
        #self.assertEqual(real_result.text, result)



#程序入口
if __name__ == '__main__':
    #TestSuite，将所有测试用例载入suite
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculatorTest)
    #TestRunner，运行测试用例
    # unittest.TextTestRunner(verbosity=2).run(suite)

    #运行case+输出报告
    runner = HtmlTestRunner.HTMLTestRunner(output='cc_report')
    runner.run(suite)