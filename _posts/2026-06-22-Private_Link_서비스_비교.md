---
layout: post
title: Private Link 서비스 비교 가이드
---

# Private Link 서비스 비교 가이드

> 주요 Hyperscaler 및 SaaS 플랫폼의 사설 연결 서비스 개요 및 비교

---

## 목차

1. [개요](#1-개요)
2. [AWS PrivateLink](#2-aws-privatelink)
3. [Azure Private Link](#3-azure-private-link)
4. [Google Cloud Private Service Connect](#4-google-cloud-private-service-connect)
5. [Salesforce Private Connect](#5-salesforce-private-connect)
6. [SAP Private Link Service](#6-sap-private-link-service)
7. [종합 비교](#7-종합-비교)
8. [참고 자료](#8-참고-자료)

---

## 1. 개요

Private Link는 각 클라우드/SaaS 플랫폼이 제공하는 **사설 연결 기술**로, 트래픽이 인터넷을 경유하지 않고 플랫폼 내부 네트워크를 통해 서비스까지 연결됩니다. 공통 목표는 다음과 같습니다:

- 인터넷 노출 제거로 공격 표면 축소
- 사설 IP 주소 기반 통신
- 규제 준수 (HIPAA, PCI DSS 등)
- NAT 게이트웨이 비용 절감

---

## 2. AWS PrivateLink

### 개념

VPC 간, AWS 서비스, AWS Marketplace 파트너 서비스까지 사설 IP로 연결. 트래픽이 인터넷을 경유하지 않음.

### 주요 구성 요소

| 구성 요소 | 역할 |
|---|---|
| **VPC Endpoint Service** (제공자) | 자신의 VPC 내 서비스를 다른 계정의 VPC에 사설로 노출 |
| **Interface VPC Endpoint** (소비자) | AWS 서비스 / 파트너 서비스 / Marketplace 솔루션에 사설 접근 |
| **Resource VPC Endpoint** | RDS 등 VPC 리소스에 사설 접근 |
| **Service Network VPC Endpoint** | VPC Lattice 서비스 네트워크 연결 |

### 특징

- 다른 AWS 계정 간 서비스 노출 가능
- AWS Marketplace에서 파트너 서비스 직접 소비
- 단일 리전 내 동작 (크로스 리전은 Transit Gateway 등 별도 구성 필요)
- NAT 게이트웨이 비용 절감 효과

---

## 3. Azure Private Link

### 개념

VNet에서 Azure PaaS, 고객 소유 서비스, Microsoft 파트너 서비스로 사설 연결. Microsoft 글로벌 네트워크 내 트래픽 유지.

### 주요 구성 요소

| 구성 요소 | 역할 |
|---|---|
| **Private Endpoint** (소비자) | VNet 내 사설 IP를 할당받은 NIC. Azure 서비스로 사설 연결 |
| **Private Link Service** (제공자) | Standard Load Balancer 뒤의 자체 서비스를 사설로 노출. 다른 VNet/테넌트의 Private Endpoint가 연결 가능 |

### 특징

- 크로스 테넌트 연결 지원 (다른 Azure AD 테넌트 간 서비스 공유)
- 서비스 연결 시 승인 워크플로우 지원
- Azure PaaS 서비스 광범위 지원 (Storage, SQL, App Service, Key Vault 등)
- Private DNS Zone과 연동하여 사설 DNS 이름 해결

---

## 4. Google Cloud Private Service Connect (PSC)

### 개념

VPC 네트워크에서 관리 서비스(Google API, 타사 서비스, 자체 서비스)로 사설 연결. Google 네트워크 내부에서만 트래픽 이동.

### 주요 구성 요소

| 구성 요소 | 역할 |
|---|---|
| **PSC Endpoint** (소비자) | VPC 내 내부 IP 주소. 관리 서비스로 사설 연결 |
| **Published Service** (제공자) | 별도 VPC에서 서비스를 사설로 발행. 소비자 연결 승인 |
| **PSC 인터페이스** | Google API 및 Google 관리 서비스 (Cloud Storage, Bigtable 등) 접근 |

### 특징

- Google API 사설 접근 지원 (Private Google Access와 상보적)
- 타사 서비스 연결 (Snowflake, MongoDB Atlas 등)
- VPC Service Controls (VPC-SC)와 함께 사용 가능 (보안 경계 + 사설 연결)
- VPC 피어링 대안으로 사용 가능
- 크로스 프로젝트, 크로스 테넌트 연결 지원

---

## 5. Salesforce Private Connect

### 개념

Salesforce Org와 AWS 간 **양방향 사설 연결**. HTTP/S 트래픽이 인터넷에 노출되지 않음. 내부적으로 **AWS PrivateLink**를 기반으로 동작합니다.

### 주요 구성 요소

| 구성 요소 | 설명 |
|---|---|
| **Inbound Connection** | AWS VPC → Salesforce (외부에서 Salesforce로 사설 호출) |
| **Outbound Connection** | Salesforce → AWS VPC (Salesforce Callout이 AWS VPC로 사설 전송) |
| **Salesforce Transit VPC** | Salesforce가 관리하는 AWS VPC. 고객 VPC와 PrivateLink로 연결 |

### 특징

- **단일 AWS 기반**: Salesforce의 Data Cloud는 AWS에 배포되어 있으며, Private Connect도 AWS PrivateLink 위에서 동작. Azure/GCP는 직접 지원 안 함
- **라이선스 기반**: Private Connect 라이선스 1개 = 양방향 (inbound + outbound) 연결 각 1개
- **리전 매핑**: Salesforce Org의 리전과 AWS 리전이 매핑됨. 지원되는 AWS 리전만 선택 가능
- **Data Cloud 확장**: Private Connect for Data Cloud로 확장되어 Data Cloud ↔ AWS Region 내 데이터 소스 간 사설 연결 지원
- **설정 방식**: Salesforce 설정 페이지에서 AWS Region 선택 → 서비스 이름 (IAM Role) 제공 → 고객 측에서 AWS VPC Endpoint 생성 → Salesforce에서 승인

### 핵심 차이점

기존 3사 Private Link가 **동일 클라우드 내** VPC/VNet 간 사설 연결이라면, Salesforce Private Connect는 **Salesforce라는 SaaS 플랫폼과 AWS 인프라 간**의 사설 연결을 제공하는 **크로스 클라우드** 서비스입니다.

---

## 6. SAP Private Link Service

### 개념

SAP BTP (Cloud Foundry / Kyma)와 Hyperscaler (Azure / AWS)의 자체 계정 내 서비스 간 **사설 연결**. 트래픽이 인터넷을 경유하지 않고 Hyperscaler 인프라 내에서만 이동합니다.

### 주요 특징

| 항목 | 내용 |
|---|---|
| **지원 IaaS** | Microsoft Azure, Amazon Web Services (AWS) |
| **지원 BTP 런타임** | Cloud Foundry, Kyma |
| **기반 기술** | Azure는 Azure Private Link, AWS는 AWS PrivateLink를 재사용 |
| **통신 방향** | BTP → Hyperscaler (현재 지원), Hyperscaler → BTP (로드맵) |
| **대체 대상** | SAP Cloud Connector 대안 (온프레미스가 아닌 Hyperscaler VM 연결) |

### 동작 방식

1. **Service Instance 생성** — SAP BTP에서 Private Link Service 인스턴스 생성 시 Hyperscaler의 서비스 식별자 (Azure: 리소스 ID, AWS: Endpoint Service 이름) 입력
2. **Private Endpoint 생성** — SAP가 BTP 환경 내부의 AWS/Azure 구성을 대신 처리. Hyperscaler 측에서 Private Endpoint 연결 승인
3. **Binding** — Service Instance를 앱에 바인딩하면 사설 엔드포인트 접근 가능
4. **Credential 제공** — User-Provided Service 등으로 Hyperscaler 서비스 인증 정보를 앱에 전달

### 주요 사용 사례

**1. SAP S/4HANA (Hyperscaler VM) ↔ BTP 사설 연결**

- 가장 일반적인 시나리오. AWS EC2 또는 Azure VM에 설치된 S/4HANA를 BTP 앱에서 사설로 접근
- Load Balancer + Endpoint Service / Private Link Service로 S/4HANA 노출 → BTP에서 사설 호스트명으로 호출
- S/4HANA가 인터넷에 노출되지 않아도 됨. Cloud Connector 없이 가능

**2. Hyperscaler 네이티브 서비스 소비**

- BTP 앱에서 AWS (Amazon S3, SQS, SES 등) 또는 Azure (Storage Account, Key Vault 등) 서비스를 사설로 사용
- 예: BTP 앱의 데이터를 Amazon S3에 사설 저장, Azure Storage Account에 통합 플로우 데이터 저장

**3. 크로스 리전 통신**

- BTP 리전과 S/4HANA 리전이 다를 경우 VPC Peering 또는 Transit Gateway로 연결

### 설정 흐름

```
SAP BTP (Cloud Foundry / Kyma)
    │
    │  SAP Private Link Service Instance
    │  (사설 엔드포인트 생성)
    ▼
┌──────────────────────────┐
│  Hyperscaler (AWS/Azure) │
│                          │
│  ┌────────────────────┐  │
│  │ Load Balancer      │  │
│  │  └→ S/4HANA / VM  │  │
│  └────────────────────┘  │
│       또는               │
│  AWS/Azure 네이티브 서비스 │
└──────────────────────────┘
```

---

## 7. 종합 비교

### 7-1. 기본 정보 비교

| 비교 항목 | AWS PrivateLink | Azure Private Link | GCP PSC | Salesforce Private Connect | SAP Private Link Service |
|---|---|---|---|---|---|
| **역할** | 클라우드 내 사설 연결 | 클라우드 내 사설 연결 | 클라우드 내 사설 연결 | SaaS ↔ AWS 크로스 클라우드 | BTP ↔ Hyperscaler 크로스 클라우드 |
| **연결 대상** | VPC ↔ AWS 서비스 / 타 계정 | VNet ↔ Azure PaaS / 자체 서비스 | VPC ↔ Google / 타사 / 자체 서비스 | Salesforce ↔ AWS VPC | SAP BTP ↔ Azure / AWS 서비스 |
| **기반 기술** | — (원천) | — (원천) | — (원천) | AWS PrivateLink | Azure Private Link / AWS PrivateLink |
| **지원 클라우드** | AWS only | Azure only | GCP only | AWS only | Azure + AWS |
| **양방향** | 단방향 | 단방향 | 단방향 | 양방향 | BTP → Hyperscaler (Hyperscaler → BTP 로드맵) |

### 7-2. 구성 요소 비교

| 비교 항목 | AWS | Azure | GCP | Salesforce | SAP |
|---|---|---|---|---|---|
| **소비자** | VPC Endpoint | Private Endpoint | PSC Endpoint | Connection | Service Instance + Binding |
| **제공자** | VPC Endpoint Service | Private Link Service | Published Service | Salesforce Transit VPC | Hyperscaler Endpoint Service / Private Link Service |
| **크로스 테넌트** | 다른 AWS 계정 | 다른 Azure AD 테넌트 | 다른 GCP 프로젝트 / 테넌트 | — | SAP BTP ↔ 고객 Hyperscaler 계정 |
| **타사 서비스** | AWS Marketplace | Azure Partner Offers | Published Services | — | — |
| **공용 API 사설 접근** | 인터페이스 엔드포인트 | Private Endpoint for PaaS | PSC 인터페이스 / Private Google Access | — | — |
| **보안 경계 연동** | VPC Flow Logs, Security Groups | NSG, Private DNS | VPC Service Controls | — | — |
| **DNS** | PrivateHostedZone | Private DNS Zone | Cloud DNS / 내부 DNS | — | 사설 호스트명 제공 |

### 7-3. 서비스 분류

| 분류 | 서비스 |
|---|---|
| **클라우드 내 사설 연결** (동일 플랫폼 내 VPC/VNet 간) | AWS PrivateLink, Azure Private Link, GCP PSC |
| **크로스 클라우드 사설 연결** (SaaS/PaaS ↔ IaaS 간) | Salesforce Private Connect (Salesforce ↔ AWS), SAP Private Link Service (SAP BTP ↔ Azure/AWS) |

---

## 8. 참고 자료

### AWS
- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink](https://aws.amazon.com/privatelink)

### Azure
- [Azure Private Link](https://azure.microsoft.com/en-us/products/private-link)
- [Private Endpoint Overview](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
- [Private Link Service Overview](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview)

### Google Cloud
- [Private Service Connect](https://cloud.google.com/private-service-connect)
- [Private Service Connect Documentation](https://docs.cloud.google.com/vpc/docs/private-service-connect)

### Salesforce
- [Private Connect Overview](https://help.salesforce.com/s/articleView?id=xcloud.private_connect_overview.htm)
- [Considerations for Private Connect with AWS](https://help.salesforce.com/s/articleView?id=xcloud.private_connect_considerations.htm)
- [Setup AWS to Salesforce PrivateLink Connection (Trailhead)](https://trailhead.salesforce.com/content/learn/modules/private-connect-inbound-connections/create-an-inbound-connection)

### SAP
- [SAP Private Link Service (Discovery Center)](https://discovery-center.cloud.sap/serviceCatalog/private-link-service?service_plan=standard&region=all&commercialModel=btpea)
- [SAP Private Link Documentation](https://help.sap.com/docs/private-link)
- [Secure connectivity with SAP Private Link service (Architecture Center)](https://architecture.learning.sap.com/docs/ref-arch/a2f89cac57)
- [How to connect SAP BTP Services with AWS Services using SAP Private Link Service (AWS Blog)](https://aws.amazon.com/blogs/awsforsap/how-to-connect-sap-btp-services-with-aws-services-using-sap-private-link-service)
