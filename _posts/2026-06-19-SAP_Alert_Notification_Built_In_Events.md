---
layout: post
title: SAP Alert Notification Service — Built-In Events 전체 목록
---

# SAP Alert Notification Service — Built-In Events 전체 목록

## 개요

SAP Alert Notification Service는 SAP BTP 리소스의 기술적 정보를 실시간으로 알림 받을 수 있는 서비스입니다. 구독 시 아래 Built-In Events를 구독할 수 있습니다.

**이벤트 범위 (Event Scope):** 각 이벤트에는 `ans:eventScope` 태그가 자동으로 추가되어, 해당 이벤트가 어떤 서비스 인스턴스에서 가시적인지 정의합니다.

---

## 1. Cloud Foundry Audit Events

SAP BTP Cloud Foundry 환경의 감사(Audit) 이벤트입니다.

- Cloud Foundry Audit Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/cloud-foundry-audit-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Audit Application Apply Manifest | 애플리케이션 매니페스트 적용 시 발생 |
| Audit Application Delete Request | `cf delete`로 애플리케이션 삭제 요청 시 발생 |
| Audit Application Droplet Created | 애플리케이션 droplet 생성 시 발생 |
| Audit Application Environment Shown | 애플리케이션 환경 정보 조회 시 발생 |
| Audit Application Environment Variables Shown | 애플리케이션 환경 변수 조회 시 발생 |
| Audit Application Revision Environment Variables Show | 특정 리비전의 환경 변수 조회 시 발생 |
| Audit Application Process Crash | 애플리케이션 내부 프로세스 크래시 시 발생 |
| Audit Application Process Scale | 애플리케이션 프로세스 스케일 변경 시 발생 |
| Audit User Space Auditor Add | Space Auditor 역할 추가 시 발생 |
| Audit User Space Auditor Remove | Space Auditor 역할 제거 시 발생 |
| Audit User Space Developer Add | Space Developer 역할 추가 시 발생 |
| Audit User Space Developer Remove | Space Developer 역할 제거 시 발생 |
| Audit User Space Manager Add | Space Manager 역할 추가 시 발생 |
| Audit User Space Manager Remove | Space Manager 역할 제거 시 발생 |

---

## 2. User-Provided Service Events

사용자가 제공한 서비스 인스턴스 관련 이벤트입니다.

- User-Provided Service Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/user-provided-service-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Audit User-Provided Service Instance Created | 사용자 제공 서비스 인스턴스 생성 시 발생 |
| Audit User-Provided Service Instance Deleted | 사용자 제공 서비스 인스턴스 삭제 시 발생 |
| Audit User-Provided Service Instance Updated | 사용자 제공 서비스 인스턴스 업데이트 시 발생 |

---

## 3. Edge Lifecycle Management Events

Edge 컴퓨팅 환경의 Kubernetes Pod/노드 상태 이벤트입니다.

- Edge Lifecycle Management Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/edge-lifecycle-management-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Node Not Ready | 노드가 준비되지 않은 상태일 때 발생 |
| Pod Evicted Status Reason | Pod가 추방(Evicted)되었을 때 발생 |
| Pod Failed Status Reason | Pod 실패 이유 발생 시 알림 |
| Pod Failed Scheduling Status | Pod 스케줄링 실패 시 발생 |
| Pod Failed Status Phase | Pod 실패 상태 단계 발생 시 알림 |
| Pod Node Lost Status Reason | 노드를 잃은 Pod 발생 시 알림 |

---

## 4. Multitarget Application Events

MTA(Multi-Target Application) 배포 관련 이벤트입니다.

- Multitarget Application Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/multitarget-application-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| MTA Deployment | MTA 배포 시 발생 |
| MTA Undeployment | MTA 언디플로이 시 발생 |

---

## 5. PostgreSQL on SAP BTP, Hyperscaler Option Events

Hyperscaler PostgreSQL 서비스의 리소스 사용량 이벤트입니다.

- PostgreSQL on SAP BTP, Hyperscaler Option Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/postgresql-on-sap-btp-hyperscaler-option-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| CPU Limit | CPU 사용량 한도 도달 시 발생 |
| Memory Limit | 메모리 사용량 한도 도달 시 발생 |
| Max Connections | 최대 연결 수 도달 시 발생 |
| Storage Full | 저장소 용량 가득 차면 발생 |

---

## 6. Redis on SAP BTP, Hyperscaler Option Events

Hyperscaler Redis 서비스의 리소스 사용량 이벤트입니다.

- Redis on SAP BTP, Hyperscaler Option Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/redis-on-sap-btp-hyperscaler-option-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| CPU Limit | CPU 사용량 한도 도달 시 발생 |
| Memory Limit | 메모리 사용량 한도 도달 시 발생 |
| Evictions | 메모리 부족으로 데이터 추방 발생 시 알림 |

---

## 7. SAP HANA Cloud Service Database Events (HDB)

SAP HANA Cloud 데이터베이스의 상세 모니터링 이벤트입니다.

- SAP HANA Cloud Service Database Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-hana-cloud-service-database-events?locale=en-US

### 7.1 세션 및 연결

| 이벤트 | 설명 |
|---|---|
| HDB Admission Control Reject Count | Admission Control에 의해 거부된 세션 요청 수 확인 |
| HDB Admission Control Queue Size | Admission Control 대기열에 있는 세션 요청 수 확인 |
| HDB Open Connection | HANA DB에 대한 오픈된 외부 연결 수가 한도의 특정 비율에 도달했을 때 알림 |
| HDB Blocked Transaction | 장시간 블로킹 상황 알림 |
| HDB Transaction Deadlock | 트랜잭션 데드락 발생 여부 확인 |

### 7.2 메모리 및 저장소

| 이벤트 | 설명 |
|---|---|
| HDB Memory Usage | 지난 10분 평균 기반 높은 메모리 사용량 알림 |
| HDB Out Of Memory | Out-of-Memory 이벤트 발생 여부 알림 |
| HDB CPU Usage | 지난 10분 평균 기반 높은 CPU 사용량 알림 |
| HDB Disk Usage | 디스크 사용량 비율 알림 |
| HDB Disk Auto Upsize | 자동 저장소 용량 증가 상태 알림 |
| HDB Savepoint Duration | 장시간 실행 중인 세이브포인트 작업 알림 |
| HDB Audit Log Table Total Memory Usage | 테이블 기반 감사 로깅 DB 테이블이 소비하는 메모리 할당 한도 비율 알림. 테이블이 너무 커지면 DB 가용성에 영향 |
| HDB Estimated Memory Size | 호스트의 추정 메모리 크기 확인. 모든 Column Store 데이터가 메모리에 로드될 경우 Out-of-Memory 상황으로 이어질 수 있음 |
| HDB Cached View Size | 캐시된 뷰가 차지하는 메모리 양 알림 |

### 7.3 Row Store

| 이벤트 | 설명 |
|---|---|
| HDB RS Table Total Memory Usage | 서비스가 사용하는 Row Store의 현재 메모리 크기 알림 |
| HDB RS Table Growth | Row Store 테이블 성장률 알림 |
| HDB RS Fragmentation | Row Store 단편화 확인 |

### 7.4 Column Store

| 이벤트 | 설명 |
|---|---|
| HDB CS Table Total Memory Usage | 개별 Column Store 테이블 전체(모든 열 및 내부 구조 포함)가 소비하는 메모리 할당 한도 비율 알림 |
| HDB CS Table Main Memory Usage | 개별 Column Store 테이블의 메인 저장소가 소비하는 메모리 할당 한도 비율 알림 |
| HDB CS Table Delta Size | Column 테이블의 비정상적으로 큰 델타 저장소 알림 |
| HDB CS Table Record Count | 비 파티션 Column Store 테이블의 레코드 수 알림 (비 파티션 테이블 최대 21억 행 제한) |
| HDB CS Table Record Count Include List Filtered | 비 파티션 Column Store 테이블 수 (Include-type 테이블) |
| HDB CS Partition Record Count | Column Store 파티션 테이블의 레코드 수 알림 (파티션당 최대 21억 행 제한) |
| HDB CS Partition Record Count Filtered Include List | Column Store 파티션 테이블의 레코드 수 (Include-type 테이블만 확인) |
| HDB CS Unload | Column Store 테이블에서 메모리에서 언로드된 열 수. 성능 문제 지표 |

### 7.5 NSE Buffer Cache

| 이벤트 | 설명 |
|---|---|
| HDB NSE Buffer Cache Full | 버퍼 캐시가 올바르게 구성되었는지 확인. Out-of-buffers 이벤트는 현재 워크로드를 처리하기에 버퍼 캐시가 충분하지 않음을 의미 |
| HDB NSE Buffer Cache Unload Threshold | 버퍼 캐시의 과도한 언로드 임계값 확인. 100% 이상 설정 시 자동으로 100%로 낮춤 |

### 7.6 인증서 및 보안

| 이벤트 | 설명 |
|---|---|
| HDB Own Certificate Expiration | 자체 인증서 또는 체인 인증서 만료 임박 또는 만료 알림 |
| HDB Trusted Certificate Expiration | 신뢰 인증서 만료 임박 또는 만료 알림 |
| HDB User Password Expiration | 구성된 비밀번호 정책대로 비밀번호가 곧 만료될 DB 사용자 알림 |
| HDB User Group Connect Restriction | 사용자 그룹 연결 제한으로 실패한 연결 시도 수 알림 |
| HDB Customer Managed Key Revoked | CCEK(고객 관리 키) 철회로 SAP HANA Database 인스턴스 종료 시 알림 |

### 7.7 성능 및 모니터링

| 이벤트 | 설명 |
|---|---|
| HDB Long Running Statement | 장시간 실행 중인 SQL 문 알림 |
| HDB Long Idle Cursor | 장시간 실행 중/대기 중인 커서 알림 |
| HDB Long Serializable Transaction | 장시간 직렬화 가능 트랜잭션 알림 |
| HDB Plan Cache Hit Ratio | 플랜 캐시 히트 비율이 너무 낮은지 확인 |
| HDB Python Trace Active | Python 트레이스 활성화 여부 및 지속 시간 알림 (성능 영향) |
| HDB Delta Merge Fail | 테이블의 델타 병합 실행 성공 여부 확인 |
| HDB SDQ Long Running Task | 장시간 실행 중인 작업 식별 |
| HDB Catalog Consistency | `_SYS_STATISTICS.Collector_Global_Catalog_Consistency`에서 감지된 오류 및 영향받는 객체 수 확인 |

### 7.8 구성 및 설정

| 이벤트 | 설명 |
|---|---|
| HDB Configuration Parameter Requires Restart | 구성 변경 후 재시작이 필요한 서비스 여부 확인 |
| HDB Configuration Parameter Unsupported Value | 구성 파라미터가 지원되지 않는 값으로 설정된 경우 알림 |
| HDB Deprecated Feature Usage | 마지막 간격에서 비활성화(Deprecated)된 기능이 사용되었는지 확인 |
| HDB Client Version | 필요한 최소 클라이언트 타입 버전 및 업데이트 필요 여부 알림 |
| HDB Client Unsupported | 지원되지 않는 클라이언트 타입 버전 사용 시 알림 |

### 7.9 DI (Deployment Infrastructure)

| 이벤트 | 설명 |
|---|---|
| HDB DI User Login Enabled | SAP HANA DI 기술 사용자에게 SQL 접근이 활성화되었는지 확인 |
| HDB DI Import Privilege Grant | SAP HANA DI 컨테이너 가져오기 기능이 활성화되어 있고, 가져오기 권한이 DB 사용자 또는 역할에 부여되었는지 확인 |
| HDB DI Support Privilege Grant | SAP HANA DI 지원 권한이 DB 사용자 또는 역할에 부여되었는지 확인 |
| HDB DI Usergroup User Admin Enabled | USER ADMIN 시스템 권한을 가진 사용자가 SAP HANA DI 사용자 그룹을 관리할 수 있는지 확인 |

### 7.10 리플리케이션

| 이벤트 | 설명 |
|---|---|
| HDB Asynchronous Table Replication Availability | 테이블 리플리케이션 관련 오류 메시지 모니터링 |
| HDB Remote Table Replication Availability | 테이블의 리플리케이션 상태가 비활성화되었는지 알림 |
| HDB Replication Log Status | 리플리케이션 로그 상태가 비활성화되었는지 확인 |

### 7.11 SDI (Smart Data Integration)

| 이벤트 | 설명 |
|---|---|
| HDB SDI Agent Availability | 에이전트가 비활성화된 시간 확인 |
| HDB SDI Agent Memory Usage | 에이전트의 총 메모리 사용 비율 확인 |
| HDB SDI Remote Source Applier Delay | 원격 소스의 변경 데이터 적용 지연 확인 |
| HDB SDI Remote Source Change Data Time | Data Provisioning Server가 소스 DB에서 마지막으로 변경 데이터를 받은 후 경과 시간 확인 |
| HDB SDI Remote Subscription Exception | 원격 구독 및 원격 소스의 최근 예외 확인 |
| HDB SDI Remote Subscription Queue Time | 원격 구독이 대기 상태에 있는 시간 확인 |

### 7.12 동기 복제 (Synchronous Replication)

| 이벤트 | 설명 |
|---|---|
| HDB Synchronous Instance Replication Source In Restricted Availability Zone | 소스 노드가 제한된 가용성 영역에 있는지 확인 |
| HDB Synchronous Instance Replication Takeover Across Availability Zones | 다른 가용성 영역으로의 인계가 트리거되었는지 확인 |
| HDB Synchronous Instance Replication Sources In Different Availability Zones | HANA 소스 컨테이너가 서로 다른 가용성 영역에 있는지 확인 |

### 7.13 인스턴스 및 마이그레이션

| 이벤트 | 설명 |
|---|---|
| HDB Free-Tier Instance Expiration | Free-Tier HANA 인스턴스가 중지되고 만료 및 삭제까지 15일 미만 남은 경우 알림 |
| HDB Inactive Service | 비활성 서비스 알림 |
| HDB Instance Cloning | TEMPLATE_RECOVERY 작업 실패로 인한 인스턴스 복제 실패 알림 |
| HDB Instance Move Pending | 다음 예약된 유지보수 창期间 중 HANA 인스턴스 이전 알림 |
| HDB Last Infrastructure Operation | 마지막 인프라 작업 실패 알림 |
| HDB Long Running Service Start Stop | 느린 서비스 시작 및 정지 식별 |
| HDB Migration Finished | Catalog 또는 Data 마이그레이션 단계 또는 전체 HANA Cloud 마이그레이션 완료 알림 |
| HDB Migration Online Phase | Downtime-optimized Migration to SAP HANA Cloud의 Online Phase 중 상태 변경 알림 |
| HDB Migration Progress | Catalog 또는 Data 마이그레이션 단계의 진행률 알림 |
| HDB Migration Record Count Check Finished | 레코드 수 확인 완료 알림 |
| HDB Restarted Service | 마지막 확인 이후 재시작된 서비스 알림 |
| HDB Tenant Count | 인스턴스의 테넌트 수 확인 |
| HDB Table Consistency | 일관성 검사 실행에서 감지된 오류 수 알림 |
| HDB Template Recovery [Deprecated] | HANA 인스턴스의 템플릿 복구 작업 실패 알림 (**비활성화됨**) |
| HDB Test Alert | 통계 서버의 알림 처리 테스트용 이벤트 |
| HDB Uncommitted Write Transaction | 장시간 커밋되지 않은 쓰기 트랜잭션 알림 |
| HDB Version Patch Available | HANA 인스턴스에 새로운 DB 패치 버전이 이용 가능해지면 알림 |
| HDB Version Upgrade Available | HANA 인스턴스에 새로운 DB 업그레이드 버전이 이용 가능해지면 알림 |
| HDB End Of Maintenance | HANA 인스턴스가 유지보수 종료(End of Maintenance)에 도달했는지 알림 |

---

## 8. SAP HANA Cloud Data Lake Events

- SAP HANA Cloud Data Lake Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-hana-cloud-data-lake-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Data Lake Free-Tier Instance Expiration | Free-Tier Data Lake 인스턴스 만료 임박 (15일 미만) 알림 |
| Data Lake HDB Compatibility | Data Lake Relational Engine 테이블이 SAP HANA DB와 호환되지 않는 컬럼 타입 포함 시 알림 |
| Data Lake Running Out of Main Space | Data Lake 인스턴스 주요 공간(IQ_SYSTEM_MAIN/user_main) 부족 임박 알림 |
| Data Lake Running Out of Temporary DBSpace | Data Lake 인스턴스 임시 공간(IQ_SYSTEM_TEMP) 부족 임박 알림 |
| Data Lake User Locked | Data Lake 사용자 잠금 알림 |

---

## 9. SAP BTP HANA Service Events

SAP BTP HANA Service(구 SAP HANA, cloud) 관련 이벤트입니다.

- SAP BTP HANA Service Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-btp-hana-service-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| SAP BTP HANA Service Notification | DB 운영자가 수동으로 트리거. 고객에게 DB 관련 정보(예: 새 DB 버전 이용 가능) 알림 |
| SAP BTP HANA Service Notification Action | 운영자가 수동으로 트리거. 고객 조치 필요 시 사용(예: DB 시스템 버전 업데이트, 재시작 필요) |

> HDB 이벤트와 유사한 모니터링 이벤트가 제공됩니다.

---

## 10. SAP BTP Destination Service Events

- SAP BTP Destination Service Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-btp-destination-service-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| SAP BTP Destination Service Expiring Certificate Notification | Destination 서비스의 인증서 만료 임박 알림 |

---

## 11. SAP Cloud Transport Management Events

클라우드 전송 관리 서비스의 이벤트입니다.

- SAP Cloud Transport Management Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-cloud-transport-management-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| SAP Cloud Transport Storage Quota Usage | 파일 업로드 중 파일 저장소 할당량 사용량이 85% 임계값을 초과할 때 발생 |
| SAP Cloud Transport Node Import Job Deactivated | 반복적인 실패로 인해 SAP Cloud Transport Management의 가져오기 작업이 비활성화되면 발생 |
| SAP Cloud Transport Management Import Started | SAP Cloud Transport Management 가져오기가 시작되면 발생 |
| SAP Cloud Transport Management Import Finished | SAP Cloud Transport Management 가져오기가 완료되면 발생 |
| SAP Cloud Transport Request Added | SAP Cloud Transport Management 요청이 추가되면 발생 |

---

## 12. SAP Integration Suite Events

- SAP Integration Suite Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-api-management-events?locale=en-US&state=PRODUCTION&version=Cloud

| 이벤트 | 설명 |
|---|---|
| API Management Alert Anomaly Detected | API Management에서 이상(anomaly) 감지 시 알림 |
| API Management Alert Training Completed | 이상 감지 모델 학습 완료 시 알림 |

---

## 13. SAP Job Scheduling Service Events

- SAP Job Scheduling Service Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-job-scheduling-service-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| SAP Job Scheduling Service Job Execution | 작업(Job) 실행 시 알림 |
| SAP Job Scheduling Service Task Execution | 작업(Task) 실행 시 알림 |

---

## 14. SAP Mobile Services Events

- SAP Mobile Services Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-mobile-services-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| SAP Mobile Services Application Alert | 모바일 서비스 애플리케이션 알림 발생 시 알림 |
| SAP Mobile Services Release Notice | 새 버전 이용 가능 시 릴리스 공지 알림 |

---

## 15. SAP Notification Service Events

- SAP Notification Service Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-notification-service-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Failed Notification Delivery Due to Invalid Destination | `SAP_Business_Notifications_Mail` 또는 `Identity_Authentication_Connectivity_IDS` Destination 설정 오류로 알림 전달 실패 시 알림 |

---

## 16. SAP Secure Login Service for SAP GUI Events

- SAP Secure Login Service for SAP GUI Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-secure-login-service-for-sap-gui-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Custom Certificate Authority Issue | 커스텀 인증서 기관 문제 발생 시 알림 |
| Certificate Subject Name Error | 인증서 주제 이름 오류 발생 시 알림 |

---

## 17. SAP Variant Configuration and Pricing Events

Configuration and Pricing Services (CPS) 관련 이벤트입니다.

- SAP Variant Configuration and Pricing Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-variant-configuration-and-pricing-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| CPS Agent Status | CPS 에이전트 상태 알림 |
| CPS Delta Replication Check Status | CPS 델타 리플리케이션 확인 상태 알림 |
| CPS Replication Check Status | CPS 리플리케이션 확인 상태 알림 |
| CPS Storage Limit Checks | CPS 저장소 한도 확인 알림 |
| CPS Support Event | CPS 지원 이벤트 알림 |
| CPS Test Event | CPS 테스트 이벤트 알림 |

---

## 18. SAPUI5 Adaptation Project Events

- SAPUI5 Adaptation Project Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sapui5-adaptation-project-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| SAPUI5 Adaptation Project Basis Application Updated | SAPUI5 적응 프로젝트의 기본 애플리케이션 업데이트 시 알림 |

---

## 19. Usage Data Management Events

- Usage Data Management Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/usage-data-management-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Usage Data Management Remaining Credits | 클라우드 크레딧 잔액 변경 시 알림 (하루 2회, 변경 없을 시 생략) |

---

## 20. SAP Cloud Management Service Events

- SAP Cloud Management Service Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-cloud-management-service-events?locale=en-US

| 이벤트 | 설명 |
|---|---|
| Budget Threshold Exceedance | 예산 임계값 초과 시 알림 |

---

## 21. SAP Alert Notification Service Events

SAP Alert Notification 서비스 자체의 이벤트입니다.

- SAP Alert Notification Service Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-alert-notification-service-events?locale=en-US

---

## 22. Service Route Binding Events

서비스 라우트 바인딩 관련 이벤트입니다.

- Service Route Binding Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/service-route-binding-events?locale=en-US

---

## 23. [[Deprecated] Resource Quota Utilization]

> **비활성화됨.** 리소스 할당량 사용량 이벤트는 더 이상 사용되지 않습니다.

---

## 24. Extension Events

SAP Alert Notification Service에 추가 통합을 통해 이벤트를 공급할 수 있는 확장 기능입니다. 사전 통합 단계가 필요합니다.

- Extension Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/extension-events?locale=en-US

| 통합 대상 | 설명 |
|---|---|
| Custom Application | SAP Alert Notification REST API를 사용하여 자체 애플리케이션 관련 이벤트를 생성 및 소비 |
| CloudEvents Publishers | CloudEvents 기반 이벤트를 SAP Alert Notification 서비스 인스턴스에 공급 |
| Dynatrace | Dynatrace 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| Amazon Simple Notification Service (SNS) | Amazon SNS 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| Amazon CloudWatch | Amazon CloudWatch 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| Microsoft Azure Monitor | Azure Monitor 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| Kibana (Open Distro for Elasticsearch) | Kibana Alerting 기능에서 생성된 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| Kibana (X-Pack) | Kibana 알림 프레임워크에서 생성된 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| OpenSearch (OpenSearch Dashboards) | OpenSearch Dashboards에서 생성된 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| SAP Cloud Logging Service | SAP Cloud Logging 서비스의 OpenSearch에서 생성된 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| SAP Automation Pilot | SAP Alert Notification 서비스 이벤트를 SAP Automation Pilot 자동화 프로세스의 트리거로 사용 및 이벤트 생성 구성 |
| Prometheus Alertmanager | Prometheus에서 생성된 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| Google Cloud Platform (GCP) Operations | Google Cloud Operations(구 Stackdriver) 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| Grafana Alert Notifications | Grafana Alert 알림을 SAP Alert Notification 서비스 인스턴스에 공급 |
| SAP Continuous Integration and Delivery | SAP CI/CD 이벤트를 SAP Alert Notification 서비스 인스턴스에 공급 |
| SAP Cloud Integration | SAP Cloud Integration 이벤트를 SAP Alert Notification 서비스 인스턴스에 공급 |

---

## 참고

- 이벤트 구독 방법: [Managing Subscriptions](https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/managing-subscriptions)
- 전체 이벤트 목록: [Built-In Events](https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/built-in-events?locale=en-US)
- 이벤트 요청: SAP BTP Feature Request를 통해 새 이벤트 요청 가능
