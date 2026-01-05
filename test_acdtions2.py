print("# TEST Actions 2")

import requests
import json
import pandas as pd
import io
import platform
# import shutil
# import datetime, time # for sleep
# import matplotlib.pyplot as plt
# from matplotlib import rc
from datetime import datetime
from tabulate import tabulate

File_Name = "NEWS/Today_Invest.md"
output = open(File_Name, 'w+t')

pageSize=60
headers={'user-agent': 'Mozilla/5.0'}

# Pension List
AMOUNT_BUDGET = 600000
PENSION_PERCS = ['0%', '50%', '15%', '10%', '10%', '15%', '0%', '0%']
PENSION_DIVIDENDS, PENSION_CALL = [], []

def __Get_ETF_List() : # Market에 따른 기업명 Symbols를 가져온다

    DF_ETF_list = []

    Breaker = False
    ETF_Symbol_List, ETF_stockName_List = [], []

    Breaker_1 = False
    for i in range(1,20) : # 60*50 = 3000 개 기업을 가져오지만 페이지는 그만큼 없음
        url = 'https://m.stock.naver.com/api/stocks/etf/marketValue?page='+str(i)+'&pageSize='+str(pageSize)
        # print(url)
        req = requests.get(url, headers=headers)
        j = json.loads(req.text) # to Dictionary
        # print(type(j)) # <class 'dict'>
        # print(len(j)) # 페이지에있던 없던 6으로 찍히므로 내부에서 또 거르자
        for x_key, x_value in j.items() :
            if not all(j.values()) :
                # print("# x-key, x-value out")
                Breaker = True
                break
            else :
                if x_key == 'stocks' :
                    # print(type(x_value)) # <class 'list'>
                    # print(len(x_value)) # 60
                    for j in x_value :
                        # print(type(j)) # <class 'dict'>
                        # print(j)
                        for y_key, y_value in j.items() :
                            if y_key == 'reutersCode' :
                                ETF_Symbol_List.append(y_value)
                            if y_key == 'stockName' :
                                ETF_stockName_List.append(y_value)

        if Breaker == True :
            # print("# TEST %s" %i )
            break

    return ETF_Symbol_List, ETF_stockName_List

def __KO_Price(Dart_Exp_Code) :

    DF_ETF_list = []
    # url = 'https://api.finance.naver.com/siseJson.naver?symbol=373220&requestType=1&startTime=1800&endTime=2100&timeframe=day'
    # https://m.stock.naver.com/api/stock/251340/price?pageSize=10&page=1
    url = 'https://api.finance.naver.com/siseJson.naver?symbol='+Dart_Exp_Code+'&requestType=1&startTime=1800&endTime=2100&timeframe=day'

    print("# called URL")
    print(url)

    try :
        req = requests.get(url, headers=headers)
        # print("# req")
        # print(req.text)
        text_1 = req.text
        for x in text_1.splitlines() :
            if len(x) == 0 or len(x) == 1 or len(x) == 2 :
                continue
            x = x.replace(" ","")
            x = x.replace("[","")
            x = x.replace("]","")
            x = x.replace("\"","")
            x = x.replace("\'","")
            list_a = x.split(",")
            if len(list_a) == 8 :
                del list_a[-1] # 외국인 비율이 없을 수도 있다 ''
            # print(list_a)
            DF_ETF_list.append(list_a)
    except jsondecodeerror as e:
        print("# exception")
        print(req.text)

    print("#######################################")
    DF_KO_Price = pd.DataFrame(columns=['날짜', '시가', '고가', '저가', '종가', '거래량', '외국인소진율'])
    # ['날짜', '시가', '고가', '저가', '종가', '거래량', '외국인소진율']
    for idx, val in enumerate(DF_ETF_list) :
        if idx == 0 :
            continue
        DF_KO_Price_Length = len(DF_KO_Price)
        DF_KO_Price.loc[DF_KO_Price_Length] = val

    DF_KO_Price.종가 = DF_KO_Price.종가.astype(int)

    print("# DF")
    # print(DF_KO_Price)
    # print(DF_KO_Price["종가"])
    # print(DF_KO_Price["종가"].min())
    # print(DF_KO_Price["종가"].max())
    # print(DF_KO_Price["종가"].mean())
    # print((DF_KO_Price["종가"].min() + DF_KO_Price["종가"].mean())/ 2)
    DF_KO_Price_List = DF_KO_Price["종가"].to_list()[-250:]
    DF_KO_Date_List = DF_KO_Price["날짜"].to_list()[-250:]
    DF_KO_Price_List = [float(i) for i in DF_KO_Price_List]
    DF_KO_Price_List_LEN = float(len(DF_KO_Price_List))
    DF_KO_Price_List_SUM = sum(DF_KO_Price_List)
    DF_KO_Price_Value = DF_KO_Price_List_SUM / DF_KO_Price_List_LEN # 200일 간의 평균값
    print("# 200일 간의 평균값")
    print(DF_KO_Price_Value)

    return DF_KO_Date_List, DF_KO_Price_List

def __Get_ETF_Price(ETF_Symbol) : # Market에 따른 기업명 Symbols를 가져온다

    DF_ETF_list = []
    # for i in range(1,500) : # 60*50 = 3000 개 기업을 가져오지만 페이지는 그만큼 없음
    Breaker = False

    # for i in range(1,500) : # 60*50 = 3000 개 기업을 가져오지만 페이지는 그만큼 없음
    ETF_Price_List, ETF_Date_List = [], []
    Breaker_1 = False
    for i in range(1,500) : # 60*50 = 3000 개 기업을 가져오지만 페이지는 그만큼 없음
        url = 'https://m.stock.naver.com/api/stock/'+ETF_Symbol+'/price?page='+str(i)+'&pageSize='+str(pageSize)
        print(url)
        req = requests.get(url, headers=headers)
        j = json.loads(req.text) # to Dictionary
        # print(type(j)) # <class 'list'>
        # print(len(j)) # <class 'list'>
        if len(j) == 0 :
            print("# For 1 out : 페이지 조회 0 ?")
            break

        # print(j[1]) 
        # {'localTradedAt': '2022-02-11',
        # 'closePrice': '37,240',
        # 'compareToPreviousClosePrice': '-350',
        # 'compareToPreviousPrice': {'code': '5','text': '하락', 'name': 'FALLING'},
        # 'fluctuationsRatio': '-0.93',
        # 'openPrice': '37,250',
        # 'highPrice': '37,505',
        # 'lowPrice': '37,065',
        # 'accumulatedTradingVolume': 2801655}
        
        Breaker_2 = False
        for x in range(len(j)) :
            # print(j[x])
            for j_key, j_value in j[x].items():
                if j_key == '' :
                    Breaker_2 = True
                else :
                    if j_key == "localTradedAt" :
                        ETF_Date = datetime.strptime(j_value, "%Y-%m-%d")
                        # print("# 1 - Key : %s, Value : %s" % (j_key, ETF_Date))
                        ETF_Date_List.append(j_value)
                    if j_key == "closePrice" :
                        # print("# 2 - Key : %s, Value : %s" % (j_key, j_value))
                        j_value = j_value.replace(",","")
                        # print("# 2 - Key : %s, Value : %s" % (j_key, j_value))
                        ETF_Price_List.append(j_value)
            if Breaker_2 == True :
                # print("# Breaker 2")
                Breaker_1 = True
                break
        if Breaker_2 == True :
            # print("# Breaker 1")
            break

    return ETF_Date_List, ETF_Price_List

def __KO_ETF_Allocation() :

    ETF_Symbol_List, ETF_stockName_List = __Get_ETF_List() # 네이버 페이지에서 ETF 리스트를 확보 (종목코드, 종목명)

    DF_ETF = pd.DataFrame()
    DF_ETF_Average = pd.DataFrame()
    DF_ETF_Average_Hist = pd.DataFrame()
    DF_ETF_Profit = pd.DataFrame()
    DF_Pension = pd.DataFrame()

    DF_Pension_StockName, PENSION_PRICES = [], []

    # 아래 ETF 리스트 중 ETF그룹을 선별
    
    # ETF_Symbol_List.index(x)
    # ETF_List = ["069500", "229200", "114800", "153130", "152380", "132030", "219480", "261240"]
    # 069500 : KODEX 200 : 연 0.150% (지정참가회사 : 0.005%, 집합투자 : 0.120%, 신탁 : 0.010%, 일반사무 : 0.015%)
    # 229200 : KODEX 코스닥 150 : 연 0.250% (지정참가회사 : 0.010%, 집합투자 : 0.200%, 신탁 : 0.020%, 일반사무 : 0.020%)
    # 114800 : KODEX 인버스 : 연 0.640% (지정참가회사 : 0.020%, 집합투자 : 0.580%, 신탁 : 0.020%, 일반사무 : 0.020%)
    # 153130 : KODEX 단기채권 : 연 0.150% (지정참가회사 : 0.020%, 집합투자 : 0.110%, 신탁 : 0.010%, 일반사무 : 0.010%)
    # 152380 : KODEX 국채선물10년 : 연 0.070% (지정참가회사 : 0.005%, 집합투자 : 0.045%, 신탁 : 0.010%, 일반사무 : 0.010%)
    # 132030 : KODEX 골드선물(H) : 연 0.680% (지정참가회사 : 0.100%, 집합투자 : 0.500%, 신탁 : 0.040%, 일반사무 : 0.040%)
    # 219480 : KODEX 미국S&P500선물(H) : 연 0.250% (지정참가회사 : 0.020%, 집합투자 : 0.190%, 신탁 : 0.020%, 일반사무 : 0.020%)
    # 261240 : KODEX 미국달러선물 : 연 0.250% (지정참가회사 : 0.020%, 집합투자 : 0.190%, 신탁 : 0.020%, 일반사무 : 0.020%)

    # 363570 : KODEX 장기종합채권(AA-이상)액티브KAP : 연 0.070% (지정참가회사 : 0.005%, 집합투자 : 0.050%, 신탁 : 0.005%, 일반사무 : 0.010%)
    # 308620 : KODEX 미국채10년선물 : 연 0.090% (지정참가회사 : 0.005%, 집합투자 : 0.045%, 신탁 : 0.020%, 일반사무 : 0.020%)
    # 304660 : KODEX 미국채울트라30년선물(H) : 연 0.300% (지정참가회사 : 0.010%, 집합투자 : 0.250%, 신탁 : 0.020%, 일반사무 : 0.020%)

    # ETF_List = ["069500", "229200", "219480", "283580", "101280", "251350"]
    # 069500 : KODEX 200 : 연 0.150% (지정참가회사 : 0.005%, 집합투자 : 0.120%, 신탁 : 0.010%, 일반사무 : 0.015%)
    # 229200 : KODEX 코스닥 150 : 연 0.250% (지정참가회사 : 0.010%, 집합투자 : 0.200%, 신탁 : 0.020%, 일반사무 : 0.020%)
    # 219480 : KODEX 미국S&P500선물(H) : 연 0.250% (지정참가회사 : 0.020%, 집합투자 : 0.190%, 신탁 : 0.020%, 일반사무 : 0.020%)
    # 283580 : KODEX 차이나CSI300 : 연 0.120% (지정참가회사 : 0.010%, 집합투자 : 0.050%, 신탁 : 0.040%, 일반사무 : 0.020%)
    # 101280 : KODEX 일본TOPIX 100
    # 251350 : KODEX 선진국MSCI World

    # ETF_List = ["102110", "360750", "319640", "192090", "105010", "195930", "241180", "360750", "225060"]
    # 102110 : TIGER 200 : 연 0.05% (운용: 0.029%, 지정참가: 0.001%, 신탁: 0.01%, 일반사무: 0.01%)
    # 360750 : TIGER 미국S&P500연 0.07%(집합투자 : 0.05%, LP : 0.001%, 신탁 : 0.01%, 사무관리 0.009%)
    # 319640 : TIGER 골드선물(H)
    # 192090 : TIGER 차이나CSI300
    # 105010 : TIGER 라틴35
    # 195930 : TIGER 유로스탁스50 (합성 H)
    # 241180 : TIGER 일본니케이225
    # 360750 : TIGER 미국S&P500
    # 225060 : TIGER 이머징마켓MSCI 레버리지(합성H) : 0.58%(운용: 0.51%, 지정참가: 0.01%, 신탁: 0.03%, 일반사무 0.03%)

    # ETF_List = ["102110", "123310", "232080", "272580", "302190", "114820", "319640"]
    # 102110 : TIGER 200 : 연 0.05% (운용: 0.029%, 지정참가: 0.001%, 신탁: 0.01%, 일반사무: 0.01%)
    # 123310 : TIGER 인버스 : 연 0.022% (운용: 0.001%, 지정참가: 0.001%, 신탁: 0.01%, 일반사무: 0.01%)
    # 232080 : TIGER 코스닥150 : 0.19% (운용 0.14%, 지정참가 0.01%, 수탁 0.02%, 사무관리 0.02%)
    # 272580 : TIGER 단기채권액티브 : 연 0.07% (운용: 0.055%, 지정참가: 0.005%, 신탁: 0.005%, 일반사무: 0.005%)
    # 302190 : TIGER 중장기국채 : 연 0.15% ( 운용 : 0.12%, 지정참가 0.01%, 신탁 : 0.01%, 일반사무 : 0.01%)
    # 114820 : TIGER 국채3년 : 연 0.15% (운용: 0.07%, 지정참가: 0.055%, 신탁: 0.01%, 일반사무: 0.015%)
    # 319640 : TIGER 골드선물(H)

    # ETF_List = ["102110", "123310", "319640", "160580", "130680", "137610"]
    # 102110 : TIGER 200 : 연 0.05% (운용: 0.029%, 지정참가: 0.001%, 신탁: 0.01%, 일반사무: 0.01%)
    # 123310 : TIGER 인버스 : 연 0.022% (운용: 0.001%, 지정참가: 0.001%, 신탁: 0.01%, 일반사무: 0.01%)
    # 319640 : TIGER 골드선물(H)
    # 139310 : TIGER 금속선물 --> 없어짐 (2026.01.01)
    # 160580 : TIGER 구리실물
    # 130680 : TIGER 원유선물Enhanced(H)
    # 137610 : TIGER 농산물선물Enhanced(H)

    # ETF_List = ["174350", "147970", "227570", "319640", "160580", "329750", "305080", "192090"]
    # 174350 : TIGER 로우볼 : 연 0.40%(운용 : 0.28%, 지정참가 : 0.07%, 신탁 : 0.02%, 일반사무 : 0.03%)
    # 147970 : TIGER 모멘텀 : 연 0.29% (운용: 0.20%, 지정참가: 0.03%, 신탁: 0.03%, 일반사무: 0.03%)
    # 227570 : TIGER 우량가치 : 연 0.40% (운용: 0.28%, 지정참가: 0.07%, 신탁: 0.02%, 일반사무: 0.03%)
    # 319640 : TIGER 골드선물(H) : 연 0.39% (운용: 0.34%, 지정참가: 0.01%, 신탁: 0.02%, 일반사무: 0.02%)
    # 160580 : TIGER 구리실물 : 연 0.83% (운용: 0.73%, 지정참가: 0.02%, 신탁: 0.05%, 일반사무: 0.03%)
    # 329750 : TIGER 미국달러단기채권액티브 : 연 0.30%(운용 : 0.225%, 지정참가 : 0.025%, 신탁 : 0.025%, 일반사무 : 0.025%)
    # 305080 : TIGER 미국채10년선물 : 연 0.29%(운용 : 0.23%, 지정참가 : 0.02%, 신탁 : 0.02%, 사무 : 0.02%)
    # 192090 : TIGER 차이나CSI300 : 연 0.63%(운용 : 0.50%, 지정참가 : 0.04%, 신탁 : 0.05%, 일반사무 : 0.04%) 

    # 225060 : TIGER 이머징마켓MSCI 레버리지(합성H) : 0.58%(운용: 0.51%, 지정참가: 0.01%, 신탁: 0.03%, 일반사무 0.03%)

    ETF_List = ["278530", "379800", "468630", "308620", "484790", "489250", "381180", "457480"]
    # 278530 코스피 KODEX 200TR
    # 069500 코스피배당 KODEX 200
    # 379800 코스피배당 KODEX 미국S&P500
    # 468630 코스피배당 KODEX iShares미국투자등급회사채액티브
    # 308620 코스피배당 KODEX 미국10년국채선물
    # 484790 코스피배당 KODEX 미국30년국채액티브(H)
    # 489250 코스피배당 KODEX 미국배당다우존스
    # 381180 코스피배당 TIGER 미국필라델피아반도체나스닥
    # 457480 코스피배당 ACE 테슬라밸류체인액티브

    for ETF_Symbol in ETF_List : # 선별된 ETF그룹의 각 ETF별 가격을 확보 (날짜, 종가)
        # print(ETF_Symbol)
        # ETF_Date_List, ETF_Price_List = __Get_ETF_Price(ETF_Symbol)
        ETF_Date_List, ETF_Price_List = __KO_Price(ETF_Symbol)
        # print(ETF_Date_List[:250]) # 1년 52주 중에서 52*주말 2일 = 104일(주말) + 공휴일까지 대충 110 빼서 1년을 250일
        # print(ETF_Price_List[:250]) # 1년 52주 중에서 52*주말 2일 = 104일(주말) + 공휴일까지 대충 110 빼서 1년을 250일

        # print("# ETF Date List")
        # print(ETF_Date_List)
        # print("# ETF_Price_List")
        # print(ETF_Price_List)

        # print("# ETF_Symbol")
        # print(ETF_Symbol)
        # print("# ETF_Symbol_List")
        # print(ETF_Symbol_List)
        # print("# ETF_Symbol_List --> ETF Symbol")
        # print(ETF_Symbol_List.index(ETF_Symbol))
        # print(ETF_Symbol_List[ETF_Symbol_List.index(ETF_Symbol)])
        # print(ETF_stockName_List[ETF_Symbol_List.index(ETF_Symbol)])
        # print("# %s : %s" % (ETF_Symbol_List[ETF_Symbol_List.index(ETF_Symbol)], ETF_stockName_List[ETF_Symbol_List.index(ETF_Symbol)]))

        ETF_StockName = ETF_stockName_List[ETF_Symbol_List.index(ETF_Symbol)]

        DF_ETF['DATE'] = ETF_Date_List[:250]
        DF_ETF[ETF_StockName] = ETF_Price_List[:250]
        DF_ETF[ETF_StockName] = round(DF_ETF[ETF_StockName].astype(float))

        ETF_Price_List = [int(i) for i in ETF_Price_List]
        ETF_Mean_Now = ETF_Price_List[0]
        ETF_Mean_2M = sum(ETF_Price_List[20:40]) / len(ETF_Price_List[20:40]) # 한달은 대충 20일
        ETF_Mean_3M = sum(ETF_Price_List[41:60]) / len(ETF_Price_List[41:60]) # 한달은 대충 20일
        ETF_Mean_4M = sum(ETF_Price_List[61:80]) / len(ETF_Price_List[61:80]) # 석달은 대충 60일
        ETF_Mean_5M = sum(ETF_Price_List[81:100]) / len(ETF_Price_List[81:100]) # 석달은 대충 60일
        ETF_Mean_6M = sum(ETF_Price_List[111:120]) / len(ETF_Price_List[111:120]) # 석달은 대충 60일
        ETF_Mean_7M = sum(ETF_Price_List[121:140]) / len(ETF_Price_List[121:140]) # 여섯달 120일
        ETF_Mean_8M = sum(ETF_Price_List[141:160]) / len(ETF_Price_List[141:160]) # 여섯달 120일
        ETF_Mean_9M = sum(ETF_Price_List[161:180]) / len(ETF_Price_List[161:180]) # 여섯달 120일
        ETF_Mean_10M = sum(ETF_Price_List[181:200]) / len(ETF_Price_List[181:200]) # 여섯달 120일
        ETF_Mean_11M = sum(ETF_Price_List[201:220]) / len(ETF_Price_List[201:220]) # 여섯달 120일
        ETF_Mean_12M = sum(ETF_Price_List[221:241]) / len(ETF_Price_List[221:241]) # 1년 : 끝까지

        ETF_Profit_Now = 0
        ETF_Profit_2M = (ETF_Price_List[0] - (sum(ETF_Price_List[20:40]) / len(ETF_Price_List[20:40]))) /             (sum(ETF_Price_List[20:40]) / len(ETF_Price_List[20:40]))
        ETF_Profit_3M = (ETF_Price_List[0] - (sum(ETF_Price_List[41:60]) / len(ETF_Price_List[41:60]))) /             (sum(ETF_Price_List[41:60]) / len(ETF_Price_List[41:60]))
        ETF_Profit_4M = (ETF_Price_List[0] - (sum(ETF_Price_List[61:80]) / len(ETF_Price_List[61:80]))) /             (sum(ETF_Price_List[61:80]) / len(ETF_Price_List[61:80]))
        ETF_Profit_5M = (ETF_Price_List[0] - (sum(ETF_Price_List[81:100]) / len(ETF_Price_List[81:100]))) /             (sum(ETF_Price_List[81:100]) / len(ETF_Price_List[81:100]))
        ETF_Profit_6M = (ETF_Price_List[0] - (sum(ETF_Price_List[101:120]) / len(ETF_Price_List[101:120]))) /             (sum(ETF_Price_List[101:120]) / len(ETF_Price_List[101:120]))
        ETF_Profit_7M = (ETF_Price_List[0] - (sum(ETF_Price_List[121:140]) / len(ETF_Price_List[121:140]))) /             (sum(ETF_Price_List[121:140]) / len(ETF_Price_List[121:140]))
        ETF_Profit_8M = (ETF_Price_List[0] - (sum(ETF_Price_List[141:160]) / len(ETF_Price_List[141:160]))) /             (sum(ETF_Price_List[141:160]) / len(ETF_Price_List[141:160]))
        ETF_Profit_9M = (ETF_Price_List[0] - (sum(ETF_Price_List[161:180]) / len(ETF_Price_List[161:180]))) /             (sum(ETF_Price_List[161:180]) / len(ETF_Price_List[161:180]))
        ETF_Profit_10M = (ETF_Price_List[0] - (sum(ETF_Price_List[181:200]) / len(ETF_Price_List[181:200]))) /             (sum(ETF_Price_List[181:200]) / len(ETF_Price_List[181:200]))
        ETF_Profit_11M = (ETF_Price_List[0] - (sum(ETF_Price_List[201:220]) / len(ETF_Price_List[201:220]))) /             (sum(ETF_Price_List[201:220]) / len(ETF_Price_List[201:220]))
        ETF_Profit_12M = (ETF_Price_List[0] - (sum(ETF_Price_List[221:241]) / len(ETF_Price_List[221:241]))) /             (sum(ETF_Price_List[221:241]) / len(ETF_Price_List[221:241]))
        # 한한달  5일  * 4주  = 20일
        # 20일 * 12 = 240 + Buffer -> 250
        
        ETF_Mean = [round(ETF_Mean_Now), round(ETF_Mean_2M), round(ETF_Mean_3M), round(ETF_Mean_4M),             round(ETF_Mean_5M), round(ETF_Mean_6M), round(ETF_Mean_7M), round(ETF_Mean_8M),             round(ETF_Mean_9M), round(ETF_Mean_10M), round(ETF_Mean_11M), round(ETF_Mean_12M)]
        ETF_History = []
        ETF_Profit = [round(ETF_Profit_Now, 2), round(ETF_Profit_2M, 2), round(ETF_Profit_3M, 2), round(ETF_Profit_4M, 2),             round(ETF_Profit_5M, 2), round(ETF_Profit_6M, 2), round(ETF_Profit_7M, 2), round(ETF_Profit_8M, 2),             round(ETF_Profit_9M, 2), round(ETF_Profit_10M, 2), round(ETF_Profit_11M, 2), round(ETF_Profit_12M, 2)]

        for idx, val in enumerate(ETF_Mean) :
            print("# idx : %s, val : %s" % (idx, val))
            if idx == 0:
                print("# ETF_History Fist insert 현재값")
                ETF_History.append(val)
            else :
                print("# ETF_History Next insert 현재값")
                if ETF_Mean[0] > ETF_Mean[idx] :
                    ETF_History.append(int(1))
                elif ETF_Mean[0] * 1.1 > ETF_Mean[idx] and ETF_Mean[0] * -1.1 < ETF_Mean[idx] :
                    ETF_History.append(int(0))
                else :
                    ETF_History.append(int(-1))

        print("# %s : %s" % (ETF_Symbol_List[ETF_Symbol_List.index(ETF_Symbol)], ETF_stockName_List[ETF_Symbol_List.index(ETF_Symbol)]))
        print("# 마지막 종가 : %s, %i" % (ETF_Date_List[-1], ETF_Price_List[-1]))

        DF_Pension_StockName.append(ETF_stockName_List[ETF_Symbol_List.index(ETF_Symbol)])
        PENSION_PRICES.append(ETF_Price_List[-1])

        # print("# Pension List")
        # print(DF_Pension_StockName)
        # print(DF_Pension_List)

        DF_ETF_Average[ETF_StockName] = ETF_Mean
        DF_ETF_Average_Hist[ETF_StockName] = ETF_History
        DF_ETF_Profit[ETF_StockName] = ETF_Profit

    print("# DF_ETF")
    print(DF_ETF)

    # DF_Pension_StockName = ['KODEX 200TR', 'KODEX 미국S&P500', 'KODEX iShares미국투자등급회사채액티브', 'KODEX 미국10년국채선물', 'KODEX 미국30년국채액티브(H)', 'KODEX 미국배당다우존스', 'TIGER 미국필라델피아반도체나스닥', 'ACE 테슬라밸류체인액티브']
    # PENSION_PRICES = [23165, 22635, 11810, 12300, 8825, 11080, 28175, 21870]

    for index, price in enumerate(PENSION_PRICES):
    #     print(index, price, PENSION_PERCS[index])
        percentage_value = float(PENSION_PERCS[index].rstrip('%')) / 100
        dividend_amount = int(AMOUNT_BUDGET * percentage_value)
        PENSION_DIVIDENDS.append(dividend_amount)
        PENSION_CALL.append(int(dividend_amount/PENSION_PRICES[index]))

    df = pd.DataFrame({
        'ETF_Name': DF_Pension_StockName,
        'Alloc_P': PENSION_PERCS,
        'Price': PENSION_PRICES,
        'Alloc_C': PENSION_DIVIDENDS,
        'CALL': PENSION_CALL
        })

    # pd.set_option('display.max_rows', n)
    # pd.set_option('display.max_columns', n)
    # pd.set_option('display.max_colwidth', 10)
    # print(tabulate(df))
    # df.set_index('ETF_Name', inplace=True)
    # print(tabulate(df, headers=COLUMNS_V))
    print(df.to_markdown(index=False))
    output.write(df.to_markdown())

    # print("# ETF_Symbol_List.index(x)")
    # for x in ETF_List :
    #     print("# %s : %s" % (ETF_Symbol_List[ETF_Symbol_List.index(x)], ETF_stockName_List[ETF_Symbol_List.index(x)]))

    # print("# DF_ETF_Average")
    # print(DF_ETF_Average)
    # print(tabulate(DF_ETF_Average, headers='keys', tablefmt='psql'))

    # print("# ETF History")
    # # print(DF_ETF_Average_Hist)
    # print(tabulate(DF_ETF_Average_Hist, headers='keys', tablefmt='psql'))

    # print("# ETF History")
    # # print(DF_ETF_Average_Hist)
    # print(tabulate(DF_ETF_Profit, headers='keys', tablefmt='psql'))

    # print("# HeatMap")
    # __HeatMap(DF_ETF)

    # print("# HeatMap_New")
    # __HeatMap_New(DF_ETF)

# def __US_Allocation() :

#     DF_ETF = pd.DataFrame()
#     ETF_List = ["IEF.O", "SPY", "AOR", "VT", "EEM", "TLT.O", "BWX", "GLD", "DBC", "BIL"]

#     Breaker = False
#     Price_List, Date_List = [], []
#     Breaker_1 = False

#     for y in ETF_List :
#         Date_List, Price_List = __US_ETF_Price(y)
#         DF_ETF["DATE_List"] = Date_List[:250]
#         DF_ETF[y] = Price_List[:250]
#         DF_ETF[y] = round(DF_ETF[y].astype(float))

#     print("# DF_ETF")
#     print(DF_ETF)

#     plt.rcParams['axes.unicode_minus'] = False
#     plt.rcParams['font.family'] = 'AppleGothic'

#     DF_ETF_corr = DF_ETF.corr()
#     DF_ETF_corr = DF_ETF_corr.apply(lambda x: round(x ,2))
#     print("# corr")
#     # print(DF_ETF_corr)
#     print(tabulate(DF_ETF_corr, headers='keys', tablefmt='psql'))
    
#     __HeatMap(DF_ETF)

def __Mix_Allocation() :

    EN_DF_ETF, KO_DF_ETF = pd.DataFrame(), pd.DataFrame()
    EN_ETF_List = ["IEF.O", "SPY", "AOR", "VT", "EEM", "TLT.O", "BWX", "GLD", "DBC", "BIL"]
    KO_ETF_List = ["272580", "114820", "360750", "225060", "102110", "069500"]

    for ETF_Symbol in EN_ETF_List :
        Date_List, Price_List = __US_ETF_Price(ETF_Symbol)
        EN_DF_ETF["DATE_List"] = Date_List[:250]
        EN_DF_ETF[ETF_Symbol] = Price_List[:250]
        EN_DF_ETF[ETF_Symbol] = round(EN_DF_ETF[ETF_Symbol].astype(float))

    for ETF_Symbol in KO_ETF_List :
        Date_List, Price_List = __Get_ETF_Price(ETF_Symbol)
        KO_DF_ETF["DATE_List"] = Date_List[:250]
        KO_DF_ETF[ETF_Symbol] = Price_List[:250]
        KO_DF_ETF[ETF_Symbol] = round(KO_DF_ETF[ETF_Symbol].astype(float))

    print("# DF_ETF EN")
    print(EN_DF_ETF)

    print("# DF_ETF KO")
    print(KO_DF_ETF)

    Mix_DF_ETF = pd.DataFrame()
    print("# For Start")
    for index, row in KO_DF_ETF.iterrows() :
        if row["DATE_List"] in EN_DF_ETF.values :
            print("# True")
            print(type(row)) # <class 'pandas.core.series.Series'>
            print(index)
            print(row)
            print(row.iloc[index])
            print(type(EN_DF_ETF.loc[EN_DF_ETF["DATE_List"] == row["DATE_List"]])) # <class 'pandas.core.frame.DataFrame'>
            print(EN_DF_ETF.loc[EN_DF_ETF["DATE_List"] == row["DATE_List"]])
            # DF_Length = len(Mix_DF_ETF)
            # Mix_DF_ETF.loc[DF_Length] = LIST
            Mix_DF_ETF = pd.concat([row,EN_DF_ETF.loc[EN_DF_ETF["DATE_List"] == row["DATE_List"]]], axis=1, join='inner')
            # Mix_DF_ETF = pd.concat([row,df2],axis=1, join='inner')
        else :
            print("# False")
            print(row["DATE_List"])
    print("# For Done")

    print(Mix_DF_ETF)

    DF_ETF = pd.merge(left = EN_DF_ETF , right = KO_DF_ETF, how = "outer", on = "Date_List")

        # df.loc[df['column_name'] == some_value]
        # dataFrame[dataFrame['column name'].str.match('string')]


    print("# Total DF_ETF")
    print(DF_ETF)

def __US_ETF_Price(Symbol) :

    Date_List, Price_List = [], []
    for i in range(1,500) : # 60*50 = 3000 개 기업을 가져오지만 페이지는 그만큼 없음
        url = 'https://api.stock.naver.com/stock/'+Symbol+'/price?page='+str(i)+'&pageSize='+str(pageSize)
        print(url)
        req = requests.get(url, headers=headers)
        j = json.loads(req.text) # to Dictionary
        # print(type(j)) # <class 'list'>
        # print(len(j)) # <class 'list'>
        if len(j) == 0 :
            # print("# For 1 out")
            break
        
        Breaker_2 = False
        for x in range(len(j)) :
            for j_key, j_value in j[x].items():
                # print("# 2 - Key : %s, Value : %s" % (j_key, j_value))
                if j_key == '' :
                    Breaker_2 = True
                else :
                    if j_key == "localTradedAt" :
                        j_value = j_value[:10]
                        ETF_Date = datetime.strptime(j_value, "%Y-%m-%d")
                        Date_List.append(j_value)
                    if j_key == "closePrice" :
                        j_value = j_value.replace(",","")
                        # print("# 2 - Key : %s, Value : %s" % (j_key, j_value))
                        Price_List.append(j_value)
            if Breaker_2 == True :
                print("# Breaker 2")
                Breaker_1 = True
                break
        if Breaker_2 == True :
            print("# Breaker 1")
            break

    print(Date_List)
    print(Price_List)

    return Date_List, Price_List

# def __HeatMap(DF_ETF) :

#     plt.rcParams['axes.unicode_minus'] = False
#     plt.rcParams['font.family'] = 'AppleGothic'

#     DF_ETF_corr = DF_ETF.corr()
#     DF_ETF_corr = DF_ETF_corr.apply(lambda x: round(x ,2))
#     print("# corr")
#     # print(DF_ETF_corr)
#     print(tabulate(DF_ETF_corr, headers='keys', tablefmt='psql'))

#     ax = sns.heatmap(DF_ETF_corr, annot=True, annot_kws=dict(color='g'), cmap='BuGn_r')
#     # ax = sns.heatmap(DF_ETF_corr, annot=True, annot_kws=dict(color='g'), cmap='RdYlBu_r')

#     # supported values are 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', \
#     # 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', \
#     # 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', \
#     # 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', \
#     # 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', \
#     # 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', \
#     # 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', \
#     # 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', \
#     # 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', \
#     # 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', \
#     # 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', \
#     # 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', \
#     # 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', \
#     # 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', \
#     # 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', \
#     # 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'twilight', 'twilight_r', 'twilight_shifted', \
#     # 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'

#     ax.tick_params(
#         left=True, labelleft=True, \
#         right=False, labelright=False, \
#         top=True, labeltop=True, \
#         bottom=False, labelbottom=False \
#         # top=False, labeltop=False, \
#         # bottom=True, labelbottom=True \
#         )
#     ax.tick_params(axis='x', labelrotation=90)

#     if platform.system() == 'Darwin' : # or win32
#         DateTime = datetime.today().strftime("%Y%m%d")
#         plt.savefig("/Users/choiyoungmin/PycharmProjects/2020Y/Anal_Comp/Allocation_"+DateTime+".png")
#         File_Name_fig = "/Users/choiyoungmin/PycharmProjects/2020Y/Anal_Comp/Allocation_"+DateTime+".png"
#     else :
#         DateTime = datetime.today().strftime("%Y%m%d")
#         plt.savefig("C:\\Python\\Allocation\\Allocation_"+DateTime+".png")
#         File_Name_fig = "C:\\Python\\Allocation\\Allocation_"+DateTime+".png"
#         shutil.copyfile(File_Name_fig, 'C:\\Python\\Allocation\\Allocation.png')

    # plt.show()

    # with io.open(File_Name, 'w', encoding='utf-8') as f:
    #     f.write('<head><meta charset="utf-8"></head>')
    #     f.write('<style>')
    #     f.write('table {border: 1px solid #444444;border-collapse: collapse}')
    #     f.write('th, td {text-align: center}')
    #     f.write('</style>')
    #     f.write(DF_ETF_corr.to_html())
    #     f.write('<br><br><br>')
    #     if platform.system() == 'Darwin' : # or win32
    #         f.write('<img class=\"fit-picture\" src=/Users/choiyoungmin/PycharmProjects/2020Y/Anal_Comp/Allocation_'+DateTime+'.png')
    #     else :
    #         f.write('<img class=\"fit-picture\" src=Allocation.png>\n')
    #     f.write('<br><br><br>')
    # f.close()

# def __HeatMap_New(DF_ETF) :

#     plt.rcParams['axes.unicode_minus'] = False
#     plt.rcParams['font.family'] = 'AppleGothic'

#     df = DF_ETF.corr()
#     df = df.corr.apply(lambda x: round(x ,2))
#     # df = sns.heatmap(DF_ETF_corr, annot=True, annot_kws=dict(color='g'), cmap='BuGn_r')
#     sns.clustermap(df, 
#                 annot = True,      # 실제 값 화면에 나타내기
#                 cmap = 'RdYlBu_r',  # Red, Yellow, Blue 색상으로 표시
#                 vmin = -1, vmax = 1, #컬러차트 -1 ~ 1 범위로 표시
#                 )
#     plt.show()

__KO_ETF_Allocation()

# __US_Allocation()
# __Mix_Allocation() # --> TEST 중 (2022.02.20)

# shutil.copyfile(File_Name, 'C:\\Python\\Allocation\\Allocation.html')
