# GIwifi密码加密算法


class Challge:
    #主方法，实例对象直接调用这个函数
    def get(self, password, token):
        return self.GetChallge(self.calPass(password), token)

    def calPass(self, pwd):
        res = ""
        temps = 0
        i = 1
        while i <= len(pwd):
            temps = temps ^ ord(pwd[i - 1])  # 获取字母对应的ascii码
            if (i % 3 == 0):
                res += self.MakeTempPass(temps)
            temps = temps << 8
            i += 1
        return res

    def MakeTempPass(self, temppwd):
        res = ""
        charlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456"
        temp = 0
        for i in range(4):
            temp = (temppwd >> ((3 - i) * 6)) & 0x3F
            res += charlist[temp]
        return res

    def GetChallge(self, MakePass, TokenChallge):
        res = ""
        for i in range(len(MakePass)):
            res += MakePass[i]
            res += TokenChallge[31 - i]
        return res
