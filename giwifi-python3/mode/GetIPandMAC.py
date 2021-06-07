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
        '''例子
        {'lo0': [snicaddr(family=<AddressFamily.AF_INET: 2>, address='127.0.0.1', netmask='255.0.0.0', broadcast=None, ptp=None),
  snicaddr(family=<AddressFamily.AF_INET6: 30>, address='::1', netmask='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', broadcast=None, ptp=None),
  snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::1%lo0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)],
 'en1': [snicaddr(family=<AddressFamily.AF_INET: 2>, address='172.17.55.228', netmask='255.255.0.0', broadcast='172.17.255.255', ptp=None),
  snicaddr(family=<AddressFamily.AF_LINK: 18>, address='ec:35:86:2b:91:44', netmask=None, broadcast=None, ptp=None),
  snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::1cdd:1f67:d66b:a4e5%en1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)],
 'vnic0': [snicaddr(family=<AddressFamily.AF_INET: 2>, address='10.10.10.2', netmask='255.255.255.0', broadcast='10.10.10.255', ptp=None),
  snicaddr(family=<AddressFamily.AF_LINK: 18>, address='00:1c:42:00:00:08', netmask=None, broadcast=None, ptp=None)],
 'vnic1': [snicaddr(family=<AddressFamily.AF_INET: 2>, address='10.20.20.2', netmask='255.255.255.0', broadcast='10.20.20.255', ptp=None),
  snicaddr(family=<AddressFamily.AF_LINK: 18>, address='00:1c:42:00:00:09', netmask=None, broadcast=None, ptp=None)],
 'en0': [snicaddr(family=<AddressFamily.AF_LINK: 18>, address='2c:4d:54:c8:fb:04', netmask=None, broadcast=None, ptp=None)],
 'p2p0': [snicaddr(family=<AddressFamily.AF_LINK: 18>, address='0e:35:86:2b:91:44', netmask=None, broadcast=None, ptp=None)],
 'awdl0': [snicaddr(family=<AddressFamily.AF_LINK: 18>, address='2e:53:fe:02:c5:18', netmask=None, broadcast=None, ptp=None),
  snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::2c53:feff:fe02:c518%awdl0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)],
 'llw0': [snicaddr(family=<AddressFamily.AF_LINK: 18>, address='2e:53:fe:02:c5:18', netmask=None, broadcast=None, ptp=None),
  snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::2c53:feff:fe02:c518%llw0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)],
 'utun0': [snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::22f4:322:f7b9:9949%utun0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)],
 'utun1': [snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::3076:39e:278c:a139%utun1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)]}
        '''
        snicList = dic[adapter]#获得当前网卡的所有信息
        for snic in snicList:#遍历当前网卡的每个信息
            '''例子：
            [snicaddr(family=<AddressFamily.AF_INET: 2>, address='172.17.55.228', netmask='255.255.0.0', broadcast='172.17.255.255', ptp=None),
 snicaddr(family=<AddressFamily.AF_LINK: 18>, address='ec:35:86:2b:91:44', netmask=None, broadcast=None, ptp=None),
 snicaddr(family=<AddressFamily.AF_INET6: 30>, address='fe80::1cdd:1f67:d66b:a4e5%en1', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)]
            '''
            if not snic.family.name.startswith('AF_INET'):#判断当前网卡是否有 ipv4 的信息
                continue #没有ipv4 信息就进行跳过

            ip = snic.address# 获取当前网卡的当前条目中的

            if ip.startswith(prefix):
                localIP = ip.strip()
                mac = snicList[1].address
                loaclMAC = mac.strip()


    return localIP , loaclMAC
