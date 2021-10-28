import requests, json, os

# server酱开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
# sever = os.environ["SERVE"]
sever = "on"
# 填写server酱sckey,不开启server酱则不用填
sckey = os.environ["SCKEY"]
# 填入glados账号对应cookie
cookie = os.environ["COOKIE"]
cookie = "koa:sess.sig=uH4NKDLISfEM9KcTXXpMfgyOFI8;koa:sess=eyJ1c2VySWQiOjc1MzM4LCJfZXhwaXJlIjoxNjQyMDAzNTMxMzIxLCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=;__cfduid=deb58b9412593d6c3f36d06d91a1af19d1616083430"


def start():
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    origin = "https://glados.rocks"
    referer = "https://glados.rocks/console/checkin"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload = {
        'token': 'glados_network'
    }
    checkin = requests.post(url,
                            headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent,
                                     'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
    state = requests.get(url2,
                         headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})

    if 'message' in checkin.text:
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        # print(time)
        if sever == 'on':
            url3 = 'https://sct.ftqqapi.com/'.__add__(sckey).__add__('.send?text=').__add__(mess).__add__(
                '，you have ').__add__(time).__add__(' days left')
            requests.get(url3)
    else:
        url4 = 'https://sct.ftqqapi.com/'.__add__(sckey).__add__('.send?text=cookie过期')
        requests.get(url4)


def main_handler(event, context):
    return start()


if __name__ == '__main__':
    start()
