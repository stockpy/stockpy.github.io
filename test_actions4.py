# choiyoungmin.com/NEWS/dataframe/ 크롤링 코드 (가장 간단한 방법)
import pandas as pd
import requests
from io import StringIO

url = "http://choiyoungmin.com/NEWS/dataframe/"

# # 방법 1: pandas read_html (가장 추천)
# try:
#     tables = pd.read_html(url)
#     df = tables[0]  # 첫 번째 테이블 선택
#     print("=== 크롤링 성공 ===")
#     print(df)
#     df.to_csv("etf_portfolio.csv", index=False, encoding='utf-8')
#     print("📁 etf_portfolio.csv 저장 완료")
#     print("# encoding")
#     df1 = pd.read_csv("etf_portfolio.csv", encoding='utf-8')
#     print(df1)
    
# except Exception as e:
    # print(f"pandas 실패: {e}")
    
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
response.encoding = 'UTF-8'  # 한글 깨짐 문제 해결을 위해 인코딩 설정
soup = BeautifulSoup(response.text, 'html.parser')

# table 찾기
table = soup.find('table')
if table:
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        if cells:  # 빈 행 제외
            rows.append(cells)
    
    df = pd.DataFrame(rows[1:], columns=rows[0])  # 첫행 헤더
    print("=== BeautifulSoup 성공 ===")
    print("# DF")
    print(df)
    df.to_csv("etf_portfolio_bs.csv", index=False, encoding='UTF-8')
    
    df1 = pd.read_csv('etf_portfolio_bs.csv', encoding='utf-8')
    print("# DF1 - encoding")
    pritn(df1)
else:
    print("❌ 테이블을 찾을 수 없음")
