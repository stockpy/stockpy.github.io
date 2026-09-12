---
layout: post
title: SAP .NET Connector (NCo) 가이드 및 S/4HANA 연결 이슈 분석
categories: general
---

# SAP .NET Connector (NCo) 가이드 및 S/4HANA 연결 이슈 분석

> SSIS에서 NCo를 이용해 SAP ECC와 S/4HANA 연결 시 발생한 이슈 분석 및 해결 과정 정리
>
> **작성일**: 2026-09-08
> **해결 방법**: NCo 3.0.x → 3.1.x 업그레이드

---

## 목차

1. [NCo 연결 구조 및 포트](#1-nco-연결-구조-및-포트)
2. [SAP 사용자 타입 및 NCo 권장 사항](#2-sap-사용자-타입-및-nco-권장-사항)
3. [Kernel vs RFC Library 호환성](#3-kernel-vs-rfc-library-호환성)
4. [SNC 파라미터 및 평문 연결](#4-snc-파라미터-및-평문-연결)
5. [S/4HANA 연결 이슈 분석 및 해결](#5-s4hana-연결-이슈-분석-및-해결)
6. [SSIS + NCo 운영 팁](#6-ssis--nco-운영-팁)
7. [참고 SAP Note](#7-참고-sap-note)

---

## 1. NCo 연결 구조 및 포트

### 1.1. 아키텍처

NCo는 **NW RFC Library (sapnwrfc.dll)**를 내장하여 RFC 프로토콜로 SAP에 연결합니다.

```
.NET App (NCo)
  └── sapnwrfc.dll (NW RFC Library)
        └── CPIC Layer (저수준 전송 계층)
              └── NI Layer (네트워크 인터페이스)
                    └── TCP/IP → SAP Gateway (32xx/48xx)
```

### 1.2. 포트 정리

| 포트 | 용도 | 비고 |
|---|---|---|
| **32xx** | SAP Gateway (평문) | NCo 기본 연결 포트 |
| **48xx** | SNC Gateway (암호화) | SNC 파라미터 설정 시 사용 |
| **3900** | Message Server | LogonGroup 사용 시 경유 |

### 1.3. CPIC (C Program Interface Call)

*   SAP RFC 통신의 **저수준 전송 계층**입니다.
*   NCo, JCo, SAP GUI 모두 내부적으로 CPIC를 사용합니다.
*   이름에 "C"가 들어갔지만 C 언어 전용이 아닙니다 (역사적 명칭).

---

## 2. SAP 사용자 타입 및 NCo 권장 사항

| 타입 | 이름 | 용도 | 라이선스 | 암호 만료/잠금 |
|---|---|---|---|---|
| **A** | Dialog | GUI/웹 사용자 | Dialog 라이선스 | 적용됨 |
| **B** | **System** | **RFC/BAPI 자동 호출** | **무료** | **SU01로 해제 가능** |
| **C** | Communication | OAuth/SAML/SSO | 무료 | 해제 가능 |
| **D** | Service | 자동화 서비스 (NW 7.50+) | 무료 | 해당 없음 |

### 권장 사항

*   **NCo는 System User (Type B)를 사용하세요.** 라이선스 무료이며, SU01에서 "암호에 로그인 데이터 없음" 체크로 암호 만료와 계정 잠금을 해제할 수 있습니다.
*   **TEST 목적**이라면 Dialog User (Type A)로도 연결 가능합니다 (LogonGroup 미사용 + 암호 유효 상태). 하지만 프로덕션에서는 System User로 변경해야 합니다.
*   **Service User (Type D)**는 SAP NetWeaver 7.50 SP05 이상에서 사용 가능하며, 다중 암호와 API 자동 교체가 필요할 때 고려합니다.

---

## 3. Kernel vs RFC Library 호환성

### 3.1. 버전 구분

*   **SAP Kernel**: 서버 측 버전 (예: 7.53, 9.16). `SYSTEM > Status` 또는 `RZ11`에서 확인.
*   **NW RFC Library**: NCo에 내장된 클라이언트 측 라이브러리 (예: 7.20, 7.50). `findstr Patch sapnwrfc.dll`로 확인.
*   **호환성**: RFC 프로토콜은 하위 호환됩니다. 새로운 Kernel은 구버전 RFC Library와 통신 가능하지만, 역은 불가능합니다.

### 3.2. NCo 버전 비교

| NCo 버전 | 내장 RFC Library | 지원 상태 |
|---|---|---|
| **3.0.x** | 7.20 ("721") | **2019.12.31 지원 종료** (Note 1025361) |
| **3.1.x** | 7.50 | **지원 중** (최신: 3.1.8, Note 3769352) |

> **핵심**: NCo Trace에서 보이는 "721"은 SAP 시스템 Kernel이 아니라 **NCo 내장 RFC Library 버전**입니다.

---

## 4. SNC 파라미터 및 평문 연결

`snc/enable = 1` 상태일 때, 평문(unprotected) 연결을 제어하는 파라미터입니다.

| 파라미터 | 기본값 | 의미 | NCo 영향 |
|---|---|---|---|
| `snc/accept_insecure_rfc` | 0 | 평문 RFC 허용 | `0`이면 RFC 계층에서 평문 연결 거부 |
| `snc/accept_insecure_cpic` | 0 | 평문 CPIC 허용 | `0`이면 **CPIC 계층에서 평문 연결 거부** |
| `snc/only_encrypted_rfc` | 0 | RFC 암호화 강제 | `1`이면 모든 RFC가 SNC 필수 |

### secinfo / reginfo와의 구분

*   `secinfo`와 `reginfo`는 **SNC 파트너 인증**만 제어합니다. "모두 허용"은 파트너 검증을 우회할 뿐, `snc/accept_insecure_*` 체크를 우회하지 않습니다.
*   평문 연결 자체를 허용하려면 `snc/accept_insecure_rfc`와 `snc/accept_insecure_cpic`가 `1`이어야 합니다.

### NCo에서 SNC 사용 여부

*   NCo 설정에 `SNC_PARTNERNAME` 파라미터가 **없으면** → 평문 RFC (32xx 포트 사용)
*   NCo 설정에 `SNC_PARTNERNAME` 파라미터가 **있으면** → 암호화 RFC (48xx 포트 사용, PSE 파일 필요)

---

## 5. S/4HANA 연결 이슈 분석 및 해결

### 5.1. 환경

| 항목 | 내용 |
|---|---|
| **소스** | SSIS (NCo 3.0.x / RFC Library 7.20) |
| **Target 1** | ECC 6.0, Kernel 7.53 → **연결 성공** |
| **Target 2** | S/4HANA 2025 Cloud, Kernel 9.16 → **연결 실패** |
| **연결 방식** | AP 서버 직접 접속 (LogonGroup 미사용) |
| **방화벽** | 3200, 3600 포트 Telnet 정상 |
| **타 시스템** | SAP Connector 사용 시 Target 2 연결 성공 |

### 5.2. Target 2 파라미터 상태

| 파라미터 | 값 |
|---|---|
| `snc/enable` | 1 (SNC 활성화) |
| `snc/accept_insecure_rfc` | 1 (평문 RFC 허용) |
| `snc/accept_insecure_cpic` | **0 (평문 CPIC 거부)** |
| `rdisp/cpicStreaming` | **on (CPIC Streaming 활성화)** |
| `secinfo` / `reginfo` | 모두 허용 |

### 5.3. 원인 분석

**1) `snc/accept_insecure_cpic = 0` → CPIC 계층에서 평문 연결 차단**

*   `snc/accept_insecure_rfc = 1`은 RFC 계층만 허용합니다.
*   NCo는 내부에서 CPIC 프로토콜을 사용하므로, `snc/accept_insecure_cpic = 0`이면 **CPIC 계층에서 연결이 거부**됩니다.
*   SAP Help Portal: "SNC 활성화 시, 평문 CPIC 연결은 기본값으로 거부됩니다."

**2) `rdisp/cpicStreaming = on` → RFC Library 7.20과 호환 불가**

*   Kernel 740 이상에서 기본 활성화되는 기능입니다.
*   **RFC Library 7.20 (NCo 3.0.x)은 CPIC Streaming을 지원하지 않습니다.**
*   SAP Note 2690316: "RFC Library 7.50 PL 3 이상이 필요합니다."

**3) TLS/SSL 프로토콜**

*   Kernel 9.16은 엄격한 TLS 기본값을 적용합니다.
*   RFC Library 7.20은 최신 TLS/Cipher Suite를 지원하지 않을 수 있습니다.

### 5.4. 타 시스템이 정상인 이유

타 시스템이 Target 2에 정상 접속한다는 것은 다음 중 하나입니다:

*   **NCo 3.1.x (RFC Lib 7.50)** 사용 → CPIC Streaming 지원 + 최신 TLS 대응
*   **SNC 적용** → `snc/accept_insecure_cpic = 0` 우회
*   **JCo 또는 최신 Integration Connector** 사용 → 내부 라이브러리 버전이 다름

### 5.5. 해결 방법

| 방법 | 작업 | 비고 |
|---|---|---|
| **A. NCo 업그레이드** | NCo 3.0.x → **3.1.x** | ✅ **적용됨**. CPIC Streaming 호환 + TLS 대응 |
| B. SAP 파라미터 변경 | `snc/accept_insecure_cpic = 1` | 보안 정책 상 허용되어야 함 |
| C. Streaming 비활성화 | `rdisp/cpicStreaming = off` | 구버전 호환성 확보 |

**결과**: NCo 3.0.x → 3.1.x 업그레이드로 Target 2(S/4HANA) 연결 성공.

---

## 6. SSIS + NCo 운영 팁

1.  **64비트 환경**: SSIS는 64비트로 실행됩니다. `sapnwrfc.dll`도 **반드시 x64 버전**이어야 합니다.
2.  **네이티브 DLL 배치**: `sapnwrfc.dll`은 .NET 어셈블리가 아닙니다. `DTExec.exe` 실행 디렉토리 또는 시스템 `PATH`에 복사해야 합니다. 없으면 `DllNotFoundException` 발생.
3.  **Connection Pooling**: `RfcDestinationManager`를 전역으로 관리하고 재사용하세요. 루프 내에서 매번 새 연결을 열면 성능이 급감합니다.
4.  **서비스 계정 권한**: SQL Server Agent / Integration Services 서비스 계정이 SAP Gateway 포트(32xx/48xx) 아웃바운드 접근 권한을 가져야 합니다.
5.  **대용량 데이터**: BAPI 호출 시 `PACKAGE SIZE`를 활용하세요. 한 번에 수만 건을 가져오면 SAP 메모리/네트워크 병목이 발생합니다.
6.  **에러 처리**: `RfcCommunicationException`, `RfcAbapRuntimeException`을 명시적으로 캐치하고, SAP 시스템 다운 시 재시도 로직을 구현하세요.

---

## 7. 참고 SAP Note

| Note | 제목 | 내용 |
|---|---|---|
| **1025361** | NW RFC Library 7.20 지원 정보 | 2019.12.31 지원 종료. 7.50으로 교체 필요 |
| **2573790** | NW RFC Library 7.50 지원 정보 | 지원 중 (2027.12까지). 모든 ABAP 시스템과 호환 |
| **2690316** | CPIC Streaming 연결 Hanging | RFC Library 7.50 PL 3 이상 필요 |
| **3411663** | CPIC 라이브러리 패치 레벨 업데이트 | JCo/NCo/RFC SDK 패치 레벨 정합성 |
| **3769352** | NCo 3.1.8 릴리즈 | 최신 NCo 버전 (2026.08.18) |
