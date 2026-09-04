---
layout: post
title: SAPGUI SSO + SLS 연동 가이드 (Corporate IdP: SingleID)
categories: sso-auth
---

# SAPGUI SSO + SLS 연동 가이드 (Corporate IdP: SingleID)

> SAP Secure Login Service(SLS)를 활용한 SAPGUI SSO 구성 가이드입니다.
> Corporate IdP로 SingleID를 사용하며, SAP Cloud Identity(SCI)/IAS를 경유합니다.

---

## 목차

1. [Cloud Connector 필요 여부](#1-cloud-connector-필요-여부)
2. [SLS 기반 SAPGUI SSO 아키텍처](#2-sls-기반-sapgui-ss-아키텍처)
3. [인증 흐름](#3-인증-흐름)
4. [Prerequisites](#4-prerequisites)
5. [설정 단계](#5-설정-단계)
6. [방화벽 설정](#6-방화벽-설정)
7. [Cloud Connector가 필요한 다른 시나리오](#7-cloud-connector가-필요한-다른-시나리오)
8. [참고 자료](#8-참고-자료)

---

## 1. Cloud Connector 필요 여부

**결론: Cloud Connector는 필요하지 않습니다.**

SAP Community 공식 답변:

> *"The cloud connector is not required in this scenario. The Secure Login Service provisions a short-lived X.509 certificate to the Secure Login Client."*

### 왜 필요 없는가?

- **인증서 발급**: End User Desktop → SLS (BTP 클라우드) → SCI → SingleID (전부 인터넷 경로)
- **SAP Backend 연결**: SAPGUI → SAP System은 **SNC/X.509 로컬 인증**만 수행. SAP System에서 클라우드로의 아웃바운드 연결 불필요
- **Cloud Connector의 역할**: 온프레미스 리소스를 BTP/클라우드에 노출하는 것. SLS 시나리오에서는 이 흐름이 **필요 없음**

---

## 2. SLS 기반 SAPGUI SSO 아키텍처

### 구성 요소

| 구성 요소 | 위치 | 역할 |
|---|---|---|
| **Secure Login Client (SLC)** | End User Desktop | X.509 인증서 요청/보관, SAPGUI에 제공 |
| **SAP Secure Login Service (SLS)** | SAP BTP (클라우드) | 단기간 X.509 인증서 발급 |
| **SAP Cloud Identity (SCI)** | SAP BTP (클라우드) | IAS + IdDS + IPS 포함. 인증 브로커 |
| **SAP Identity Authentication Service (IAS)** | SAP BTP (클라우드) | 인증 정책 강제, Corporate IdP로 인증 위임 |
| **SingleID** | Corporate IdP | 실제 사용자 인증 |
| **SAP Backend (AS ABAP)** | 온프레미스 / 클라우드 | SNC/X.509 인증 검증 |

### 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                     End User Desktop                        │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │ Secure Login │         │   SAPGUI     │                  │
│  │   Client     │────────▶│              │                  │
│  │   (SLC)      │         │              │                  │
│  └──────┬───────┘         └──────┬───────┘                  │
│         │ X.509 Cert             │ SNC/X.509 Auth            │
└─────────┼────────────────────────┼──────────────────────────┘
          │                        │
          │  인터넷                 │  직접 연결 (SNC)
          ▼                        ▼
┌─────────────────┐      ┌──────────────────┐
│   SAP BTP       │      │  SAP Backend     │
│  ┌───────────┐  │      │  (AS ABAP)       │
│  │ SLS       │  │      │                  │
│  └────┬──────┘  │      │  STRUST          │
│       │         │      │  SNCCONFIG       │
│  ┌────▼──────┐  │      └──────────────────┘
│  │ SCI / IAS │  │
│  └────┬──────┘  │
│       │         │
│  ┌────▼──────┐  │
│  │ SingleID  │  │
│  │(Corporate │  │
│  │   IdP)    │  │
│  └───────────┘  │
└─────────────────┘
```

> **핵심**: SAP Backend는 클라우드로의 연결이 필요 없습니다.
> 인증서 발급 시에만 End User Desktop → 클라우드 경로가 사용됩니다.

---

## 3. 인증 흐름

### 전체 인증 시퀀스

```
1. User → SAPGUI 실행
   ↓
2. SAPGUI → SAP Backend 연결 요청 (SNC 인증 필요)
   ↓
3. Secure Login Client → SLS (BTP) 에 X.509 인증서 요청
   ↓
4. SLS → SCI/IAS 로 인증 위임
   ↓
5. IAS → SingleID 로 인증 리다이렉트 (SAML 2.0)
   ↓
6. SingleID → User 인증 (MFA 등)
   ↓
7. SingleID → 인증 성공 Assertion → IAS
   ↓
8. IAS → SLS 로 인증 결과 전달
   ↓
9. SLS → 단기간 X.509 인증서 발급 (기본 12시간, 비내보내기)
   ↓
10. SLS → Secure Login Client 에 인증서 전달
   ↓
11. Secure Login Client → SAPGUI 에 인증서 제공
   ↓
12. SAPGUI → SAP Backend 로 SNC/X.509 인증
   ↓
13. SAP Backend → STRUST 에서 SAP Cloud Root CA 로 인증서 검증
   ↓
14. 인증 성공 → SAPGUI 세션 시작
```

### 중요 포인트

- **인증서 유효기간**: 기본 12시간 또는 User 로그오프 시 만료
- **인증서 특성**: 단기간(short-lived), 비내보내기(non-exportable)
- **SAP Backend → 클라우드 연결**: 불필요
- **Kerberos vs X.509**: SLS는 X.509 방식 사용. Kerberos는 도메인 네트워크 연결 필요

---

## 4. Prerequisites

| 구성 요소 | 설명 |
|---|---|
| **SAP BTP Subaccount** | SLS 서비스 구독/할당 필요 |
| **SAP Cloud Identity (SCI)** | IAS + IdDS + IPS 포함 |
| **SingleID Tenant** | Corporate IdP로 연동 (SAML 2.0) |
| **Secure Login Client 3.0 SP2 Patch 16+** | End User Desktop 설치 |
| **SAP Backend (AS ABAP)** | SNC 활성화, STRUST 설정 |
| **BTP 역할** | `SecureLoginServiceAdministrator` 역할 필요 |

---

## 5. 설정 단계

### Step 1: SCI/IAS에 SingleID를 Corporate IdP로 연동

1. **SCI Tenant** 로그인
2. **Authentication → Identity Providers** 에서 SingleID 추가
   - SAML 2.0 기반 연동 설정
   - SingleID의 Metadata URL 또는 인증서/엔드포인트 정보 입력
3. **Identity Federation** 활성화
   - User Store: "Identity Authentication User Store" 사용
   - Corporate IdP로 SingleID 선택

> **참고**: Corporate IdP 생성 및 신뢰 구성의 상세 절차는 [Corporate_IdP_Guide_3.md](Corporate_IdP_Guide_3.md) 참조

---

### Step 2: BTP에서 SLS 서비스 활성화

1. **BTP Cockpit → Security → Trust Configuration**
   - IAS Tenant과 BTP Subaccount 간 신뢰 설정 완료
2. **SLS 서비스** 구독 및 인스턴스 생성
3. **SLS Admin 역할** 할당
   - `SecureLoginServiceAdministrator` 역할 필요
   - SCI Tenant에서 할당 (BTP user store에서 직접 관리 불가)

---

### Step 3: SLS Web UI 설정

1. SLS Web UI 로그인
2. **인증서 유효기간** 설정 (기본 12시간)
3. **Host Policy Group URL** 획득 → Step 6 SLC 설정에 필요

---

### Step 4: IAS에서 SLS 애플리케이션의 Subject Name Identifier 설정

1. IAS Admin Console → **Applications → SLS**
2. Subject Name Identifier 설정
   - 사용자 마스터 데이터의 attribute가 SingleID 설정과 일치해야 함
   - 테스트 시 `login name` 또는 `email` attribute 사용 가능
3. **Common Name / Pseudonym attribute** 설정
   - 인증서에 들어갈 CN 값 결정

---

### Step 5: SAP Backend (AS ABAP) 설정

#### STRUST 설정

1. `STRUST` 트랜잭션 실행
2. **SAP Cloud Root CA** 인증서 가져오기
   - Environment → Import Own Certificate → SAP Cloud CA 인증서 등록
3. SSF 버전 확인 (Environment → Display SSF Version)

#### SNC 설정

1. `SNCCONFIG` 트랜잭션
2. Profile 파라미터 설정:
   - `snc/enable = 1`
   - `snc/enable_ssl_library_trustmech = 1`
   - `snc/accept_insecure_ephimeral = 1` (필요 시)
   - `snc/identity/as = p:CN=<SAP System SNC name>`
3. `RSBDCOS0` 프로그램 실행 → `sapgenpse` 명령어 확인
4. `SSF02` 프로그램 실행

#### 사용자 SNC 이름 업데이트

1. `SU01` 트랜잭션 → 사용자 마스터
2. **SNC 탭** 에서 SLS 기반 인증서 형식으로 업데이트:
   ```
   p:CN=<username>,<SLS issuer domain>
   ```
   - 정확한 형식은 SLS Web UI에서 확인 가능

---

### Step 6: Secure Login Client (SLC) 설정 (End User Desktop)

1. **Secure Login Client 3.0 SP2 Patch 16+** 설치
2. **File → Options** 설정:
   - **SNC 탭**: SNC 활성화
   - **Policy Group 탭**: Step 3에서 획득한 Host Policy Group URL 입력
   - **SSH Agent 탭**: 기본값 유지
   - **Tracing 탭**: 기본값 유지
3. Windows 기본 앱으로 SAPGUI 설정

---

### Step 7: 테스트

1. Windows 로그인 후 SAPGUI 실행
2. 최초 연결 시 SLC 인증 요청 발생
3. SingleID에서 인증 → X.509 인증서 발급 (12시간 유효)
4. SAPGUI 로깅 성공 (ID/PW 불필요)

---

## 6. 방화벽 설정

SLS 기반 SAPGUI SSO의 네트워크 흐름입니다. SingleID가 클라우드 IdP이므로 온프레미스 방화벽 설정이 필요할 수 있습니다.

### 네트워크 흐름

| 방향 | 프로토콜 | 포트 | 설명 |
|---|---|---|---|
| End User Desktop → SLS (BTP) | HTTPS (TCP) | 443 | X.509 인증서 요청 |
| IAS → SingleID | HTTPS (TCP) | 443 | SAML AuthnRequest 전송 |
| SingleID → IAS | HTTPS (TCP) | 443 | SAML Assertion 응답 (브라우저 POST 경유) |
| SAPGUI → SAP Backend (SNC) | TCP | SAP 메시지 서버 포트 | SNC/X.509 인증 |

### 방화벽 설정 요약

| 항목 | 내용 |
|---|---|
| **허용 방향** | End User Desktop → 아웃바운드 (BTP/SingleID) |
| **프로토콜** | TCP |
| **포트** | 443 (HTTPS) + SAP 메시지 서버 포트 |
| **대상** | SAP BTP 리전 IP, SingleID 엔드포인트 |

### SAP BTP Neo 리전별 NAT IP (아웃바운드)

| 리전 | 호스트 | NAT IP (CIDR) | IP 범위 |
|---|---|---|---|
| Japan (Tokyo) | jp1.hana.ondemand.com | `157.133.182.32/27`, `130.214.244.32/27` | .32~.63 |
| Europe (Frankfurt) | eu2.hana.ondemand.com | `130.214.228.32/27` | .32~.63 |
| Europe (Rot) | eu1.hana.ondemand.com | `157.133.160.32/27`, `130.214.226.32/27` | .32~.63 |
| US East (Ashburn) | us1.hana.ondemand.com | `157.133.166.32/27`, `130.214.234.32/27` | .32~.63 |
| US West (Chandler) | us2.hana.ondemand.com | `130.214.254.32/27` | .32~.63 |
| US West (Colorado) | us4.hana.ondemand.com | `130.214.242.32/27` | .32~.63 |
| Australia (Sydney) | ap1.hana.ondemand.com | `157.133.168.32/27`, `130.214.240.32/27` | .32~.63 |
| Europe (Amsterdam) | eu3.hana.ondemand.com | `157.133.170.32/27`, `130.214.230.32/27` | .32~.63 |
| UAE (Dubai) | ae1.hana.ondemand.com | `130.214.250.32/27` | .32~.63 |

> **참고**: `/27` CIDR는 32개 IP를 의미합니다 (예: `157.133.182.32` ~ `157.133.182.63`).

### 설정 절차

1. IAS 테넌트 URL 확인 → `https://<tenant>.accounts.ondemand.com`
2. 호스트에서 리전 확인 (예: `jp1.hana.ondemand.com` → Tokyo)
3. 해당 리전의 NAT IP를 End User Desktop 아웃바운드 허용 (TCP 443)
4. SingleID 엔드포인트 URL도 아웃바운드 허용

### 참고 사항

- SAP Note **3513325** 구독 권장 — NAT IP 변경 시 알림 받음
- 추가 IP가 모든 Neo 리전에 추가될 예정이므로 주기적으로 확인 필요
- SingleID는 클라우드 IdP이므로 온프레미스 인바운드 방화벽 설정 불필요
- 출처: [SAP Help Portal — Regions and Hosts Available for the Neo Environment](https://help.sap.com/docs/btp/sap-btp-neo-environment/regions-and-hosts-available-for-neo-environment)

---

## 7. Cloud Connector가 필요한 다른 시나리오

| 시나리오 | Cloud Connector 필요 여부 |
|---|---|
| SAPGUI SSO (SLS 기반) | **불필요** |
| Fiori Launchpad → 온프레미스 S/4HANA | 필요 |
| BTP 앱 → 온프레미스 SAP 시스템 | 필요 |
| Cloud ALM → 온프레미스 시스템 | 필요 |

**Cloud Connector는 클라우드 애플리케이션이 온프레미스 SAP 시스템에 접근해야 하는 경우에만 필요합니다.**
SLS는 인증서 발급 인프라일 뿐이며, SAPGUI → SAP Backend 연결은 직접 SNC/X.509 경로로 처리됩니다.

---

## 7. 참고 자료

| 자료 | 링크 |
|---|---|
| SAP Community: How to Configure SSO for SAP GUI Including MFA | [링크](https://community.sap.com/t5/technology-blog-posts-by-sap/how-to-configure-sso-for-sap-gui-including-mfa/ba-p/14213388) |
| SAP Community: Does SLS require CC? | [링크](https://community.sap.com/t5/technology-q-a/does-secure-login-service-require-a-cc-for-on-premise-sapgui-logon-with/qaq-p/12796994) |
| Xiting: SAP Secure Login Service for SAP GUI Guide | [링크](https://xiting.com/en/sap-knowledge/sap-secure-login-service-for-sap-gui-guide) |
| AWS: SSO – SAPGUI Front-End | [링크](https://docs.aws.amazon.com/sap/latest/general/sso-sapgui.html) |
| SAP Help: Migrating from SAP Single Sign-On to SLS | [링크](https://help.sap.com/docs/SAP%20SECURE%20LOGIN%20SERVICE/c35917ca71e941c5a97a11d2c55dcacd/bd28a94ee69c4c8d8be876044f73abe2.html) |
| SAP Product: Secure Login Service for SAP GUI | [링크](https://www.sap.com/products/financial-management/secure-login-service-for-gui.html) |
| Corporate IdP 가이드 (SingleID 연동 상세) | [Corporate_IdP_Guide_3.md](Corporate_IdP_Guide_3.md) |

---

> **출처**: SAP Community Blog, SAP Help Portal, AWS SAP Guides, Xiting
> **작성일**: 2026-08-26
