---
layout: post
title: SAP HANA Cloud Service Database Events (HDB) — 전체 목록
categories: monitoring
---

# SAP HANA Cloud Service Database Events (HDB) — 전체 목록

## 개요

SAP HANA Cloud 데이터베이스의 상세 모니터링 이벤트입니다.

- SAP HANA Cloud Service Database Events: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-hana-cloud-service-database-events?locale=en-US

---

## HDB 이벤트 목록

| 이벤트 | 설명 |
|---|---|
| HDB Admission Control Reject Count | Admission Control에 의해 최근 거부된 세션 요청 수 확인 |
| HDB Admission Control Queue Size | Admission Control 대기열에 있는 세션 요청 수 확인 |
| HDB Asynchronous Table Replication Availability | 테이블 리플리케이션 관련 오류 메시지 모니터링 |
| HDB Audit Log Table Total Memory Usage | 테이블 기반 감사 로깅 DB 테이블이 소비하는 메모리 할당 한도 비율 알림. 테이블이 너무 커지면 DB 가용성에 영향 |
| HDB Blocked Transaction | 장시간 블로킹 상황 알림 |
| HDB Cached View Size | 캐시된 뷰가 차지하는 메모리 양 알림 |
| HDB Catalog Consistency | `_SYS_STATISTICS.Collector_Global_Catalog_Consistency`에서 감지된 오류 및 영향받는 객체 수 확인 |
| HDB Client Version | 필요한 최소 클라이언트 타입 버전 및 업데이트 필요 여부 알림 |
| HDB Client Unsupported | 지원되지 않는 클라이언트 타입 버전 사용 시 알림 |
| HDB Configuration Parameter Requires Restart | 구성 변경 후 재시작이 필요한 서비스 여부 확인 |
| HDB Configuration Parameter Unsupported Value | 구성 파라미터가 지원되지 않는 값으로 설정된 경우 알림 |
| HDB CPU Usage | 지난 10분 평균 기반 높은 CPU 사용량 알림 |
| HDB CS Partition Record Count Filtered Include List | Column Store 파티션 테이블의 레코드 수 (Include-type 테이블만 확인) |
| HDB CS Partition Record Count | Column Store 파티션 테이블의 레코드 수 알림 (파티션당 최대 21억 행 제한) |
| HDB CS Table Delta Size | Column 테이블의 비정상적으로 큰 델타 저장소 알림 |
| HDB CS Table Main Memory Usage | 개별 Column Store 테이블의 메인 저장소가 소비하는 메모리 할당 한도 비율 알림 |
| HDB CS Table Record Count | 비 파티션 Column Store 테이블의 레코드 수 알림 (비 파티션 테이블 최대 21억 행 제한) |
| HDB CS Table Record Count Include List Filtered | 비 파티션 Column Store 테이블 수 (Include-type 테이블) |
| HDB CS Table Total Memory Usage | 개별 Column Store 테이블 전체(모든 열 및 내부 구조 포함)가 소비하는 메모리 할당 한도 비율 알림 |
| HDB CS Unload | Column Store 테이블에서 메모리에서 언로드된 열 수. 성능 문제 지표 |
| HDB Customer Managed Key Revoked | CCEK(고객 관리 키) 철회로 SAP HANA Database 인스턴스 종료 시 알림 |
| HDB Delta Merge Fail | 테이블의 델타 병합 실행 성공 여부 확인 |
| HDB Deprecated Feature Usage | 마지막 간격에서 비활성화(Deprecated)된 기능이 사용되었는지 확인 |
| HDB DI User Login Enabled | SAP HANA DI 기술 사용자에게 SQL 접근이 활성화되었는지 확인 |
| HDB DI Import Privilege Grant | SAP HANA DI 컨테이너 가져오기 기능이 활성화되어 있고, 가져오기 권한이 DB 사용자 또는 역할에 부여되었는지 확인 |
| HDB DI Support Privilege Grant | SAP HANA DI 지원 권한이 DB 사용자 또는 역할에 부여되었는지 확인 |
| HDB DI Usergroup User Admin Enabled | USER ADMIN 시스템 권한을 가진 사용자가 SAP HANA DI 사용자 그룹을 관리할 수 있는지 확인 |
| HDB Disk Usage | 디스크 사용량 비율 알림 |
| HDB Disk Auto Upsize | 자동 저장소 용량 증가 상태 알림 |
| HDB Estimated Memory Size | 호스트의 추정 메모리 크기 확인. 모든 Column Store 데이터가 메모리에 로드될 경우 Out-of-Memory 상황으로 이어질 수 있음 |
| HDB End Of Maintenance | HANA 인스턴스가 유지보수 종료(End of Maintenance)에 도달했는지 알림 |
| HDB Free-Tier Instance Expiration | Free-Tier HANA 인스턴스가 중지되고 만료 및 삭제까지 15일 미만 남은 경우 알림 |
| HDB Inactive Service | 비활성 서비스 알림 |
| HDB Instance Cloning | TEMPLATE_RECOVERY 작업 실패로 인한 인스턴스 복제 실패 알림 |
| HDB Instance Move Pending | 다음 예약된 유지보수 창期间 중 HANA 인스턴스 이전 알림 |
| HDB Last Infrastructure Operation | 마지막 인프라 작업 실패 알림 |
| HDB Long Idle Cursor | 장시간 실행 중/대기 중인 커서 알림 |
| HDB Long Running Service Start Stop | 느린 서비스 시작 및 정지 식별 |
| HDB Long Running Statement | 장시간 실행 중인 SQL 문 알림 |
| HDB Long Serializable Transaction | 장시간 직렬화 가능 트랜잭션 알림 |
| HDB Memory Usage | 지난 10분 평균 기반 높은 메모리 사용량 알림 |
| HDB Migration Finished | Catalog 또는 Data 마이그레이션 단계 또는 전체 HANA Cloud 마이그레이션 완료 알림 |
| HDB Migration Online Phase | Downtime-optimized Migration to SAP HANA Cloud의 Online Phase 중 상태 변경 알림 |
| HDB Migration Progress | Catalog 또는 Data 마이그레이션 단계의 진행률 알림 |
| HDB Migration Record Count Check Finished | 레코드 수 확인 완료 알림 |
| HDB NSE Buffer Cache Full | 버퍼 캐시가 올바르게 구성되었는지 확인. Out-of-buffers 이벤트는 현재 워크로드를 처리하기에 버퍼 캐시가 충분하지 않음을 의미 |
| HDB NSE Buffer Cache Unload Threshold | 버퍼 캐시의 과도한 언로드 임계값 확인. 100% 이상 설정 시 자동으로 100%로 낮춤 |
| HDB Out Of Memory | Out-of-Memory 이벤트 발생 여부 알림 |
| HDB Open Connection | HANA DB에 대한 오픈된 외부 연결 수가 한도의 특정 비율에 도달했을 때 알림 |
| HDB Own Certificate Expiration | 자체 인증서 또는 체인 인증서 만료 임박 또는 만료 알림 |
| HDB Plan Cache Hit Ratio | 플랜 캐시 히트 비율이 너무 낮은지 확인 |
| HDB Python Trace Active | Python 트레이스 활성화 여부 및 지속 시간 알림 (성능 영향) |
| HDB RS Fragmentation | Row Store 단편화 확인 |
| HDB RS Table Growth | Row Store 테이블 성장률 알림 |
| HDB RS Table Total Memory Usage | 서비스가 사용하는 Row Store의 현재 메모리 크기 알림 |
| HDB Remote Table Replication Availability | 테이블의 리플리케이션 상태가 비활성화되었는지 알림 |
| HDB Replication Log Status | 리플리케이션 로그 상태가 비활성화되었는지 확인 |
| HDB Restarted Service | 마지막 확인 이후 재시작된 서비스 알림 |
| HDB Savepoint Duration | 장시간 실행 중인 세이브포인트 작업 알림 |
| HDB SDI Agent Availability | 에이전트가 비활성화된 시간 확인 |
| HDB SDI Agent Memory Usage | 에이전트의 총 메모리 사용 비율 확인 |
| HDB SDI Remote Source Applier Delay | 원격 소스의 변경 데이터 적용 지연 확인 |
| HDB SDI Remote Source Change Data Time | Data Provisioning Server가 소스 DB에서 마지막으로 변경 데이터를 받은 후 경과 시간 확인 |
| HDB SDI Remote Subscription Exception | 원격 구독 및 원격 소스의 최근 예외 확인 |
| HDB SDI Remote Subscription Queue Time | 원격 구독이 대기 상태에 있는 시간 확인 |
| HDB SDQ Long Running Task | 장시간 실행 중인 작업 식별 |
| HDB Synchronous Instance Replication Source In Restricted Availability Zone | 소스 노드가 제한된 가용성 영역에 있는지 확인 |
| HDB Synchronous Instance Replication Takeover Across Availability Zones | 다른 가용성 영역으로의 인계가 트리거되었는지 확인 |
| HDB Synchronous Instance Replication Sources In Different Availability Zones | HANA 소스 컨테이너가 서로 다른 가용성 영역에 있는지 확인 |
| HDB Table Consistency | 일관성 검사 실행에서 감지된 오류 수 알림 |
| HDB Template Recovery [Deprecated] | HANA 인스턴스의 템플릿 복구 작업 실패 알림 (**비활성화됨**) |
| HDB Tenant Count | 인스턴스의 테넌트 수 확인 |
| HDB Test Alert | 통계 서버의 알림 처리 테스트용 이벤트 |
| HDB Transaction Deadlock | 트랜잭션 데드락 발생 여부 확인 |
| HDB Trusted Certificate Expiration | 신뢰 인증서 만료 임박 또는 만료 알림 |
| HDB Uncommitted Write Transaction | 장시간 커밋되지 않은 쓰기 트랜잭션 알림 |
| HDB User Group Connect Restriction | 사용자 그룹 연결 제한으로 실패한 연결 시도 수 알림 |
| HDB User Password Expiration | 구성된 비밀번호 정책대로 비밀번호가 곧 만료될 DB 사용자 알림. 기술 사용자의 경우 비밀번호 수명 확인을 비활성화하는 것이 권장됨 |
| HDB Version Patch Available | HANA 인스턴스에 새로운 DB 패치 버전이 이용 가능해지면 알림 |
| HDB Version Upgrade Available | HANA 인스턴스에 새로운 DB 업그레이드 버전이 이용 가능해지면 알림 |

---

## 참고

- 전체 이벤트 목록: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/sap-hana-cloud-service-database-events?locale=en-US
- 이벤트 구독 방법: https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp/managing-subscriptions?locale=en-US
