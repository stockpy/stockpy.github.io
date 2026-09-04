---
layout: post
title: SAP Alert Notification Service — Feature Scope Description 요약
categories: monitoring
---

# SAP Alert Notification Service — Feature Scope Description 요약

**문서 버전:** 1.0.0 (2024-09-17) | **공개 범위:** PUBLIC  
**원문:** https://help.sap.com/doc/2737fa955b6246e0b074bcdea5d690f8/Cloud/en-US/FSD_Alert_Notification_Service_en.pdf

---

## 1. 서비스 개요

SAP BTP (Business Technology Platform)용 Alert Notification Service는 프로바이더가 알림을 게시하고, 소비자가 구독할 수 있는 공통 API를 제공합니다. 비즈니스/운영에 관심 있을 수 있는 이벤트에 대해 실시간 알림을 자동 발송합니다.

---

## 2. 주요 기능

- **[플랫폼 이벤트 전달]**  
  SAP BTP 리소스의 정상 동작과 관련된 핵심 기술 정보 수신 (Built-In Events 참조)

- **[이벤트 필터링]**  
  관심 있는 이벤트를 선택해 구독 가능

- **[다양한 전달 채널]**  
  선호하는 통신 채널 또는 모니터링 도구로 이벤트 수신

- **[이벤트 게시/수신]**  
  단순 REST API로 자체 앱 관련 이벤트 생성·수신 (Java/Node.js 오픈소스 라이브러리 제공)

- **[멀티테넌시 지원]**  
  다중 테넌트 환경에서 공유 컴퓨트 유닛으로 운영 가능

---

## 3. 서비스 가용성

| 항목 | 내용 |
|---|---|
| 인프라 | AWS, Microsoft Azure, Google Cloud, Alibaba Cloud |
| 환경 | SAP BTP Neo, SAP BTP Cloud Foundry, Kyma |
| 언어 | 중국어, 영어, 일본어, 한국어 (관리 UI) |
| 무료 체험 | 플랫폼 무료 체험에 포함됨 |

---

## 4. 컴플라이언스 및 보안

| 항목 | 내용 |
|---|---|
| 인증 | ISO 인증서, SOC (Service Organizational Control) 감사 리포트 정기 제공 |
| 데이터 | SAP 글로벌 데이터 보호/개인정보 가이드라인 준수 |
| 접근성 | 고대비 다크 테마, UI 요소 속성/ID, 내비게이션 지원 |

---

## 5. SLA (서비스 수준 계약)

**가동 시간:** 전 지역(MENA/APJ/Europe/Americas) 제로 다운타임 보장

**Major 업그레이드 윈도우** (연 4회 이내, 각 4시간)

| 지역 | 시간 (UTC) |
|---|---|
| APJ | 토요일 07:00 |
| Europe | 금요일 14:00 |
| Americas | 금요일 22:00 |
| MENA | 토요일 04:00 |

---

## 6. 브라우저 지원

| 브라우저 | 지원 버전 |
|---|---|
| Google Chrome | 최신 버전 |
| Mozilla Firefox | ESR 및 최신 버전 |
| Microsoft Edge | 최신 Current Branch for Business (Chromium) |
| Safari | 최신 2개 버전 (macOS만) |

---

## 핵심 포인트

이 서비스는 SAP BTP 환경에서 실시간 알림/알람을 구독·게시하는 공통 플랫폼이며, REST API 기반으로 자체 앱 이벤트도 연동 가능합니다. 전 지역 제로 다운타임 SLA를 보장하고, ISO/SOC 컴플라이언스를 갖추고 있습니다.
