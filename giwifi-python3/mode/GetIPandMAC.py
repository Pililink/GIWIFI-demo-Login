import psutil
'''
获取连接giwifi网卡的ip和mac地址
'''


def GetLocalIPandMAC(prefix):
    r"""
    多网卡情况下，根据前缀获取IP,和MAC
    测试可用：Windows、Linux，Python 3.6.x，psutil 5.4.x
    ipv4/ipv6 地址均适用
    注意如果有多个相同前缀的 ip，只随机返回一个
    """

    localIP = '' #保存匹配到的ip
    loaclMAC = '' #保存匹配到的mac

    dic = psutil.net_if_addrs() #获得所有网卡信息

    #两次循环进行遍历，获得网卡的名字，然后再遍历每一个网卡的信息进行匹配
    for adapter in dic:#获得字符串形式的网卡名
        snicList = dic[adapter]#获得当前网卡的所有信息
        for snic in snicList:#遍历当前网卡的每个信息
            if not snic.family.name.startswith('AF_INET'):#判断当前网卡是否有 ipv4 的信息
                continue #没有ipv4 信息就进行跳过

            ip = snic.address# 获取当前网卡的当前条目中的

            if ip.startswith(prefix):
                localIP = ip.strip()
                mac = snicList[1].address
                loaclMAC = mac.strip()


    return localIP , loaclMAC
