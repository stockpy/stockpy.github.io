---
layout: post
title: SAP Cloud Identity Services - Corporate IdP 신뢰 설정 가이드
categories: identity
---

# SAP Cloud Identity Services - Corporate IdP 신뢰 설정 가이드

## 개요

SAP Cloud Identity Services(구 Identity Authentication, 이하 IAS)를 사내 Corporate Identity Provider(IdP)와 연동하기 위해서는 **양방향 신뢰(Bidirectional Trust)** 설정이 필요합니다.

SAML 2.0 연동 구조:

| 역할 | 시스템 |
|---|---|
| **Identity Provider (IdP)** | 사내 Corporate IdP (Azure AD, ADFS, Okta 등) |
| **Service Provider (SP)** | SAP Cloud Identity Services |

---

## Step 1. Configure Trust on the Corporate Identity Provider Site

**목적:** 사내 IdP에 SAP IAS를 서비스 프로바이더(SP)로 등록

### 절차

1. **SAP IAS의 SAML 2.0 메타데이터 XML 다운로드**
   - SAP IAS 관리 콘솔 > Tenant SAML 2.0 Configurations 에서 다운로드

2. **사내 IdP 관리 콘솔에 SAP IAS 등록**
   - 다운로드한 메타데이터 XML을 업로드 또는 수동 입력
   - 등록 시 주요 항목:
     - **Entity ID** — SAP IAS의 고유 식별자
     - **ACS(Assertion Consumer Service) URL** — SAML 인증 응답을 SAP IAS로 전송하는 주소
     - **서명 인증서** — 메타데이터에 포함됨

3. **ACS URL 설정 시 참고**
   - IdP-초기화 SSO(IdP-initiated SSO)를 사용할 경우 ACS URL에 `?sp=<sp_name>` 파라미터 추가 필요
   - 예: `https://<ACS_URL>?sp=<sp_name>`
   - `sp_name`은 SAML 2.0 서비스 프로바이더 이름

### ACS 엔드포인트의 역할

```
1. 사용자가 SAP 앱에 접속
2. SAP IAS → 사내 IdP로 인증 요청 (SAML AuthnRequest)
3. 사용자가 사내 IdP에서 로그인
4. 사내 IdP → ACS 엔드포인트로 인증 응답 전송 (SAML Response)
5. SAP IAS가 응답을 받아 사용자 인증 완료
```

ACS는 4번 단계에서 IdP가 SAML 응답을 POST하는 URL입니다. 등록하지 않으면 IdP가 응답을 보낼 곳을 모르므로 SSO가 작동하지 않습니다.

---

## Step 2. Configure Trust on Identity Authentication Side

**목적:** SAP IAS에 사내 Corporate IdP를 신뢰하는 IdP로 등록

### 전제 조건

- Manage Corporate Identity Providers 관리자 역할 보유
- Step 1 완료 (사내 IdP에 SAP IAS 등록 완료)
- 사내 IdP의 SAML 2.0 메타데이터 XML 준비

### 절차

1. SAP Cloud Identity Services 관리 콘솔 로그인
2. **Identity Providers** > **Corporate Identity Providers** 타일 선택
3. 구성할 Corporate IdP 선택
4. **SAML 2.0** > **SAML 2.0 Configuration** 선택
5. 사내 IdP 메타데이터 XML 파일 업로드 또는 수동 입력

### 주요 설정 항목

| 항목 | 설명 |
|---|---|
| **Metadata File** | 사내 IdP의 메타데이터 XML 파일 |
| **Name** | IdP의 Entity ID |
| **Single Sign-On Endpoint URL** | 인증 요청을 수신하는 IdP의 SSO 엔드포인트 주소 |
| **Single Logout Endpoint URL** | 로그아웃 메시지를 수신하는 IdP의 엔드포인트 주소 |
| **Binding** | SAML 프로토콜 메시지 전송 방식 (HTTP-Redirect, HTTP-Post 등) |
| **Signing Certificate** | IdP가 SAML 메시지를 서명하는 base64 인코딩 인증서 (최대 2개) |
| **Algorithm** | outgoing 메시지 서명 알고리즘 (SHA-1 / SHA-256(기본) / SHA-512) |

- 메타데이터 XML 업로드 시 필드가 자동으로 채워짐
- Microsoft ADFS / Entra ID 사용 시 Algorithm은 SHA-256 필수

---

## 전체 흐름 요약

```
Step 1: 사내 IdP 관리 콘솔
  → SAP IAS 메타데이터 다운로드 → 사내 IdP에 SAP IAS를 SP로 등록

Step 2: SAP IAS 관리 콘솔
  → 사내 IdP 메타데이터 다운로드 → SAP IAS에 사내 IdP를 IdP로 등록

Step 3: 애플리케이션 설정 (필수)
  → S/4HANA 애플리케이션의 기본 IdP로 Corporate IdP 선택
```

---

## Step 3. Choose Default Identity Provider for an Application (필수)

**목적:** S/4HANA 애플리케이션의 기본 인증 IdP를 Corporate IdP로 지정

### 왜 필수인가?

이 단계를 건너뛰면:

- S/4HANA의 기본 IdP는 **로컬 IAS**로 유지됨
- 사용자는 IAS 자체 계정(이메일/비밀번호)으로 로그인해야 함
- 사내 Corporate IdP로 인증 위임이 발생하지 않음 → **Proxy 모드 미작동**

IAS Proxy 모드에서 S/4HANA를 연동하려면 이 단계가 반드시 필요합니다:

```
S/4HANA → IAS(프록시) → 사내 Corporate IdP
```

### 전제 조건

- Manage Corporate Identity Providers 관리자 역할 보유
- Step 1, Step 2 완료
- Conditional Authentication 규칙이 추가되어 있지 않은 상태

### 절차

1. SAP Cloud Identity Services 관리 콘솔 로그인
2. **Applications and Resources** > **Applications** 타일 선택
3. S/4HANA 애플리케이션 선택
4. **Trust** 탭 선택
5. **Conditional Authentication** 섹션 > **Conditional Authentication** 목록 선택
6. 드롭다운에서 Corporate IdP 선택
7. 저장

### Corporate IdP 선택 시 주의 사항

- **Authentication**, **Access and Branding and Layout** 탭의 설정이 **일부만 사용 가능**
- 사용자는 단일 로그인 페이지에서 사내 계정으로 인증
- Optional: **Allow Identity Authentication Users Log On** 옵션 활성화 시 Corporate IdP가 기본이지만 IAS 로컬 사용자도 로그인 가능

### 필수 단계 요약

| 단계 | 필수 여부 | 내용 |
|---|---|---|
| Step 1: 사내 IdP에 IAS 등록 | 필수 | 양방향 신뢰 설정 |
| Step 2: IAS에 사내 IdP 등록 | 필수 | 양방향 신뢰 설정 |
| Step 3: 애플리케이션 기본 IdP 선택 | **필수** | S/4HANA 앱에 Corporate IdP 적용 |

3단계 모두 완료해야 S/4HANA 사용자가 사내 계정(SSO)으로 로그인할 수 있습니다.

---

## IdP-Initiated SSO vs SP-Initiated SSO (참고)

### SSO 방식 비교

| 방식 | 흐름 | 필요 여부 |
|---|---|---|
| **SP-Initiated SSO** | S/4HANA URL 접속 → IAS → 사내 IdP 인증 → S/4HANA 진입 | **기본 흐름 (필수)** |
| **IdP-Initiated SSO** | 사내 IdP 포털(Azure AD MyApps, Okta Dashboard 등)에서 앱 클릭 → S/4HANA 진입 | **선택 사항** |

S/4HANA Cloud Public Edition의 표준 인증 흐름은 **SP-Initiated SSO**입니다. Step 1~3만 완료해도 SSO가 정상 작동합니다.

### IdP-Initiated SSO 설정 시 주의 사항

| 레벨 | 설정 | 기본값 |
|---|---|---|
| **테넌트 레벨** | IdP-Initiated SSO 옵션 | ✅ 기본 활성화 |
| **애플리케이션 레벨** | Trust Corporate Identity Providers | ❌ 기본 비활성화 |

테넌트 레벨이 기본 활성화되어 있어도 **애플리케이션 레벨 설정이 별도로 필요합니다.**

### IdP-Initiated SSO가 필요한 경우

- 사내 포털(Azure AD, Okta 등)에서 S/4HANA 앱 아이콘을 클릭하여 바로 진입하게 하고 싶을 때
- 파트너사가 각자의 Corporate IdP를 통해 S/4HANA에 접근해야 할 때 (다중 IdP 시나리오)

### IdP-Initiated SSO 설정 방법 (선택)

1. SAP Cloud Identity Services 관리 콘솔 로그인
2. **Applications and Resources** > **Applications** 타일 선택
3. S/4HANA 애플리케이션 선택
4. **Trust** 탭 선택
5. **Conditional Authentication** 섹션 > **Trust Corporate Identity Providers** 선택
6. 슬라이더 활성화(모든 Corporate IdP 허용) 또는 특정 Corporate IdP 선택
7. 저장

---

## 추가 고려 사항 (상황에 따라 필수)

| 항목 | 필수 여부 | 내용 |
|---|---|---|
| **User Provisioning** | 상황에 따라 필수 | 사내 사용자가 S/4HANA에 처음 로그인할 때 사용자 계정이 없으면 접근 거부. Identity Provisioning 또는 수동 등록 필요 |
| **Attribute Mapping** | 필수 확인 | Corporate IdP가 SAML 응답에 보내는 사용자 속성이 S/4HANA의 매핑과 일치해야 함 (email, name 등) |
| **Allow Identity Authentication Users Log On** | 선택 | Corporate IdP가 기본이지만 IAS 로컬 사용자도 로그인 가능하게 함 (관리자용 폴백) |
| **Configure Identity Federation** | 선택 | Corporate IdP 선택 시 일부 앱 설정이 제한됨. Identity Federation 활성화 시 커스텀 설정 적용 가능 |

---

## 참고 문서

- [Configure Trust with SAML 2.0 Corporate Identity Provider](https://help.sap.com/docs/IDENTITY_AUTHENTICATION/6d6d63354d1242d185ab4830fc04feb1/d43e484d1f5143a2bca694d0a75dfadb.html)
- [Tenant SAML 2.0 Configurations](https://help.sap.com/docs/IDENTITY_AUTHENTICATION/6d6d63354d1242d185ab4830fc04feb1/0a177592b39e49298c1d44a85a33321e.html)
- [Choose Default Identity Provider for an Application](https://help.sap.com/docs/IDENTITY_AUTHENTICATION/6d6d63354d1242d185ab4830fc04feb1/e9d82742d42b4f769c2d0f16d8e9ee41.html)
