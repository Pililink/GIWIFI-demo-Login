package main
//加密测试
import "fmt"

/*

string GetChallge(string MakePass, string TokenChallge)
{
    string res = "";
    for (size_t i = 0; i < MakePass.length(); i++)
    {
        res += MakePass[i];
        res += TokenChallge[31 - i];
    }
    return res;
}
*/
func main() {
	challge := GetChallge(calPass("密码"), "12sax1a1x5sa1da2w864t8hf1h5tf2bf1")
	fmt.Print(challge)
}

func GetChallge(MakePass string, TokenChallge string) string {
	res := ""
	i := 0
	for i = 0; i < len(MakePass); i++ {

		res += string(MakePass[i])
		res += string(TokenChallge[31-i])
	}
	return res
}

func calPass(pwd string) string {
	res := ""
	var temps uint32 = 0
	i := 1
	lens := len(pwd)
	for i < lens+1 {

		temps = temps ^ uint32(pwd[i-1])
		//fmt.Print(temps)
		//fmt.Print("\n")
		if i%3 == 0 {
			res += MakeTempPass(temps)
		}
		temps = temps << 8
		i += 1
	}

	return res
}

func MakeTempPass(temppwd uint32) string {
	res := ""
	charlist := "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456"
	var temp uint32 = 0
	var i int
	for i = 0; i < 4; i++ {
		temp = (temppwd >> ((3 - i) * 6)) & 0x3F
		res += string(charlist[temp])
	}
	return res
}
