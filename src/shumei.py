# coding: utf8
"""
---------------------------------------------
    File Name: shumei
    Description: 
    Author: wangdawei
    date:   2018/4/8
---------------------------------------------
    Change Activity: 
                    2018/4/8
---------------------------------------------    
"""


import logging
import time
import random
import re
import requests
import urllib.parse as urlparse
import sys

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from io import BytesIO

"""
程序目的：
访问国家企业信用信息公示系统（http://www.gsxt.gov.cn/index.html），
输入查询关键字，
破解弹出的极验验证码系统（geetest）并搜索，最后获取搜索结果。
"""

VERSION = "1.0"
CONFIG = {
    'log_format': "%(asctime)s pid[%(process)d] %(levelname)7s %(name)s.%(funcName)s - %(message)s",
    'save_temp_file': False, }

import utils
import random as r
import jieba
import imageUtils

class Shumei(object):
    """"""

    def __init__(self, driver):
        """构造函数"""
        super(Shumei, self).__init__()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Init Shumei instance")

        self.browser = None
        self.__setup_browser(driver)
        pass

    def __del__(self):
        """析构函数"""
        self.logger.debug("Del Gsxt instance")

        # if self.browser is not None:
        #     self.browser.quit()
        pass

    def __setup_browser(self, driver):
        """装载浏览器驱动"""
        self.logger.debug("Setup selenium webdriver")

        driver = driver.lower()
        if "phantomjs" == driver:
            self.browser = webdriver.PhantomJS()
        elif "chrome" == driver:
            options = ChromeOptions()
            # options.add_argument("user-data-dir=C:/Users/wangdawei/AppData/Local/Google/Chrome/User Data")
            # options.add_argument('--disable-java')
            # options.add_argument('--disable-logging')
            # options.add_argument('--incognito')
            # options.add_argument('--use-mock-keychain')
            options.add_argument("disable-infobars?")
            # self.browser = webdriver.Chrome(chrome_options=options)
            self.browser = webdriver.Chrome("E:\github\crawler\src\chromedriver.exe", chrome_options=options)

        elif "firefox" == driver:
            self.browser = webdriver.Firefox()
            # raise Exception("请不要使用firefox，因为geckodriver暂时有点功能不全！凸(-｡-;")
        else:
            raise Exception("不识别的浏览器驱动")

        # 设置打开页面超时时间(但这对firefox的geckodriver 0.13.0版本无效，不知道后续改进没有)
        self.browser.set_page_load_timeout(8)

        # 设置查询dom的隐式等待时间（影响find_element_xxx,find_elements_xxx）
        self.browser.implicitly_wait(10)

    def login(self):
        """
        Args:
            keyword: 要搜索的关键字
        Returns:
        """

        self.logger.debug(u"准备搜索")

        # 打开搜索页面
        self.browser.get("https://passport.hupu.com/login")
        time.sleep(1)

        # <input autocomplete="off" type="text" name="username" placeholder="登录名/手机号/邮箱" data-rule="empty" data-name="帐号" id="J_username" tabindex="1">
        self.browser.find_element_by_id("J_username").clear()
        # <input autocomplete="off" type="password" name="password" placeholder="密码" data-rule="empty" data-name="密码" id="J_pwd" tabindex="2">
        self.browser.find_element_by_id("J_pwd").clear()

        account = []
        try:
            fileaccount = open("../data/hupu_account.txt")
            accounts = fileaccount.readlines()
            for acc in accounts:
                account.append(acc.strip())
            fileaccount.close()
        except Exception as err:
            print(err)
            input("请正确在account.txt里面写入账号密码")
            exit()
        self.browser.find_element_by_id("J_username").send_keys(account[0])
        self.browser.find_element_by_id("J_pwd").send_keys(account[1])

        # WebDriverWait(self.browser, 30).until(lambda the_driver: the_driver.find_element_by_xpath(
        #     "//div[@class='gt_slider_knob gt_show']").is_displayed())
        # WebDriverWait(self.browser, 30).until(
        #     lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_bg gt_show']").is_displayed())
        # WebDriverWait(self.browser, 30).until(
        #     lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_fullbg gt_show']").is_displayed())

        time.sleep(2.3)

        while True:
        # for i in range(1):
        # self.logger.info("下载第%s次...", i)
        # self.browser.refresh()
            time.sleep(1.3)
            # <input autocomplete="off" type="text" name="username" placeholder="登录名/手机号/邮箱" data-rule="empty" data-name="帐号" id="J_username" tabindex="1">
            # self.browser.find_element_by_id("J_username").clear()
            fg = self.get_image("shumei_captcha_loaded_img_fg")
            bg = self.get_image("shumei_captcha_loaded_img_bg")
            path = "E:\github\crawler\data\shumei"
            fg = utils.download_original_name((fg[0].get_attribute("src"), path))
            bg = utils.download_original_name((bg[0].get_attribute("src"), path))

            center = imageUtils.edge_center(file=bg)
            print (center)
            xoffset = int(center[1][0] / 2 - 15)
            print(xoffset)

            # dom_div_slider = self.browser.find_element_by_class_name("shumei_captcha_slide_btn")
            # ActionChains(self.browser).click_and_hold(on_element=dom_div_slider).perform()
            # ActionChains(self.browser).move_to_element_with_offset(
            #     to_element=dom_div_slider,
            #     xoffset=int(center[1]/2-15),
            #     yoffset=22).perform()
            # time.sleep(0.2)
            # ActionChains(self.browser).release(on_element=dom_div_slider).perform()
            # time.sleep(1)

            # 根据缺口位置计算移动轨迹
            track = self.get_track(xoffset)
            print(track)



            # 移动滑块
            result = self.simulate_drag(track)
            print(result)
            time.sleep(1.1)

        # <input autocomplete="off" type="password" name="password" placeholder="密码" data-rule="empty" data-name="密码" id="J_pwd" tabindex="2">


    def get_image(self, class_name):
        """
        下载并还原极验的验证图
        Args:
            class_name: 验证图所在的html标签的class name
        Returns:
            返回验证图
        Errors:
            IndexError: list index out of range. ajax超时未加载完成，导致image_slices为空
        """
        time.sleep(1.3)
        self.logger.debug(u"获取验证图像: class='%s'", class_name)
        image_slices = self.browser.find_elements_by_class_name(class_name)
        if len(image_slices) == 0:
            self.logger.warn(u"无法找到class='%s'的标签", class_name)
            return

        self.logger.warn(u"找到class='%s'的标签", class_name)
        return image_slices

    def get_track(self, x_offset):
        """
        根据缺口位置x_offset，仿照手动拖动滑块时的移动轨迹。
        手动拖动滑块有几个特点：
            开始时拖动速度快，最后接近目标时会慢下来；
            总时间大概1~3秒；
        但是现在这个简单的模拟轨迹成功率并不高，只能说能用。我并不懂关于机器学习的知识，但我想如果能用上的话应该会好一些
        Args:
            x_offset: 验证图像的缺口位置，亦即滑块的目标地址
        Returns:
            返回一个轨迹数组，数组中的每个轨迹都是[x,y,z]三元素：x代表横向位移，y代表竖向位移，z代表时间间隔
            [[x1,y1,z1], [x2,y2,z2], ...]
        """
        track = list()

        # 实际上滑块的起始位置并不是在图像的最左边，而是大概有6个像素的距离，所以滑动距离要减掉这个长度
        length = x_offset - 7
        total_time = 0

        length_6 = int(length*3./4)
        length_9 = int(length * 1. / 11)
        length_9 = min(7, length_9)
        length_9 = max(4, length_9)
        while length > 0:
            if length>length_6:
                x = random.randint(4, 9)
                track.append([x, 0, random.random() * 0.0001 + 0.0001])
            elif length>length_9:
                x = random.randint(1, 4)
                track.append([x, 0, random.random() * 0.001 + 0.0005])
            else:
                x = 1
                track.append([x, 0, random.randint(10, 22) / 100.0])
            total_time += track[-1][2]
            length -= x

        # x = random.randint(1, 2)
        # while length - x >= 4:
        #     track.append([x, 0, random.random()*0.03])
        #     length = length - x
        #     x = random.randint(1, 2)
        #     total_time += track[-1][2]
        #
        # for i in range(length):
        #     track.append([1, 0, random.randint(20, 50) / 100.0])
        #     total_time += track[-1][2]

        self.logger.debug(u"计算出移动轨迹; %s", track)
        self.logger.debug(u"预计耗时: %s", total_time)
        return track

    def simulate_drag(self, track):
        """
        根据移动轨迹，模拟拖动极验的验证滑块
        Args:
            track: 移动轨迹
        Returns:

        """
        self.logger.warn(u"开始模拟拖动滑块")

        moveX = r.randint(3,8) - 5

        moveY = 1;

        # 获得滑块元素
        dom_div_slider = self.browser.find_elements_by_class_name("shumei_captcha_slide_btn")
        print(len(dom_div_slider))
        dom_div_slider=dom_div_slider[0]
        self.logger.warn(u"滑块初始位置: %s", dom_div_slider.location)
        time.sleep(0.2)
        ActionChains(self.browser).move_to_element(dom_div_slider).perform()
        # ActionChains(self.browser).
        time.sleep(1)
        ActionChains(self.browser).click_and_hold(on_element=dom_div_slider).perform()
        ActionChains(self.browser).move_by_offset(1, 0)
        time.sleep(0.1)

        for x, y, z in track:
            self.logger.warn(u"位移: (%s, %s), 等待%s秒", x, y, z)
            # ActionChains(self.browser).move_to_element_with_offset(
            #     to_element=dom_div_slider,
            #     # xoffset=x + 22,
            #     xoffset=x,
            #     yoffset=1).perform()
            ActionChains(self.browser).move_by_offset(x+22, 0)
            # ActionChains(self.browser).click_and_hold(on_element=dom_div_slider).perform()
            self.logger.warn(u"滑块当前位置: %s", dom_div_slider.location)
            # time.sleep(1)
            time.sleep(z)
            pass

        time.sleep(0.2)
        ActionChains(self.browser).release(on_element=dom_div_slider).perform()

        time.sleep(1)
        # dom_div_gt_info = self.browser.find_element_by_class_name("gt_info_text")
        # self.logger.debug(u"拖动结果【%s】", dom_div_gt_info.text)
        # return dom_div_gt_info.text

shumei = Shumei("chrome")
shumei.login()
