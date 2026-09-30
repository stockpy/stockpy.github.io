



⸻

layout: post
title: “Jekyll Liquid 문법 이해하기 — site, page, post, categories, data”
date: 2026-10-01
categories: [ABAP]
tags: [Jekyll, Liquid, Markdown, site, categories, data]

Jekyll Liquid 문법 이해하기

Jekyll에서 HTML을 동적으로 구성할 때는 Liquid 템플릿 문법을 사용합니다.

특히 다음과 같은 코드를 이해하려면 Liquid의 기본 개념을 알아야 합니다.

{% assign cat_label = site.data.category_labels[cat_key] %}
<h2 class="section-title">{{ cat_label | default: cat_key }}</h2>
<ul class="post-list">
  {% for post in cat[1] %}
  <li>
    <a href="{{ post.url | relative_url }}" class="post-title">{{ post.title }}</a>
    <div class="post-date">{{ post.date | date: "%Y-%m-%d" }}</div>
  </li>
  {% endfor %}
</ul>

또 다른 예:

{% for post in site.categories.sso %}
  <li>
    <a href="{{ post.url | relative_url }}" class="post-title">{{ post.title }}</a>
    <div class="post-date">{{ post.date | date: "%Y-%m-%d" }}</div>
  </li>
{% endfor %}

이 문서에서는 site, site.categories, site.data, post, cat, cat_key 등이 무엇인지 알아봅니다.

⸻

1. {% ... %}와 {{ ... }}의 차이

Liquid에서 가장 먼저 구분해야 하는 것은 두 가지 문법입니다.

{% ... %}

명령을 실행할 때 사용합니다.

{% assign name = "Dash" %}

변수를 생성합니다.

{% for post in site.posts %}

반복문을 실행합니다.

{% if page.title %}

조건문을 실행합니다.

즉,

{% ... %}

는

“무언가를 실행하라.”

라는 의미입니다.

⸻

2. {{ ... }}

값을 HTML 화면에 출력할 때 사용합니다.

{{ page.title }}

현재 페이지의 제목을 출력합니다.

{{ post.title }}

현재 게시글의 제목을 출력합니다.

{{ post.date }}

현재 게시글의 날짜를 출력합니다.

즉,

{{ ... }}

는

“값을 화면에 출력하라.”

라는 의미입니다.

⸻

3. site는 무엇인가?

site는 우리가 직접 만든 일반 변수가 아니라 Jekyll이 기본적으로 제공하는 Site 객체입니다.

예를 들어 다음과 같이 사용할 수 있습니다.

{{ site.title }}
{{ site.url }}
{{ site.posts }}
{{ site.categories }}
{{ site.data }}

개념적으로 보면 다음과 같은 구조입니다.

site
 ├── title
 ├── url
 ├── posts
 ├── categories
 ├── tags
 └── data

즉 site는 Jekyll 사이트 전체에 대한 정보를 가지고 있는 객체라고 이해하면 됩니다.

⸻

4. site.categories는 무엇인가?

Jekyll은 게시글의 categories 정보를 바탕으로 카테고리별 게시글 목록을 만들어줍니다.

예를 들어 어떤 게시글에 다음과 같이 작성했다고 가정합니다.

---
layout: post
title: "ABAP 시작하기"
categories: [ABAP]
---

또 다른 게시글은:

---
layout: post
title: "SSO 이해하기"
categories: [SSO]
---

그러면 Jekyll 내부에서는 개념적으로 다음과 같은 구조를 갖게 됩니다.

site.categories
│
├── ABAP
│    ├── post1
│    ├── post2
│    └── post3
│
└── SSO
     ├── post4
     └── post5

따라서:

site.categories.sso

는

site.categories 안에 있는 sso 카테고리의 게시글 목록

이라는 의미입니다.

⸻

5. site.categories.sso에서 sso는 예약어인가?

아닙니다.

이것은 매우 중요한 개념입니다.

site.categories.sso

에서 sso가 Jekyll의 예약어인 것이 아닙니다.

게시글의 카테고리가 다음과 같이 정의되어 있기 때문에 만들어지는 것입니다.

categories: [SSO]

즉,

site
 ↓
categories
 ↓
sso

라는 데이터 구조에서 sso라는 key를 찾아가는 것입니다.

예를 들어 카테고리가 ABAP이라면:

site.categories.abap

가 될 수 있고,

카테고리가 Basis라면:

site.categories.basis

처럼 사용할 수 있습니다.

⸻

6. post는 예약어인가?

아닙니다.

다음 코드를 보겠습니다.

{% for post in site.categories.sso %}

여기서 post는 Liquid의 예약어가 아닙니다.

for문에서 반복되는 객체를 저장하기 위해 우리가 정한 변수 이름입니다.

따라서 다음과 같이 바꿔도 됩니다.

{% for article in site.categories.sso %}
  {{ article.title }}
{% endfor %}

또는:

{% for abc in site.categories.sso %}
  {{ abc.title }}
{% endfor %}

모두 가능합니다.

즉:

{% for post in site.categories.sso %}

는 다음과 같이 이해하면 됩니다.

SSO 카테고리의 게시글을 하나씩 꺼내서
각각을 post라는 변수에 넣어라.

⸻

7. post.title, post.url, post.date

반복문 안에서 post는 현재 처리하고 있는 게시글입니다.

따라서:

{{ post.title }}

현재 게시글의 제목

{{ post.url }}

현재 게시글의 URL

{{ post.date }}

현재 게시글의 날짜

를 의미합니다.

예를 들어:

{% for post in site.categories.sso %}
  {{ post.title }}
{% endfor %}

는 SSO 카테고리에 있는 모든 게시글의 제목을 출력합니다.

⸻

8. cat은 무엇인가?

cat 역시 예약어가 아닙니다.

다음과 같은 코드에서 만들어진 변수라고 생각하면 됩니다.

{% for cat in site.categories %}

Jekyll이 카테고리를 하나씩 꺼내면서 cat 변수에 넣습니다.

개념적으로:

첫 번째 반복
cat = ["abap", [ABAP 게시글 목록]]
두 번째 반복
cat = ["sso", [SSO 게시글 목록]]
세 번째 반복
cat = ["basis", [Basis 게시글 목록]]

과 같은 형태로 생각할 수 있습니다.

⸻

9. cat[0]과 cat[1]

이제 다음 코드가 이해됩니다.

cat[0]

현재 카테고리의 이름입니다.

cat[1]

현재 카테고리에 속한 게시글 목록입니다.

따라서:

{% for post in cat[1] %}

는

현재 카테고리의 게시글 목록을 하나씩 post에 넣어라.

라는 의미입니다.

⸻

10. cat_key는 무엇인가?

cat_key 역시 Jekyll의 예약어가 아닙니다.

코드에서 직접 만들어 사용하는 변수입니다.

예를 들어:

{% assign cat_key = cat[0] %}

라고 하면:

cat[0]
  ↓
cat_key

가 됩니다.

예를 들어 현재 카테고리가 SSO라면:

cat[0] = "sso"
cat_key = "sso"

가 됩니다.

⸻

11. site.data는 무엇인가?

Jekyll에는 _data라는 특별한 폴더가 있습니다.

예를 들어:

_data/
└── category_labels.yml

파일을 만들 수 있습니다.

내용:

abap: "ABAP"
sso: "SSO / 인증"
basis: "SAP Basis"

그러면 Jekyll에서 다음과 같이 접근할 수 있습니다.

site.data.category_labels

구조를 보면:

site
 └── data
      └── category_labels
           ├── abap
           ├── sso
           └── basis

입니다.

⸻

12. site.data.category_labels.sso

따라서 다음 코드는:

site.data.category_labels.sso

_data/category_labels.yml의:

sso: "SSO / 인증"

값을 가져옵니다.

결과:

SSO / 인증

⸻

13. site.data.category_labels[cat_key]

이 부분은 조금 더 중요합니다.

site.data.category_labels[cat_key]

만약:

{% assign cat_key = "sso" %}

라면 다음과 같이 동작합니다.

site.data.category_labels[cat_key]

↓

site.data.category_labels["sso"]

따라서:

sso: "SSO / 인증"

의 값을 가져옵니다.

즉, []를 이용하면 변수의 값을 이용해서 데이터의 key를 동적으로 찾을 수 있습니다.

⸻

14. .과 [ ]의 차이

둘의 차이를 기억하는 것이 중요합니다.

고정된 이름으로 접근

site.categories.sso

site.categories에서 sso라는 key를 직접 지정합니다.

변수로 접근

site.categories[cat_key]

cat_key에 들어 있는 값을 key로 사용합니다.

예를 들어:

{% assign cat_key = "sso" %}

이면:

site.categories[cat_key]

는 다음과 같은 의미입니다.

site.categories["sso"]

⸻

15. assign

assign은 Liquid에서 변수를 만드는 명령입니다.

{% assign name = "Dash" %}

그러면 이후:

{{ name }}

으로 사용할 수 있습니다.

결과:

Dash

다른 예:

{% assign cat_key = cat[0] %}

현재 카테고리의 이름을 cat_key에 저장합니다.

⸻

16. default Filter

다음 코드를 보겠습니다.

{{ cat_label | default: cat_key }}

여기서 |는 Filter를 의미합니다.

cat_label 값이 있으면 그것을 사용하고,

값이 없으면 cat_key를 사용합니다.

예를 들어:

cat_label = "SSO / 인증"
cat_key   = "sso"

이면:

SSO / 인증

이 출력됩니다.

반대로 cat_label이 없다면:

sso

가 출력됩니다.

⸻

17. relative_url Filter

다음 코드:

{{ post.url | relative_url }}

에서 relative_url도 Filter입니다.

현재 게시글의 URL을 Jekyll 사이트의 설정에 맞는 상대 URL 형태로 변환합니다.

일반적으로 Jekyll에서 링크를 만들 때 다음처럼 사용합니다.

<a href="{{ post.url | relative_url }}">

⸻

18. date Filter

다음 코드:

{{ post.date | date: "%Y-%m-%d" }}

는 날짜를 원하는 형식으로 변환합니다.

예를 들어 게시글 날짜가:

2026-10-01 08:30:00 +0900

이라면:

2026-10-01

형태로 표시할 수 있습니다.

⸻

19. 첫 번째 전체 코드 해석

다시 처음의 코드를 보겠습니다.

{% assign cat_label = site.data.category_labels[cat_key] %}
<h2 class="section-title">
  {{ cat_label | default: cat_key }}
</h2>
<ul class="post-list">
  {% for post in cat[1] %}
  <li>
    <a href="{{ post.url | relative_url }}" class="post-title">
      {{ post.title }}
    </a>
    <div class="post-date">
      {{ post.date | date: "%Y-%m-%d" }}
    </div>
  </li>
  {% endfor %}
</ul>

순서대로 해석하면:

① 카테고리 표시 이름 찾기

{% assign cat_label = site.data.category_labels[cat_key] %}

cat_key를 이용해 _data/category_labels.yml에서 표시 이름을 찾습니다.

⸻

② 카테고리 이름 출력

{{ cat_label | default: cat_key }}

표시 이름이 있으면 표시 이름을 출력하고,

없으면 cat_key를 출력합니다.

⸻

③ 카테고리의 게시글 반복

{% for post in cat[1] %}

현재 카테고리에 속한 게시글을 하나씩 처리합니다.

⸻

④ 게시글 제목 출력

{{ post.title }}

현재 게시글의 제목입니다.

⸻

⑤ 게시글 링크 생성

{{ post.url | relative_url }}

현재 게시글의 URL을 가져옵니다.

⸻

⑥ 게시글 날짜 출력

{{ post.date | date: "%Y-%m-%d" }}

게시글 날짜를 YYYY-MM-DD 형태로 표시합니다.

⸻

20. 두 번째 코드 해석

다음 코드:

{% for post in site.categories.sso %}
  <li>
    <a href="{{ post.url | relative_url }}" class="post-title">
      {{ post.title }}
    </a>
    <div class="post-date">
      {{ post.date | date: "%Y-%m-%d" }}
    </div>
  </li>
{% endfor %}

는 훨씬 단순합니다.

site
 ↓
categories
 ↓
sso
 ↓
게시글 목록
 ↓
post

즉:

SSO 카테고리의 모든 게시글을 하나씩 가져와서 제목, URL, 날짜를 출력한다.

는 뜻입니다.

⸻

21. Jekyll Liquid에서 자주 보는 이름 정리

Jekyll에서는 다음과 같은 이름들을 자주 볼 수 있습니다.

이름	성격	설명
site	Jekyll 객체	사이트 전체 정보
page	Jekyll 객체	현재 페이지 정보
site.posts	Jekyll 객체	전체 게시글
site.categories	Jekyll 객체	카테고리별 게시글
site.tags	Jekyll 객체	태그별 게시글
site.data	Jekyll 객체	_data 데이터
post	사용자 변수	반복 중인 게시글
cat	사용자 변수	반복 중인 카테고리
cat_key	사용자 변수	카테고리 key
cat_label	사용자 변수	카테고리 표시 이름

중요한 것은 post, cat, cat_key, cat_label은 예약어가 아니라 코드에서 만들어 사용하는 변수라는 점입니다.

⸻

22. Liquid의 주요 예약어

반면 다음과 같은 것은 Liquid에서 사용하는 문법입니다.

assign
for
endfor
if
elsif
else
endif
case
when
endcase
capture
include
unless

예:

{% assign name = "Dash" %}
{% if name %}
  Hello {{ name }}
{% endif %}

⸻

23. 핵심 구조 한 번에 보기

Jekyll Liquid를 이해할 때 다음 구조를 기억하면 좋습니다.

Jekyll
│
├── site
│   ├── posts
│   ├── categories
│   ├── tags
│   └── data
│       └── category_labels
│
├── page
│
└── Liquid에서 만든 변수
    ├── post
    ├── cat
    ├── cat_key
    └── cat_label

그리고 접근 방법은:

site.categories.sso
       │        │
       │        └── key
       └── Jekyll이 제공하는 데이터

또는:

site.data.category_labels[cat_key]
       │          │              │
       │          │              └── 변수값을 이용한 동적 key
       │          └── _data/category_labels.yml
       └── Jekyll data

⸻

24. 최종적으로 기억할 것

Jekyll Liquid를 처음 공부할 때는 다음 7가지만 확실히 이해하면 됩니다.

1. {{ ... }}
   → 값을 출력
2. {% ... %}
   → 명령 실행
3. site
   → Jekyll이 제공하는 사이트 객체
4. post / cat / cat_key
   → 코드에서 만들어 사용하는 변수
5. site.categories.sso
   → categories에서 sso라는 key에 접근
6. site.data.category_labels
   → _data/category_labels.yml에 접근
7. [변수]
   → 변수값을 이용해서 동적으로 key에 접근

특히 다음 두 문장을 구분해서 기억하면 됩니다.

site.categories.sso

sso라는 key를 직접 지정한다.

site.categories[cat_key]

cat_key 변수에 들어 있는 값을 key로 사용한다.

이 차이를 이해하면 Jekyll의 Liquid 코드를 읽는 것이 훨씬 쉬워집니다.