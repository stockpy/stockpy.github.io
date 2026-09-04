---
layout: post
title: SAP PCE 환경 — 사내 SAP GUI SSO 인증 가이드 (Kerberos)
---

# SAP PCE 환경 — 사내 SAP GUI SSO 인증 가이드 (Kerberos)

## 1. 개요

SAP S/4HANA Cloud, Private Edition (PCE/RISE) 환경에서 **사내 네트워크**를 통해 SAP GUI 접속 시 SSO 인증을 구현하기 위한 필요한 사항과 작업 내용을 정리합니다.

사내 도메인 가입 PC 환경에서는 **Kerberos SSO**를 사용합니다. 별도 라이선스 구매가 필요 없으며, Windows 도메인 로그온 후 SAP GUI 실행 시 자동으로 인증됩니다.

---

## 2. 필요 조건

### 2.1 사전 요구 사항

| 항목 | 내용 |
|---|---|
| **OS** | Windows 10/11 (MS Active Directory 도메인 가입) |
| **SAP GUI** | 7.70 이상 |
| **SAP Cryptographic Library** | PCE 구독에 포함 (서버 측 설치 필요) |
| **네트워크** | 사내 네트워크 (KDC 접근 가능) |
| **비용** | 무료 (PCE 구독 포함) |

### 2.2 아키텍처 흐름

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Windows    │────▶│  MS AD (KDC) │────▶│  SAP S/4HANA│
│  PC         │◀────│  (Kerberos   │◀────│  AS ABAP    │
│  (도메인 가입)│     │   Ticket)    │     │  (SNC)      │
└─────────────┘     └──────────────┘     └─────────────┘
```

1. 사용자가 Windows PC에 도메인 계정으로 로그온 → Kerberos TGT 발급
2. SAP GUI 실행 → SAP 시스템 접근 시 Kerberos 서비스 티켓 요청
3. SAP 시스템이 Kerberos 토큰 검증 후 자동 로그온

---

## 3. 서버 측 작업 (BASIS)

### 3.1 SNC 라이브러리 설정

**1) SAP Cryptographic Library 설치 확인**
```
서버 OS에 SAP Cryptographic Library 설치 확인
(설치 경로 예: C:\usr\sap\<SID>\SYS\exe\uc\ntamd64\sapcrypto.dll)
```

**2) 프로파일 파라미터 설정 (RZ10)**
```
트랜잭션: RZ10
프로파일: DEFAULT.PFL

파라미터:
  SNC_LIB = $(DIR_LIBRARY)/$(DS SNC_LIB)
  login/no_automatic_user_sapstar = TRUE
```

### 3.2 STRUST — SNC 및 Kerberos 설정

**1) STRUST 트랜잭션 실행**
```
트랜잭션: STRUST
```

**2) SNC 설정 탭**
- Kerberos principal 등록
- KDC 서버 정보 확인 및 연동
- PSE (Personal Security Environment) 생성/확인

**3) Kerberos principal 설정**
```
principal 형식: SAPSSO/<시스템명>.<도메인>@<도메인>
예: SAPSSO/PRD.COMPANY.COM@COMPANY.COM
```

### 3.3 SU01 — 사용자 SNC 이름 설정

**1) 사용자 마스터 데이터 설정**
```
트랜잭션: SU01
사용자 선택 → 변경 모드
```

**2) 로그인 데이터 탭 — SNC 이름 입력**
```
SNC 이름 형식: p:username@YOUR.DOMAIN.COM
예: p:kimhs@COMPANY.COM
```

> 모든 SAP GUI SSO 사용자에게 SNC 이름을 설정해야 합니다.

### 3.4 SPN 등록 (Windows 서버 관리자)

**1) SAP 시스템의 SPN 등록**
```powershell
setspn -S SAPSSO/<시스템명>.<도메인> <서버명>
```

**2) SPN 확인**
```powershell
setspn -L <서버명>
```

---

## 4. 클라이언트 측 작업

### 4.1 SAP GUI 설치 및 설정

**1) SAP GUI for Windows 7.70 이상 설치**
- SAP Software Downloads에서 최신 버전 다운로드
- 또는 사내 소프트웨어 배포 도구 (SCCM 등)를 통해 배포

**2) SAP GUI SNC 활성화**
```
SAP GUI 실행 → 옵션 (Options) → SNC 탭
- "SNC 활성화" 체크
- SNC 라이브러리: sapcrypto.dll (자동 감지)
- SNC 파트너 이름 확인 (서버 측 STRUST 설정과 일치해야 함)
```

### 4.2 Windows 도메인 환경 확인

**1) PC 도메인 가입 확인**
```
시스템 속성 → 컴퓨터 이름 탭
- 도메인 가입 상태 확인
```

**2) 도메인 계정 로그온**
- 사용자가 MS AD 도메인 계정으로 Windows에 로그온해야 함
- 로컬 계정은 Kerberos SSO 불가

### 4.3 그룹 정책 배포 (대규모 환경)

**1) SAP GUI SNC 설정을 GPO로 배포**
- 레지스트리 기반 정책 또는 SAP GUI 설정 파일 배포
- 모든 클라이언트에서 일관된 SNC 설정 보장

**2) SAP GUI 설치 패키지 배포**
- SCCM/Intune를 통해 SAP GUI 7.70 이상统一部署

---

## 5. 테스트

### 5.1 Kerberos SSO 로그온 테스트

1. Windows PC에 도메인 계정으로 로그온
2. SAP GUI 실행
3. SAP 시스템 연결 시 사용자 ID/비밀번호 없이 자동 로그온 확인
4. SAP GUI 로그온 화면에서 "SNC" 아이콘이 활성화되어 있는지 확인

### 5.2 문제 발생 시 확인 사항

| 증상 | 확인 사항 |
|---|---|
| 로그온 화면에서 비밀번호 요청 | SU01 SNC 이름 설정 확인 |
| "SNC partner rejected" 오류 | STRUST 설정 및 SPN 확인 |
| SAP GUI에서 SNC 아이콘 비활성화 | SAP GUI 옵션 → SNC 활성화 확인 |
| KDC 관련 오류 | 네트워크 연결, KDC 접근성 확인 |

---

## 6. 체크리스트

### 서버 측
- [ ] SAP Cryptographic Library 설치 확인
- [ ] RZ10 — SNC_LIB 파라미터 설정
- [ ] STRUST — SNC 활성화 및 Kerberos principal 등록
- [ ] SU01 — 사용자 SNC 이름 설정 (모든 SSO 대상 사용자)
- [ ] SPN 등록 (Windows 서버 관리자)
- [ ] 시스템 재시작 후 설정 적용 확인

### 클라이언트 측
- [ ] SAP GUI 7.70 이상 설치
- [ ] SAP GUI 옵션 → SNC 활성화
- [ ] PC가 MS AD 도메인에 가입되어 있는지 확인
- [ ] 도메인 계정으로 Windows 로그온

### 테스트
- [ ] Kerberos SSO 자동 로그온 확인
- [ ] SNC 아이콘 활성화 확인
- [ ] 다수 사용자 테스트

---

## 7. SAP Secure Login Service (SLS) 도입 고려 사항

사내 Kerberos SSO만으로는 해결되지 않는 상황이 발생할 경우, SLS 도입을 고려합니다.

### 7.1 SLS가 필요한 상황

| 상황 | 설명 |
|---|---|
| **원격/재택근무 SAP GUI 접근** | 사내 네트워크 외부에서 SAP GUI를 사용해야 하며 VPN 없이도 안전하게 접근해야 할 때 |
| **SAP GUI에 MFA (다중 인증) 필수** | 보안 정책상 SAP GUI 접근 시 OTP, 생체 인증, FIDO2 등 다중 인증이 필수일 때 |
| **기존 SAP SSO 3.0 사용 중** | 현재 SAP SSO Secure Login Server를 사용하고 있다면, **2027년 12월 31일 유지보수 종료**에 따라 SLS로 마이그레이션 필수 |
| **Zero Trust 보안 정책** | 클라우드 기반 아이덴티티 관리와 Zero Trust 아키텍처를 구축하려는 경우 |

### 7.2 SLS 도입 시 추가 작업 내용

**1) SAP BTP 측 작업**
- SAP BTP Cockpit에서 **Secure Login Service for SAP GUI** 구독
- SAP Cloud Identity Services (IAS) 또는 기업 IdP (Okta, Azure AD 등) 연동
- SLS ↔ IAS 간 신뢰 관계 설정, MFA 정책 구성

**2) SAP ABAP 서버 측 추가 작업**
- `STRUST` — SAP Cloud Root CA 인증서 등록
- `RZ10` — CCL/SNC namealias 파라미터 추가 설정
- `SU01` — 사용자의 SNC 이름을 X.509 형식으로 변경 또는 병렬 설정

**3) 클라이언트 측 추가 작업**
- Secure Login Client 설치 (SAP GUI 7.70 이상 시 포함)
- Windows 레지스트리 정책 설정 (`HKEY_LOCAL_MACHINE\SOFTWARE\Policies\SAP\SecureLogin\`)
- 그룹 정책 또는 SCCM/Intune를 통해 레지스트리 설정 배포

**4) 라이선스 및 비용**
- 500명 단위 블록 구매, **€450/블록/월** (≈ €0.90/사용자/월)
- PCE 구독에 포함되지 않으므로 별도 구매 필요

### 7.3 Kerberos + SLS 병렬 운영

사내는 Kerberos, 외부/원격은 SLS를 사용하도록 구성할 수 있습니다:

- 클라이언트 레지스트리 `GSSTargetName`으로 인증 방식 구분
- 서버 측 `ccl/snc/namealias` 파라미터로 기존 SU01 SNC 이름 변경 없이 병렬 지원

```
사용자 로그온
    │
    ├─ 사내 네트워크 → Kerberos 토큰 → SAP GUI SSO (무료)
    │
    └─ 네트워크 외부 → SLS (X.509 + MFA) → SAP GUI SSO (별도 라이선스)
```

---

## 8. 참고 자료

- SAP Note 2338952 — CommonCryptoLib 8.5: Configuration Profile Parameters
- [SAP Help: Kerberos Authentication](https://help.sap.com)
- [SAP Help: SNC Parameters](https://help.sap.com)
- [SAP Help: Secure Login Service](https://help.sap.com/docs/secure-login-service)
- SAP Community: "A Single Sign-On Guide for SAP S/4HANA Cloud, Private Edition"
- SAP Community: "Step-by-Step Guide: SAP GUI SSO Setup Using Kerberos"
- SAP Community: "Implementing SAP BTP Secure Login Service for SAP GUI"
- SAP Community: "Step by Step Implementation of Secure Login Service for SAP GUI"
