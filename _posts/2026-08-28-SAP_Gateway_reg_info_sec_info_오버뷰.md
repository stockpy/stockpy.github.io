---
layout: post
title: SAP Note 1305851 — SAP Gateway reg_info 및 sec_info 오버뷰
categories: general
---

# SAP Note 1305851 정리

> SAP Gateway 보안 파일 reg_info 및 sec_info 개요 노트
>
> **작성일**: 2026-08-28
> **출처**: SAP Note 1305851

---

## 목차

1. [개요](#개요)
2. [reg_info 파일](#reg_info-파일)
3. [sec_info 파일](#sec_info-파일)
4. [프로필 파라미터](#프로필-파라미터)
5. [파일 형식](#파일-형식)
6. [acl_mode 설정](#acl_mode-설정)
7. [관련 SAP Note](#관련-sap-note)

---

## 개요

SAP Note 1305851은 SAP Gateway의 외부 프로그램 등록 및 실행을 제어하는 보안 파일(`reg_info`, `sec_info`)에 대한 **오버뷰 노트**입니다.

Gateway는 외부 프로그램(예: SLD, SAProuter, Standalone Gateway 등)이 SAP 시스템에 등록되거나 실행되는 것을 제어합니다.

---

## reg_info 파일

**목적**: 외부 프로그램의 Gateway **등록(Registration)**을 제어

- 외부 시스템이 SAP Gateway에 프로그램을 등록할 수 있는지 여부 결정
- 파일이 존재하지만 빈 규칙이면 → 모든 외부 시스템 등록 차단
- 허용할 시스템/프로그램을 명시적 규칙으로 정의

**예시**: SAP SLD 시스템이 ABAP 시스템에 `SLD_UC`, `SLD_NUC` 프로그램 등록 시 reg_info에서 허용 규칙 필요

---

## sec_info 파일

**목적**: 외부 프로그램의 **실행(Launching)**을 제어

- 권한 없는 외부 프로그램 실행 방지
- Gateway를 통해 실행 가능한 프로그램 명시적 허용

---

## 프로필 파라미터

| 파라미터 | 설명 | 기본값 |
|---|---|---|
| `gw/reg_info` | reg_info 파일 경로 | `$(DIR_DATA)/reginfo` |
| `gw/sec_info` | sec_info 파일 경로 | `$(DIR_DATA)/secinfo` |
| `gw/acl_mode` | ACL 모드 (0 또는 1) | — |

파일이 존재하지 않으면 해당 보안 체크가 활성화되지 않습니다.

---

## 파일 형식

- 첫 번째 줄: `#VERSION=2` (필수)
- 각 줄은 하나의 완전한 규칙 (여러 줄로 분할 불가)
- 규칙은 호스트/IP, 프로그램명 등을 명시

---

## acl_mode 설정

| 값 | 동작 |
|---|---|
| `0` | ACL 제한 없음 — 외부 프로그램 등록/실행 unrestricted |
| `1` | ACL 제한 적용 — reg_info/sec_info 규칙 준수 필요 |

---

## 관련 SAP Note

| Note | 제목 |
|---|---|
| 1408081 | Basic settings for reg_info and sec_info |
| 1069911 | GW: Changes to the ACL list of the gateway (reginfo) |
| 614971 | GW: Changes to the ACL list of the gateway (secinfo) |
| 1689663 | GW: Simulation mode for reg_info and sec_info |
| 1425765 | Generating sec_info reg_info |
| 1444282 | gw/reg_no_conn_info settings |
| 910919 | Setting up Gateway logging |

---

> **출처**: SAP Note 1305851 — Overview note: reg_info and sec_info
> **작성일**: 2026-08-28
