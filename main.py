from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["wxbf73c33dd2558e0c"]
app_secret = os.environ["592a937529b54d54c1ba51a7ecfb057e"]

user_id = os.environ["okWP15uqYtqSxrpiQ3_BmvKn88Qo"]
template_id = os.environ["JbZ38T5mCdXWMJZy9IyvDMjTdm0gE7NtGVdHa_WBVEY"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(wxbf73c33dd2558e0c, 592a937529b54d54c1ba51a7ecfb057e)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(okWP15uqYtqSxrpiQ3_BmvKn88Qo	, JbZ38T5mCdXWMJZy9IyvDMjTdm0gE7NtGVdHa_WBVEY, data)
print(res)
