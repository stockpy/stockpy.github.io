---
layout: post
title: SAP Secure Login Service for SAP GUI — 종합 가이드
categories: sapgui
---

# SAP Secure Login Service for SAP GUI — 종합 가이드

## 1. 개요

- **SAP SSO 3.0의 클라우드 기반 후속 제품**
- SAP SSO 3.0 (및 Secure Login Server)는 **2027년 12월 31일 유지보수 종료**
- SAP BTP 서비스로 제공 (클라우드 기반)
- SAP GUI SSO + MFA (Multi-Factor Authentication) 지원
- X.509 인증서 기반 인증
- 기존 Kerberos SSO와 **병렬 사용 가능**

---

## 2. 필요 라이선스 및 비용

| 항목 | 내용 |
|---|---|
| **라이선스 모델** | 500명 단위 블록 구매 |
| **단가** | 블록 1~6개: **€450/블록/월** (≈ €0.90/사용자/월) |
| **7개 이상** | 추가 블록 할인가 (SAP에 문의) |
| **PCE/RISE 포함 여부** | SAP S/4HANA Cloud Private Edition 구독에 **포함되지 않음** — 별도 구매 필요 |
| **SAP Cloud Identity Services (IAS)** | SAP 클라우드 애플리케이션 연동 시 별도 비용 없음 |

> 예: 500명 → €450/월, 1,000명 → €900/월

---

## 3. 아키텍처 구성 요소

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  SAP GUI    │────▶│  Secure Login     │────▶│  SAP S/4HANA │
│  (Client)   │     │  Service (SLS)   │     │  (ABAP)      │
│             │◀────│  (SAP BTP)       │◀────│              │
└─────────────┘     └────────┬─────────┘     └─────────────┘
                             │
                      ┌──────▼────────┐
                      │  SAP IAS /    │
                      │  Corporate IdP│
                      │  (MFA 제공)   │
                      └───────────────┘
```

- **Secure Login Client (SLC)**: Windows/macOS 클라이언트에 설치 (SAP GUI와 함께 설치)
- **Secure Login Service (SLS)**: SAP BTP 서비스 (클라우드)
- **SAP IAS / Corporate IdP**: 인증 제공자 (Okta, Azure AD 등 연동 가능)
- **SAP S/4HANA (ABAP)**: SNC/X.509 인증서 기반 인증 설정

---

## 4. 구현 단계

### Step 1: SAP BTP에서 Secure Login Service 구독 및 활성화

1. SAP BTP Cockpit에서 Subaccount 생성/선택
2. Service Marketplace에서 **Secure Login Service for SAP GUI** 구독
3. HELPGUIDE에 따라 서비스 활성화

### Step 2: SAP IAS (또는 기업 IdP)와 신뢰 설정

1. SAP Cloud Identity Services (IAS) 또는 기업 IdP (Okta, Azure AD 등) 구성
2. SLS와 IAS 간 신뢰 관계 설정
3. MFA 정책 구성 (기업 IdP에서 이미 설정된 경우 활용 가능)

### Step 3: SAP ABAP 시스템 서버 측 설정 (STRUST)

1. `STRUST` 트랜잭션 실행
2. SAP Cloud Root CA 인증서 다운로드 및 등록
3. SNC 설정 활성화 (SNC partner name 구성)
4. SNC 파라미터 설정 ([SAP Help](https://help.sap.com) 참조)

### Step 4: SAP 프로파일 파라미터 설정

| 파라미터 | 값 | 설명 |
|---|---|---|
| `SETENV_XX` | `CCL_PROFILE=$(DIR_PROFILE)/DEFAULT.PFL` | XX는 사용되지 않는 번호 |
| `ccl/snc/namealias/value_1` | `, L=<IAS tenant url>, OU=secure-login-service, OU=Clients, O=SAP, C=DE` | SLS에서 생성된 SNC 이름 |
| `ccl/snc/namealias/replacement_1` | (비워두기) | 기존 Kerberos SSO와 병렬 사용 시 CN=username만 사용 |
| `ccl/snc/partner_case_x509` | `Upper` | |
| `ccl/snc/server_partner_name_x509` | `EMailPrincipalOnlyOrSubject` | |
| `ccl/snc/server_partner_name_mapping_for_SLC` | `1` | |

### Step 5: 클라이언트 측 Windows 레지스트리 설정

**프로필 설정:**
```
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\SAP\SecureLogin\profiles\CLOUD-LOGIN
```

| 파라미터 | 타입 | 값 |
|---|---|---|
| `profileName` | STRING | `CLOUD-LOGIN` |
| `pseType` | STRING | `browser` (또는 macOS는 `standardBrowser`) |
| `enrollURL0` | STRING | `<SLS 도메인>/slc/v1/login` |
| `sslHostCommonNameCheck` | DWORD | `0` |
| `sslHostAlternativeNameCheck` | DWORD | `1` |
| `showErrorMsg` | DWORD | `1` |

**애플리케이션 정책 설정:**
```
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\SAP\SecureLogin\applications\CLOUD-APPLICATION
```

| 파라미터 | 타입 | 값 |
|---|---|---|
| `GSSTargetName` | STRING | SAP 서버의 SNC 이름 (와일드카드 가능) |
| `profile` | STRING | `CLOUD-LOGIN` |
| `allowFavorite` | DWORD | `0` |

> **핵심:** `GSSTargetName`을 통해 Kerberos SSO 시스템과 SLS SSO 시스템을 구분. 기존 Kerberos SSO에는 레지스트리 엔트리를 설정하지 않고, SLS를 사용할 시스템의 SNC 이름만 지정.

### Step 6: 사용자 인증서 SNC 이름 형식

```
p:CN=<email>, L=<IAS tenant url>, OU=cf-us20-secure-login-service, OU=SAP BTP Clients, O=SAP SE, C=DE
```

### Step 7: 테스트

1. X.509 인증서 기반 SLS 인증으로 SAP GUI 로그온 테스트
2. 기존 Kerberos SSO 시스템 로그온 테스트 (병렬 동작 확인)

---

## 5. Kerberos SSO와의 병렬 사용

기존 Kerberos SSO를 유지하면서 SLS를 추가할 수 있습니다:

- **클라이언트 측:** Windows 레지스트리 `GSSTargetName`으로 인증 방법 구분
- **서버 측:** `ccl/snc/namealias` 파라미터로 기존 SU01 SNC 이름 변경 없이 X.509 인증 지원
- 기업 네트워크 내 → Kerberos, 외부/원격 → SLS (MFA 포함)

---

## 6. 참고 자료

- [SAP Help: Secure Login Service](https://help.sap.com/docs/secure-login-service)
- SAP Note 2338952 — CommonCryptoLib 8.5: Configuration Profile Parameters
- SAP Community 블로그: "Implementing SAP BTP Secure Login Service for SAP GUI"
- SAP Community 블로그: "Step by Step Implementation of Secure Login Service for SAP GUI"
