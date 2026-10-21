---
layout: post
title: "Mac에서 로컬 AI 설치하고 CrewAI 연결하기"
date: 2026-10-22
categories: [AI]
tags: [Ollama, CrewAI, Local AI, Python, Mac]
---

## 1. 목표와 전체 구조

Mac에서 로컬 AI를 실행하고 CrewAI에 연결하여 개인 AI 비서의 기본 환경을 구성합니다.

목표는 **추가적인 AI 모델 API 사용료 없이 시작하는 것**입니다.

    Mac
    ├── Ollama       : 로컬 AI 모델 실행 도구
    ├── Llama 3.2    : 답변을 생성하는 AI 모델
    └── CrewAI       : AI 에이전트와 작업 흐름 관리

- **Ollama**: AI 모델을 Mac에서 실행합니다.
- **Llama 3.2**: 답변을 생성하는 로컬 AI 모델입니다.
- **CrewAI**: AI 에이전트에 역할과 작업을 부여하고 실행을 관리합니다.

로컬 모델을 사용하면 모델 API 호출 비용 없이 실행할 수 있습니다. 단, Mac의 메모리와 저장 공간은 필요합니다.

## 2. 설치 전 준비

### 2-1. Mac 사양 확인

1. 화면 왼쪽 위의 Apple 메뉴를 선택합니다.
2. `이 Mac에 관하여`를 선택합니다.
3. macOS 버전과 메모리(RAM)를 확인합니다.

- [Ollama Mac 다운로드](https://ollama.com/download/mac)

### 2-2. 터미널 실행

1. `Command + Space`를 누릅니다.
2. `터미널(Terminal)`을 검색해 실행합니다.

아래 명령어는 터미널에 입력합니다.

## 3. Ollama 설치

### 3-1. 공식 앱 설치

1. [Ollama 공식 다운로드 페이지](https://ollama.com/download/mac)에 접속합니다.
2. Mac용 앱을 다운로드합니다.
3. 앱을 설치하고 실행합니다.

### 3-2. 설치 확인

터미널에서 다음 명령어를 실행합니다.

    ollama --version

버전 정보가 표시되면 설치가 완료된 것입니다.

## 4. 로컬 AI 모델 설치 및 실행

이 가이드에서는 `llama3.2` 모델을 사용합니다.

### 4-1. 모델 다운로드

    ollama pull llama3.2

다운로드가 완료될 때까지 기다립니다.

### 4-2. 모델 실행

    ollama run llama3.2

다음과 같은 질문을 입력합니다.

    안녕하세요. 한국어로 짧게 자기소개해 주세요.

AI가 답변하면 로컬 모델이 정상적으로 실행되는 것입니다.

대화를 종료하려면 `Ctrl + D`를 누릅니다.

### 4-3. 설치된 모델 확인

    ollama list

목록에 `llama3.2`가 표시되는지 확인합니다.

**체크포인트:** CrewAI를 설치하기 전에 Ollama만으로 질문과 답변이 정상적으로 이루어져야 합니다.

## 5. Python과 CrewAI 설치

### 5-1. Python 버전 확인

    python3 --version

CrewAI 공식 문서에서 지원하는 Python 버전을 확인합니다.

- [Python 공식 다운로드](https://www.python.org/downloads/)

### 5-2. uv 설치

`uv`는 Python 프로젝트와 패키지를 관리하는 도구입니다.

    curl -LsSf https://astral.sh/uv/install.sh | sh

설치 후 터미널을 다시 열고 확인합니다.

    uv --version

### 5-3. CrewAI 프로젝트 생성

다음 명령어를 순서대로 실행합니다.

    mkdir -p ~/local-ai-assistant
    cd ~/local-ai-assistant
    uv init
    uv add "crewai[openai]"

이 명령어는 프로젝트 폴더를 만들고 CrewAI 패키지를 설치합니다.

여기서 `openai` 패키지는 로컬 Ollama와 연결하기 위한 인터페이스로 사용합니다. 아래 예제는 OpenAI API가 아니라 Mac 내부의 Ollama 서버를 호출합니다.

## 6. CrewAI와 Ollama 연결

### 6-1. main.py 파일 생성

`~/local-ai-assistant` 폴더 안에 `main.py` 파일을 생성하고 다음 코드를 저장합니다.

    from crewai import Agent, Crew, Process, Task, LLM

    local_llm = LLM(
        model="openai/llama3.2",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    assistant = Agent(
        role="개인 업무 정리 비서",
        goal="사용자의 요청을 이해하고 한국어로 명확하게 답변한다.",
        backstory=(
            "사용자의 업무 기록과 문서 정리를 돕는 "
            "신중한 개인 AI 비서다."
        ),
        llm=local_llm,
        verbose=True,
    )

    task = Task(
        description=(
            "로컬 AI와 CrewAI의 역할을 "
            "각각 한 문장으로 설명해 주세요."
        ),
        expected_output=(
            "한국어 두 문장. 첫 문장은 로컬 AI, "
            "둘째 문장은 CrewAI의 역할을 설명한다."
        ),
        agent=assistant,
    )

    crew = Crew(
        agents=[assistant],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    print("\n===== 실행 결과 =====")
    print(result)

### 6-2. 코드 실행

터미널에서 프로젝트 폴더로 이동합니다.

    cd ~/local-ai-assistant

다음 명령어를 실행합니다.

    uv run main.py

정상적으로 실행되면 CrewAI가 작업을 진행하고 최종 결과를 출력합니다.

**주의:** CrewAI와 Ollama의 버전에 따라 모델 이름이나 연결 설정이 달라질 수 있습니다. 오류가 발생하면 공식 문서의 최신 예제를 확인합니다.

- [CrewAI 설치 안내](https://docs.crewai.com/en/installation)
- [CrewAI LLM 연결 안내](https://docs.crewai.com/en/learn/llm-connections)
- [Ollama 공식 문서](https://docs.ollama.com/)

## 7. 오류 해결 방법

### 7-1. `ollama: command not found`

- Ollama가 설치되어 있는지 확인합니다.
- 터미널을 종료하고 다시 실행합니다.
- 다음 명령어로 확인합니다.

    ollama --version

### 7-2. `localhost:11434` 연결 오류

Ollama가 실행 중인지 확인하고 모델을 테스트합니다.

    ollama list
    ollama run llama3.2

### 7-3. 메모리 부족 또는 응답 지연

- 실행 중인 다른 앱을 종료합니다.
- Mac의 메모리에 맞는 더 작은 모델을 검토합니다.
- 모델이 커질수록 반드시 더 좋은 결과가 나오는 것은 아닙니다.

### 7-4. CrewAI 패키지 오류

프로젝트 폴더에서 실행합니다.

    uv sync

문제가 계속되면 공식 문서를 확인합니다.

- [CrewAI 설치 안내](https://docs.crewai.com/en/installation)
- [CrewAI LLM 연결 안내](https://docs.crewai.com/en/learn/llm-connections)

## 8. 다음 단계: 문서와 업무 내용을 기억하는 비서

여기까지는 로컬 AI와 CrewAI의 연결을 확인하는 최소 예제입니다.

아직 문서를 자동으로 읽거나 장기 기억을 저장하는 기능은 구현하지 않았습니다.

앞으로 다음 순서로 확장할 수 있습니다.

1. 지정한 폴더에서 문서를 읽는 기능
2. 문서 제목, 날짜, 핵심 내용을 정리하는 기능
3. 원본 문서와 요약을 검색하는 저장소
4. 새 문서의 중복을 확인하고 기록을 갱신하는 기능
5. 개인정보와 업무 자료의 접근 범위 및 백업 정책

처음부터 여러 에이전트를 만들기보다는 **단일 비서로 문서 검색과 정리 기능을 먼저 완성한 뒤**, 실제로 분업이 필요할 때 에이전트를 추가하는 것을 권장합니다.

## 9. 공식 참고 링크

- [Ollama Mac 다운로드](https://ollama.com/download/mac)
- [Ollama 공식 문서](https://docs.ollama.com/)
- [CrewAI 설치 안내](https://docs.crewai.com/en/installation)
- [CrewAI LLM 연결 안내](https://docs.crewai.com/en/learn/llm-connections)
- [uv 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)
- [Python 공식 다운로드](https://www.python.org/downloads/)

## 10. 설치 완료 체크리스트

- [ ] Mac의 macOS 버전과 메모리를 확인했다.
- [ ] Ollama를 설치했다.
- [ ] `llama3.2` 모델을 다운로드했다.
- [ ] Ollama에서 직접 질문하고 답변을 확인했다.
- [ ] Python과 uv를 준비했다.
- [ ] CrewAI 프로젝트를 생성했다.
- [ ] `main.py`를 작성했다.
- [ ] `uv run main.py` 실행 결과를 확인했다.