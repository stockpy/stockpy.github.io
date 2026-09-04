---
layout: post
title: SAP Alert Notification Service — Basis Consultant 관점 요약
---

# SAP Alert Notification Service — Basis Consultant 관점 요약

**원문:** https://community.sap.com/t5/c-khhcw49343/SAP+Alert+Notification+service+for+SAP+BTP/pd-p/73555000100800001401  
**참고:** https://help.sap.com/docs/alert-notification/sap-alert-notification-for-sap-btp

---

## 1. 이 서비스는 무엇인가?

SAP BTP에서 제공하는 중앙 집중식 알림 서비스입니다. SAP HANA Cloud를 포함한 다양한 SAP BTP 서비스의 이벤트/알림을 구독하고, 이메일/웹훅/Slack 등으로 실시간 알림을 받을 수 있습니다.

기존 SAP HANA의 내부 알림 시스템과 별개로, BTP 레이어에서 운영하는 알림 플랫폼입니다.

---

## 2. Basis 관점에서 중요한 Built-In 이벤트 (SAP HANA Cloud)

SAP HANA Cloud 데이터베이스에서 구독 가능한 주요 이벤트 목록:

**[성능]**
- HDB CPU Usage
- HDB Admission Control Reject Count
- HDB Admission Control Queue Size

**[저장소]**
- HDB Cached View Size
- HDB Audit Log Table Total Memory Usage

**[복제]**
- HDB Asynchronous Table Replication Availability

**[트랜잭션]**
- HDB Blocked Transaction

**[설정]**
- HDB Configuration Parameter Requires Restart
- HDB Configuration Parameter Unsupported Value

**[일관성]**
- HDB Catalog Consistency

**[클라이언트]**
- HDB Client Version
- HDB Client Unsupported

---

## 3. 설정 방법 (5단계)

1. **Subaccount에서 서비스 활성화**  
   SAP BTP Cockpit → Subaccount → Services → Alert Notification 서비스 인스턴스 생성

2. **Actions 정의**  
   알림 전달 채널 설정 (이메일, Slack, 웹훅, ServiceNow 등)

3. **Conditions 정의**  
   어떤 이벤트를 모니터링할지 필터링  
   예: `eventType = CPIIntegrationFlowExecutionFailure`  
   HANA 예: HDB CPU Usage > 80% 지속 시 알림

4. **Subscription 생성**  
   Actions + Conditions를 조합해 구독 등록

5. **(선택) 자체 이벤트 게시**  
   REST API로 자체 앱에서 커스텀 이벤트 발송 가능 (Java/Node.js SDK 제공)

---

## 4. Basis Consultant에게 유용한 포인트

- **[HANA 모니터링 대체/보완]**  
  기존 SAP HANA Cockpit 알림 + BTP Alert Notification으로 중복 모니터링 가능

- **[중앙 집중화]**  
  여러 BTP 서비스(HANA Cloud, Integration Suite, Destination 등) 알림을 한 곳에서 관리

- **[SLA]**  
  전 지역 제로 다운타임 보장

- **[자동 알림]**  
  수동 체크 없이 실시간 알림으로 다운타임/성능 문제 조기 감지

- **[통합]**  
  ServiceNow, Jira 등 기존 ITSM 도구와 웹훅 연동 가능

- **[무료 체험]**  
  BTP 무료 체험에 포함

---

## 5. 기존 HANA 알림과의 차이

| 항목 | 기존 HANA 내부 알림 | BTP Alert Notification |
|---|---|---|
| 범위 | 단일 HANA 시스템 | 전체 BTP 환경 |
| 전달 채널 | 제한적 | 이메일, Slack, 웹훅 등 |
| 커스터마이징 | 제한적 | 조건/액션/구독 자유 조합 |
| 운영 주체 | Basis 담당자 직접 관리 | BTP 플랫폼 서비스 |

---

## 핵심 결론

SAP Basis Consultant라면 HANA Cloud 환경에서 시스템 성능/가용성 알림을 중앙에서 관리하고, 기존 ITSM 도구와 연동하려면 이 서비스를 활용하는 것이 좋습니다. 여러 BTP 서비스를 운영하는 경우, 각 서비스별 알림을 한 곳으로 통합할 수 있어 모니터링 효율이 크게 향상됩니다.
