package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	//初始化账户信息
	var userInfo UserInfo

	userInfo.Version = "1.1.4.2"
	userInfo.Sta_type = "pc"
	userInfo.Sta_nic_type = 1
	userInfo.Sta_model = "mac10.15"
	userInfo.Service_type = 1
	userInfo.Name = "账号"//账号
	userInfo.Mac = "" //下面自动获取
	userInfo.Ip = "172.17.55.228" //本机ip
	userInfo.Gw_id = "xx:xx:xx:xx:xx:xx"//giwifi mac地址
	userInfo.Gw_address = "172.17.1.2"//giwifi ip地址
	userInfo.Challege = "" //下面自动计算得出
	userInfo.Ap_mac = ""
	userInfo.Cookie = ""
	userInfo.Loginlink = ""

	//检测登录状态
	var authstate Authstate
	var authstatedata AuthstateData
	get_auth_state(&authstate, &authstatedata, &userInfo)
	//fmt.Println(authstate)
	//记录本机mac地址
	userInfo.Mac = authstatedata.Client_mac
	userInfo.Gw_id = authstatedata.Gw_id

	fmt.Println("本机的mac地址为：", userInfo.Mac)

	//判断登录状态
	auth_state := authstatedata.Auth_state
	if auth_state == 1 {
		fmt.Println("您已未登录")
	} else if auth_state == 2 {
		fmt.Println("您已登录")
		//return
	}

	//身份认证，获取challege_id和cookie
	var authIdentityJson AuthIdentityJson
	var authIdentityDataJson AuthIdentityDataJson
	authIdentity(&authIdentityJson, &authIdentityDataJson, &userInfo)
	if authIdentityDataJson.Challege_id == "" { //没有登录地址不往下执行
		return
	}

	//计算加密后的密码
	userInfo.Challege = GetChallge(calPass("密码"), authIdentityDataJson.Challege_id)
	fmt.Printf(userInfo.Challege)

	//获取登录地址
	var authChallegeJson AuthChallegeJson
	var authChallegeDataJson AuthChallegeDataJson
	authChallege(&authChallegeJson, &authChallegeDataJson, &userInfo)
	fmt.Printf(authChallegeDataJson.Redirect_url)

	if userInfo.Loginlink == "" {
		return
	}

	//提交登录
	var authJson AuthJson
	var authDataJson AuthDataJson
	Auth(&authJson, &authDataJson, &userInfo)

	get_auth_state(&authstate, &authstatedata, &userInfo)
	//判断登录状态
	auth_state = authstatedata.Auth_state
	if auth_state == 1 {
		fmt.Println("您已未登录")
	} else if auth_state == 2 {
		fmt.Println("您已登录")
		//return
	}
}

//用户信息结构
type UserInfo struct {
	Ip           string
	Mac          string
	Cookie       string
	Version      string
	Sta_type     string
	Sta_nic_type int
	Sta_model    string
	Service_type int
	Name         string
	Gw_id        string
	Gw_address   string
	Challege     string
	Ap_mac       string
	Loginlink    string
}

//账户登录状态返回值json结构
type Authstate struct {
	ResultCode uint8  `json:"resultCode"`
	Data       string `json:"data"`
}

//账户登录状态返回值中data的json结构
type AuthstateData struct {
	Auth_state    uint   `json:"auth_state"`
	Gw_id         string `json:"gw_id"`
	Access_type   string `json:"access_type"`
	AuthStaType   string `json:"authStaType"`
	Station_sn    string `json:"station_sn"`
	Client_mac    string `json:"client_mac"`
	Online_time   uint32 `json:"online_time"`
	Logout_reason uint   `json:"logout_reason"`
	Contact_phone string `json:"contact_phone"`
	Suggest_phone string `json:"suggest_phone"`
	Station_cloud string `json:"station_cloud"`
	OrgId         string `json:"orgId"`
}

//检测登录状态
func get_auth_state(authstate *Authstate, authstatedata *AuthstateData, userInfo *UserInfo) {
	url := "http://172.17.1.2:8060/wifidog/get_auth_state"
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println(err)
	}
	//添加请求参数
	q := req.URL.Query()
	q.Add("ip", userInfo.Ip)
	q.Add("mac", userInfo.Mac)
	req.URL.RawQuery = q.Encode()
	fmt.Println(req.URL.String())
	// 设置Header
	req.Header.Set("User-Agent", "GiWiFi/1.1.4.1 (Mac OS X Version 10.15.7 (Build 19H15))")
	req.Header.Set("Accept", "*/*")
	req.Header.Set("Accept-Language", "zh-Hans-CN;q=1, en-CN;q=0.9")
	req.Header.Set("Accept-Encoding", "gzip, deflate")
	req.Header.Set("Connection", "keep-alive")
	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)

	// 只定义需要获取的那部分消息体的结构
	//fmt.Println(string(body))

	json.Unmarshal([]byte(body), &authstate)
	json.Unmarshal([]byte(authstate.Data), &authstatedata)

}

//身份认证 json结构
type AuthIdentityJson struct {
	ResultCode uint8  `json:"resultCode"`
	ResultMsg  string `json:"resultMsg"`
	Data       string `json:"data"`
}

//身份认证 json中data的结构
type AuthIdentityDataJson struct {
	Challege_id string `json:"challege_id"`
}

//检测登录状态
func authIdentity(authidentityjson *AuthIdentityJson, authidentitydata *AuthIdentityDataJson, userInfo *UserInfo) {
	url := "http://login.gwifi.com.cn/cmps/admin.php/ppi/authIdentity"
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println(err)
	}
	//添加请求参数
	q := req.URL.Query()
	q.Add("name", userInfo.Name)
	q.Add("version", userInfo.Version)
	req.URL.RawQuery = q.Encode()
	fmt.Println(req.URL.String())
	// 设置Header
	req.Header.Set("User-Agent", "GiWiFi/1.1.4.1 (Mac OS X Version 10.15.7 (Build 19H15))")
	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	cookie := resp.Header["Set-Cookie"]
	userInfo.Cookie = cookie[0]
	//fmt.Println(cookie)
	// 只定义需要获取的那部分消息体的结构
	//fmt.Println(string(body))

	json.Unmarshal([]byte(body), &authidentityjson)
	json.Unmarshal([]byte(authidentityjson.Data), &authidentitydata)

}

//获取登录地址 json结构
type AuthChallegeJson struct {
	ResultCode int    `json:"resultCode"`
	ResultMsg  string `json:"resultMsg"`
	Data       string `json:"data"`
}

//获取登录地址 json中data的结构
type AuthChallegeDataJson struct {
	Redirect_url string `json:"redirect_url"`
}

func authChallege(authChallegeJson *AuthChallegeJson, authChallegeDataJson *AuthChallegeDataJson, userInfo *UserInfo) {
	url := "http://login.gwifi.com.cn/cmps/admin.php/ppi/authChallege"
	req, err := http.NewRequest("POST", url, nil)
	if err != nil {
		fmt.Println(err)
	}
	//添加请求参数
	q := req.URL.Query()

	q.Add("version", string(userInfo.Version))
	q.Add("sta_type", string(userInfo.Sta_type))
	q.Add("sta_nic_type", string(userInfo.Sta_nic_type))
	q.Add("sta_model", string(userInfo.Sta_model))
	q.Add("service_type", string(userInfo.Service_type))
	q.Add("name", string(userInfo.Name))
	q.Add("mac", string(userInfo.Mac))
	q.Add("ip", string(userInfo.Ip))
	q.Add("gw_id", string(userInfo.Gw_id))
	q.Add("gw_address", string(userInfo.Gw_address))
	q.Add("challege", string(userInfo.Challege))
	q.Add("ap_mac", string(userInfo.Ap_mac))
	req.URL.RawQuery = q.Encode()
	fmt.Println("")
	fmt.Println(req.URL.String())
	// 设置Header
	req.Header.Set("User-Agent", "GiWiFi/1.1.4.1 (Mac OS X Version 10.15.7 (Build 19H15))")
	req.Header.Set("Accept", "*/*")
	req.Header.Set("Accept-Language", "zh-Hans-CN;q=1, en-CN;q=0.9")
	//req.Header.Set("Accept-Encoding", "gzip, deflate")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("Cookies", userInfo.Cookie)
	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)

	// 只定义需要获取的那部分消息体的结构
	//fmt.Println(string(body))

	json.Unmarshal([]byte(body), &authChallegeJson)
	json.Unmarshal([]byte(authChallegeJson.Data), &authChallegeDataJson)
	userInfo.Loginlink = authChallegeDataJson.Redirect_url

}

//登录操作 json结构
type AuthJson struct {
	ResultCode int    `json:"resultCode"`
	ResultMsg  string `json:"resultMsg"`
	Data       string `json:"data"`
}

//登录操作 json中data的结构
type AuthDataJson struct {
	WillStop     int    `json:"willStop"`
	UserType     int    `json:"userType"`
	UserToken    string `json:"userToken"`
	LimitTime    int    `json:"limitTime"`
	Mode         int    `json:"mode"`
	Showtext     string `json:"showtext"`
	Redirect_url string `json:"redirect_url"`
}

//访问登录地址
func Auth(authJson *AuthJson, authDataJson *AuthDataJson, userInfo *UserInfo) {
	url := userInfo.Loginlink
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println(err)
	}
	// 设置Header
	req.Header.Set("User-Agent", "GiWiFi/1.1.4.1 (Mac OS X Version 10.15.7 (Build 19H15))")
	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	cookie := resp.Header["Set-Cookie"]
	userInfo.Cookie = cookie[0]
	//fmt.Println(cookie)
	// 只定义需要获取的那部分消息体的结构
	//fmt.Println(string(body))

	json.Unmarshal([]byte(body), &authJson)
	json.Unmarshal([]byte(authJson.Data), &authDataJson)

}

//加密程序
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
