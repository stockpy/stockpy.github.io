---
layout: post
title: SAP PCE 환경 — SAPGUI SSO 구성 가이드 (사내 AD 없음)
---

# SAP PCE 환경 - SAPGUI SSO 구성 가이드 (사내 AD 없음)

## 1. 개요

SAP S/4HANA Cloud, Private Edition (PCE/RISE) 환경에서 사내 Active Directory가 없는 경우 Kerberos SSO는 불가능하며, **SAP Secure Login Service (SLS) for SAP GUI**를 사용해야 한다.

- SLS는 SAP SSO 3.0의 클라우드 기반 후속 제품 (SAP BTP 서비스)
- 기존 SAP SSO 3.0 (Secure Login Server)은 **2027년 12월 31일 유지보수 종료**
- X.509 인증서 기반 인증 + MFA 지원
- SAP GUI 7.70 이상에서 Secure Login Client 포함 설치

---

## 2. 아키텍처

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  SAP GUI    │────▶│  Secure Login     │────▶│  SAP S/4HANA │
│  (Client)   │     │  Service (SLS)   │     │  (ABAP)      │
│             │◀────│  (SAP BTP)       │◀────│              │
└─────────────┘     └────────┬─────────┘     └─────────────┘
                             │
                    ┌────────▼────────┐
                    │  SAP IAS /      │
                    │  Corporate IdP  │
                    │  (MFA 제공)     │
                    └─────────────────┘
```

- **Secure Login Client (SLC)**: 클라이언트에 설치 (SAP GUI 7.70+ 포함)
- **Secure Login Service (SLS)**: SAP BTP 서비스 (클라우드)
- **SAP IAS / Corporate IdP**: 인증 제공자 (Okta, Azure AD 등 연동 가능)

---

## 3. 필요 라이선스 및 비용

### 3.1 Secure Login Service for SAP GUI

| 항목 | 내용 |
|---|---|
| **라이선스 모델** | 500명 단위 블록 구매 |
| **단가 (1~6블록)** | **€450/블록/월** (≈ €0.90/사용자/월) |
| **USD 기준** | **USD 531.00/블록/월** |
| **7블록 이상** | 추가 블록 할인가 (SAP에 문의) |
| **계약 기간** | 1~5년, 자동 갱신 |
| **PCE/RISE 포함 여부** | **포함되지 않음** — 별도 구매 필요 |

**예시**:
- 500명 → €450/월 (USD 531/월)
- 1,000명 → €900/월 (USD 1,062/월)

> **근거**: SAP 공식 가격 페이지 (sap.com/products/financial-management/secure-login-service-for-gui.html)

### 3.2 SAP Cloud Identity Services (IAS)

| 항목 | 내용 |
|---|---|
| **정의** | SAP의 중앙 클라우드 IAM 서비스 (인증, SSO, 아이덴티티 라이프사이클) |
| **라이선스** | SAP BTP 구독에 포함 (인증용 별도 비용 없음) |
| **역할** | SLS의 Identity Provider로 사용 또는 기업 IdP와 연동 |

> **근거**: SAP Discovery Center - License Model for SAP Cloud Identity Services (discovery-center.cloud.sap)

---

## 4. 구현 단계

### Step 1: SAP BTP에서 Secure Login Service 구독

1. SAP BTP Cockpit → Subaccount 생성/선택
2. Service Marketplace → **Secure Login Service for SAP GUI** 구독
3. HELPGUIDE에 따라 서비스 활성화

### Step 2: SAP IAS (또는 기업 IdP)와 신뢰 설정

1. SAP Cloud Identity Services (IAS) 또는 기업 IdP (Okta, Azure AD 등) 구성
2. SLS ↔ IAS 간 신뢰 관계 설정
3. MFA 정책 구성

### Step 3: SAP ABAP 서버 측 설정

**STRUST**:
- SAP Cloud Root CA 인증서 다운로드 및 등록
- SNC 설정 활성화 (SNC partner name 구성)

**RZ10 프로파일 파라미터**:

| 파라미터 | 값 | 설명 |
|---|---|---|
| `SETENV_XX` | `CCL_PROFILE=$(DIR_PROFILE)/DEFAULT.PFL` | XX는 사용되지 않는 번호 |
| `ccl/snc/namealias/value_1` | `, L=<IAS tenant url>, OU=secure-login-service, OU=Clients, O=SAP, C=DE` | SLS에서 생성된 SNC 이름 |
| `ccl/snc/namealias/replacement_1` | (비워두기) | 기존 Kerberos SSO와 병렬 사용 시 |
| `ccl/snc/partner_case_x509` | `Upper` | |
| `ccl/snc/server_partner_name_x509` | `EMailPrincipalOnlyOrSubject` | |
| `ccl/snc/server_partner_name_mapping_for_SLC` | `1` | |

**SU01**:
- 사용자 SNC 이름을 X.509 형식으로 설정
- 형식: `p:CN=<email>, L=<IAS tenant url>, OU=cf-us20-secure-login-service, OU=SAP BTP Clients, O=SAP SE, C=DE`

### Step 4: 클라이언트 측 Windows 레지스트리 설정

**프로필 설정**:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\SAP\SecureLogin\profiles\CLOUD-LOGIN
```

| 파라미터 | 타입 | 값 |
|---|---|---|
| `profileName` | STRING | `CLOUD-LOGIN` |
| `pseType` | STRING | `browser` |
| `enrollURL0` | STRING | `<SLS 도메인>/slc/v1/login` |
| `sslHostCommonNameCheck` | DWORD | `0` |
| `sslHostAlternativeNameCheck` | DWORD | `1` |
| `showErrorMsg` | DWORD | `1` |

**애플리케이션 정책 설정**:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\SAP\SecureLogin\applications\CLOUD-APPLICATION
```

| 파라미터 | 타입 | 값 |
|---|---|---|
| `GSSTargetName` | STRING | SAP 서버의 SNC 이름 (와일드카드 가능) |
| `profile` | STRING | `CLOUD-LOGIN` |
| `allowFavorite` | DWORD | `0` |

### Step 5: 테스트

1. X.509 인증서 기반 SLS 인증으로 SAP GUI 로그온 테스트
2. MFA 동작 확인

---

## 5. 체크리스트

### BTP/구독
- [ ] SAP BTP Subaccount 준비
- [ ] Secure Login Service for SAP GUI 구독
- [ ] SAP Cloud Identity Services (IAS) 구독 또는 기업 IdP 준비
- [ ] SLS ↔ IAS 신뢰 관계 설정
- [ ] MFA 정책 구성

### 서버 측 (SAP ABAP)
- [ ] STRUST — SAP Cloud Root CA 인증서 등록
- [ ] RZ10 — ccl/snc/namealias 파라미터 설정
- [ ] SU01 — 사용자 SNC 이름 (X.509 형식) 설정

### 클라이언트 측
- [ ] SAP GUI 7.70 이상 설치
- [ ] Windows 레지스트리 정책 설정 (프로필 + 애플리케이션)
- [ ] SCCM/Intune를 통해 레지스트리 설정 배포 (대규모 환경)

### 테스트
- [ ] X.509 인증서 기반 SSO 자동 로그온 확인
- [ ] MFA 동작 확인
- [ ] 다수 사용자 테스트

---

## 6. 참고 자료

- SAP 공식 가격 페이지: sap.com/products/financial-management/secure-login-service-for-gui.html
- SAP Discovery Center: License Model for SAP Cloud Identity Services
- SAP Help: Secure Login Service (help.sap.com/docs/secure-login-service)
- SAP Note 2338952 — CommonCryptoLib 8.5: Configuration Profile Parameters
- SAP Community: "Implementing SAP BTP Secure Login Service for SAP GUI"
- SAP Community: "Step by Step Implementation of Secure Login Service for SAP GUI"
