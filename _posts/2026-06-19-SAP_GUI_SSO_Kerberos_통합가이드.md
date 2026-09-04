---
layout: post
title: SAP GUI SSO (Kerberos 인증) — 통합 가이드
---

# SAP GUI SSO (Kerberos 인증) — 통합 가이드

> **중요 안내 (SAP 공식 블로그 기준)**
> - **SAP Single Sign-On** 제품: 2027년 메인스트림 유지보수 종료, 2030년 확장 유지보수 종료
> - 후속 솔루션: **SAP Secure Login Service for SAP GUI**
> - 본 구성 내용은 후속 솔루션에도 동일하게 적용됨

---

## 1. 목적 및 작동 원리

Windows 도메인 인증된 사용자가 SAP GUI에 별도 계정 입력 없이 자동 로그인하도록 구성한다.

### 흐름
1. 사용자가 Windows 도메인 로그인
2. SAP Secure Login Service for SAP GUI가 Kerberos 토큰 발급 (Microsoft AD 기반)
3. SNC(Secure Network Communication)를 통해 SAP GUI ↔ AS ABAP 간 신뢰 관계 수립 및 암호화 통신
4. SAP GUI 자동 로그인

### 장점
- **보안 강화**: 비밀번호 기반 로그인 제거, SNC를 통한 통신 암호화
- **사용자 편의**: 반복적인 자격 증명 입력 불필요
- **운영 효율성**: 비밀번호 관련 지원 티켓 감소
- **서버 추가 불필요**: 별도 인증 서버 없이 구현 가능

---

## 2. 구성 단계

### Step 1: Active Directory — 서비스 계정 및 SPN 등록

| 항목 | 내용 |
|---|---|
| 작업 | AD에 Kerberos 서비스 계정 생성 |
| SPN 형식 | `SAP/SAPService<시스템명>` (예: `SAP/S4H`) |
| 위치 | AD Users & Computers → Advanced Features → 계정 속성 → Attribute Editor → `servicePrincipalName` |
| 참고 | SAP Note 1696905: Kerberos 및 인증서용 SNC 이름 구성 |

### Step 2: Cryptolib 버전 확인 (8.5 이상 필수)

| 방법 | 절차 |
|---|---|
| `STRUST` | Toolbar → Environment → Display SSF Version |
| `SE38` (RSBDCOS0) | `sapgenpse` 명령 실행 |
| `SE38` (SSF02) | Execute 선택 |
| 트레이스 파일 | `dev_w*` 확인 |

### Step 3: Secure Login Client 설치

- SAP Support Portal에서 최신 버전 다운로드  
  (`me.sap.com/softwarecenter` → Support Packages & Patches → SAP SINGLE SIGN-ON → Secure Login Client)
- **모든 사용자 PC**에 설치
- 설치 후 작업 표시줄에 아이콘 표시

### Step 4: 백엔드 SNC 구성

| 항목 | 내용 |
|---|---|
| 트랜잭션 | `SNCCONFIG` (SNC Wizard) |
| 주의사항 | `snc/identity/as` 파라미터가 `STRUST` 설정과 일치해야 함 (다중 AS 환경 시 특히 중요) |
| 작업 | 애플리케이션 재시작 후 SNC Wizard 실행 → AD 서비스 계정 자격 증명 입력 |

### Step 5: SAP 사용자 ↔ AD 사용자 매핑

| 항목 | 내용 |
|---|---|
| 개별 매핑 | `SU01` → SNC 탭에 `p:CN=...,...` 형식으로 AD 사용자 정보 입력 |
| 대량 매핑 | `SNC1` T-code (AD ID와 SAP ID가 **동일한 경우**에만 작동) |
| ID 불일치 시 | 수동 또는 커스텀 스크립트로 업데이트 |
| 정보 확인 | Secure Login Client에서 SNC 이름 확인 가능 |

### Step 6: SAP GUI 네트워크 설정

- SAP GUI 시스템 엔트리의 SNC 이름 구성
- 사용자가 SAP 클라이언트 선택 시 자동 로그인 적용

---

## 3. 주요 파라미터

| 파라미터 | 권장 값 | 설명 |
|---|---|---|
| `login/password_change_for_SSO` | `0` | SSO 환경에서 SAP GUI 내 비밀번호 변경 금지 (조직 보안 정책에 맞게 조정) |

---

## 4. 두 자료 간 비교 검증

| 비교 항목 | Q&A 자료 (2025) | 공식 블로그 (2017) | 검증 결과 |
|---|---|---|---|
| 구성 단계 | 상세 단계별 설명 (실무 중심) | 개념 설명 + 비디오 참조 | **일치**. Q&A가 블로그의 비디오 내용을 텍스트로 상세화한 형태 |
| SPN 형식 | `SAP/SAPService<시스템명>` | 명시 안 함 | Q&A의 SPN 형식 채택 |
| Cryptolib 버전 | 8.5 이상 명시 | 명시 안 함 | Q&A의 8.5 이상 요구사항 채택 |
| 대량 매핑 | `SNC1` / 커스텀 스크립트 | Part 2 비디오 참조 | **일치** |
| 유지보수 종료 | 언급 없음 | 2027/2030 종료 | 블로그의 공식 정보 채택 |
| 후속 솔루션 | 언급 없음 | SAP Secure Login Service for SAP GUI | 블로그의 공식 정보 채택 |
| 문제 해결 자료 | 언급 없음 | SAP Note 1732610, Wiki 페이지 | 블로그의 참조 자료 채택 |

**상충점:** 없음. 두 자료는 동일한 구성 절차를 다른 수준으로 설명한 것이다.

---

## 5. 문제 해결 및 추가 자료

| 항목 | 링크 |
|---|---|
| Kerberos SSO 권장사항 & 트러블슈팅 | [SAP Wiki](https://wiki.scn.sap.com/wiki/display/Security/Single+Sign-On+with+Kerberos%3A+Recommendations+and+Troubleshooting) |
| SAP Note 1732610 | SPNEGO for ABAP 문제 해결 |
| SAP Note 1696905 | Kerberos 및 인증서용 SNC 이름 구성 |
| SAP Note 1837331 | SAP HANA DB용 Kerberos SSO |
| 멀티 도메인 환경 | [SAP 블로그](https://blogs.sap.com/2019/11/22/kerberos-spnego-for-sap-as-abap-in-a-multi-domain-environment/) |
| 공식 커뮤니티 | [community.sap.com/topics/single-sign-on](https://community.sap.com/topics/single-sign-on) |

---

## 6. 참고 사항

- SAML 2.0 Identity Federation은 SAP Fiori/BTP용이며, **SAP GUI에는 적용 불가**
- 다중 SAP GUI 클라이언트 사용 시 각 클라이언트별 SNC 파라미터 업데이트 필요
