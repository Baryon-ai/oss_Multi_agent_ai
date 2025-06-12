---
marp: true
theme: default
paginate: true
header: '**멀티에이전트 프로토콜 학습 과정**'
footer: 'Week 4: AGP & ACP 프로토콜 탐구'
style: |
  section {
    font-size: 21px;
  }
  h1 {
    color: #ff6b35;
  }
  h2 {
    color: #e55a2b;
  }
  .cisco-theme {
    background-color: #004c93;
    color: white;
  }
  .ibm-theme {
    background-color: #0f62fe;
    color: white;
  }
---

# Week 4: AGP & ACP 프로토콜 탐구

## ⚡ 성능 vs 단순성의 대결

---

## 🎯 학습 목표

- **AGP (Agent Gateway Protocol)**의 고성능 네트워크 아키텍처 이해
- **ACP (Agent Communication Protocol)** 두 변형의 차이점 분석
- **성능 vs 단순성** 트레이드오프 관점에서 프로토콜 비교
- **엔터프라이즈 환경**에서의 실제 적용 시나리오 학습

---

# Part 1: AGP (Agent Gateway Protocol)

## 🚀 Cisco의 고성능 네트워킹 접근

---

## 🔧 AGP 핵심 개념

### Cisco + AGNTCY Collective 공동 개발
> **"네트워크 레벨에서 에이전트 통신을 최적화하는 전송 계층 프로토콜"**

### 설계 철학
- ⚡ **고성능**: gRPC + HTTP/2 + Protocol Buffers
- 🛡️ **엔터프라이즈 보안**: mTLS, RBAC, End-to-End 암호화
- 🎯 **중앙화된 제어**: Gateway를 통한 메시지 라우팅
- 🌐 **Internet of Agents**: 분산 에이전트 런타임

---

## 🏗️ AGP 아키텍처

```
    [Agent A] ←→ [Agent Gateway] ←→ [Agent B]
         ↑              ↑              ↑
    [gRPC Client]  [Routing Rules] [gRPC Client]
         ↑              ↑              ↑
    [mTLS Auth]   [Control Plane]  [mTLS Auth]
```

### 계층 구조
- **Data Plane**: 실제 메시지 라우팅 및 전달
- **Control Plane**: 인증, 권한, 정책 관리
- **Management Plane**: 모니터링, 로깅, 분석

---

## 🔄 AGP 통신 패턴

### 1. Request-Response
- **사용 사례**: 동기적 에이전트 호출
- **성능**: 낮은 지연시간 (<5ms P50)

### 2. Pub/Sub (발행-구독)
- **사용 사례**: 이벤트 기반 아키텍처
- **확장성**: 다대다 통신 지원

### 3. Fire-and-Forget
- **사용 사례**: 로깅, 알림
- **성능**: 최고 처리량 (10,000+ RPS)

### 4. Streaming
- **사용 사례**: 실시간 데이터 스트림
- **지연시간**: 마이크로초 단위

---

## 🔒 AGP 보안 모델

### mTLS (Mutual TLS)
- **양방향 인증**: 클라이언트와 서버 모두 인증서 검증
- **End-to-End 암호화**: 메시지 레벨 암호화

### RBAC (Role-Based Access Control)
```
User → Role → Permission → Resource
 ↓      ↓        ↓          ↓
John → Admin → Read/Write → All Agents
Jane → User  → Read       → Public Agents
```

### OAuth2 토큰 로테이션
- **자동 갱신**: 토큰 만료 전 자동 재발급
- **보안 강화**: 짧은 토큰 수명으로 위험 최소화

---

## 📊 AGP 성능 특성

### 목표 성능 지표
- **처리량**: 10,000+ RPS
- **지연시간**: <5ms P50, <50ms P99
- **가용성**: 99.9% 업타임
- **확장성**: 1,000+ 동시 에이전트

### 실제 벤치마크 (Cisco 발표)
```
Single Gateway: 15,000 RPS
Clustered Setup: 100,000+ RPS
Memory Usage: <2GB per gateway
CPU Usage: <20% under normal load
```

---

## 🌐 Internet of Agents (IoA)

### 분산 런타임 환경
- **지리적 분산**: 글로벌 에이전트 네트워크
- **자동 디스커버리**: 네트워크 토폴로지 자동 구성
- **로드 밸런싱**: 트래픽 자동 분산
- **장애 복구**: 자동 failover 메커니즘

### 실제 구현: AGNTCY Collective
- **GitHub**: https://github.com/agntcy/agp
- **프로덕션 사례**: 여러 스타트업에서 검증
- **커뮤니티**: 활발한 오픈소스 개발

---

# Part 2: ACP (Agent Communication Protocol)

## 🤝 단순성을 추구하는 두 가지 접근

---

## 🔀 ACP의 두 가지 변형

### 1. IBM ACP (Linux Foundation)
- **거버넌스**: Linux Foundation으로 기증 (2025년 3월)
- **플랫폼**: BeeAI 플랫폼 기반
- **목적**: 범용 에이전트 통신 표준

### 2. AGNTCY ACP (Agent Connect Protocol)
- **거버넌스**: Cisco AGNTCY Collective
- **목적**: 프레임워크 간 통합 중심
- **특징**: OASF(Open Agent Service Framework) 연계

---

## 🏢 IBM ACP (Linux Foundation)

### 핵심 특징
- **RESTful API**: HTTP 기반 단순한 인터페이스
- **중앙화된 레지스트리**: 에이전트 등록 및 발견
- **SDK 불요**: curl로 직접 호출 가능
- **BeeAI 통합**: IBM의 AI 플랫폼과 네이티브 연동

### 아키텍처
```
[Agent] → [REST API] → [ACP Registry] → [BeeAI Platform]
   ↑                        ↑                ↑
[HTTP POST]           [Service Discovery]  [AI Model]
```

---

## 🔧 AGNTCY ACP (Agent Connect Protocol)

### 핵심 특징
- **프레임워크 중립**: LangChain, AutoGen, 커스텀 에이전트 지원
- **MIME 타입 지원**: 다양한 데이터 형식 처리
- **상태 기반 세션**: 장기 실행 작업 지원
- **Async-first 설계**: 비동기 처리 최적화

### 아키텍처
```
[LangChain] ←→ [ACP Bridge] ←→ [AutoGen]
     ↑              ↑             ↑
[Chain Logic]  [Protocol    [Multi-Agent
                Translation]  Discussion]
```

---

## 📊 두 ACP 변형 비교

| 특징 | IBM ACP | AGNTCY ACP |
|:---:|:---:|:---:|
| **거버넌스** | Linux Foundation | Cisco AGNTCY |
| **목적** | 범용 에이전트 통신 | 프레임워크 통합 |
| **플랫폼** | BeeAI 중심 | 프레임워크 중립 |
| **복잡성** | 단순 (REST만) | 중간 (브릿지 필요) |
| **확장성** | 중앙화 제한 | 분산 친화적 |

### 공통점
- **RESTful API** 기반
- **SDK 없는 접근** 가능
- **오픈소스** 라이선스
- **Async-first** 설계

---

## 🛠️ ACP 실제 사용 예시

### IBM ACP - curl 직접 호출
```bash
# 에이전트 실행
curl -X POST http://acp-server/agents/data-analyst/runs \
  -H "Content-Type: application/json" \
  -d '{
    "input": [{
      "parts": [{
        "content": "Analyze Q3 sales data",
        "content_type": "text/plain"
      }]
    }]
  }'
```

### AGNTCY ACP - 프레임워크 브릿지
```python
# LangChain → AutoGen 통신
from acp_bridge import LangChainToAutoGenBridge

bridge = LangChainToAutoGenBridge()
result = await bridge.delegate_task(
    from_agent="langchain_analyst",
    to_agent="autogen_discussion_group",
    task="Analyze and discuss sales trends"
)
```

---

## 🔄 멀티모달 메시지 지원

### MIME 타입 처리
```json
{
  "input": [{
    "parts": [
      {
        "content": "Analyze this chart",
        "content_type": "text/plain"
      },
      {
        "content": "base64_encoded_image...",
        "content_type": "image/png"
      },
      {
        "content": "sales_data.csv content",
        "content_type": "text/csv"
      }
    ]
  }]
}
```

### 지원 형식
- **텍스트**: text/plain, text/markdown
- **이미지**: image/png, image/jpeg
- **데이터**: text/csv, application/json
- **문서**: application/pdf

---

## 🏢 오프라인 발견 메커니즘

### 패키지 메타데이터 기반
```json
{
  "name": "financial-analysis-agent",
  "version": "1.2.0",
  "acp_capabilities": [
    "data-analysis",
    "financial-modeling",
    "risk-assessment"
  ],
  "endpoints": {
    "run": "/agents/financial/runs",
    "status": "/agents/financial/status"
  }
}
```

### 에어갭 환경 지원
- **오프라인 카탈로그**: 로컬 에이전트 목록 관리
- **수동 등록**: 네트워크 없이 에이전트 발견
- **보안 환경**: 격리된 네트워크에서도 사용 가능

---

## 🔄 4가지 프로토콜 종합 비교

| 특징 | MCP | A2A | AGP | ACP |
|:---:|:---:|:---:|:---:|:---:|
| **목적** | LLM 도구 연결 | 에이전트 협업 | 고성능 통신 | 단순한 통신 |
| **복잡성** | 중간 | 높음 | 높음 | 낮음 |
| **성능** | 보통 | 좋음 | 최고 | 보통 |
| **보안** | 기본 | 강함 | 최강 | 기본 |
| **진입장벽** | 낮음 | 중간 | 높음 | 최저 |

---

## 🎯 프로토콜 선택 가이드

### 성능이 최우선인 경우 → **AGP**
- 금융 거래 시스템
- 실시간 게임 AI
- IoT 대규모 네트워크

### 빠른 프로토타이핑이 필요한 경우 → **ACP**
- 스타트업 MVP
- 교육 및 연구 프로젝트
- 레거시 시스템 통합

### LLM 도구 통합이 주목적 → **MCP**
- AI 어시스턴트 개발
- 데이터 분석 파이프라인
- 개발 도구 통합

### 전문 에이전트 협업이 필요 → **A2A**
- 복잡한 워크플로우 자동화
- 다중 전문가 시스템
- 크로스 플랫폼 통합

---

## 🚨 각 프로토콜의 한계

### AGP의 한계
- **높은 복잡성**: 설정 및 유지보수 어려움
- **벤더 종속**: Cisco 생태계에 의존
- **과도한 성능**: 단순한 용도에는 오버스펙

### ACP의 한계
- **성능 제한**: RESTful API의 오버헤드
- **표준화 부족**: 두 변형으로 인한 혼란
- **기능 제한**: 고급 보안 기능 부족

### 공통 과제
- **상호 운용성**: 프로토콜 간 브릿지 필요
- **학습 곡선**: 각각 다른 개념과 도구
- **생태계 분열**: 표준 통합의 어려움

---

## 🔮 미래 전망

### 단기 전망 (1-2년)
- **하이브리드 접근**: 여러 프로토콜 조합 사용
- **성능 최적화**: 각 프로토콜의 병목지점 개선
- **도구 개선**: 개발자 경험 향상

### 장기 전망 (3-5년)
- **표준 수렴**: 성공적인 특징들의 통합
- **새로운 패러다임**: 현재 프로토콜을 뛰어넘는 혁신
- **산업 표준화**: W3C, IETF 등 공식 표준 채택

---

## 📝 1부 총정리

### 4가지 프로토콜의 위치
1. **MCP**: LLM 생태계의 허브
2. **A2A**: 에이전트 협업의 표준
3. **AGP**: 고성능 네트워킹의 강자
4. **ACP**: 단순함과 접근성의 챔피언

### 다음 주 예고: 실습 시작
**Week 5-6: MCP 실습 프로젝트**
- "통합 개발 환경 확장 시스템" 구현
- Claude Desktop 실제 연동 체험
- 5가지 프리미티브 실제 활용

---

## 🎯 과제 안내

### 주간 과제: 프로토콜 비교 분석
1. **가상의 비즈니스 시나리오** 설정
2. **4가지 프로토콜**로 각각 해결 방안 설계
3. **성능, 복잡성, 비용** 관점에서 비교 분석
4. **최종 추천안** 및 근거 제시
5. **A4 5페이지** 분량으로 작성

### 평가 기준
- 시나리오의 현실성 (25%)
- 프로토콜 이해도 (35%)
- 분석의 깊이 (25%)
- 추천의 합리성 (15%)

---

## 💭 토론 주제

### 생각해볼 질문들
- 🤔 성능과 단순성 중 무엇이 더 중요할까?
- 🤔 프로토콜 분열이 생태계에 미치는 영향은?
- 🤔 10년 후에도 이 4가지 프로토콜이 살아남을까?
- 🤔 새로운 프로토콜이 나타난다면 어떤 특징을 가져야 할까?

### 다음 수업 준비
- 개발 환경 설정 완료 (Python, Node.js, Docker)
- GitHub, Google Drive 계정 준비
- Claude Desktop 설치 (선택사항)

**이론 기초 완료! 이제 실습으로 넘어갑니다! 🚀** 