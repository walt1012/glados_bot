import requests, json, os
import cloudscraper
scraper = cloudscraper.create_scraper(disableCloudflareV1=True)

# server酱开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
# sever = os.environ["SERVE"]
# sever = "on"
# 填写server酱sckey,不开启server酱则不用填
# sckey = os.environ["SCKEY"]
# 填入glados账号对应cookie
cookie1 = os.environ["COOKIE1"]
cookie2 = os.environ["COOKIE2"]

def start():
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    origin = "https://glados.rocks"
    referer = "https://glados.rocks/console/checkin"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload = {
        'token': 'glados.network'
    }
    checkin1 = scraper.post(url, headers={'cookie': cookie1, 'referer': referer, 'origin': origin, 'user-agent': useragent,
                                     'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
    checkin2 = scraper.post(url, headers={'cookie': cookie2, 'referer': referer, 'origin': origin, 'user-agent': useragent,
                                 'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
    
    state1 = scraper.get(url2, headers={'cookie': cookie1, 'referer': referer, 'origin': origin, 'user-agent': useragent})
    state2 = scraper.get(url2, headers={'cookie': cookie2, 'referer': referer, 'origin': origin, 'user-agent': useragent})

    if ('message' in checkin1.text) and ('message' in checkin2.text):
        mess1 = checkin1.json()['message']
        mess2 = checkin2.json()['message']

        time1 = state1.json()['data']['leftDays'].split('.')[0]
        time2 = state2.json()['data']['leftDays'].split('.')[0]

        url3 = 'https://api.day.app/VHBmnRjJh7fKC47ZcELLr/'
            .__add__('🚩🚩🚩🚩打卡1🚩🚩🚩🚩').__add__(mess1).__add__('，').__add__(time1).__add__(' days left')
            .__add__('🚩🚩🚩🚩打卡2🚩🚩🚩🚩').__add__(mess2).__add__('，').__add__(time2).__add__(' days left')

        scraper.get(url3)
    else:
        url4 = 'https://api.day.app/VHBmnRjJh7fKC47ZcELLr/COOKIE过期'
        scraper.get(url4)


def main_handler(event, context):
    return start()


if __name__ == '__main__':
    start()
