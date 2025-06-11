# 1주차: 멀티에이전트 시스템 개요

## 📋 학습 목표
- 에이전트 기반 시스템의 개념과 필요성 이해
- 멀티에이전트 환경의 도전과제 파악
- 프로토콜의 역할과 중요성 체험

## 🛠️ 실습 내용

### 실습 1: 단일 에이전트 시스템
간단한 단일 에이전트를 구현하여 에이전트의 기본 개념을 이해합니다.

### 실습 2: 멀티에이전트 통신 문제
프로토콜 없이 여러 에이전트가 통신할 때 발생하는 문제점을 직접 체험합니다.

### 실습 3: 통신 프로토콜의 필요성
표준화된 프로토콜을 적용했을 때의 개선점을 확인합니다.

## 🚀 실행 방법

```bash
# 실습 환경 준비
cd 01_theory_foundation/week01_multi_agent_overview
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 실습 1: 단일 에이전트
python single_agent_demo.py

# 실습 2: 멀티에이전트 문제점
python multi_agent_problems.py

# 실습 3: 프로토콜 적용
python protocol_solution.py

# 전체 데모 실행
python run_demo.py
```

## 📝 과제
일상 속 멀티에이전트 시스템 사례를 조사하고 `homework/report.md`에 정리하세요.

## 📚 참고 자료
- [에이전트 기반 모델링 기초](docs/agent_based_modeling.md)
- [분산 시스템 통신 패턴](docs/communication_patterns.md) 