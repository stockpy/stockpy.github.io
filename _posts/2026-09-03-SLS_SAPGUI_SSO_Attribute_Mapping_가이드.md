---
layout: post
title: SLS SAP GUI SSO — Attribute Mapping 설정 가이드 (Corporate IdP + IAS)
categories: sso-auth
---

# SLS SAP GUI SSO — Attribute Mapping 설정 가이드 (Corporate IdP + IAS)

> **작성일:** 2026-09-03
> **참조 제품:** SAP Secure Login Service for SAP GUI, SAP Cloud Identity Services (IAS)

---

## 전체 흐름

```
Corporate IdP (Entra ID 등)
  → SAML/OIDC Assertion (Attribute 전송)
  → IAS (Proxy, Attribute 변환/보강)
  → SLS Application (Certificate CN/Pseudonym 결정)
  → X.509 Certificate → SNC → SAP GUI
```

---

## 1. Corporate IdP → IAS: Enrich Assertion Attributes

Corporate IdP에서 받은 Assertion Attribute를 IAS에서 변환하는 단계입니다.

**설정 경로:** `Identity Providers → Corporate Identity Providers → [Corporate IdP 선택] → Trust → Enriched Assertion Attributes`

- Corporate IdP에서 받은 Attribute를 최대 **30개**까지 수정/추가/재매핑 가능
- Static 값 또는 Dynamic 값 (`${received_attribute}`) 설정 가능
- Subject Name Identifier도 `${NameID}` 변수로 덮어쓰기 가능

**예시:**

| Attribute | Value |
|---|---|
| `mail` | `${mail:function[lowercase]}` |
| `NameID` | `SNC_${NameID}` |

> **근거:** SAP Help Portal — *Enrich Assertion Attributes Coming from Corporate IdP*
> https://help.sap.com/docs/IDENTITY_AUTHENTICATION/6d6d63354d1242d185ab4830fc04feb1/7124201682434efb946e1046fde06afe.html

---

## 2. IAS → SLS Application: Default Attribute Mapping

SLS Application에 보낼 Attribute를 정의하는 단계입니다. **Corporate IdP 사용자**의 경우 `corporateIdP.` 접두사를 반드시 사용해야 합니다.

**설정 경로:** `Applications & Resources → Applications → [SLS Application] → Trust → Attributes`

### 핵심 포맷

```
${corporateIdP.<attribute_name>}
```

| 파라미터 | 필수 | 설명 |
|---|---|---|
| `attribute_name` | O | Administration Console에서 정의하는 Attribute 이름 |
| `corporateIdP.` | O | 고정 문자열. Corporate IdP Assertion에서 값을 가져옴을 표시 |
| `corporateIdP_attribute_name` | O | Corporate IdP에서 전송하는 Attribute 이름 |
| `:regex[filter]` | X | Corporate IdP Attribute 필터링 |
| `:function[uppercase\|lowercase]` | X | 대소문자 변환 |

**예시:**

| Attribute Name | Value |
|---|---|
| `mail` | `${corporateIdP.mail:function[lowercase]}` |
| `groups` | `${corporateIdP.groups:regex[SAP-]}` |
| `custom-mail` | `${corporateIdP.givenName}_${corporateIdP.mail}` |

### Identity Federation — User Store 활성화 (필수)

Corporate IdP의 Attribute를 IAS에서 참조하려면 **Identity Federation의 User Store를 ON**으로 해야 합니다.

**설정 경로:** `Identity Providers → Corporate Identity Providers → [Corporate IdP 선택] → Single Sign-On → Identity Federation → Use Identity Authentication user store → ON`

> **근거:** SAP Help Portal — *Configuring Attributes Based on Flexible Expressions* (Identity Federation 섹션)
> https://help.sap.com/docs/IDENTITY_AUTHENTICATION/6d6d63354d1242d185ab4830fc04feb1/a2f1e4692e7d4379ab82144ab309e7b3.html
>
> SAP Help Portal — *Configuring User Attributes from a Corporate Identity Provider*
> https://help.sap.com/docs/IDENTITY_AUTHENTICATION/6d6d63354d1242d185ab4830fc04feb1/621017f2623c4ac59923e4ef531304d2.html

---

## 3. SLS Certificate CN 설정 (2가지 옵션)

SLS가 발급하는 X.509 Certificate의 Common Name(CN)을 어떤 Attribute로 할지 결정합니다. 기본값은 `sub` (Subject Name Identifier, GUID)입니다.

### Option 1: Subject Name Identifier 수정

**설정 경로:** `Applications & Resources → Applications → [SLS Application] → Trust → Subject Name Identifier`

Primary/Fallback Attribute의 Source와 Value를 선택하여 변경.

- **IAS 사용자:** `${loginName}`
- **Corporate IdP 사용자:** `${corporateIdP.loginName}` 또는 `${corporateIdP.mail}`

### Option 2: sls_common_name Attribute 사용

**설정 경로:** `Applications & Resources → Applications → [SLS Application] → Trust → Attributes`

`sls_common_name`이라는 커스텀 Default Attribute에 원하는 값을 설정.

| Attribute Name | Value |
|---|---|
| `sls_common_name` | `${corporateIdP.loginName}` |

공백 또는 존재하지 않는 Attribute 변수가 설정되면 `sls_common_name`이 비활성화되고 기본 `sub` Attribute가 사용됩니다.

### Pseudonym (선택): sls_pseudonym

Certificate에 추가 Subject Name Attribute(Pseudonym)를 포함하고 싶으면 `sls_pseudonym` Attribute를 설정.

| Attribute Name | Value |
|---|---|
| `sls_pseudonym` | `${corporateIdP.employeeNumber}` |

> **근거:** SAP Help Portal — *Set Up the Common Name Attribute for User Certificates*
> https://help.sap.com/docs/SAP%20SECURE%20LOGIN%20SERVICE/c35917ca71e941c5a97a11d2c55dcacd/81fe0a1211514e84bc7d63d3541349ad.html
>
> SAP Help Portal — *Set Up the Pseudonym Attribute for User Certificates*
> https://help.sap.com/docs/SAP%20SECURE%20LOGIN%20SERVICE/c35917ca71e941c5a97a11d2c55dcacd/d8ee0cae04b94709bd1665c4e019a9b6.html

---

## Certificate Subject Name 규칙

| 항목 | 제한 |
|---|---|
| **CN 최대 길이** | 64 characters |
| **Pseudonym 최대 길이** | 128 characters |
| **허용 문자** | `a-z A-Z 0-9 : . - _ / ( ) @ Space` |
| **중복 금지** | 선택한 Attribute는 User Store 내에서 **Unique**해야 함 |

Unique 플래그 설정: `Applications & Resources → Tenant Settings → Logon Alias → [Attribute 선택] → Unique`

Custom CA 사용 시 Custom Subject Pattern 예시:

```
<CN=${sls_common_name}, OU=My Department, O=My Company, C=DE>
```

- `<CN>`과 `<C>`는 1회만, `<OU>`는 최대 4회 사용 가능
- `<C>`는 대문자만 허용 (최대 2자)

> **근거:** SAP Help Portal — *Configure Secure Login Service* (Client Certificate Subject Name)
> https://help.sap.com/docs/SAP%20SECURE%20LOGIN%20SERVICE/c35917ca71e941c5a97a11d2c55dcacd/d77b13dd223f422cb8194bf81a516596.html

---

## SAP AS ABAP 측: SNC User Name 매핑

Certificate가 발급되면 SAP 시스템에서 **SNC User Name**을 SAP User에 매핑해야 합니다.

- **SU01**: 개별 사용자별 SNC Name 설정
- **SNC1**: 대량 매핑 (SAP Note 1898778 참고 — SLS에서 발급된 긴 User Name 지원)

> **근거:** SAP Community — *How to Configure SSO for SAP GUI Including MFA* (Step 4)
> https://community.sap.com/t5/technology-blog-posts-by-sap/how-to-configure-sso-for-sap-gui-including-mfa/ba-p/14213388

---

## 설정 체크리스트

| # | 단계 | 설정 위치 |
|---|---|---|
| 1 | 필요한 Attribute를 SAML/OIDC Assertion에 포함 | Corporate IdP |
| 2 | Enriched Assertion Attributes로 Attribute 변환 | IAS → Corporate IdP → Trust |
| 3 | Identity Federation User Store **ON** | IAS → Corporate IdP → Identity Federation |
| 4 | Subject Name Identifier 또는 `sls_common_name`에 `corporateIdP.` Attribute 매핑 | IAS → SLS Application → Trust |
| 5 | (선택) `sls_pseudonym` 설정 | IAS → SLS Application → Trust → Attributes |
| 6 | Host Policy Group URL 확인, Certificate 유효기간 설정 | SLS Web UI |
| 7 | SU01/SNC1로 SNC User Name 매핑 | SAP AS ABAP |
