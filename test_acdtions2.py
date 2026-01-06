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
from datetime import datetime, timedelta, timezone
from tabulate import tabulate

File_Name = "NEWS/Today_Invest.md"
output = open(File_Name, 'w+t')

pageSize=60
headers={'user-agent': 'Mozilla/5.0'}

# Pension List
AMOUNT_BUDGET = 600000
PENSION_PERCS = ['0%', '50%', '15%', '10%', '10%', '15%', '0%', '0%']
PENSION_DIVIDENDS, PENSION_CALL = [], []

MY_STOCK_PRICE, MY_PERC = [], []
# MY_STOCK_COUNT = [191, 507, 193, 259, 175, 197, 1054, 795]
MY_STOCK_COUNT_Dict = {'KODEX 200TR' : 191,
                       'KODEX 미국S&P500' : 507,
                       'KODEX iShares미국투자등급회사채액티브' : 193,
                       'KODEX 미국10년국채선물' : 259,
                       'KODEX 미국30년국채액티브(H)' : 175,
                       'KODEX 미국배당다우존스' : 197,
                       'TIGER 미국필라델피아반도체나스닥' : 1054,
                       'ACE 테슬라밸류체인액티브' : 795}

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
    sum, sum1 =0, 0
    
    # 아래 ETF 리스트 중 ETF그룹을 선별
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

    for idx, val in enumerate(list(MY_STOCK_COUNT_Dict.values())) :
      print("%s, %i" %(DF_Pension_StockName[idx], PENSION_PRICES[idx]*val))
      Result = int(PENSION_PRICES[idx]*val)
      MY_STOCK_PRICE.append(Result)
      sum+=Result
      if PENSION_PERCS[idx] != '0%' :
        sum1+=Result

    for idx, val in enumerate(MY_STOCK_PRICE) :
        if PENSION_PERCS[idx] != '0%' :
            print(f"{round((val/sum1*100), 0)}%")
            MY_PERC.append(f"{round((val/sum1*100), 0)}%")
        else :
            MY_PERC.append("0%")

    print("# MY_PERC")
    print(MY_PERC)
    
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
    df['MY_PERC'] = MY_PERC
    
    DateTime_TT = datetime.today().strftime("%Y%m%d_%H%M")
    utc_now = datetime.now(timezone.utc)
    seoul_time = utc_now + timedelta(hours=9)
    formatted_time = seoul_time.strftime("%Y%m%d_%H%M")
    
    # output.write('<center>Vers : %s </center>\n' % DateTime_TT)
    # output.write('<center>Vers : %s </center>\n' % formatted_time)
    # output.write('<br><br><br>\n')

    print(df.to_markdown(index=False))
    output.write(df.to_markdown())

__KO_ETF_Allocation()
