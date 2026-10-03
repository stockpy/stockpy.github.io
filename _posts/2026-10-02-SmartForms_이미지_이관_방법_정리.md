---
layout: post
title: SmartForms 이미지(그래픽) 이관 방법 — 개별/전체 이관 및 RSTXSCRP 한계
categories: [general]
---

# SmartForms 이미지(그래픽) 이관 방법 정리

SmartForms 이관 후 대상 시스템에서 이미지(로고 등)가 표시되지 않는 문제를 해결하기 위한 이미지 이관 방식을 정리한 문서입니다.

---

## 핵심 개념: SmartForms 이미지는 "Form Graphics"라는 별도 객체

SmartForms에 삽입한 이미지(로고, 아이콘 등)는 **Form Graphics**라는 독립 객체로 저장됩니다. SmartForms 본체(레이아웃/프로그램)와 **별도 객체**이므로 이관 방식이 다릅니다.

SmartForms 이관 요청서에만 본체가 포함되고 Form Graphics가 빠지면, 대상 시스템에서 이미지가 표시되지 않거나 폼 생성 시 `SSFCOMPOSER005` 오류가 발생할 수 있습니다.

### 관련 테이블: STXBITMAPS + BDS

Form Graphics는 두 단계로 저장됩니다.

| 테이블 | 역할 | 주요 필드 |
|---|---|---|
| **STXBITMAPS** | 그래픽 **헤더 정보(메타데이터)** — SE78에서 관리하는 속성 | `TDNAME`(그래픽명), `TDOBJECT`='GRAPHICS', `TDID`='BMAP', `TDBTYPE`(BCOL/BMON 등), `DOCID`(BDS 참조) |
| **BDS 테이블** (BDSCONT3, BDSX_CON04 등) | 그래픽의 **실제 바이너리 데이터** | `DOCID`로 STXBITMAPS와 연결 |

- **STXBITMAPS**: 그래픽의 헤더(이름, 해상도, 비트 유형 등)를 저장. `TDOBJECT`='GRAPHICS', `TDID`='BMAP' 조건으로 조회. `DOCID` 필드로 BDS 테이블의 실제 데이터 위치를 가리킴.
- **BDS(Binary Data Store)**: 실제 이미지 바이너리를 저장. `STXBITMAPS.DOCID`로 연결.
- **TDBTYPE**: 비트맵 유형 — `BCOL`(컬러), `BMON`(흑백) 등.

> 이관 시 **STXBITMAPS(헤더)와 BDS(바이너리 데이터)가 함께** 대상 시스템으로 전송되어야 이미지가 정상 표시됩니다. 한쪽만 이관되면 "헤더는 있지만 데이터가 없음" 또는 그 반대 상황이 되어 `SSFCOMPOSER210`(그래픽 접근 오류) 등이 발생할 수 있습니다. (Note 2550288)

---

## 1. 개별 이관 — SE78

특정 이미지 하나를 이관 요청서에 포함시키는 방법입니다.

1. 트랜잭션 **SE78** (Administering Form Graphics) 실행
2. 트리에서 이관할 그래픽 선택
3. **Graphic → Transport** 선택
4. 워크벤치 요청서(Workbench Request) 선택 또는 새로 생성
5. **Continue** 선택

→ 해당 그래픽이 요청서에 포함되며, Transport Organizer에서 릴리즈 시 대상 시스템으로 이관됩니다.

---

## 2. 전체 이관 — 하나의 요청서에 여러 그래픽 묶기

**SE78에는 "전체(일괄) 이관" 버튼이 없습니다.** 공식 문서의 "Transporting Graphics"도 단일 그래픽 선택 → Graphic Transport 방식만 설명합니다.

따라서 "전체 이관"은 **여러 그래픽을 하나의 이관 요청서에 함께 포함**하는 방식으로 구현합니다.

### 방법 1: 이관 요청서에 여러 그래픽 반복 등록 (권장)

1. **SE78** 실행
2. 트리에서 **이관할 그래픽을 하나씩 선택** → **Graphic → Transport**
3. **모든 그래픽에 동일한 워크벤치 요청서** 선택 (첫 번째에서 생성/선택, 나머지도 동일 요청서)
4. 대상 그래픽 전체를 동일한 요청서에 등록 완료
5. **SE09**에서 해당 요청서 **릴리즈** → 대상 시스템으로 일괄 이관

### 방법 2: SmartForms 수정 시 함께 등록 (최초 개발 시)

SmartForms를 개발하면서 이미지를 추가할 때, **이미지와 SmartForms 본체를 같은 워크벤치 요청서에 등록**해 두면, SmartForms 이관 요청서에 그래픽이 자동으로 포함됩니다.

- 이 방식이 가장 깔끔하며, SmartForms와 이미지가 항상 함께 이관됩니다.

### 방법 3: SE03에서 요청서에 직접 추가

**SE03 (Transport Organizer)**에서 요청서에 그래픽 객체를 직접 추가하는 방법도 가능합니다.

- SE03 → 요청서 선택 → **Objects → Add** → PgmID: `R3TR`, Object: `SSF`, Object name: 그래픽 이름

> 단, Form Graphics의 정확한 객체 유형 코드는 시스템 릴리스에 따라 다를 수 있으므로, **SE78 Graphic Transport(방법 1)를 사용하는 것이 가장 안전**합니다.

---

## 3. RSTXSCRP로 SmartForms 이미지 이관이 가능한가? — 불가

**RSTXSCRP는 SAPscript 전용 리포트**입니다. 대상 객체는 SAPscript의 문서(text) / 스타일(style) / 폼(form) / 그래픽(graphic)이며, **SmartForms는 지원 대상이 아닙니다.**

- SAPscript 그래픽: 표준 텍스트에 포함, RSTXSCRP/RSTXLDMC 대상
- SmartForms Form Graphics: `STXBITMAPS`(헤더) + BDS(바이너리 데이터)에 별도 저장, **SE78** 대상

RSTXSCRP의 GRAPHICS 노드에서 import하는 그래픽은 **SAPscript 표준 텍스트에 포함된 그래픽**이며, SmartForms Form Graphics(STXBITMAPS/BDS)와는 무관합니다.

### 참고: RSTXSCRP 사용법 (SAPscript 대상)

KBA 2172623 기준:

**EXPORT (내보내기)**

1. SE38에서 리포트 **RSTXSCRP** 실행
2. 선택 조건: Object name = 대상 SAPscript 폼 이름, Mode = `EXPORT`, Binary File Format 체크
3. 실행 → 파일 저장 경로 지정
4. Export Log 확인

**IMPORT (가져오기)**

1. SE38에서 RSTXSCRP 실행
2. 선택 조건: Object name = 대상 SAPscript 폼 이름, Mode = `IMPORT`
3. **Binary File Format**: export 시 체크했다면 import 시에도 **반드시 체크** (KBA 2493689: 체크 불일치 시 `Invalid start marker: RSTX@ instead of SFORM` 오류)
4. 실행 → 팝업에서 export한 파일 선택
5. Import Log 확인

**주의사항**

- 디바이스 타입(device type) export/import에는 부적합 — `RSPODOWNLOAD`/`RSPOUPLOAD` 사용 (Note 1450140)
- 언어 벡터: 소스 언어가 대상 시스템에 설치되어 있지 않으면 import/export 불가 (Note 2736859)
- non-Unicode ↔ Unicode 간 이관 시 텍스트 깨짐 주의 (Note 898074, 1936593)
- import는 기본적으로 client 000로 진행

---

## 4. 관련 리포트 요약

| 프로그램 | 대상 | 용도 |
|---|---|---|
| **RSTXLDMC** | SAPscript | 그래픽(TIFF/BMP/PS)을 표준 텍스트로 업로드 |
| **RSTXSCRP** | SAPscript | 폼/스타일/디바이스 타입의 파일 기반 export/import |
| **RSTXGALL** | Smart Forms | 이관 후 Smart Forms 함수 모듈 일괄 생성 (Note 630105) |

### RSTXGALL (이관 후 Smart Forms 활성화)

이관 후 대상 시스템에서 Smart Forms는 **처음 호출될 때까지 재생성되지 않음**(표준 시스템 동작). RSTXGALL 실행으로 일괄 생성:

```abap
report rstxgall.

data: form  type tdsfname,
      forms type table of tdsfname.

select formname from stxfadm into table forms
  where formtype = space.

loop at forms into form.
  call function 'SSF_FUNCTION_MODULE_NAME'
    exporting
      formname = form
    exceptions
      others   = 1.
endloop.
```

---

## 5. 요약

| 목적 | 도구 |
|---|---|
| SmartForms image(Form Graphics) **개별 이관** | SE78 → Graphic → Transport |
| SmartForms image(Form Graphics) **전체 이관** | SE78 → 여러 그래픽을 **동일 요청서에 반복 등록** → SE09 릴리즈 |
| 최초 개발 시 | SmartForms 수정 시 이미지와 본체를 같은 요청서에 등록 |
| SAPscript 폼/스타일/텍스트/그래픽 이관 | RSTXSCRP (파일 기반) 또는 RSTXR3TR (R/3 트랜스포트 기반) |
| 이관 후 Smart Forms 활성화 | RSTXGALL 실행 (Note 630105) |

**핵심**: SE78 자체에는 일괄 선택 기능이 없으므로, 전체 이관은 **여러 그래픽을 하나의 요청서에 묶는 것**으로 달성합니다. SmartForms image 이관에는 RSTXSCRP를 사용할 수 없습니다.

---

## 근거

- SAP Help Portal "Transporting Graphics" (ABAP platform, Smart Forms) — 단일 그래픽 Graphic Transport 절차
- SAP Help Portal "Transporting Documents, Styles, and Forms" (BC Style and Form Maintenance) — RSTXSCRP는 SAPscript 대상
- KBA 2172623 — How to IMPORT/EXPORT SAPScript forms by using Report RSTXSCRP
- KBA 2493689 — Binary file format 체크 불일치 오류
- KBA 2777644 — SSFCOMPOSER005 - Unable to generate form
- Note 630105 — Generating Smart Forms after transport (RSTXGALL)
- Note 1450140 — RSPOUPLOAD/RSPODOWNLOAD (디바이스 타입은 RSTXSCRP 부적합)
- Note 2736859 — RSTXSCRP: Import of forms if language is not installed
- Note 825230 — SE78 graphic change, STXBITMAPS rollback
- Note 1333355 — Graphic not displayed in SAPscript or Smart Forms (STXBITMAPS/BDS)
- Note 906453 — Performance problems during access to graphics in BDS (STXBITMAPS)
- Note 2550288 — Error when accessing graphic (BDS); SSFCOMPOSER210 (STXBITMAPS 헤더 + BDS 바이너리 저장 구조)
