---
layout: post
title: SAP Cloud Identity Services — Corporate Identity Provider 가이드
---

# SAP Cloud Identity Services — Corporate Identity Provider 가이드



> SAP Help Portal의 Corporate Identity Providers 관련 문서를 정리한 가이드입니다.



---



## 목차

1. [IAS Proxy 역할 이해 (핵심 개념)](#0-ias-proxy-역할-이해-핵심-개념)
2. [Administration Console에서 Corporate IdP 생성](#1-create-corporate-idp-in-administration-console)
3. [SAML 2.0 Corporate Identity Provider로 신뢰 구성](#2-configure-trust-with-saml-20-corporate-identity-provider)
4. [Corporate Identity Provider를 이용한 IdP-Initiated SSO 구성](#3-configure-idp-initiated-sso-with-corporate-identity-providers)
5. [Corporate Identity Provider를 이용한 SSO 활성화](#4-enable-sso-with-corporate-identity-providers)
6. [Corporate IdP에서 전달되는 Assertion 속성 보강](#5-enrich-assertion-attributes-coming-from-corporate-idp)
7. [SingleID와 Corporate IdP 연동 - 참고 사항](#6-singleid-corporate-idp-참고)
8. [IAS ↔ 온프레미스 Corporate IdP 방화벽 설정](#7-ias-온프레미스-corporate-idp-방화벽-설정)

---

## 0. IAS Proxy 역할 이해 (핵심 개념)

> 이 섹션은 IAS가 "중간자(Proxy)"로 동작하는 방식을 정리한 것입니다.

### 역할 정의

| 역할 | 실제 시스템 | 설명 |
|---|---|---|
| **SP (Service Provider)** | S/4HANA | 보호할 서비스 |
| **IAS Proxy (IdP 역할)** | SAP Cloud Identity Services | S/4HANA에 인증을 제공 |
| **IAS Proxy (SP 역할)** | SAP Cloud Identity Services | Corporate IdP에 인증을 위임 |
| **Corporate IdP** | 고객사 내부 IdP (예: SingleID) | 실제 인증을 담당 |

---

### 핵심: IAS Proxy는 IdP와 SP의 이중 역할

**IAS Proxy 구조:**

```
User → S/4HANA(SP) → IAS Proxy(IdP)
                            ↓
                    IAS Proxy(SP) → Corporate IdP
```

> `↓`는 SAML 요청 방향이 아니라, **IAS Proxy 내부 처리 순서**입니다.
> 1. IAS Proxy의 **IdP 역할**이 S/4HANA의 요청을 수신
> 2. → 내부 전달
> 3. IAS Proxy의 **SP 역할**이 Corporate IdP로 요청 발송

**SAML 요청 방향 (SP → IdP):**

```
S/4HANA(SP) ──AuthnRequest──→ IAS Proxy(IdP)
IAS Proxy(SP) ──AuthnRequest──→ Corporate IdP
```

**SAML 응답 방향 (IdP → SP):**

```
Corporate IdP ──Assertion──→ IAS Proxy(SP)
IAS Proxy(IdP) ──Assertion──→ S/4HANA(SP)
```

> 두 단계 모두 **SP가 IdP로 요청을 보내고, IdP가 SP로 응답을 보내는 것**입니다.
> IAS Proxy는 한쪽에서는 IdP이고, 다른 쪽에서는 SP입니다.

**같은 IAS Proxy이지만, 상대 시스템에 따라 역할이 다릅니다.**

| 관점 | IAS Proxy의 역할 | 상대 시스템 |
|---|---|---|
| S/4HANA 입장 | **IdP** (인증 제공자) | S/4HANA는 IAS Proxy를 신뢰함 |
| Corporate IdP 입장 | **SP** (서비스 제공자) | Corporate IdP는 IAS Proxy를 신뢰함 |

> 즉, **IAS Proxy는 S/4HANA에게는 IdP이고, Corporate IdP에게는 SP입니다.** 이것이 "Proxy"의 의미입니다.

---

### 실제 인증 흐름 (SP-Initiated SSO 기준)

고객사 직원이 S/4HANA에 접근하는 경우:

```
  요청 방향 (SP → IdP)
  ┌──────────────────────────────────────────────┐
1. S/4HANA(SP) ──SAML AuthnRequest──→ IAS Proxy(IdP)
2. IAS Proxy(SP) ──SAML AuthnRequest──→ Corporate IdP
  └──────────────────────────────────────────────┘

  응답 방향 (IdP → SP)
  ┌──────────────────────────────────────────────┐
3. Corporate IdP ──SAML Assertion──→ IAS Proxy(SP)
   (User 인증 완료)
4. IAS Proxy(IdP) ──SAML Assertion──→ S/4HANA(SP)
   (Assertion 검증 + 변환 후 재발급)
  └──────────────────────────────────────────────┘

5. S/4HANA → User 접근 허용
```

**IAS Proxy가 하는 일:**
- Corporate IdP에서 온 SAML을 **검증**하고
- S/4HANA가 이해할 수 있는 SAML로 **재발급**
- 즉, **단순 pass-through가 아님** — 두 개의 독립적인 SAML 세션을 운영

---

### 설정도 "양쪽"에서 해야 하는 이유

| 설정 위치 | 누구와 누구 사이 신뢰? |
|---|---|
| **Corporate IdP 측** | Corporate IdP <-> IAS Proxy (IAS Proxy를 SP로 등록) |
| **IAS Proxy 측** | IAS Proxy <-> Corporate IdP (Corporate IdP로 등록, 메타데이터 업로드) |
| **S/4HANA 측** | S/4HANA <-> IAS Proxy (IAS Proxy를 IdP로 신뢰) |

문서에서 **Section 2**가 이 "양쪽" 설정을 다루고 있습니다.

---

## 1. Create Corporate IdP in Administration Console

Administration Console에서 새로운 Corporate Identity Provider(IdP)를 생성하거나, 기존 IdP 설정을 복사하여 생성합니다.

### Prerequisites

- `Manage Corporate Identity Providers` 역할이 부여되어 있어야 합니다.

### Context

새 Corporate IdP를 생성할 때 기본 SAML 2.0 Compliant 타입 대신 다음 중 하나를 선택할 수 있습니다:

- Single Sign-On (SAML 2.0)
- Microsoft ADFS / Entra ID (SAML 2.0)
- OpenID Connect Compliant

기존 IdP의 설정을 새 Corporate IdP에 복사할 수도 있습니다. 예: 동일한 Corporate IdP에 대해 SAML 2.0과 OpenID Connect 신뢰 구성을 별도로 유지한 후, 애플리케이션별로 프로토콜을 전환하여 마이그레이션할 수 있습니다.

> **참고**: 다른 유형의 Corporate IdP에서 설정을 복사할 경우, 프로토콜별 설정(SAML 2.0 또는 OpenID Connect)은 복사되지 않습니다. 복사 후 새로 생성된 IdP의 신뢰를 수동으로 구성하고, Enriched Token Claims 섹션의 키-값 쌍을 조정해야 합니다.

### Procedure

1. SAP Cloud Identity Services Administration Console에 로그인합니다.
2. **Identity Providers**에서 **Corporate Identity Providers** 타일을 선택합니다.
3. 왼쪽 패널의 **Create** 버튼을 선택합니다.
4. 대화 상자에서 다음 정보를 입력합니다:

| Field | Notes |
|---|---|
| **Display Name** | 필수. Identity Provider의 표시 이름입니다. |
| **Identity Provider Type** | 선택. 옵션: `SAML 2.0 Compliant` / `SAP Single Sign-On (SAML 2.0)` / `Microsoft ADFS / Entra ID (SAML 2.0)` / `OpenID Connect Compliant` |
| **Copy Settings from Identity Provider** | 선택. `Don't copy (default)` 또는 기존 Corporate IdP 목록에서 선택 |

> **주의**: `Microsoft ADFS / Entra ID` 유형의 경우, Corporate IdP의 digest algorithm이 **SHA-256**이어야 합니다.

5. 변경 사항을 저장합니다.

### Results

- `Identity provider <name of identity provider> created.` 메시지가 표시됩니다.
- 새로 생성된 IdP가 왼쪽 목록에 나타나고 선택된 상태로, 구성을 계속 진행할 수 있습니다.

---

## 2. Configure Trust with SAML 2.0 Corporate Identity Provider

Identity Authentication을 프록시로 사용하여 SAML 2.0 Corporate IdP로 인증을 위임하도록 신뢰를 구성합니다.

### Context

Identity Authentication은 SAML 2.0 IdP를 외부 인증 권한으로 사용할 수 있으며, 인증을 외부 Corporate IdP로 위임하는 프록시 역할을 합니다.

- **Service Provider에 대해**: SAML 2.0 IdP 역할
- **Corporate IdP에 대해**: SAML 2.0 Service Provider 역할

사용자가 Corporate IdP에서 인증되면, Identity Authentication 세션이 활성인 동안 동일한 Corporate IdP를 사용하는 Service Provider의 후속 인증 요청은 Corporate IdP로 전달되지 않습니다.

> **참고**: 애플리케이션에서 강제 인증(`ForceAuthn="true"`)을 요구하는 경우, SSO가 활성화되어 있더라도 사용자가 애플리케이션에 접근할 때마다 Corporate IdP에 인증해야 합니다.

---

### 2-1. Corporate Identity Provider 측에서 신뢰 구성

Identity Authentication을 Service Provider로 등록합니다.

#### Prerequisites

- Identity Authentication의 SAML 2.0 메타데이터가 필요합니다. ([Tenant SAML 2.0 Configurations](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/tenant-saml-2-0-configurations) 참조)

#### Procedure

1. Corporate IdP에 Identity Authentication을 Service Provider로 등록합니다.

> **참고**: IdP-Initiated SSO를 사용하려면 Corporate IdP 측에 구성된 Assertion Consumer Service(ACS) 엔드포인트에 `sp=<sp_name>` 파라미터를 추가해야 합니다.
>
> 예: `https://<the current ACS endpoint URL>?sp=<sp_name>`
>
> `sp`는 SSO가 수행되는 SAML 2.0 Service Provider의 이름입니다.

2. **(선택)** Corporate IdP의 SAML 2.0 메타데이터를 다운로드합니다. Identity Authentication 측 신뢰 설정에 필요합니다.

---

### 2-2. Identity Authentication 측에서 신뢰 구성

Administration Console에서 Corporate IdP와의 신뢰를 설정합니다.

#### Prerequisites

- `Manage Corporate Identity Providers` 역할이 부여되어 있어야 합니다.
- Corporate IdP에 Identity Authentication을 Service Provider로 등록한 상태여야 합니다.
- Corporate IdP의 SAML 2.0 메타데이터가 필요합니다.

#### Procedure

1. SAP Cloud Identity Services Administration Console에 로그인합니다.
2. **Identity Providers**에서 **Corporate Identity Providers** 타일을 선택합니다.
3. 구성할 Corporate IdP를 선택합니다.
4. **SAML 2.0**에서 **SAML 2.0 Configuration**을 선택합니다.
5. Corporate IdP 메타데이터 XML 파일을 업로드하거나, 메타데이터 URL을 사용하거나, 통신 설정을 수동으로 입력합니다.

> **참고**: `.xml` 확장자의 파일을 사용하세요. 메타데이터가 업로드되거나 URL이 사용되면 XML에서 파싱된 데이터로 필드가 자동으로 채워집니다. 최소 구성: Name 필드 완료, 최소 하나의 SSO 엔드포인트 추가, 서명 인증서 제공.

| Field | Description |
|---|---|
| **Metadata File** | Identity Provider의 메타데이터 XML 파일 |
| **Metadata URL** | Identity Provider 메타데이터 URL (쿼리 파라미터 포함 불가) |
| **Name** | Identity Provider의 Entity ID |
| **Single Sign-On Endpoint URL** | 인증 요청을 받는 IdP의 SSO 엔드포인트 URL |
| **Single Logout Endpoint URL** | 로그아웃 메시지를 받는 IdP의 SLO 엔드포인트 URL |
| **Binding** | SAML 프로토콜 메시지가 전송 프로토콜을 통해 전달되는 방식 |
| **Signing Certificate** | SAML 프로토콜 메시지 서명에 사용되는 base64 인코딩 인증서 (최대 2개 추가 가능) |

**추가 설정:**

| Option | Notes |
|---|---|
| **Digest Algorithm** | `SHA-1` / `SHA-256 (default)` / `SHA-512` — Microsoft ADFS/Entra ID 유형은 SHA-256 필수 |
| **Sign authentication requests** | Enabled (default) |
| **Sign single logout messages** | Enabled (default) |
| **Include scoping attribute** | Enabled (default) — SAML 2.0 요청에 Scoping 요소 포함. Microsoft ADFS/Entra ID 유형은 Disabled |

> **참고**: 여러 Corporate IdP가 있고 Identity Authentication이 프록시로 동작할 때 특정 IdP로 연결하는 링크가 필요한 경우, HTTP-Redirect를 기본 바인딩으로 사용하세요.

6. 변경 사항을 저장합니다.

### Next Steps

- 구성한 IdP를 애플리케이션의 인증 Identity Provider로 선택합니다. ([Choose Default Identity Provider for an Application](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/choose-default-identity-provider-for-an-application) 참조)

---

## 3. Configure IdP-Initiated SSO with Corporate Identity Providers

Corporate Identity Provider에서 시작하는 IdP-Initiated Single Sign-On(SSO)을 구성합니다.

### Context

이 시나리오는 직원에게 Corporate IdP를 통해 클라우드 애플리케이션에 대한 접근을 제공해야 하는 고객/파트너에게 적합합니다. Identity Authentication은 IdP 프록시로 동작하며:

- **애플리케이션에 대해**: SAML 2.0 IdP 역할
- **Corporate IdP에 대해**: SAML 2.0 Service Provider 역할

여러 Corporate IdP를 사용한 인증도 지원합니다.

### Configuration Steps 요약

| Role | System | Configuration | More Info |
|---|---|---|---|
| Application Administrator | Consumer Application | Trust | Identity Authentication을 신뢰하는 IdP로 구성 |
| Tenant Administrator | Identity Authentication Tenant | Authenticating IdPs | (선택) Trust Corporate Identity Providers 기능 구성 |
| Tenant Administrator | Identity Authentication Tenant | (선택) 사용자 속성 및 접근 제어 | (선택) Identity Federation 옵션 구성 |
| Corporate IdP Administrator | Corporate IdP | Trust, ACS Endpoint | Corporate IdP 구성 |

### Prerequisites

- Identity Authentication 테넌트에서 **IDP-Initiated SSO** 옵션이 활성화되어 있어야 합니다. (기본값: 활성화)

---

### 3-1. 애플리케이션에서 Identity Authentication을 신뢰하는 IdP로 구성

애플리케이션 관리자가 수행합니다.

- 애플리케이션에서 Identity Authentication을 신뢰하는 IdP로 구성합니다.
- Identity Authentication의 SAML 2.0 메타데이터가 필요합니다. (테넌트 관리자에게 요청)

**Next Steps**: Service Provider 메타데이터를 Identity Authentication 관리자에게 전송합니다.

---

### 3-2. Identity Authentication에서 Corporate IdP를 신뢰하도록 구성

Identity Authentication 테넌트 관리자가 수행합니다.

#### Procedure

1. Administration Console을 통해 Service Provider와 신뢰를 구성합니다. ([Configure SAML 2.0 Service Provider](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-saml-2-0-service-provider) 참조)

> **참고**: Service Provider 메타데이터에는 unsolicited SAML 응답을 처리할 수 있는 기본 ACS 엔드포인트가 포함되어야 합니다. S/4HANA의 경우 로그인 페이지 URL입니다.
>
> Trust Corporate Identity Providers 옵션을 구성하는 시나리오에서는 index가 포함된 ACS 엔드포인트도 필요합니다:
> ```xml
> <ns3:AssertionConsumerService index="1" isDefault="false"
>   Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
>   Location="https://<application URL>/protected.jsp" />
> ```

2. Corporate IdP와 신뢰를 구성합니다. ([Configure Trust with SAML 2.0 Corporate Identity Provider](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/corp-idp-configure-trust-with-saml-2-0-corporate-identity-provider) 참조)

3. Identity Provider를 선택합니다:
   - **여러 Corporate IdP**: Trust Corporate Identity Providers 기능을 구성합니다. ([Enable SSO with Corporate Identity Providers](#4-enable-sso-with-corporate-identity-providers) 참조)
   - **단일 Corporate IdP**: 구성한 IdP를 애플리케이션의 인증 IdP로 설정합니다.

#### Next Steps

- Service Provider의 Entity ID를 Corporate IdP 관리자에게 전송합니다.
  - 위치: Administration Console → Applications → `<application_name>` → Trust → SAML 2.0 Configuration → Name
- 여러 Corporate IdP 시나리오에서는 ACS 엔드포인트의 index도 함께 전송합니다.
- Identity Authentication 테넌트의 메타데이터를 Service Provider 관리자 및 Corporate IdP 관리자에게 전송합니다.

---

### 3-3. Corporate IdP 구성

Corporate IdP 관리자가 수행합니다.

#### Procedure

1. Identity Authentication을 Service Provider로 등록합니다. (Identity Authentication의 SAML 2.0 메타데이터 필요)
2. `sp=<sp_name>` 파라미터 및 (있는 경우) 애플리케이션 ACS 엔드포인트의 index를 추가합니다.
   - ACS 엔드포인트 URL 형식:
     ```
     https://<the current ACS endpoint URL>?sp=<sp_name>&index=<index_number>
     ```
   - `sp_name`: Service Provider의 Entity ID로 대체
   - `index`: 애플리케이션에 여러 ACS 엔드포인트가 있고 기본이 아닌 엔드포인트를 사용해야 할 때 필요

#### Results

- 신뢰가 구성되면 사용자는 Corporate IdP 관리자가 제공하는 링크를 통해 애플리케이션에 접근할 수 있습니다.

> **참고**: Corporate IdP가 Identity Authentication인 경우 IdP-Initiated SSO 링크 패턴:
> ```
> https://<tenant_ID>.accounts.ondemand.com/saml2/idp/sso?sp=<sp_name>[&RelayState=<sp_specific_value>&index=<index_number>]
> ```

---

### 3-4. (선택) Identity Authentication에서 추가 설정 구성

테넌트 관리자가 수행합니다.

#### Send Specific Assertion and Name ID Attributes to the Application

| Use Identity Authentication User Store | 동작 |
|---|---|
| **Disabled** | Corporate IdP에서 받은 속성을 그대로 애플리케이션으로 전송 |
| **Enabled** | Corporate IdP의 assertion에서 NameID로 작성된 고유 식별자를 가진 사용자가 Identity Authentication 사용자 저장소에 있는지 확인 |

- **사용자가 존재**: 애플리케이션에 대해 구성된 새 nameID, assertion, 기본 속성을 발급
- **사용자가 존재하지 않음**: Corporate IdP assertion의 nameID와 애플리케이션 구성에 따른 속성 전송

#### Restrict Access to Users in Identity Authentication User Store

Identity Authentication 사용자 저장소에 있는 사용자만 애플리케이션에 접근할 수 있도록 제한합니다.

1. 접근을 허용할 사용자를 프로비저닝 또는 CSV 파일로 가져옵니다.
2. Identity Federation에서 **Use Identity Authentication user store** 및 **Allow Identity Authentication users only** 옵션을 활성화합니다.

> **결과**: 사용자 저장소에 없는 사용자는 `Sorry, but you are currently not authorized for access.` 메시지를 받습니다.

#### Restrict Access to Users in Certain Groups

특정 그룹에 속한 사용자만 애플리케이션에 접근할 수 있도록 제한합니다.

1. Administration Console에서 필요한 그룹을 생성합니다.
2. 접근을 허용할 사용자를 프로비저닝 또는 CSV로 가져옵니다.
   > **주의**: CSV 파일의 Groups 열이 Administration Console에서 생성한 그룹과 일치해야 합니다.
3. Identity Federation에서 **Use Identity Authentication user store** 및 **Allow Identity Authentication users only** 옵션을 활성화합니다.
4. Corporate IdP에 그룹을 할당합니다.

> **결과**: 해당 그룹의 구성원만 인증 후 애플리케이션에 접근할 수 있습니다.

#### Apply Application Configurations

Identity Authentication이 프록시로 사용될 때 애플리케이션 구성을 적용합니다.

1. 사용자를 프로비저닝 또는 CSV로 가져옵니다.
2. Identity Federation에서 **Use Identity Authentication user store** 및 **Allow Identity Authentication users only** 옵션을 활성화합니다.
3. **Apply Application Configurations** 옵션을 활성화합니다.

---

## 4. Enable SSO with Corporate Identity Providers

테넌트 관리자가 Administration Console에서 구성된 하나, 여러 개, 또는 모든 Corporate IdP에 대한 IdP-Initiated SSO를 활성화할 수 있습니다.

### Prerequisites

- `Manage Applications` 역할이 부여되어 있어야 합니다.
- Administration Console에서 하나 이상의 Corporate IdP가 구성되어 있어야 합니다.
- **(SAML 2.0 애플리케이션)** 애플리케이션 메타데이터에 index가 포함된 ACS 엔드포인트가 추가되어 있어야 합니다:
  ```xml
  <ns3:AssertionConsumerService index="1" isDefault="false"
    Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    Location="https://<application URL>/protected.jsp" />
  ```

### Context

IdP-Initiated SSO를 사용할 때 애플리케이션은 Administration Console에 구성된 하나, 여러 개, 또는 모든 Corporate IdP를 신뢰하도록 구성할 수 있습니다. 사용자는 Corporate IdP에서 제공하는 URL을 통해 애플리케이션에 접근합니다.

### Procedure

1. SAP Cloud Identity Services Administration Console에 로그인합니다.
2. **Applications and Resources**에서 **Applications** 타일을 선택합니다.
3. 편집할 애플리케이션을 선택합니다.
4. **Trust** 탭을 선택합니다.
5. **Conditional Authentication** 섹션에서 **Trust Corporate Identity Providers** 목록 항목을 선택합니다.

| Option | Notes |
|---|---|
| **슬라이더 활성화** — 모든 구성된 Corporate IdP에 대한 SSO 허용 | 모든 Corporate IdP가 로그인에 허용됩니다. 기본값: 비활성화. 활성화 시 개별 IdP 선택 목록이 숨겨집니다. |
| **목록에서 특정 Corporate IdP 선택** | 오른쪽 상단 슬라이더가 비활성화되어 있어야 합니다. 활성화 상태면 모든 구성된 Corporate IdP가 숨겨집니다. |

6. 변경 사항을 저장합니다.

### Results

- 애플리케이션은 Administration Console에 구성된 선택된 Corporate IdP를 신뢰합니다.

---

## 5. Enrich Assertion Attributes Coming from Corporate IdP

테넌트 관리자가 Corporate IdP에서 받은 assertion 속성을 애플리케이션(Service Provider)으로 전송하기 전에 수정할 수 있습니다.

### Context

- Corporate IdP에서 Identity Authentication으로 받은 속성은 수정되어 assertion에 포함됩니다.
- OpenID Connect 애플리케이션의 경우 속성이 `id_token`에도 포함됩니다.
- SAML 2.0 및 OpenID Connect 애플리케이션 모두에서 다음을 구성할 수 있습니다:

| Type | Description |
|---|---|
| **Dynamic values** | 최대 2개의 동적 값 사용 가능. 패턴: `<prefix> ${<received_attribute>} <suffix>`. 다중 값 속성도 사용 가능. |
| **Static values** | 고정 값 |

> **제한**:
> - 두 다중 값 속성의 조합은 허용되지 않습니다. (단일 값 2개 또는 단일 값 + 다중 값 가능)
> - `sap_licenses` 속성은 Enrich Assertion Attributes 시나리오에서 지원되지 않습니다.
> - Corporate IdP당 최대 30개의 속성 추가 가능.

### Identity Federation

| Use Identity Authentication User Store | 동작 |
|---|---|
| **Disabled** | Administration Console에서 보강된 assertion 속성이 수정된 형태로 애플리케이션으로 전송됨 |
| **Enabled** | Corporate IdP를 사용하는 애플리케이션의 Default Attributes 섹션에서 수정된 속성 사용 |

### Subject Name Identifier 덮어쓰기

Enrich Assertion Attributes 옵션을 통해 Subject Name Identifier를 덮어쓸 수 있습니다.

- SAML 2.0 assertion: `NameID`로 전송
- OpenID Connect 토큰: `sub`로 전송
- `${NameID}` 변수를 사용하여 IdP에서 받은 NameID를 포함할 수 있습니다. (다른 속성에는 사용 불가)

| Attribute | Value |
|---|---|
| NameID | `<prefix>${NameID}<suffix>` |

### Procedure

1. SAP Cloud Identity Services Administration Console에 로그인합니다.
2. **Identity Providers**에서 **Corporate Identity Providers** 타일을 선택합니다.
3. 구성할 Corporate IdP를 선택합니다.
4. **Trust**에서 **Enriched Assertion Attributes** 목록 항목을 선택합니다.
5. Corporate IdP에서 받은 속성을 애플리케이션으로 전송할 새 값과 함께 추가합니다.
6. 구성을 저장합니다.

> **결과**: `Identity provider "<name of identity provider>" updated.` 메시지가 표시됩니다.

---

## 6. SingleID를 Corporate IdP로 연동 시 참고

삼성 SDS **SingleID**를 SAP Cloud Identity Services의 Corporate IdP로 연동할 때 필요한 정보를 정리합니다.

### SingleID 개요

| 항목 | 내용 |
|---|---|
| **제공사** | 삼성 SDS |
| **유형** | 클라우드 IdP (SaaS) |
| **지원 프로토콜** | SAML 2.0, OIDC |
| **기술 가이드** | [SDS Technical Guide (2023)](https://cloud.samsungsds.com/serviceportal/sub/assets/pdf/en/SDS_Technical_Guide_Integrating_authentication_between_SingleID_and_Service_Provider_using_SAML_and_OIDC_v1.0_en.pdf) |

---

### SAML 인증 흐름 (SingleID 관점)

```
1. 사용자 → SP 서비스 접근 → SAML Request → SingleID (IdP)
2. SingleID 인증 성공 → SAML Response → 브라우저 POST → SP의 ACS URL
3. SP의 ACS → SAML Response 유효성 검사 → 서비스 접근 허용
```

---

### SingleID에 IAS를 SP로 등록하는 절차

SingleID 운영자에게 다음 정보를 전달하여 IAS를 SP로 등록합니다.

| SingleID 등록 항목 | IAS에서 대응 값 | 설명 |
|---|---|---|
| **Service Name** | IAS 테넌트 식별자 | 영문 12자 이내 |
| **Service Name (KR)** | 한글 서비스 이름 | 50자 이내 |
| **Service URL (ACS)** | IAS의 ACS URL | `https://<tenant>.accounts.ondemand.com/saml2/sp/acs/...` |
| **Authentication Request Sign** | Yes/No | Yes면 IAS의 CSR 파일(SP 공개 키) 전달 |
| **수신할 사용자 정보** | First Name, Last Name, Email, Department, KnoxId 등 | 필요 속성 명시 |

> **ACS URL 확인 방법**: IAS Administration Console → **Tenant SAML 2.0 Configurations**에서 메타데이터 XML 다운로드 후 `<AssertionConsumerService>` 태그 확인

---

### SingleID에서 제공하는 연동 정보

SP 등록 후 SingleID 운영자로부터 다음 정보를 받습니다. IAS 측 신뢰 구성(2-2절)에 사용됩니다.

| 정보 | 예시 | IAS 매핑 |
|---|---|---|
| **IdpSsoTargetUrl** | SingleID SSO 타겟 URL | Single Sign-On Endpoint URL |
| **NameIdentifierFormat** | `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` | Name ID Format |
| **AuthenticationDestination** | SingleID 인증 엔드포인트 | SSO Endpoint URL |
| **TenantId** | `sds.company` | Entity ID |

---

### IdP-Initiated SSO 시 ACS URL 파라미터 추가

SingleID에서 IdP-Initiated SSO를 구성할 경우, ACS 엔드포인트에 다음 파라미터를 추가해야 합니다.

```
https://<IAS ACS endpoint URL>?sp=<sp_name>&index=<index_number>
```

| 파라미터 | 설명 |
|---|---|
| `sp` | Service Provider의 Entity ID |
| `index` | 여러 ACS 엔드포인트가 있을 때 사용 (기본이 아닌 경우) |

---

## 7. IAS ↔ 온프레미스 Corporate IdP 방화벽 설정

온프레미스 Corporate IdP를 사용하는 경우, 온프레미스 방화벽에서 SAP BTP의 아웃바운드 IP를 허용해야 합니다.

### 네트워크 흐름

| 방향 | 프로토콜 | 포트 | 설명 |
|---|---|---|---|
| IAS → Corporate IdP | HTTPS (TCP) | 443 | 메타데이터 호출, SAML AuthnRequest 전송 |
| Corporate IdP → IAS | HTTPS (TCP) | 443 | SAML Assertion 응답 (브라우저 POST 경유) |
| User → IAS | HTTPS (TCP) | 443 | SAML 리다이렉트 (브라우저) |

### 방화벽 설정 요약

| 항목 | 내용 |
|---|---|
| **방화벽 위치** | 온프레미스 IdP 측 |
| **허용 방향** | Inbound (외부 → 온프레미스 IdP) |
| **프로토콜** | TCP |
| **포트** | 443 |
| **소스 IP** | SAP BTP Neo 리전별 NAT IP |

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
3. 해당 리전의 NAT IP를 온프레미스 방화벽에 Inbound 허용 (TCP 443)

### 참고 사항

- SAP Note **3513325** 구독 권장 — NAT IP 변경 시 알림 받음
- 추가 IP가 모든 Neo 리전에 추가될 예정이므로 주기적으로 확인 필요
- 출처: [SAP Help Portal — Regions and Hosts Available for the Neo Environment](https://help.sap.com/docs/btp/sap-btp-neo-environment/regions-and-hosts-available-for-neo-environment)

---

> **출처**: SAP Help Portal — Cloud Identity Services, Corporate Identity Providers
> - [Create Corporate IdP](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/create-corporate-idp-in-administration-console?locale=en-US)
> - [Configure Trust with SAML 2.0](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/corp-idp-configure-trust-with-saml-2-0-corporate-identity-provider?locale=en-US)
> - [Configure IdP-Initiated SSO](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-idp-initiated-sso-with-corporate-identity-providers?locale=en-US)
> - [Enrich Assertion Attributes](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/enrich-assertion-attributes-coming-from-corporate-idp?locale=en-US)
> - [SingleID 기술 가이드 (삼성 SDS, 2023)](https://cloud.samsungsds.com/serviceportal/sub/assets/pdf/en/SDS_Technical_Guide_Integrating_authentication_between_SingleID_and_Service_Provider_using_SAML_and_OIDC_v1.0_en.pdf)
