import urllib.request, urllib.error, urllib.parse
import json

def fetch_zhimaip(num=3,time=3):
    proxies = {}
    # time 1为5~25分钟，2为25分~3小时，3为3~6小时
    request = urllib.request.Request('http://webapi.http.zhimacangku.com/getip/time/'+str(time)+'/num/'+str(num)+'/type/2/pro/0/city/0/yys/100026/port/1/ts/1/ys/0/cs/0/lb/1/sb/0/pb/45/mr/1/regions/110000,130000,410000')
    # request = urllib.request.Request('http://webapi.http.zhimacangku.com/getip?num='+str(num)+'&type=2&pro=&city=0&yys=100026&port=1&pack=29034&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
    html = urllib.request.urlopen(request)

    json_body = json.loads(html.read())
    for a in json_body['data']:
        proxy = "http://%s:%s" % (a['ip'], a['port'])
        # print(a['expire_time'])
        proxies[proxy]= 0
    return proxies

def get_proxies(num=3):
    proxies = {}

    proxies.update(fetch_zhimaip(num))
    # 可以从更多ip源添加
    # proxies.update(fetch_xx())

    return proxies

# print(get_proxies())