import urllib.request, urllib.error, urllib.parse
import json

def fetch_zhimaip(num=3,time=3):
    # 添加ip白名单
    urllib.request.urlopen(
        'http://web.http.cnapi.cc/index/index/save_white?neek=5454&appkey=yourappkey&white=' +
        json.load(urllib.request.urlopen('http://httpbin.org/ip'))['origin'])
    proxies = {}
    request = urllib.request.Request('http://webapi.http.zhimacangku.com/getip/time/'+str(time)+'/num/'+str(num)+'/type/2/pro/0/city/0/yys/100026/port/1/ts/1/ys/0/cs/0/lb/1/sb/0/pb/45/mr/2/regions/110000,130000,410000')
    # request = urllib.request.Request('http://webapi.http.zhimacangku.com/getip?num='+str(num)+'&type=2&pro=&city=0&yys=100026&port=1&pack=29034&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
    html = urllib.request.urlopen(request)

    json_body = json.loads(html.read())
    for a in json_body['data']:
        proxy = "http://%s:%s" % (a['ip'], a['port'])
        # dirt的默认值都设为1而不是0，方便以后用if语句判断是否存在，不然None和0会混淆
        proxies[proxy]= 1
    return proxies

def get_proxies(num=3,time=3):
    proxies = {}

    proxies.update(fetch_zhimaip(num,time))
    # 可以从更多ip源添加
    # proxies.update(fetch_xx())

    return proxies

# print(get_proxies())