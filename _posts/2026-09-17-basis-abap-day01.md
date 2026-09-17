---
layout: post
title: "Basis를 위한 ABAP 마스터 1일차 - ABAP 메모리와 데이터 구조"
date: 2026-09-17 13:00:00 +0900
categories: [ABAP, Basis]
tags: [abap, basis, memory, data-types, se38]
---

# Basis를 위한 ABAP 마스터 1일차 - ABAP 메모리와 데이터 구조

## ⏱️ 이론 세션: 3가지 핵심 데이터 구조

Basis 컨설턴트 관점에서 SAP Application Server(PAS/AAS)의 Work Process(`wp`)와 Local Memory(`Roll Area`) 개념을 떠올려 봅니다. ABAP 프로그램이 실행되면, 할당된 Work Process 메모리 공간에 데이터를 올려두고 연산을 처리합니다.

이때 메모리에 방을 만드는 작업이 **데이터 선언**이며, 크게 3가지 형태가 있습니다.

### 1. 변수 (Elementary Type) : 단일 값 저장 공간
- **개념**: 딱 한 값만 들어가는 방입니다. (숫자 1개, 문자열 1개 등)
- **Basis 매칭**: OS 레벨의 단일 변수/파라미터 값 저장 공간.

### 2. 구조체 (Structure / Work Area) : 한 줄(Row)짜리 데이터 방
- **개념**: 여러 종류의 변수를 가로로 이어 붙인 형태입니다. (`사원번호`, `이름`, `부서`를 가로로 묶음)
- **Basis 매칭**: 데이터베이스 테이블의 레코드 1건(Row).

### 3. 인터널 테이블 (Internal Table) : 메모리에 적재된 대량 데이터 방
- **개념**: 구조체(Work Area)를 세로로 수없이 쌓아 올린 형태입니다.
- **Basis 매칭**: Application Server RAM(Roll Area)에 상주하는 임시 데이터 버퍼.

---

## 💻 실습 세션: T-Code SE38에서 첫 변수 선언해보기

### 실습 단계
1. T-Code **`SE38`** (ABAP Editor) 실행.
2. Program 이름에 **`ZEXAM_BASIS_01`** 입력 후 **Create** 클릭.
3. Title: `Basis 변수 선언 실습`, Type: `Executable program` 선택 후 **Save**.
4. Package: **`$TMP`** (Local Object) 선택.

### 실습 소스 코드
```abap
REPORT zexam_basis_01.

" 1. 기본 변수 선언 (타입 i는 Integer 정수형)
DATA: gv_user_count TYPE i.

" 2. 시스템 변수 사용하기 (sy-uname은 현재 로그인한 사용자 ID)
WRITE: / '현재 접속한 Basis 컨설턴트 ID:', sy-uname.

" 3. 변수에 값 대입 및 출력
gv_user_count = 5.
WRITE: / '현재 관리 중인 SAP 시스템 개수:', gv_user_count.
