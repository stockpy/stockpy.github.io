from datetime import datetime

print("# blog python")
print(datetime.now())
print("#############")

import requests
import datetime, time # for sleep

start = time.time()
headers={'user-agent': 'Mozilla/5.0'}

DateTime = datetime.today().strftime("%Y%m%d_%H%M")
    
File_Name = "NEWS.md"
output = open(File_Name, 'w+t')

def __NEWS(SECTION) :

    Break_Stop = 0
    if SECTION == "Internal" :
        File_Name = "NEWS/Internal_NEWS.md"
    else :
        File_Name = "NEWS/Ranking_NEWS.md"
    output = open(File_Name, 'w+t')

    for i in range(1,8) :
        if Break_Stop == 1 :
            break
        
        if SECTION == "Internal" :
            url = 'https://api.stock.naver.com/news/worldNews?pageSize=60&page='+str(i)
        else :
            url = 'https://m.stock.naver.com/api/news/list?category=ranknews&pageSize=60&page='+str(i)
        # print(url)

        req = requests.get(url, headers=headers)
        j = json.loads(req.text) # to Dictionary

        if len(j) == 0 :
            break

        # print(type(j)) # <class 'list'>
        DateTime = datetime.today().strftime("%Y%m%d")
        DateTime_TT = datetime.today().strftime("%Y%m%d_%H%M")

        output.write('<head><meta charset="utf-8"><title>Vers : %s </title></head>\n' % DateTime_TT)

        for key, val in enumerate(j) :

            if val['dt'][:8] != DateTime :
                print("# Date NOT OK")
                Break_Stop = 1
            if SECTION == "Internal" :
                if len(val['relatedItems']) > 0 :
                    print("#### %s(https://m.stock.naver.com/news/worldnews/view/fnGuide/%s)\n" % (val['tit'], val['aid']))
                    output.write("#### [%s](https://m.stock.naver.com/news/worldnews/view/fnGuide/%s)\n" % (val['tit'], val['aid']))
                    output.write("#### 종목정보 : <%s>\n" % val['relatedItems'][0]['endUrl'])
                else :
                    print("#### %s(https://m.stock.naver.com/news/worldnews/view/fnGuide/%s)\n" % (val['tit'], val['aid']))
                    output.write("#### [%s](https://m.stock.naver.com/news/worldnews/view/fnGuide/%s)\n" % (val['tit'], val['aid']))
                    print("")
                    output.write("")
            else :
#                 https://m.stock.naver.com/news/ranknews/view/011/0004032789
                print("#### [%s](https://m.stock.naver.com/news/ranknews/view/%s/%s)\n" % (val['tit'], val['oid'], val['aid']))
                output.write("#### [%s](https://m.stock.naver.com/news/ranknews/view/%s/%s)\n" % (val['tit'], val['oid'], val['aid']))
                # https://m.stock.naver.com/api/news/item/008/0004722452
                
    output.close()

__NEWS("Internal")
__NEWS("Ranking")
