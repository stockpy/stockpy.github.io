---
layout: post
title: SAPGUI SSO + MFA 방안 (SingleID 환경)
---

# SAPGUI SSO + MFA 방안 (SingleID 환경)

> SAP Secure Login Service(SLS) + SingleID Corporate IdP 환경에서
> SAPGUI SSO에 MFA를 추가하는 방안입니다.
>
> **작성일**: 2026-08-27
> **참고 문서**: SAPGUI_SSO_SLS_SingleID_가이드.md, Corporate_IdP_Guide_3.md

---

## 목차

1. [현재 인증 흐름에서 MFA 적용 위치](#1-현재-인증-흐름에서-mfa-적용-위치)
2. [SingleID MFA 인증 방식](#2-singleid-mfa-인증-방식)
3. [SingleID MFA 핵심 기능](#3-singleid-mfa-핵심-기능)
4. [MFA 적용 시 상세 인증 흐름](#4-mfa-적용-시-상세-인증-흐름)
5. [MFA 인증 화면 — 별도 개발 필요 여부](#5-mfa-인증-화면--별도-개발-필요-여부)
6. [SingleID Admin Portal MFA 설정](#6-singleid-admin-portal-mfa-설정)
7. [인증서 유효기간과 MFA 빈도](#7-인증서-유효기간과-mfa-빈도)
8. [SingleID SSO 세션과 MFA 재발생](#8-singleid-sso-세션과-mfa-재발생)
9. [도입 단계](#9-도입-단계)
10. [SingleID 운영팀 요청 사항](#10-singleid-운영팀-요청-사항)

---

## 1. 현재 인증 흐름에서 MFA 적용 위치

```
1. User → SAPGUI 실행
2. SAPGUI → SAP Backend 연결 요청 (SNC 인증 필요)
3. SLC → SLS (BTP)에 X.509 인증서 요청
4. SLS → SCI/IAS로 인증 위임
5. IAS → SingleID로 인증 리다이렉트 (SAML 2.0)
6. SingleID → User 인증 (MFA 등)   ← MFA enforcement 지점
7. SingleID → SAML Assertion → IAS
8. IAS → SLS로 인증 결과 전달
9. SLS → X.509 인증서 발급 (기본 12시간)
10. SLC → SAPGUI에 인증서 제공
11. SAPGUI → SAP Backend SNC/X.509 인증 → 로그인 성공
```

**핵심: MFA는 Step 6에서 SingleID 레이어에서 enforcement됩니다.**
SLS/IAS/SLC는 MFA를 인지하지도, 처리하지도 않습니다.

---

## 2. SingleID MFA 인증 방식

| 인증 방식 | 설명 | 사용 시나리오 |
|---|---|---|
| **SMS OTP** | 휴대폰으로 일회용 번호 발송 | 기본 MFA |
| **이메일 OTP** | 이메일로 일회용 번호 발송 | 백업 인증 수단 |
| **mOTP (Mobile OTP)** | SingleID 앱에서 생성하는 일회용 번호 | 오프라인 환경 |
| **TOTP (Time-based OTP)** | RFC 6238 기반 시간 동기화 OTP | 외부 앱 연동 |
| **PIN** | 사용자가 설정한 고정 PIN 코드 | 간단한 2차 인증 |
| **생체 인증** | 지문, 얼굴 인식 (모바일) | 모바일 UX 최우선 |
| **Knox Messenger** | 삼성 Knox 기반 푸시 알림 | 삼성 기기 대상 |
| **Passkey** | FIDO2 기반 패스워드리스 | 패스워드리스 인증 |

---

## 3. SingleID MFA 핵심 기능

### 3-1. MFA 모듈

| 기능 | 설명 |
|---|---|
| **PC/모바일 MFA** | 웹/모바일 환경 모두 MFA 챌린지 지원 |
| **기존 1차 인증 연동** | 기존 인증 환경(AD/LDAP)을 1차 인증으로 유지, SingleID가 2차 MFA만 담당 |
| **Private CA 인증서 인증** | 사설 인증서 발급/관리 (별도 Use Case) |

### 3-2. ADM (Anomaly Detection Management) — 조건부 MFA

| 탐지 요소 | 설명 |
|---|---|
| **사용자 유형** | 임직원/협력사/파트너별 정책 적용 |
| **로그인 IP** | 신뢰 IP 범위 외부 접근 시 MFA 강제 |
| **디바이스 정보** | 신규/신뢰하지 않는 디바이스 접근 시 MFA 강제 |
| **접속 시간** | 비업무 시간대 접근 시 MFA 강제 |

---

## 4. MFA 적용 시 상세 인증 흐름

```
1. User → SAPGUI 실행
2. SAPGUI → SAP Backend 연결 요청 (SNC 인증 필요)
3. SLC → SLS (BTP)에 X.509 인증서 요청
4. SLS → SCI/IAS로 인증 위임
5. IAS → SingleID로 인증 리다이렉트 (SAML 2.0)
        ↓
   ┌─────────────────────────────────────┐
   │        SingleID 인증 흐름           │
   │                                     │
   │  6a. SingleID → 사용자 ID/PW 인증   │
   │  6b. SingleID → MFA 정책 평가       │  ← MFA 결정 지점
   │       · 인증 정책 확인              │
   │       · ADM 상황 분석 (IP/기기/시간) │
   │  6c. (MFA 필요 시) MFA 챌린지       │
   │       · SMS/mOTP/TOTP/생체/PIN 등  │
   │  6d. MFA 통과 확인                  │
   └─────────────────────────────────────┘
        ↓
7. SingleID → SAML Assertion → IAS
8. IAS → SLS로 인증 결과 전달
9. SLS → X.509 인증서 발급 (12시간 유효)
10. SLC → SAPGUI에 인증서 제공
11. SAPGUI → SAP Backend SNC/X.509 인증 → 로그인 성공
```

---

## 5. MFA 인증 화면 — 별도 개발 필요 여부

**결론: 별도 개발이 불필요합니다.**

SingleID에서 MFA 정책을 활성화하면, SAPGUI 인증 시 SingleID의 표준 MFA 인증 화면이
SLC 내장 browser를 통해 자동으로 표시됩니다.

### 자동 연결 동작 흐름

```
SAPGUI 실행
  ↓
SLC가 X.509 인증서 필요 감지 (또는 인증서 만료)
  ↓
SLC 내장 hardened browser 자동 팝업
  ↓
Browser가 SingleID 로그인 페이지로 자동 리다이렉트
  ↓
SingleID 표준 로그인 화면 표시 (ID/PW 입력)
  ↓
SingleID가 MFA 정책 평가 → MFA 필요 시
  ↓
SingleID 표준 MFA 챌린지 화면 표시 (SMS OTP 입력 등)
  ↓
MFA 통과 → SAML Assertion → IAS → SLS → X.509 발급
  ↓
SLC가 인증서를 SAPGUI에 제공 → SAPGUI 로그인 성공
```

### 화면 흐름 (사용자 관점)

```
┌─────────────────────────────────────┐
│   SLC 내장 Browser (자동 팝업)      │
│                                     │
│   ┌─────────────────────────────┐   │
│   │     SingleID 로그인         │   │
│   │                             │   │
│   │  ID: [____________]         │   │
│   │  PW: [____________]         │   │
│   │  [로그인]                   │   │
│   └─────────────────────────────┘   │
│           ↓ (ID/PW 인증 후)          │
│   ┌─────────────────────────────┐   │
│   │     MFA 인증                │   │
│   │                             │   │
│   │  휴대폰으로 발송된          │   │
│   │  인증번호를 입력하세요      │   │
│   │                             │   │
│   │  [ 1 2 3 4 5 6 ]           │   │
│   │  [확인]                     │   │
│   └─────────────────────────────┘   │
│           ↓ (MFA 통과)              │
│   ┌─────────────────────────────┐   │
│   │     인증 완료               │   │
│   │     SAPGUI로 돌아가고 있습니다 │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### 별도 개발이 불필요한 이유

1. **SLC 내장 browser** — Secure Login Client 3.0 SP2 Patch 16+에 hardened browser가
   내장되어 있어 SingleID 웹 페이지를 직접 표시하며,
   사용자는 SAPGUI 외부에서 별도 브라우저 작업을 할 필요가 없음
2. **SingleID 표준 UI** — SingleID가 제공하는 표준 로그인/MFA 화면이
   SAML 2.0 프로토콜 흐름에 따라 자동으로 표시됨
3. **표준 프로토콜 연동** — 전체 흐름이 표준 프로토콜로 구성됨:
   - SAML 2.0: IAS ↔ SingleID 간 인증 위임/응답
   - X.509: SLS → SLC 인증서 발급
   - SNC: SAPGUI ↔ SAP Backend 간 인증
   커스텀 개발이 필요 없는 구조
4. **MFA는 IdP 레이어 기능** — MFA enforcement는 SingleID(Corporate IdP)에서 처리하며,
   SLS/IAS/SLC/SAPGUI는 MFA를 인지하지도, 처리하지도 않음.
   SingleID 운영팀에서 MFA 정책만 활성화하면 끝남

### 해야 할 일

- **SingleID 운영팀에 MFA 정책 활성화 요청** (대상 서비스: IAS ACS URL)
- SAPGUI 측, SLC 측, SLS 측, IAS 측 — **코드 변경 또는 개발 불필요**

---

## 6. SingleID Admin Portal MFA 설정

### Step 1: 서비스(IAS ACS URL)에 MFA 정책 할당

| 설정 항목 | 내용 |
|---|---|
| **대상 서비스** | IAS ACS URL (`https://<tenant>.accounts.ondemand.com/saml2/sp/acs/...`) |
| **MFA 정책** | 해당 서비스에 접근하는 모든 인증에 MFA 강제 |
| **MFA 방식** | SMS, mOTP, TOTP, 생체 등 조직 정책 기준 |

### Step 2: MFA 정책 유형 선택

| 정책 유형 | 설명 | SAPGUI SSO 적합도 |
|---|---|---|
| **무조건 MFA** | 모든 인증에 MFA 필수 | ✅ 기본 적용 권장 |
| **조건부 MFA** | ADM 규칙(IP/기기/시간)에 따라 MFA 결정 | ✅ 운영 안정화 후 적용 |
| **신뢰 디바이스 제외** | 등록한 기기에서는 MFA 생략 | ⚠️ 보안 트레이드오프 |

### Step 3: (선택) ADM — 조건부 MFA 규칙 정의

| 규칙 | 예시 |
|---|---|
| **신뢰 IP 범위** | 사내 IP 대역에서는 MFA 생략 |
| **신뢰 디바이스** | 등록한 PC/모바일에서는 MFA 생략 |
| **비업무 시간** | 22:00~08:00 접근 시 MFA 강제 |
| **사용자 유형** | 관리자 계정은 항상 MFA |

---

## 7. 인증서 유효기간과 MFA 빈도

| 인증서 유효기간 | MFA 발생 빈도 | UX | 보안성 |
|---|---|---|---|
| **12시간 (기본)** | 하루 1~2회 | 좋음 | 충분 |
| **8시간** | 하루 2~3회 | 보통 | 높음 |
| **4시간** | 하루 4~6회 | 낮음 | 매우 높음 |
| **24시간** | 하루 1회 | 매우 좋음 | 보통 |

**권장: 기본 12시간 유지 → 조건부 MFA로 보안성 보강**

---

## 8. SingleID SSO 세션과 MFA 재발생

| 시나리오 | MFA 재발생 여부 |
|---|---|
| SingleID에서 이미 로그인 + SSO 세션 활성 | **아니오** — SSO 세션으로 통과 |
| SingleID SSO 세션 만료 | **예** — 재인증 + MFA |
| IAS에서 `ForceAuthn=true` 설정 | **예** — 매 접속마다 재인증 + MFA |
| SLC 인증서 만료 후 재발급 | **SingleID 세션 상태에 따라 다름** |

**SingleID 운영팀에 확인 필요:**
1. SingleID SSO 세션 유효기간
2. SAPGUI SSO 대상 서비스(IAS ACS)에 MFA 정책 적용 여부
3. `ForceAuthn` 플래그 영향

---

## 9. 도입 단계

| 단계 | 수행 주체 | 작업 |
|---|---|---|
| **1. 현황 확인** | SingleID 운영팀 | MFA 정책 현황, 지원 인증 방식, SSO 세션 설정 |
| **2. 정책 정의** | 보안팀 + SingleID 운영팀 | MFA 정책(무조건/조건부), MFA 방식 결정 |
| **3. 서비스 등록 확인** | SingleID 운영팀 | IAS ACS URL에 MFA 정책 적용 확인 |
| **4. 테스트 그룹 적용** | SingleID 운영팀 | 소수 그룹 MFA 정책 활성화 |
| **5. E2E 테스트** | SAP팀 + 테스트 그룹 | SAPGUI → SLC → SingleID MFA → X.509 → SAP 로그인 |
| **6. 인증서 유효기간 조정** | SAP팀 | SLS Web UI에서 유효기간 정책 결정 |
| **7. 전체 롤아웃** | SingleID 운영팀 | 전체 대상 그룹 MFA 정책 적용 |
| **8. (선택) ADM 조건부 MFA** | SingleID 운영팀 | IP/기기/시간 기반 조건부 MFA 추가 |

---

## 10. SingleID 운영팀 요청 사항

1. **MFA 정책 적용 범위** — IAS ACS URL 등록된 서비스에 MFA 정책 적용 방법
2. **MFA 인증 방식 선택** — 조직에서 사용할 MFA 방식(SMS/mOTP/TOTP/생체)
3. **SSO 세션 정책** — SingleID SSO 세션 유효기간 및 MFA 재발생 조건
4. **ADM 조건부 MFA** — IP/기기/시간 기반 조건부 MFA 설정 방법
5. **ForceAuthn 영향** — IAS에서 `ForceAuthn=true` 사용 시 MFA 재발생 여부
6. **모니터링/로깅** — MFA 인증 로그 확인 방법 (보안 감사용)

---

> **출처**: SingleID 공식 문서, SAP Community Blog, SAP Help Portal, Samsung SDS
> **작성일**: 2026-08-27
