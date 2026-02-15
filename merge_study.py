import pandas as pd
import re
import requests
import json

# 고객정보
고객 = pd.DataFrame({
    '고객ID': ['100', '200', '300', '500'], 
    '이름': ['김철수', '이영희', '박민수', '테스트']
})

# 주문정보  
주문 = pd.DataFrame({
    '고객ID': ['100', '100', '200', '300', '400'], 
    '상품': ['노트북', '마우스', '키보드', '모니터', '패드']
})

print("고객:\n", 고객)
print("\n주문:\n", 주문)

# 1. Inner Join (기본값) - 양쪽 다 있는 데이터만
inner = pd.merge(고객, 주문, on='고객ID', how='inner')
print("")
print("고객ID 기준, inner")
print("Inner:\n", inner)

# 2. Left Join - 고객 기준 (모든 고객 포함)
left = pd.merge(고객, 주문, on='고객ID', how='left') 
print("")
print("고객ID 기준, left")
print("\nLeft:\n", left)

# 3. Right Join - 주문 기준 (모든 주문 포함)
right = pd.merge(고객, 주문, on='고객ID', how='right')
print("")
print("고객ID 기준, right")
print("\nRight:\n", right)

# 4. Outer Join - 모두 포함 (NaN으로 빈칸)
outer = pd.merge(고객, 주문, on='고객ID', how='outer')
print("")
print("고객ID 기준, outer")
print("\nOuter:\n", outer)

print("############################################################")

text = "딥러닝 모델을 학습시키기 위해 데이터를 전처리합니다"
words = text.split()
print("# words")
print(words)
bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
bigrams2 = [(words[i:i+2]) for i in range(len(words)-1)]
print("# bigrams")
print(bigrams)
print("# bigrams[:3]")
print(bigrams[:3])
print("# bigrams2")
print(bigrams2)

print("############################################################")

text = "와아아아아아아 대박 !!!!  2026년"
text = re.sub(r'\d+', '', text)
text = re.sub(r'(.)\1{2,}', r'\1\1', text)
print("# TEXT")
print(text)

print("############################################################")


# OpenWatch API 엔드포인트 (재산 현황)
API_URL = "https://api.openwatch.kr/v1/national-assembly/assets"

def fetch_member_assets(member_name=None, year=None):
    """
    국회의원 재산 현황을 OpenWatch API로 조회
    - member_name: 의원명 (옵션)
    - year: 연도 (옵션, 예: 2025)
    """
    params = {}
    if member_name:
        params['member_name'] = member_name
    if year:
        params['year'] = year
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # JSON에서 DataFrame으로 변환
        if 'data' in data:
            df = pd.DataFrame(data['data'])
            return df
        else:
            print("데이터를 찾을 수 없습니다:", data)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패: {e}")
        return None

# 사용 예시 1: 전체 국회의원 재산 현황
all_assets = fetch_member_assets()
if all_assets is not None:
    print("전체 국회의원 재산 현황:")
    print(all_assets.head())
    print(f"총 {len(all_assets)}명의 의원 데이터")

# 사용 예시 2: 특정 의원 재산 조회
member_assets = fetch_member_assets(member_name="김영주")
if member_assets is not None:
    print(f"\n김영주 의원 재산:")
    print(member_assets)

# 사용 예시 3: 특정 연도 재산 조회
year_assets = fetch_member_assets(year=2025)
if year_assets is not None:
    print(f"\n2025년 재산 현황:")
    print(year_assets.head())
    
    # 재산 총액 상위 10명
    if 'total_amount' in year_assets.columns:
        top10 = year_assets.nlargest(10, 'total_amount')[['member_name', 'total_amount']]
        print("\n재산 상위 10명:")
        print(top10)