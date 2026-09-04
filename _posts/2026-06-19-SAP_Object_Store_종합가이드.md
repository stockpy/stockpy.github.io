---
layout: post
title: SAP Object Store on SAP BTP — 종합 가이드
categories: btp
---

# SAP Object Store on SAP BTP — 종합 가이드

## 1. 개요

SAP Object Store는 SAP BTP에서 **blob/객체 저장 및 관리**를 위한 관리형 서비스입니다. 서비스 인스턴스를 프로비저닝하면 내부적으로 계정, 리소스 관리, 보안 설정 등을 자동으로 처리합니다.

- **지원 IaaS**: Azure Blob Storage, Amazon S3, Google Cloud Storage, SAP Cloud Infrastructure
- **지원 환경**: Cloud Foundry, Kyma
- **핵심 가치**: 다중 클라우드 지원, SAP BTP 통합, 인프라 관리 최소화

---

## 2. 핵심 기능

| 기능 | 설명 |
|---|---|
| **간편하고 안전한 접근** | 저장소 버킷/컨테이너 생성 후 앱에 보안 자격 증명 전달 |
| **높은 가용성** | 중단 없는 지속적 저장소 접근 보장 |
| **높은 내구성** |底层 기술의 스토리지 복제를 통한 내구성 보장 |
| **확장성** | Cloud Foundry 및 Kyma 앱에서 사용 가능한 확장형 저장소 |

---

## 3. IaaS별 추가 기능

| 기능 | 정의 | Azure | AWS | GCP | SAP Cloud Infra |
|---|---|---|---|---|---|
| Object Versioning | 객체 수정/삭제 시 이전 버전 유지 | ✓ | ✓ | ✓ | ✓ |
| Custom Encryption (KMS) | 고객 관리 키를 사용한 데이터 암호화 | ✓ | ✓ | ✓ | — |
| Server Access Logging | 저장소 접근 요청 이력 기록 및 추적 | — | ✓ | — | — |
| Prevent Accidental Deletion | 버킷/객체의 실수 삭제 방지 (Lock/대기) | ✓ | ✓ | ✓ | ✓ |
| Cross-Origin Resource Sharing (CORS) | 타 도메인 스크립트의 저장소 접근 허용 | — | ✓ | — | ✓ |
| Object Level Tagging | 객체별 키-값 태그를 통한 분류/정책 적용 | ✓ | ✓ | — | — |
| Continuous Backup / Point-in-Time Restore | 지속 백업 및 과거 특정 시점 복원 | — | ✓ | — | — |
| Zone-Redundant Storage (ZRS) | 다중 가용성 존 복제를 통한 내구성 향상 | ✓ | — | — | — |
| Role-Based Bindings/Service Keys | 역할 기반 최소 권한 접근 제한 | ✓ | ✓ | ✓ | — |

---

## 4. Service Plans & Entitlements

- **Service Plan**: `standard`
- **Entitlements**: `object-store` (standard plan) — 서비스 인스턴스 생성용
- **Prerequisites**: SAP BTP Application Runtime, Subaccount, Entitlement 할당 완료

---

## 5. 가격 정책 (Commercial Model별)

| Commercial Model | 설명 |
|---|---|
| **BTPEA** (BTP Enterprise Agreement) | 소비량 기반 과금. 100 GB 블록 단위. Google Cloud 기준 EUR 12.00/월/100 GB. IaaS별 차이 존재. Free Tier 사용 가능. |
| **PAYG** (Pay-As-You-Go) | 사용량 기반 과금. Discovery Center에서 모델 전환 시 가격 확인 필요. |
| **CPEA** (Cloud Platform Enterprise Agreement) | 기존 볼륨 라이선싱 모델. 장기 계약 시 단가 유리. |

**공통 구매 조건**: 100 GB 블록 단위, 계약 기간 3~12개월, 자동 갱신

> **참고**: 정확한 가격 비교는 Discovery Center Pricing 탭에서 Commercial Model을 전환하며 확인 필요.

---

## 6. SAP Object Store vs AWS S3

| 구분 | AWS S3 (Direct) | SAP Object Store on SAP BTP |
|---|---|---|
| **관리 위치** | AWS Console / CLI | SAP BTP Cockpit |
| **접근 권한** | AWS IAM Policy 직접 관리 | SAP BTP Service Key / Binding |
| **다중 클라우드** | AWS 전용 | AWS, Azure, GCP, SAP Cloud Infra |
| **코드 의존성** | AWS SDK 종속 | 표준 API 사용 시 백엔드 변경 영향 최소화 |
| **기능 범위** | S3 전체 기능 | SAP이 제공하는 Subset 기능 |
| **결제 대상** | AWS | SAP |
| **통합성** | 별도 설정 필요 | SAP BTP 서비스와 즉시 바인딩 |

**SAP Object Store 사용 시**: SAP BTP 앱 개발, 다중 클라우드 고려, 인프라 관리 최소화, SAP 제품 연동
**AWS S3 직접 사용 시**: S3 고급 기능 활용, BTP 외부 사용, AWS 직접 결제 유리, AWS 생태계 연동

---

## 7. 개발 및 보안

### 개발
- Cloud Foundry 앱 빌딩 가이드 제공
- IaaS별 Java 코드 스니펫 제공
- Instance Sharing 기능 지원

### 보안
- Cross-Origin Resource Sharing 보안 가이드라인
- Object Store Access Key 보안
- 데이터 암호화 전략
- 데이터 보호 및 개인정보 보호

### 백업/복원
- 기본 구성 및 백업/복원 절차
- AWS 기준 Continuous Backup + Point-in-Time Restore 지원

---

## 8. 관련 문서 구조

```
Object Store on SAP BTP (Help Portal)
├── What Is Object Store
├── What's New / Feature Availability
├── Object Store Concepts
├── Service Plans and Entitlements
├── Configuring Parameters
├── Object Store on Azure (8 하위 항목)
├── Object Store on AWS (10 하위 항목)
├── Object Store on GCP (6 하위 항목)
├── Object Store on SAP Cloud Infrastructure (4 하위 항목)
├── Development
├── Security (4 하위 항목)
├── Backup and Restore
├── Instance Sharing
├── Service Requests
└── FAQ
```

---

## 9. 참조 링크

- **제품 페이지**: https://www.sap.com/products/technology-platform/object-store.html
- **Help Portal**: https://help.sap.com/docs/object-store/object-store-service-on-sap-btp/what-is-object-store
- **Discovery Center**: https://discovery-center.cloud.sap/serviceCatalog/object-store
