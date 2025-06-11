# Week 11-12: ACP 실습 프로젝트
## 에이전트 연합 학습 플랫폼

### 📋 프로젝트 개요
ACP(Agent Communication Protocol)를 활용하여 **에이전트 연합 학습 플랫폼**을 구축합니다. 이 플랫폼은 RESTful API 기반의 단순한 인터페이스를 통해 다양한 프레임워크의 에이전트들이 협력하여 지식을 공유하고 함께 학습할 수 있는 환경을 제공합니다.

### 🎯 학습 목표
- **ACP 프로토콜 이해**: RESTful API 기반의 단순하고 직관적인 에이전트 통신
- **오픈 거버넌스**: Linux Foundation 모델의 커뮤니티 기반 개발 체험
- **크로스 프레임워크**: 다양한 AI 프레임워크 간 상호 운용성 구현
- **오프라인 발견**: 네트워크 없이도 가능한 에이전트 서비스 발견
- **Async-first 설계**: 장기 실행 작업을 위한 비동기 우선 아키텍처

### 🏗️ 시스템 아키텍처

```
┌─────────────────── ACP Federation Platform ───────────────────┐
│                                                                │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │
│  │   Discovery   │  │   Registry    │  │   Execution   │     │
│  │    Service    │  │   Service     │  │    Engine     │     │
│  └───────────────┘  └───────────────┘  └───────────────┘     │
│           │                 │                 │               │
│           └─────────────────┼─────────────────┘               │
│                             │                                 │
└─────────────────────────────┼─────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │   LangChain     │ │    AutoGen      │ │   Custom Agent  │
    │     Agent       │ │     Agent       │ │   (BeeAI)       │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              ▼               ▼               ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  Knowledge DB   │ │  Shared Memory  │ │   Result Store  │
    │   (Vector)      │ │    (Redis)      │ │  (PostgreSQL)   │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 🚀 핵심 구현 요소

#### 1. RESTful ACP API
- **Agent Detail**: GET /agents/{id} - 에이전트 정보 조회
- **Agent Run**: POST /agents/{id}/runs - 에이전트 실행 요청
- **Message Handling**: 텍스트, JSON, 파일 등 다양한 형태 지원
- **Streaming**: Server-Sent Events를 통한 실시간 결과 스트리밍

#### 2. 오프라인 에이전트 발견
- **패키지 메타데이터**: setup.py, package.json 기반 서비스 정보
- **로컬 레지스트리**: 네트워크 없이도 에이전트 발견 가능
- **자동 등록**: 에이전트 배포 시 자동 서비스 등록

#### 3. 연합 학습 메커니즘
- **지식 공유**: 벡터 데이터베이스를 통한 학습 결과 공유
- **모델 연합**: 분산 환경에서의 모델 파라미터 동기화
- **성능 추적**: 각 에이전트의 기여도 및 성능 모니터링

### 📁 프로젝트 구조

```
week11_12_acp_project/
├── README.md
├── docker-compose.yml
├── federation_platform/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── agents.py
│   │   ├── discovery.py
│   │   └── federation.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── registry.py
│   │   ├── executor.py
│   │   └── knowledge_store.py
│   └── models/
│       ├── __init__.py
│       ├── agent.py
│       ├── message.py
│       └── run.py
├── agents/
│   ├── langchain_agent/
│   │   ├── agent.py
│   │   ├── requirements.txt
│   │   └── setup.py
│   ├── autogen_agent/
│   │   ├── agent.py
│   │   ├── requirements.txt
│   │   └── setup.py
│   └── custom_beeai_agent/
│       ├── agent.py
│       ├── requirements.txt
│       └── setup.py
├── federation_learning/
│   ├── __init__.py
│   ├── knowledge_aggregator.py
│   ├── model_synchronizer.py
│   └── performance_tracker.py
├── configs/
│   ├── platform.yaml
│   ├── agents.yaml
│   └── federation.yaml
├── scripts/
│   ├── setup_platform.sh
│   ├── deploy_agent.sh
│   └── run_federation.sh
├── tests/
│   ├── test_api.py
│   ├── test_agents.py
│   └── test_federation.py
└── examples/
    ├── basic_usage.py
    ├── curl_examples.sh
    ├── federation_demo.py
    └── offline_discovery.py
```

### 🛠️ 구현 단계

#### Phase 1: ACP API 플랫폼 구축 (2-3일)
1. **FastAPI 기반 RESTful 서버**: ACP 표준 API 구현
2. **에이전트 레지스트리**: 에이전트 등록 및 관리
3. **기본 실행 엔진**: 에이전트 호출 및 결과 처리

#### Phase 2: 에이전트 통합 (2-3일)
1. **LangChain 에이전트**: 기존 LangChain 체인을 ACP 에이전트로 래핑
2. **AutoGen 에이전트**: Multi-agent conversation을 ACP로 노출
3. **커스텀 에이전트**: BeeAI 스타일의 순수 ACP 에이전트

#### Phase 3: 연합 학습 구현 (2-3일)
1. **지식 저장소**: 벡터 데이터베이스 기반 지식 공유
2. **모델 동기화**: 에이전트 간 학습 결과 동기화
3. **성능 추적**: 연합 학습 효과 측정

#### Phase 4: 오프라인 기능 및 최적화 (1-2일)
1. **오프라인 발견**: 패키지 메타데이터 기반 서비스 발견
2. **성능 최적화**: 비동기 처리 및 캐싱
3. **모니터링**: 플랫폼 상태 및 성능 모니터링

### 🔧 주요 기술 스택

#### Backend
- **FastAPI**: RESTful API 서버
- **Pydantic**: 데이터 검증 및 직렬화
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **Celery**: 비동기 작업 큐

#### AI/ML Frameworks
- **LangChain**: 체인 기반 LLM 애플리케이션
- **AutoGen**: 멀티 에이전트 대화 시스템
- **Hugging Face**: 트랜스포머 모델
- **scikit-learn**: 전통적 머신러닝

#### Infrastructure
- **PostgreSQL**: 메인 데이터베이스
- **Redis**: 캐싱 및 세션 스토어
- **Chroma**: 벡터 데이터베이스
- **Prometheus**: 메트릭 수집

### 📊 성능 목표

#### API 응답 시간
- **Agent Detail**: < 100ms
- **Run Creation**: < 200ms
- **Stream Start**: < 500ms

#### 연합 학습 효율성
- **지식 공유 지연**: < 1분
- **모델 동기화**: < 5분
- **성능 향상**: 단독 학습 대비 20% 이상

#### 확장성
- **동시 에이전트**: 100+
- **동시 실행**: 50+
- **연합 참여자**: 10+

### 🧪 실습 시나리오

#### 시나리오 1: 크로스 프레임워크 질문답변
```python
# LangChain 에이전트와 AutoGen 에이전트가 협력하여 복잡한 질문 해결
federation_task = {
    "question": "Python에서 비동기 프로그래밍의 장단점을 설명하고, 실제 예제 코드를 제공해주세요.",
    "participants": [
        {"agent": "langchain_researcher", "role": "information_gathering"},
        {"agent": "autogen_coder", "role": "code_generation"},
        {"agent": "custom_reviewer", "role": "quality_assurance"}
    ],
    "knowledge_sharing": True,
    "result_aggregation": "consensus"
}
```

#### 시나리오 2: 연합 모델 훈련
```python
# 여러 에이전트가 서로 다른 데이터셋으로 훈련한 결과를 연합
federated_training = {
    "model_type": "text_classification",
    "participants": [
        {"agent": "agent_1", "dataset": "news_data", "contribution": 0.4},
        {"agent": "agent_2", "dataset": "social_media", "contribution": 0.3},
        {"agent": "agent_3", "dataset": "academic_papers", "contribution": 0.3}
    ],
    "aggregation_method": "federated_averaging",
    "privacy_preserving": True
}
```

### 🎯 실습 과제

#### 기본 과제 (필수)
1. **ACP API 구현**: RESTful API로 에이전트 실행
2. **3개 프레임워크 통합**: LangChain, AutoGen, 커스텀 에이전트
3. **curl 테스트**: SDK 없이 순수 REST API 호출
4. **연합 학습 데모**: 간단한 지식 공유 시연

#### 심화 과제 (선택)
1. **오프라인 발견**: 네트워크 없이 에이전트 발견
2. **성능 최적화**: 비동기 처리 및 캐싱 적용
3. **보안 강화**: API 키 인증 및 권한 관리
4. **BeeAI 통합**: 실제 BeeAI 플랫폼과 연동

### 📈 평가 기준

#### API 구현 (35%)
- RESTful API 완성도
- ACP 표준 준수
- 에러 처리 및 검증

#### 에이전트 통합 (30%)
- 다양한 프레임워크 지원
- 에이전트 간 통신 성공
- 결과 품질

#### 연합 학습 (25%)
- 지식 공유 메커니즘
- 성능 개선 효과
- 협력 시연

#### 운영 및 문서화 (10%)
- 오프라인 기능
- 사용 편의성
- 문서 완성도

### 🔍 ACP의 특징과 장점

#### 단순성의 힘
```bash
# SDK 없이 curl로 즉시 에이전트 호출 가능
curl -X POST http://localhost:8000/agents/langchain_qa/runs \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      {
        "parts": [
          {
            "content": "What is the capital of France?",
            "content_type": "text/plain"
          }
        ]
      }
    ]
  }'
```

#### 오픈 거버넌스의 장점
- **투명한 개발**: 모든 결정 과정이 공개
- **커뮤니티 참여**: 다양한 의견 수렴
- **빠른 피드백**: 실사용자 의견 반영
- **표준화**: 업계 공통 표준 추진

#### Async-first 설계
- **장기 작업 지원**: 몇 시간씩 걸리는 작업도 안정적 처리
- **리소스 효율성**: 비동기 처리로 서버 리소스 절약
- **사용자 경험**: 논블로킹 방식으로 반응성 향상

### 💡 학습 포인트

#### ACP의 철학 이해
- **단순함이 최고**: 복잡한 기술보다 단순한 해결책
- **접근성**: 누구나 쉽게 사용할 수 있는 API
- **상호 운용성**: 다양한 시스템과 쉽게 통합

#### 실무 적용 가능성
- **빠른 프로토타이핑**: 즉시 테스트 가능한 API
- **레거시 통합**: 기존 시스템과 쉬운 연동
- **팀 협업**: 기술 스택에 관계없이 협업 가능

#### 제약사항 인식
- **성능 한계**: RESTful API의 오버헤드
- **보안 고려**: 단순함과 보안의 트레이드오프
- **표준화 진행**: 아직 발전 중인 표준

### 🌟 실제 활용 사례

#### 교육 분야
- **다중 AI 튜터**: 각기 다른 전문성을 가진 AI 튜터들의 협력
- **학습 경로 최적화**: 여러 에이전트가 협력하여 개인화된 학습 경로 제공

#### 연구 분야
- **문헌 조사 자동화**: 다양한 데이터베이스에서 정보 수집
- **실험 설계 지원**: 여러 전문가 에이전트의 의견 종합

#### 비즈니스 분야
- **고객 서비스**: 여러 전문 영역 에이전트의 협력
- **의사결정 지원**: 다각도 분석을 통한 종합적 의사결정

이 실습을 통해 ACP의 단순함과 접근성을 체험하면서, 동시에 실제 연합 학습 환경에서의 에이전트 협력 메커니즘을 이해할 수 있습니다. 