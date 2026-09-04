---
layout: post
title: Knox Portal + SAP Secure Login Service 연계 검토
---

# Knox Portal + SAP Secure Login Service 연계 검토

## 1. 결론

고객이 제공한 Knox Portal 사양을 기준으로 검토한 결과, Knox Portal을
Identity Provider(IdP)로 사용하여 SAP Secure Login Service와 SAML
Federation을 구성하는 것은 기술적으로 가능합니다.

단, 구축 전 Metadata 교환, Attribute Mapping, Signature Algorithm,
Binding 방식에 대한 PoC를 권장합니다.

## 2. 아키텍처

``` text
User
  |
SAP GUI
  |
Secure Login Client
  |
SAP Secure Login Service (SP)
  |
SAML AuthnRequest
  v
Knox Portal (IdP)
  |
사용자 인증(ID/PW, MFA)
  |
SAML Assertion
  v
SAP Secure Login Service
  |
Short-lived X.509 Certificate
  v
Secure Login Client
  |
SNC
  v
SAP S/4HANA PCE
```

## 3. 호환성

  항목                Knox   SLS    결과
  ------------------- ------ ------ ------
  SAML 2.0            지원   지원   가능
  IdP                 지원   요구   가능
  Metadata            지원   요구   가능
  Assertion           지원   요구   가능
  Attribute Mapping   지원   지원   가능

## 4. 프로젝트 확인사항

-   Knox IdP Metadata(XML)
-   HTTP POST Binding
-   SHA-256 Signature
-   NameID Format
-   Attribute Mapping(Knox ID, E-mail, EPID)

## 5. 결론

현재 정보 기준으로는 Knox Portal을 Corporate IdP로 사용하는 구성이
적합합니다. 다만 SAP 공식 문서에는 Knox Portal을 명시적으로 검증한
레퍼런스는 확인되지 않았으므로 PoC를 권장합니다.

## 참고

-   SAP Help: Configure IdP-Initiated SSO with Corporate Identity
    Providers
-   SAP Help: SAP Secure Login Service for SAP GUI
