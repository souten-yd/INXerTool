#-*-coding:utf8;-*-
#qpy:quiet
#qpy:qpyapp

####設定変更箇所###
INXTokenHoldCount = 1000 #INXToken保有数を記載
ShowStockPrice = False #True:INX株価表示, False:INX株価非表示 処理時間が変わる。
##################

import androidhelper
droid = androidhelper.Android()
droid.vibrate(100)

import requests
import json
import math
from bs4 import BeautifulSoup as bs

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

def getSoup(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    header = {'User-Agent': user_agent}
    res = requests.get(url,headers=header)
    soup = bs(res.text, "html.parser")
    return soup

def getINXTokenPrice():
    url = "https://www.inx.co/inx-token/"
    soup = getSoup(url)
    targetElement = soup.find("div",class_="elementor-element elementor-element-907dbcc elementor-widget__width-auto elementor-widget elementor-widget-text-editor")
    INXTokenValue = (targetElement.find("div").text).strip("\n $")
    return float(INXTokenValue)

def getINXTokenHolder():
    url = "https://etherscan.io/dex/uniswapv3/0x4a9353bd25abe95f103e91e27eb63652f2cb7e6a"
    soup = getSoup(url)
    targetElement = soup.select("#ContentPlaceHolder1_divHolders .col-7")
    INXHolder = (targetElement[0].text).strip('\n') #改行コードを削除
    return INXHolder

def exchangeRatio():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    res = requests.get(url)
    data = res.json()
    USDJPY = data["rates"]["JPY"]
    return float(USDJPY)

def getStockPrice(Name:str):
    url = "https://finance.yahoo.com/quote/" + Name
    soup = getSoup(url)
    value = soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text
    return float(value)

USDJPY = exchangeRatio()
INXTokenPrice = getINXTokenPrice()
INXTokenJPY = USDJPY * INXTokenPrice
INXTokenHolder = getINXTokenHolder()
if ShowStockPrice:
    INXStockPrice = getStockPrice("INXDF")
    INXStockJPY = USDJPY * INXStockPrice

INXTokenSum = int(INXTokenJPY * INXTokenHoldCount)

if ShowStockPrice:
    mes = "INXStock: $" + str(round(INXStockPrice,3)) + ", ¥" + str(round(INXStockJPY,1))
    mes = mes + "\n" + "INXToken: $" + str(round(INXTokenPrice,3)) + ", ¥" + str(round(INXTokenJPY,1))
else:
    mes = "INXToken: $" + str(round(INXTokenPrice,3)) + ", ¥" + str(round(INXTokenJPY,1))

mes = mes + "\n" + "INXTokenSum: ¥" + str("{:,d}".format(INXTokenSum))
mes = mes + "\n" + "INXHodler: " + str(INXTokenHolder)
mes = mes + "\n" + "USDJPY: " + str(USDJPY)

droid.vibrate(100)
droid.makeToast(mes)
droid.makeToast(mes)
droid.makeToast(mes)