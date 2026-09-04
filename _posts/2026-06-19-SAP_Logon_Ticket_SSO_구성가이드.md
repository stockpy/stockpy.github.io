---
layout: post
title: SAP Logon Ticket 기반 SAPGUI SSO 구성 가이드
categories: sso-auth
---

# SAP Logon Ticket 기반 SAPGUI SSO 구성 가이드

**참조 소스**
- SAP Help Portal: "Configuring SAP Systems to Accept and Verify Logon Tickets"
- SAP Help Portal: "Using Transaction STRUSTSSO2 in SAP System >= 4.6C"
- SAP Help Portal: "Configuring the AS ABAP for Issuing Tickets for Logon"

---

## 1. 핵심 개념

Logon Ticket은 SAP 시스템(또는 Portal)이 발급하는 디지털 서명된 인증 토큰으로, 브라우저 쿠키(`MYSAPSSO2`)로 전달됩니다. SAPGUI가 이 쿠키를 사용하여 SAP 시스템에 SSO로 로그온할 수 있습니다.

---

## 2. 구성 단계

### 2-1. 프로파일 파라미터 설정 (RZ10)

모든 관련 SAP 시스템의 인스턴스 프로파일에서 설정:

| 파라미터 | 값 | 의미 |
|---|---|---|
| `login/accept_sso2_ticket` | `1` | SSO 티켓 수락 활성화 (모든 대상 시스템) |
| `login/create_sso2_ticket` | `0` | 티켓 발급 안 함 (기본값) |
| `login/create_sso2_ticket` | `1` | Assertion 티켓만 발급 |
| `login/create_sso2_ticket` | `2` | Logon 티켓 + Assertion 티켓 모두 발급 |

- **티켓 발급 시스템** (Portal 또는 Ticket Server 역할):
  - `login/create_sso2_ticket = 2`
- **티켓 수락 시스템** (대상 SAP 시스템):
  - `login/accept_sso2_ticket = 1`
  - `login/create_sso2_ticket = 0`

### 2-2. 인증서 교환 및 ACL 구성 (STRUSTSSO2)

트랜잭션 `STRUSTSSO2` (SAP >= 4.6C 기준)를 사용:

**대상 SAP 시스템에서:**
1. STRUSTSSO2 실행
2. 티켓 발급 시스템(Portal 등)의 공개 키 인증서를 대상 시스템의 인증서 목록에 가져옴
3. 티켓 발급 시스템을 대상 시스템의 ACL(Access Control List)에 추가

**절차:**
- Portal 서버에서 `verify.der` 파일 다운로드 (NWA → Keystore Administration)
- 대상 SAP 시스템에서 STRUSTSSO2 → "Binary" 탭 → Portal 인증서 가져오기
- Portal 서버를 ACL에 추가 (호스트명, 시스템명 등 입력)

### 2-3. SAP Security Library (SAPSECULIB)

- 모든 애플리케이션 서버에 최신 SAPSECULIB 설치
- SAP Service Marketplace → Download → Support Packages and Patches → SAP Technology Components → SAPSECULIB
- 레거시 시스템(4.0/4.5)의 경우 프로파일 파라미터 `SAPSECULIB`로 라이브러리 경로 설정

---

## 3. 주요 트랜잭션 정리

| 트랜잭션 | 용도 |
|---|---|
| `STRUSTSSO2` | Portal 인증서 가져오기 + ACL 구성 (Logon Ticket용) |
| `STRUST` | 일반 Trust Manager (SSL/SNC 인증서 관리) |
| `RZ10` | 프로파일 파라미터 설정 |
| `ST01` | 로그인 추적 (문제 해결용, 설정 아님) |
| `SM50` | 런타임 워크프로세스 추적 (Ticket 인증 추적 가능) |

---

## 4. SAPGUI에서 Logon Ticket SSO 작동 방식

1. 사용자가 티켓 발급 시스템(Portal 등)에 로그온
2. 시스템이 `MYSAPSSO2` 쿠키로 Logon Ticket 발급
3. SAPGUI가 브라우저 쿠키에서 Ticket 읽음
4. SAPGUI가 Ticket을 대상 SAP 시스템에 전송
5. 대상 시스템이 Portal 인증서로 Ticket 서명 검증 후 로그온

---

## 5. 요약

| 항목 | 내용 |
|---|---|
| 설정 트랜잭션 | `STRUSTSSO2` (인증서 + ACL), `RZ10` (파라미터) |
| 추적 트랜잭션 | `ST01` (로그인 추적), `SM50` (워크프로세스 추적) |
| 핵심 파라미터 | `login/accept_sso2_ticket`, `login/create_sso2_ticket` |
| 쿠키명 | `MYSAPSSO2` |
