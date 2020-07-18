# python2.7 
#-*- coding: utf-8 -*
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import os
import pywifi
import sys
import json
import base64



def wifi_list():
    wifi = pywifi.PyWiFi()  # 创建实例
    iface = wifi.interfaces()[0]  # 调用网卡
    while True:
          iface.scan()  # 扫描
          time.sleep(2)  # 延迟两秒
          wifi_l = iface.scan_results()  # 所有WiFi数据
          wifi = [(i.ssid, i.signal, i) for i in wifi_l]
          # 根据信号强弱排序，并去除重复名称
          wifi.sort(key=lambda x: x[1], reverse=True)
          lTemp = {}
          for i in wifi:
              if i[0] not in lTemp.keys():
                  lTemp[i[0]] = i[1]
          wifis = list(lTemp.items())
          suda_wifi = []  # 连接wifi：优先连接5G的
          for i in wifis:
              if "SUDA_WIFI_5G" == i[0]:
                  suda_wifi.append(i)
              if "SUDA_WIFI" == i[0]:
                  suda_wifi.append(i)
          suda_wifi.sort(reverse=True)
          if suda_wifi:
              print "正在连接的网络为：{}".format(suda_wifi[0][0])
              wifi_n = suda_wifi[0][0]
              break 	
          else:	
              print '无苏大WiFi！'
              time.sleep(10)
          time.sleep(1)
    
    return wifi_n

def cntwifi(l): 

    profile = pywifi.Profile()  # 创建wifi配置实例
    profile.ssid = l  # 配置名称
    wifi = pywifi.PyWiFi()  # 创建wifi实例
    iface = wifi.interfaces()[0]  # 调用网卡
    profile = iface.add_network_profile(profile)  # 配置wifi信息
    iface.connect(profile)  # 连接wifi




class Login:
    def __init__(self, url, username, password, browser_url):
        self.username = username
        self.password = password
        self.url = url
        self.browser_url = browser_url

    def login(self):
        try:
            #browser = webdriver.Chrome(executable_path=self.browser_url)
            browser = webdriver.Firefox(executable_path=self.browser_url)
            browser.get(self.url)
            browser.find_element_by_id('username').send_keys(self.username)
            browser.find_element_by_id('password').send_keys(self.password)
            browser.find_element_by_id('login').click()
        except:
            print self.getCurrentTime(), "登陆函数异常"
        finally:
            browser.close()
    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #判断当前是否可以连网
    def canConnect(self):
        try:
            baidu_request=requests.get("http://www.baidu.com")
            if(baidu_request.status_code==200):
                baidu_request.encoding = 'utf-8'
                baidu_request_bsObj = BeautifulSoup(baidu_request.text, 'html.parser')
                baidu_input = baidu_request_bsObj.find(value="百度一下")
                if baidu_input==None:
                    return False
                return True
            else:
                return False
        except:
            print 'error'

    #主函数
    def main(self):

        print self.getCurrentTime(), "自动登陆脚本正在运行"
        while True:
            while True:
                can_connect = self.canConnect()
                if not can_connect:
                    print self.getCurrentTime(), "断网了..."
                    # WiFi列表
                    wifi_l = wifi_list()
                    try:
                        # 连接wifi
                        cntwifi(wifi_l)
                        print '正在登陆...'
                        self.login()
                    except:
                        print self.getCurrentTime(), "浏览器出了bug"
                    finally:
                        time.sleep(2)
                        if self.canConnect():
                            print self.getCurrentTime(), "重新登陆成功"
                        else:
                            print self.getCurrentTime(), "登陆失败，再来一次"
                else:
                    print self.getCurrentTime(), "一切正常..."
                    time.sleep(180)
                time.sleep(1)
            time.sleep(self.every)

if __name__ == "__main__":

    wifi_l = wifi_list()

    cntwifi(wifi_l)
    # 学号
    username = '学号'

    # 密码
    password = '密码'

    # 登陆网关
    url = 'http://a.suda.edu.cn/'

    # 使用Chrome
   # browser_url = './chromedriver'

    # 使用Firefox
    browser_url = './geckodriver'

    login = Login(
        username=username,
        password=password,
        url=url,
        browser_url=browser_url,
    )
    login.main()
