---
layout: post
title: rdisp/max_wprun_time 기본값·권장값과 대체 파라미터 검토
categories: general
---

# rdisp/max_wprun_time 기본값·권장값과 대체 파라미터 검토

## 개요

대화형 워크프로세스의 최대 실행시간을 제어하는 프로필 파라미터 `rdisp/max_wprun_time`은 SAP NetWeaver 7.40 SP2 (Kernel 722)에서 세션 우선순위(session priority)가 도입되면서 우선순위별 3개 파라미터로 대체되었고, ABAP Platform 2020 (SAP_BASIS 7.55 / Kernel 781)부터 커널에서 완전히 제거되었습니다.

근거 Note: **2918906** (Deprecation of Profile Parameter "rdisp/max_wprun_time"), **25528** (Configuration of maximum work process runtime), **2001276** (Changed configuration as of 7.40 SP2)

---

## 기본값과 권장값

| 항목 | 값 |
|---|---|
| 기본값 | **600초 (10분)** |
| 권장값 | **설정하지 말 것 (프로필에서 제거)** |

Note 25528은 "이 파라미터는 더 이상 사용하지 말라"고 명시하고, 7.40 이후 시스템에서는 obsolete 파라미터가 사용 중인지 확인해 필요 시 제거하라고 안내합니다.

---

## 대체 파라미터 (7.40 SP2 이후)

세션 우선순위별 최대 실행시간을 제어하는 3개 파라미터입니다.

| 파라미터 | 기본값 | 적용 우선순위 |
|---|---|---|
| `rdisp/scheduler/prio_high/max_runtime` | **11분 (660초)** | HIGH — 일반 대화 요청 |
| `rdisp/scheduler/prio_normal/max_runtime` | **60분** | MEDIUM — RFC, HTTP 요청 |
| `rdisp/scheduler/prio_low/max_runtime` | **무제한** | LOW — 배경 작업에서 트리거된 RFC 등 |

### 우선순위 구분 기준

- **HIGH**: 디스패처로 직접 분배된 일반 대화 요청
- **NORMAL**: RFC, HTTP 요청
- **LOW**: 배경 작업(background job)에서 트리거된 RFC 호출은 자동으로 LOW로 실행

---

## SAP 권장사항 3가지 (Note 2918906)

### 1. 옛 파라미터와 새 파라미터 모두 제거

> "SAP recommends to **remove both** the old parameter `rdisp/max_wprun_time` **and** the new parameters `rdisp/scheduler/prio_*/max_runtime` **from all profiles**."

옛 파라미터 하나만 제거하는 것이 아니라, 3개 우선순위별 파라미터까지 포함해 **전부 제거하고 기본값으로 운영**하라는 것입니다.

제거 후 특정 애플리케이션에서 `TIME_OUT` short dump가 발생하면:
- 근본 해결: ABAP 개발자에게 개발자 대응(아래 참고)을 요청
- 임시 조치(workaround): `rdisp/scheduler/prio_high/max_runtime` 또는 `rdisp/scheduler/prio_normal/max_runtime` 중 **하나만** 구(舊) 실행시간 한도로 설정

### 2. 기본값이 대부분의 요구를 충족한다는 전제

> "SAP assumes that the **default values** of the new profile parameter should meet the needs of most customers and their applications."

기본값(11분/60분/무제한)이 대부분의 고객·애플리케이션 요구를 충족한다고 SAP가 전제합니다. 다만 1909 이전 호환성 규칙(옛 파라미터가 새 값을 덮어쓰는 동작) 때문에 이 이점이 손실되는 경우가 많다고 지적하며:

> "a switch from an old profile ... to the new priority-based defaults **might cause incompatibilities if the ABAP code of the application is not well written**."

옛 프로필에서 새 기본값으로 전환할 때, ABAP 코드가 잘 작성되지 않은 애플리케이션은 비호환 문제가 발생할 수 있다고 경고합니다.

### 3. `prio_low/max_runtime`는 절대 설정하지 말 것

> "the profile parameter `rdisp/scheduler/prio_low/max_runtime` **should never be set**. Its default value already allows unlimited uninterrupted run-time for batch-like dialog requests."

LOW 우선순위 파라미터는 **절대 설정하지 말라**고 명시하며, 기본값이 이미 배치형(batch-like) 대화 요청에 대해 **무제한 실행시간**을 허용하기 때문이라고 설명합니다.

---

## 호환성 규칙 (중요)

| 릴리스 | 동작 |
|---|---|
| **ABAP Platform 1909 (SAP_BASIS 7.54)까지** | `rdisp/max_wprun_time`이 **명시적으로** 설정되어 있으면 그 값이 3개 새 파라미터를 **모두 덮어씀** → 우선순위별 세분화 효과 무효화 |
| **ABAP Platform 2020 (SAP_BASIS 7.55 / Kernel 781)부터** | `rdisp/max_wprun_time`이 커널에서 **완전히 제거**. 업그레이드 절차가 프로필에서 자동 삭제 |

즉, 1909 이하 시스템에서 옛 파라미터가 남아 있으면 새 파라미터를 아무리 세분화해도 의미가 없습니다.

---

## 개발자 측 대응 (TIME_OUT 재발 방지, Note 2918906)

- **NORMAL로 강등**: 장시간 코드를 비동기 RFC로 실행 — `CALL FUNCTION ... DESTINATION 'NONE' STARTING NEW TASK ...`
- **LOW로 강등**:
  ```abap
  cl_session_admin=>reduce_task_priority( ).
  call function ... destination 'NONE' starting new task ...
  cl_session_admin=>reset_task_priority( ).
  ```
  (메소드는 ABAP Platform 1909 / SAP_BASIS 7.54 이상에서 사용 가능)
- **우선순위 강등이 불가능한 경우**:
  - `max_runtime = cl_runtime=>get_my_max_runtime( ).` 으로 현재 세션의 실행시간 한도 조회
  - 한도 도달 전에 `WAIT UP TO 0 SECONDS` 같은 sync point로 타임아웃 시계 리셋

---

## 실무 결론

기존 시스템에서 `rdisp/max_wprun_time = 600` 같은 설정이 남아 있으면, 우선순위별 세분화(11분/60분/무제한)의 이점을 전혀 못 받는 상태입니다. **삭제 후 기본값으로 운영**을 권장하며, 삭제 전에는 11분을 초과하는 대화형 트랜잭션 등 애플리케이션 실행시간에 영향이 없는지 확인이 필요합니다.

---

## 참고 Note

- **Note 2918906** — Deprecation of Profile Parameter "rdisp/max_wprun_time" (권장사항 본문 출처)
- **Note 25528** — Configuration of maximum work process runtime - parameter rdisp/max_wprun_time
- **Note 2001276** — Changed configuration as of 7.40 SP2 (7.40 SP2 커널의 파라미터 변경 사항)
