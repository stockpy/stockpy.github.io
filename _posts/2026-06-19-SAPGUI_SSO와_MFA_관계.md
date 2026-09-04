---
layout: post
title: SAPGUI SSO (Kerberos/Logon Ticket)와 MFA의 관계
---

# SAPGUI SSO (Kerberos/Logon Ticket)와 MFA의 관계

**결론:** Kerberos와 Logon Ticket 방식 자체는 **MFA(다중 인증)가 아닙니다.**

두 가지 방식이 존재한다고 해서 MFA가 되는 것은 아니며, 보안의 관점에서는 여전히 **단일 인증(Single Factor)**으로 분류됩니다.

---

## 1. MFA의 정의 (3가지 요소 중 2가지 이상 필요)

MFA(Multi-Factor Authentication)는 다음 세 가지 요소 중 **최소 두 가지**를 조합해야 성립합니다.

1.  **알고 있는 것 (Something you know):** 비밀번호, PIN
2.  **가지고 있는 것 (Something you have):** 스마트폰, USB 킨, 스마트카드
3.  **본인인 것 (Something you are):** 지문, 얼굴 인식, 홍채

**Kerberos나 Logon Ticket 방식**은 대부분 **"알고 있는 것(비밀번호)"** 하나만으로 인증이 완료됩니다.

---

## 2. "방식 2가지" ≠ "인증 요소 2가지"

질문하신 내용처럼 "Kerberos"와 "Logon Ticket"이 두 가지 프로토콜로 존재한다고 해서 MFA가 되는 것은 아닙니다.

*   **비유:** 문 열는 방식에 "열쇠"와 "카드"가 있다고 해서, 문이 두 번 잠겨 있는 것은 아닙니다. 둘 다 "입증 수단"일 뿐입니다.
*   **실무:** 사용자는 보통 Kerberos **또는** Logon Ticket 중 하나의 프로토콜을 사용하여 로그인합니다. 두 가지를 동시에 사용하여 "비밀번호 + 티켓"으로 인증하는 것이 아닙니다.

---

## 3. 티켓(Ticket)은 "증명서"일 뿐 "인증"이 아님

*   **Kerberos:** 사용자가 Windows에 비밀번호를 입력하면(1차 인증), Windows가 티켓을 발급합니다. SAPGUI는 이 티켓을 보여주기만 합니다.
*   **Logon Ticket:** 사용자가 Portal에 비밀번호를 입력하면(1차 인증), Portal이 쿠키(티켓)를 줍니다. SAPGUI는 이 쿠키를 보여주기만 합니다.

즉, **티켓은 "비밀번호를 입력했다는 증명서"**일 뿐, 별도의 보안 요소가 추가되지 않습니다.

---

## 4. 언제 SAPGUI SSO가 MFA가 될까요?

SSO의 **출처(Source)**에서 MFA가 적용되면, SAPGUI도 간접적으로 MFA가 됩니다.

*   **Kerberos + MFA:** Windows 로그인 시 "비밀번호 + 스마트카드"를 사용한다면, SAPGUI로 넘어가는 Kerberos 티켓도 MFA 기반이 됩니다.
*   **Logon Ticket + MFA:** Portal 로그인 시 "비밀번호 + OTP 인증앱"을 사용한다면, SAPGUI로 넘어가는 티켓도 MFA 기반이 됩니다.

**결론:**
SAPGUI SSO 방식(Kerberos/Logon Ticket)은 **편의성(SSO)**을 위한 기술이지, **보안성(MFA)**을 위한 기술이 아닙니다. MFA가 필요하다면 **SAP Secure Login Service**와 같은 별도의 솔루션을 도입하거나, Windows/Portal 로그인 단계에서 MFA를 구성해야 합니다.
