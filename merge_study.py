import pandas as pd
import re

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