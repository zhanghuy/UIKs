# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

caps = {}
caps["platformName"] = "Android"
caps["deviceName"] = "PD2717C"
caps["appPackage"] = "com.zybang.kousuan"
caps["appActivity"] = ".activity.InitActivity"

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

TouchAction(driver).tap(x=792, y=1923).perform()
TouchAction(driver).tap(x=792, y=1916).perform()
TouchAction(driver).tap(x=536, y=792).perform()
TouchAction(driver).tap(x=795, y=1920).perform()
TouchAction(driver).tap(x=540, y=1883).perform()
TouchAction(driver).tap(x=536, y=1879).perform()
TouchAction(driver).tap(x=999, y=1868).perform()
TouchAction(driver).tap(x=100, y=614).perform()
TouchAction(driver).tap(x=544, y=1879).perform()
TouchAction(driver).tap(x=751, y=1076).perform()
TouchAction(driver).tap(x=288, y=1091).perform()
TouchAction(driver).tap(x=939, y=1650).perform()
TouchAction(driver).press(x=1036, y=1675).move_to(x=41, y=1687).release().perform()

TouchAction(driver).tap(x=510, y=847).perform()
TouchAction(driver).tap(x=640, y=1938).perform()
TouchAction(driver).tap(x=995, y=1864).perform()
TouchAction(driver).tap(x=939, y=329).perform()
TouchAction(driver).tap(x=499, y=1221).perform()
TouchAction(driver).tap(x=577, y=1982).perform()
TouchAction(driver).press(x=348, y=2001).move_to(x=337, y=1302).release().perform()

TouchAction(driver).press(x=385, y=1920).move_to(x=381, y=1298).release().perform()

driver.quit()