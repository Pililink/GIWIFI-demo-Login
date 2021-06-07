#giwifi登录模块
'''
编写思路：
通过定义类方法实现giwifi登录/退出的操作，
每个类方法中解析得到的json文件，并添加到类属性。方便其他类方法使用。


'''

import requests
from urllib.parse import quote
from mode.Challge import Challge#密码加密
import json



class GiWiFi(object):
    def __init__(self,phone,password,ip,mac,version = "1.1.4.1"):
        self.ip = ip.strip()# ip 地址
        self.mac = mac.strip()#mac 地址
        self.version = version.strip()
        self.challege = ""#加密后的密码
        self.password = password#密码
        self.phone = phone#手机号
        self.gw_id = ""
        self.access_type = ""
        self.gw_address = "172.17.1.2"
        self.sta_model = "mac10.15"
        self.sta_type = "pc"


        self.PHPSESSID=''#cookie
        self.HEADERS = {#头信息
            'Accept': '*/*',
            'User-Agent': 'GiWiFi/1.1.4.1 (Mac OS X Version 10.15.7 (Build 19H15))',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        self.Loginlink = ''#获取到的登录地址


    #检测登录状态
    def Status(self):
        #请求地址
        url = 'http://172.17.1.2:8060/wifidog/get_auth_state'
        #get方式url后面的数据
        url_data = {
            "ip":str(self.ip),
            "mac":str(self.mac)
        }

        #调用get请求
        ret = self.GET(url=url,url_data=url_data,headers=self.HEADERS)
        #转json
        tojson = self.toJson(ret)
        if tojson['data']['auth_state'] == 2:
            print('已登录')
            #print('auth_state：', tojson['auth_state'])
        #添加类属性
        self.auth_state = tojson['data']['auth_state']
        self.gw_id = tojson['data']['gw_id']
        self.access_type = tojson['data']['access_type']
        self.authStaType = tojson['data']['authStaType']
        self.station_sn = tojson['data']['station_sn']
        self.client_mac = tojson['data']['client_mac']
        self.online_time = tojson['data']['online_time']

        '''例子
        {'resultCode': 0,
         'data': 
             {
             'auth_state': 2,
             'gw_id': 'GWIFI-zhongbeixinshang02',
             'access_type': '1',
              'authStaType': '2',
             'station_sn': '000babf63722',
             'client_mac': 'ec:35:86:2b:91:44',
             'online_time': 28219,
             'logout_reason': 7,
             'contact_phone': '400-038-5858',
             'suggest_phone': '400-038-5858',
             'station_cloud': 'login.gwifi.com.cn',
             'orgId': '872'
            }
         }
         '''
        return tojson


    #1、身份认证，获取cookie信息
    def authIdentity(self):

        data={
            'name':str(self.phone),
            'version':str(self.version)
        }
        #url地址
        url='http://login.gwifi.com.cn/cmps/admin.php/ppi/authIdentity'

        #调用自定义的get方法
        ret = self.GET(url=url,url_data=data,headers=self.HEADERS)
        cookies = requests.utils.dict_from_cookiejar(ret.cookies)
        self.PHPSESSID = 'PHPSESSID=' + cookies['PHPSESSID']#将cookie信息保存到类属性中
        tojson = self.toJson(ret)

        #添加类属性
        self.challege_id = tojson['data']['challege_id']

        '''例子
         {'resultCode': 0, 'resultMsg': '', 'data': {'challege_id': 'c4ef032c95d8e9dbdab6e3b99886e984'}}
        '''
        return tojson

    #2、获取登录地址，通过post
    def authChallege(self):
        challege = Challge()
        self.challege = challege.get(self.password,self.challege_id)
        print(self.mac)
        data = 'ap_mac=&' \
               'challege='+str(self.challege)+'&' \
               'gw_address=+'+str(self.gw_address)+'&' \
               'gw_id='+str(self.gw_id)+'&' \
               'ip='+str(self.ip)+'&' \
               'mac='+str(self.mac)+'&' \
               'name='+str(self.phone)+'&' \
               'service_type=1&' \
               'sta_model='+str(self.sta_model)+'&' \
               'sta_nic_type=1&' \
               'sta_type='+str(self.sta_type)+ '&' \
               'version='+str(self.version)
        headers = dict.copy(self.HEADERS)#通过copy 复制一个独立的headers信息，避免修改原本的信息
        headers['Content-Length'] = str(len(data))
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Cookie'] = self.PHPSESSID
        #print(headers)
        url = 'http://login.gwifi.com.cn/cmps/admin.php/ppi/authChallege'
        ret = self.POST(url=url,data=data,heards=headers)
        tojson = self.toJson(ret)
        self.Loginlink = tojson['data']['redirect_url'].replace(" ","")#将得到登录地址保存
        print(self.Loginlink)
        return tojson

    #登录
    def Login(self):
        print(self.Loginlink)
        ret = requests.request("GET", self.Loginlink, headers=self.HEADERS)
        tojson = self.toJson(ret)
        return tojson


    #退出登录
    def OutLogin(self, reason = '1'):
        url = 'http://172.17.1.2:8060/wifidog/userlogout'
        #get方式url后面的数据
        url_data = {
            "ip":self.ip,
            "mac":self.mac,
            "reason":reason
        }
        ret = self.GET(url=url,url_data=url_data,headers=self.HEADERS)
        tojson = self.toJson(ret)

        #调用get方法，并返回执行结果
        return tojson


    #get方式url拼接
    def get_urljoin(self,url,dict,encode = True):
        data = ""#保存拼接的地址信息
        l = len(dict)#读取字段内容的长度
        if encode == True:#如果进行url编码执行这个
            for key,value in dict.items():
                l = l - 1#通过判断字段长度的方式，实现最后一个键值对不加 &
                data += key+"="+quote(str(value))
                if l >=0:
                    data += "&"
        elif encode == False:#不进行url转码 执行这个
            for key,value in dict.items():
                l = l - 1
                data += key+"="+str(value)
                if l >=0:
                    data += "&"
        return url+"?"+data

    #自定义get请求
    def GET(self,url,url_data=None,headers = {},encode = True):
        #判断是否需要URL拼接
        if url_data != None :
            # 组成完整的URL地址
            url = self.get_urljoin(url=url,dict=url_data,encode=encode)

        # 发生请求
        response = requests.request("GET", url, headers=headers)
        print("GET > ",response.text)
        return response

    #将HttpResponse中的内容转换成json
    def toJson(self,HttpResponse):
        # 解析返回的json信息
        ret = json.loads(HttpResponse.text.encode('utf8'))

        #判断data数据是否存在

        if ret["data"] =='' or 'data' not in ret:
            return ret
        ret_data = json.loads(ret['data'])
        ret['data'] = ret_data
        print("tojson > ", ret)
        return ret

    #自定义POST 请求
    def POST(self,url,heards,data):
        ret = requests.post(url=url,data=data,headers=heards)
        return ret





