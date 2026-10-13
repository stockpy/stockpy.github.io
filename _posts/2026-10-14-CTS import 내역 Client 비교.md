---
layout: post
title: "300번 및 500번 클라이언트별 TR Import 내역 추출 및 DB-OS 교차 검증 가이드"
date: 2026-10-14 08:00:00 +0900
author: dash
categories: [SAP, Basis]
tags: [SAP, Basis, STMS, Transport Request, SQL, Linux, Shell, dash]
---

# 300번 및 500번 클라이언트별 TR Import 내역 추출 및 DB-OS 교차 검증 가이드

**작성자 (Author):** dash  
**작성일자 (Date):** 2026년 10월 14일  

---

## 1. 개요

SAP 시스템 운영 및 감사 대응 시, 특정 Target Client(예: 300번, 500번)로 이송(Import) 완료된 Transport Request(TR) 리스트를 정밀하게 추출해야 하는 경우가 있습니다. 

본 가이드는 **1) DB SQL 직접 조회** 방식과 **2) OS 레벨 `tp` 로그 파싱** 방식을 활용해 클라이언트별 TR 목록을 추출하고, 두 결과를 `diff` 명령어로 교차 검증하는 전체 표준 절차를 다룹니다.

---

## 2. DB SQL 쿼리를 활용한 TR 내역 추출

SAP 헤더 테이블(`E070`)과 클라이언트 속성 매핑 테이블(`E070A`), 내역 테이블(`E077T`)을 조인하여 Target Client별로 Import가 완료된 TR 리스트를 추출합니다.

```sql
SELECT 
    A.TRKORR          AS "TR_NUMBER",
    H.AS4USER         AS "OWNER",
    H.AS4DATE         AS "IMPORT_DATE",
    H.AS4TIME         AS "IMPORT_TIME",
    A.REFERENCE       AS "TARGET_CLIENT",
    T.AS4TEXT         AS "DESCRIPTION"
FROM E070A A
JOIN E070 H 
  ON A.TRKORR = H.TRKORR
LEFT JOIN E077T T 
  ON A.TRKORR = T.TRKORR 
 AND T.LANGU = '3' -- 한국어 주석 ('3'), 영문 필요 시 'E'
WHERE A.ATTRIBUTE = 'CLIENT'     -- 클라이언트 지정 속성
  AND A.REFERENCE IN ('300', '500') -- 대상 Target Client
  AND H.TRSTATUS = 'R'            -- Released / Imported 상태
ORDER BY A.REFERENCE, H.AS4DATE DESC, H.AS4TIME DESC;
```

> **Note:** `E070A-REFERENCE` 필드에 Target Client 번호가 바인딩되어 있으므로, 쿼리 실행 후 300번과 500번 결과 집합을 각각 추출하여 별도 텍스트 파일로 저장합니다.

---

## 3. OS Shell 명령어를 활용한 TR 내역 추출 (`cat`, `grep`, `awk`)

SAP 전송 디렉토리(`/usr/sap/trans/log`)에 쌓이는 Import 시스템 로그 파일 및 ULOG를 파싱하여 이력 데이터를 추출합니다.

### ① `cat` & `grep`을 통한 기본 로그 추출
로그 파일 내에서 Target Client 매핑 문구 및 Import 결과 라인을 필터링합니다.

```bash
cd /usr/sap/trans/log

# 300번 클라이언트 Import 내역 추출
cat *I*.<SID> | grep -E "import.*client 300|u300" -B 1 -A 2

# 500번 클라이언트 Import 내역 추출
cat *I*.<SID> | grep -E "import.*client 500|u500" -B 1 -A 2
```

### ② 비교 검증용 라인 정제 출력 (`awk` 조합)
DB 결과값과의 1:1 비교를 위해 TR 번호 및 주요 매개변수만 파싱하여 저장합니다.

```bash
cd /usr/sap/trans/log

# [300번 클라이언트] TR 번호 및 Return Code 추출
cat *I*.<SID> | grep -i "client 300" | awk '{print $1, $2, $3, $NF}' > os_300.txt

# [500번 클라이언트] TR 번호 및 Return Code 추출
cat *I*.<SID> | grep -i "client 500" | awk '{print $1, $2, $3, $NF}' > os_500.txt
```

### ③ ULOG (User Log) 기반 `tp import` 구문 추적
`tp` 명령어가 직접 로깅되는 ULOG 파일에서 특정 클라이언트로 전송된 수동/자동 이송 내역을 추출합니다.

```bash
# ULOG 파일에서 Target Client별 tp import 명령어 조준 추출
grep -E "tp import.* 300" ULOG*
grep -E "tp import.* 500" ULOG*
```

---

## 4. DB vs OS 결과 교차 검증 (Diff)

추출된 데이터의 누락이나 부정합 여부를 검증하기 위해 DB SQL 결과(`db_300.txt`)와 OS 로그 파싱 결과(`os_300.txt`)에서 TR 번호만 정렬하여 추출한 뒤 `diff` 구문으로 대조합니다.

```bash
# 두 추출 결과의 정합성 비교 (차이점이 없을 경우 출력 없음)
diff -u db_300.txt os_300.txt
diff -u db_500.txt os_500.txt
```

---

## 5. 최종 리포트 양식 예시

교차 검증이 완료된 최종 내역은 아래 포맷으로 가공하여 감사 및 관리 문서로 활용합니다.

| Target Client | Transport Request | Description | Owner | Import Date/Time | Return Code |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **300** | `PRDK900123` | [FI] 전표 처리 BAPI 연동 수정 | USER01 | 2026-10-10 14:20:11 | **RC=0** |
| **300** | `PRDK900125` | [SD] Pricing Procedure 커스텀 | USER02 | 2026-10-12 09:15:00 | **RC=4** |
| **500** | `PRDK900110` | [BC] G/W Security 매개변수 적용 | dash | 2026-10-08 18:00:30 | **RC=0** |