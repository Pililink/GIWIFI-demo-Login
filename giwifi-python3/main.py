from mode.Giwifi import GiWiFi
from mode.GetIPandMAC import GetLocalIPandMAC
import time


#1、检查登录状态（get_auth_state）
#获取ip地址
loaclip,localmac = GetLocalIPandMAC('172.17')#匹配得到连接giwifi网卡的ip和地址
print(loaclip)
print(localmac)
#发送请求，得到wifi信息
giwifi=GiWiFi(phone=账号,password="密码",ip=loaclip,mac=localmac)#初始化
state = giwifi.Status()#查看登录状态


#2、账号验证（authldentity）
#发送请求获取challege_id
authidentity = giwifi.authIdentity()

#3、获取登录地址进行登录（authChallege）
authchallege = giwifi.authChallege()

#4、登录
login = giwifi.Login()

state = giwifi.Status()#查看登录状态

