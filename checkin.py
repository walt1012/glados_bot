import requests, json, os
import cloudscraper
scraper = cloudscraper.create_scraper(disableCloudflareV1=True)

cookie = os.environ["COOKIE"]

def start():
    url1 = "https://glados.cloud/console/checkin"
    url2 = "https://glados.cloud/console/account"
    origin = "https://glados.cloud"
    referer = "https://glados.cloud/console/checkin"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload = {
        'token': 'glados.one'
    }
    checkin = scraper.post(url1, headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent,
                                 'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
    state = scraper.get(url2, headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})

    if ('message' in checkin.text):
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays']
        print(mess)
        print(time)

def main_handler(event, context):
    return start()


if __name__ == '__main__':
    start()
