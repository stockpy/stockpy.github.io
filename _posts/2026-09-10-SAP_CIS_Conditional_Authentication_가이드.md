---
layout: post
title: SAP Cloud Identity Services — 조건부 인증 (Conditional Authentication) 가이드
categories: sso
---

# SAP Cloud Identity Services — 조건부 인증 (Conditional Authentication) 가이드

## 개요

조건부 인증은 애플리케이션 접근 시 사용자 속성에 따라 인증 제공자(IdP)를 다르게 라우팅하는 규칙을 정의하는 기능입니다. 사원은 사내 IdP, 고객은 Identity Authentication으로 분리하는 등 **혼합 인증 환경**에서 사용됩니다.

**모든 사용자가 단일 Corporate IdP로 인증하는 구조라면 이 기능은 필요 없습니다.** Default Identity Provider를 Corporate IdP로 설정하는 것으로 충분합니다.

---

## 규칙 조건

| 조건 | 설명 |
|---|---|
| 이메일 도메인 | `@company.com` 등 도메인별 구분 |
| 사용자 유형 | 사원 / 고객 등 |
| 사용자 그룹 | 그룹 기반 구분 |
| IP 범위 | CIDR 표기법 (`192.168.0.0/16`) |

---

## 동작 방식

- 규칙은 **우선순위** 순으로 평가되며, 첫 번째 매칭 규칙이 적용되고 나머지는 무시됨
- 모든 규칙과 매칭되지 않으면 **기본 IdP**로 인증됨
- 규칙은 **기본 IdP가 Identity Authentication**일 때만 정의 가능

---

## 중요 사항

- 규칙이 **IP 범위만** 포함하면 로그인 화면에서 사용자 식별자를 입력하지 않고 바로 평가됨
- IP 범위 외 조건이 있으면 사용자 식별자 입력 후 평가됨
- 기본 IdP를 Corporate IdP로 변경하면 기존 규칙은 **무시됨**
- 여러 Corporate IdP를 사용하고 Identity Authentication으로 떨어지는 것을 막으려면 가장 낮은 우선순위에 `0.0.0.0/0` 캐치올 규칙을 추가해야 함

---

## 설정 절차

1. 관리 콘솔 로그인
2. **Applications and Resources** > **Applications** > 대상 애플리케이션 선택
3. **Trust** 탭 > **Conditional Authentication** 선택
4. 규칙 추가 / 수정 / 삭제 / 우선순위 변경
5. 기본 IdP 선택 (Identity Authentication이어야 함)
6. 저장

---

## 예시

| 규칙 | IdP | 이메일 도메인 | 사용자 유형 | 사용자 그룹 |
|---|---|---|---|---|
| 1 | 사내 Corporate IdP | `companya.com` | — | — |
| 기본 | Identity Authentication | — | — | — |

- `@companya.com` 사원 → 사내 IdP로 인증
- 그 외 사용자 → Identity Authentication으로 인증

---

## 조건부 인증 흐름

### Corporate IdP 인증 경로

```
1. 사용자 → 애플리케이션 접속
2. 애플리케이션 → Identity Authentication으로 리다이렉트 (규칙 확인)
3. Identity Authentication → 사용자 식별자 입력 요청
4. 사용자 → 식별자 입력
5. Identity Authentication → 규칙 매칭 → Corporate IdP로 리다이렉트 (login_hint 포함)
6. 사용자 → Corporate IdP에서 인증
7. Corporate IdP → 인증 성공 → 애플리케이션 접근
```

### Identity Authentication 인증 경로

```
1. 사용자 → 애플리케이션 접속
2. 애플리케이션 → Identity Authentication으로 리다이렉트 (규칙 확인)
3. Identity Authentication → 사용자 식별자 입력 요청
4. 사용자 → 식별자 입력
5. Identity Authentication → 규칙 미매칭 → Identity Authentication 로그인 화면
6. 사용자 → 비밀번호 입력
7. Identity Authentication → 인증 성공 → 애플리케이션 접근
```

---

## 적용 여부 판단

| 시나리오 | 필요 여부 |
|---|---|
| 사원은 Corporate IdP, 고객은 Identity Authentication으로 혼합 인증 | 필요 |
| IP 범위에 따라 IdP를 다르게 라우팅 | 필요 |
| 모든 사용자가 단일 Corporate IdP로 인증 | 불필요 |

---

## 참조

- [SAP Help — Configure Conditional Authentication for an Application](https://help.sap.com/docs/cloud-identity-services/cloud-identity-services/configure-conditional-authentication-for-application?locale=en-US)
