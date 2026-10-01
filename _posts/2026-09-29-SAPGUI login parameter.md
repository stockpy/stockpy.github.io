---
layout: post
title: SAP 로그인 관련 프로파일 파라미터 정리 (암호/로그인 실패/GUI/중복 로그인)
categories: SAPGUI
---

# SAP 로그인 관련 프로파일 파라미터 정리
> 암호 주기·길이·복잡성, 로그인 실패, GUI 연결 수, 중복 로그인 관련 프로파일 파라미터를 정리한 문서입니다.
> 근거: SAP Help Portal "Profile Parameters for Logon and Password (Login Parameters)"
> <https://help.sap.com/docs/ABAP_PLATFORM_NEW/c6e6d078ab99452db94ed7b3b7bbcccf/4ac3f18f8c352470e10000000a42189c.html>
> SAP Help Portal "rdisp/tm_max_no", "Profile Parameter Changes (ABAP Server Infrastructure)"
>
> **참고**: "권장되는 값"은 SAP 공식 권장값이 아닌 일반적인 보안 모범 사례(best practice) 기준입니다. 시스템 환경에 맞게 조정하세요.

---

| 번호 | 파라미터명 | default값 | 권장되는 값 | 파라미터 설명 |
|---|---|---|---|---|
| 1. 암호 주기 | `login/password_expiration_time` | 0 (제한 없음) | 60~90 | 암호 유효기간(일). 0이면 자동 만료 없음. Security Policy 속성: PASSWORD_CHANGE_INTERVAL |
| 1. 암호 주기 | `login/password_change_waittime` | 1 | 1 | 암호를 변경한 후 다시 변경할 수 있는 최소 대기일(1~1000일). 속성: MIN_PASSWORD_CHANGE_WAITTIME |
| 1. 암호 주기 | `login/password_history_size` | 5 | 5~10 | 재사용이 금지되는 과거 암호 저장 개수(1~100). 속성: PASSWORD_HISTORY_SIZE |
| 1. 암호 주기 | `login/password_max_idle_productive` | 0 (체크 비활성) | 0 또는 90 | 사용자가 직접 설정한 암호가 미사용 상태로 유효한 최대 기간(일). 속성: MAX_PASSWORD_IDLE_PRODUCTIVE |
| 1. 암호 주기 | `login/password_max_idle_initial` | 0 (체크 비활성) | 0 또는 90 | 관리자가 부여한 초기 암호의 미사용 유효 최대 기간(일). 속성: MAX_PASSWORD_IDLE_INITIAL |
| 2. 암호 길이 | `login/min_password_lng` | 6 | 10 이상 | 암호의 최소 길이(3~40). Security Policy 속성: MIN_PASSWORD_LENGTH |
| 3. 암호 복잡성 | `login/min_password_digits` | 0 | 1 | 암호에 포함해야 할 숫자(0-9) 최소 개수. 속성: MIN_PASSWORD_DIGITS |
| 3. 암호 복잡성 | `login/min_password_letters` | 0 | 1 | 영문(A-Z) 최소 개수. 속성: MIN_PASSWORD_LETTERS |
| 3. 암호 복잡성 | `login/min_password_lowercase` | 0 | 1 | 소문자 최소 개수. 속성: MIN_PASSWORD_LOWERCASE |
| 3. 암호 복잡성 | `login/min_password_uppercase` | 0 | 1 | 대문자 최소 개수. 속성: MIN_PASSWORD_UPPERCASE |
| 3. 암호 복잡성 | `login/min_password_specials` | 0 | 1 | 영문·숫자 외의 문자(특수문자) 최소 개수. 속성: MIN_PASSWORD_SPECIALS |
| 3. 암호 복잡성 | `login/min_password_diff` | 1 | 3 | 신규 암호와 기존 암호가 달라야 하는 최소 문자 수(1~40). 속성: MIN_PASSWORD_DIFFERENCE |
| 4. 로그인 실패 | `login/fails_to_user_lock` | 5 | 3~5 | 실패한 로그인 시도 몇 회 후에 사용자를 잠금하는지(1~99). 속성: MAX_FAILED_PASSWORD_LOGON_ATTEMPTS |
| 4. 로그인 실패 | `login/fails_to_session_end` | 3 | 3 | 로그인 실패 몇 회 후에 해당 로그인 시도를 더 이상 허용하지 않는지(1~99). `login/fails_to_user_lock` 값보다 작게 설정 |
| 4. 로그인 실패 | `login/failed_user_auto_unlock` | 0 (자동 해제 없음) | 1 | 로그인 실패로 잠긴 사용자가 자정에 자동으로 잠금 해제되는지 여부(0/1). 속성: PASSWORD_LOCK_EXPIRATION |
| 5. GUI 연결 수 | `rdisp/tm_max_no` | 1000 | 환경에 맞게 조정 | 인스턴스당 허용되는 최대 사용자 수 (GUI/RFC/HTTP 모든 로그인 포함). 변경 시 인스턴스 재시작 필요 |
| 5. GUI 연결 수 | `rdisp/max_alt_modes` | 6 (2020 FPS01부터 16) | 6~16 | 한 로그인 세션에서 열 수 있는 최대 GUI 윈도우(모드) 수 |
| 5. GUI 연결 수 | `rdisp/gui_auto_logout` | 0 (2020 FPS01부터 3600) | 300~3600 | SAP GUI 연결의 최대 유휴 시간(초). 유휴 초과 시 자동 로그아웃 |
| 6. 중복 로그인 | `login/disable_multi_gui_login` | 0 (허용) | 1 (권장) | 동일 클라이언트에서 동일 사용자의 여러 다이얼로그 로그인을 차단(0/1) |
| 6. 중복 로그인 | `login/multi_login_users` | (빈 값) | 필요 시 지정 | 중복 로그인이 허용되는 사용자 목록. `login/disable_multi_gui_login = 1`일 때 예외 처리 |

## 중복 로그인 관련 파라미터 간 관계

`login/disable_multi_gui_login = 1`은 **"동일 클라이언트에 동일 사용자의 2번째 다이얼로그 로그인"** 만 차단합니다. 다른 클라이언트로 로그인하거나 배치(백그라운드) 세션이 생성되는 것은 막지 않습니다.

**참고: 사용자당 세션 총수를 직접 제한하는 프로파일 파라미터는 존재하지 않습니다** (SAP Community 확인). 중복 로그인 제어는 아래 두 파라미터 조합으로 수행합니다.

```
disable_multi_gui_login = 1
  → "같은 클라이언트에 같은 사용자가 다이얼로그로 2번째 로그인"만 차단
  → 다른 클라이언트 로그인, 배치 세션은 그대로 허용
rdisp/max_alt_modes
  → 한 세션(로그인) 안의 GUI 윈도우(모드) 수 제한
  → 로그인 횟수 제한과는 무관
```

즉, 두 파라미터는 서로 다른 레벨에서 작동합니다:

1. `disable_multi_gui_login` — **로그인 자체를 막을 것인가** (동일 클라이언트 다이얼로그 한정)

2. `max_alt_modes` — **세션 내 윈도우 수 제한**

---

## 적용 시 참고사항

- **Security Policy 우선**: 암호 관련 파라미터(`login/min_password_lng` 등)는 Security Policy 속성으로 대체 가능하며, Security Policy가 설정된 경우 사용자별로 세밀한 제어가 가능

- **설정 위치**: 시스템 전체 적용은 DEFAULT.PFL, 인스턴스별 적용은 인스턴스 프로파일 (RZ10)

- **활성화**: 대부분의 파라미터는 시스템 재시작 후 적용 (동적 변경 가능 파라미터는 RZ11에서 즉시 변경 가능)

- **릴리스별 default값 변경**: `rdisp/max_alt_modes`(6→16)와 `rdisp/gui_auto_logout`(0→3600)의 default값은 ABAP Platform 2020 FPS01부터 변경됨. 시스템 릴리스에 따라 RZ11에서 확인 필요

- **사용자당 세션 수 제한**: 사용자당 세션 총수를 직접 제한하는 프로파일 파라미터는 존재하지 않음. 중복 로그인 제어는 `login/disable_multi_gui_login` + `login/multi_login_users` 조합으로 수행
