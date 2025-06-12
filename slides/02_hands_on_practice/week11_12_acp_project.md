---
marp: true
theme: default
paginate: true
header: '**멀티에이전트 프로토콜 학습 과정**'
footer: 'Week 11-12: ACP 실습 프로젝트 - 에이전트 연합 학습 플랫폼'
style: |
  section {
    font-size: 22px;
  }
  h1 {
    color: #0f62fe;
  }
  h2 {
    color: #0043ce;
  }
  .ibm-box {
    background-color: #0f62fe;
    color: white;
    padding: 20px;
    border-left: 5px solid #78a9ff;
    margin: 15px 0;
  }
  .cisco-box {
    background-color: #004c93;
    color: white;
    padding: 20px;
    border-left: 5px solid #00bceb;
    margin: 15px 0;
  }
---

# Week 11-12: ACP 실습 프로젝트

## 🤝 "에이전트 연합 학습 플랫폼" 구현

---

## 🎯 프로젝트 개요

### 프로젝트 목표
> **"SDK 없이도 curl로 호출 가능한 초단순 에이전트 연합 플랫폼 구축"**

### 핵심 아이디어
- **RESTful 단순성**: 복잡한 SDK 없이 HTTP만으로 통신
- **두 ACP 비교**: IBM ACP vs AGNTCY ACP 실제 구현
- **연합 학습**: 다양한 프레임워크 에이전트의 협력 학습
- **오픈소스 거버넌스**: Linux Foundation vs Cisco 모델

---

## 🔀 두 가지 ACP 변형 비교 구현

### Part A: IBM ACP (Linux Foundation)
- **BeeAI 플랫폼**: IBM AI 생태계 통합
- **중앙화된 레지스트리**: 단일 에이전트 등록소
- **범용 통신**: 모든 종류의 에이전트 지원

### Part B: AGNTCY ACP (Cisco)
- **프레임워크 브릿지**: LangChain ↔ AutoGen 연결
- **분산 발견**: 패키지 메타데이터 기반
- **오프라인 지원**: 네트워크 없이도 에이전트 발견

### 실습 목표
두 접근 방식의 **장단점을 직접 체험**하고 비교 분석

---

## 📋 Week 11: IBM ACP 구현

### Day 1-2: 중앙화된 Registry 구축
- **에이전트 등록 API**: POST /agents/register
- **능력 기반 검색**: GET /agents/search?capability=X
- **BeeAI 연동**: IBM Watson 통합

### Day 3-4: RESTful 에이전트 API
- **동기 실행**: POST /agents/{id}/runs
- **비동기 실행**: POST /agents/{id}/runs/async
- **스트리밍**: GET /agents/{id}/runs/{run_id}/stream

### Day 5: curl 친화적 테스트
- **SDK 없는 호출**: 순수 curl 명령어만 사용
- **JSON 페이로드**: 표준 REST API 패턴
- **HTTP 상태 코드**: RESTful 규칙 준수

---

## 📋 Week 12: AGNTCY ACP 구현

### Day 1-2: 프레임워크 브릿지
- **LangChain 래퍼**: 체인을 ACP 에이전트로 변환
- **AutoGen 통합**: 멀티에이전트 그룹 연결
- **커스텀 에이전트**: 독립적인 AI 모델 통합

### Day 3-4: 오프라인 발견 시스템
- **패키지 메타데이터**: npm/pip 스타일 발견
- **로컬 카탈로그**: 네트워크 없는 에이전트 목록
- **에어갭 환경**: 격리된 네트워크 지원

### Day 5: 두 ACP 비교 데모
- **동일 작업**: 두 시스템으로 같은 작업 수행
- **성능 비교**: 응답 시간, 복잡성, 사용성
- **장단점 분석**: 실무 적용 관점에서 평가

---

## 🏗️ IBM ACP 아키텍처

```
    [Client (curl)]
           ↓ (HTTP POST)
    [ACP REST Server]
           ↓
    [Agent Registry]
           ↓
  ┌─────────────────┐
  │    BeeAI        │
  │  ┌───┬───┬───┐  │
  │  │LLM│ML │NLP│  │
  │  │   │   │   │  │
  │  └───┴───┴───┘  │
  └─────────────────┘
```

### 특징
- **중앙화**: 모든 에이전트가 하나의 레지스트리에 등록
- **표준화**: 일관된 API 인터페이스
- **통합**: IBM 생태계와의 깊은 연동

---

## 🏗️ AGNTCY ACP 아키텍처

```
[LangChain Agent] ←→ [ACP Bridge] ←→ [AutoGen Group]
       ↑                  ↑                ↑
   [package.json]   [ACP Translator]   [setup.py]
       ↑                  ↑                ↑
   [Local Catalog] ←→ [Discovery] ←→ [Local Catalog]
```

### 특징
- **분산화**: 각 프레임워크가 독립적 운영
- **유연성**: 기존 프레임워크와 최소 수정으로 통합
- **오프라인**: 네트워크 분리 환경에서도 작동

---

## 🎮 실습 시나리오: 연합 학습

### 시나리오 1: 다국어 번역 품질 개선
```
IBM ACP 방식:
curl -X POST http://acp-server/agents/translator/runs \
  -H "Content-Type: application/json" \
  -d '{
    "input": [{
      "parts": [{
        "content": "Improve translation quality",
        "content_type": "text/plain"
      }]
    }],
    "feedback_mode": true
  }'

AGNTCY ACP 방식:
# LangChain 번역 에이전트 ↔ AutoGen 품질 평가 그룹
```

### 시나리오 2: 협업 코드 리뷰
```
여러 에이전트가 협력하여 코드 품질 향상:
1. [문법 검사 에이전트] → 기본적인 문법 오류 발견
2. [성능 분석 에이전트] → 성능 병목 지점 분석
3. [보안 검토 에이전트] → 보안 취약점 검사
4. [통합 평가 에이전트] → 종합적인 개선 권고
```

---

## 📊 curl 친화적 API 설계

### IBM ACP REST API
```bash
# 에이전트 등록
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-analyst",
    "capabilities": ["data-analysis", "visualization"],
    "description": "Advanced data analysis agent"
  }'

# 에이전트 검색
curl "http://localhost:8000/agents?capability=data-analysis"

# 작업 실행
curl -X POST http://localhost:8000/agents/data-analyst/runs \
  -H "Content-Type: application/json" \
  -d '{
    "input": [{
      "parts": [{
        "content": "Analyze sales data for Q3",
        "content_type": "text/plain"
      }]
    }]
  }'
```

---

## 🔄 프레임워크 간 통합 (AGNTCY ACP)

### LangChain 에이전트 ACP 래핑
```python
from acp_bridge import LangChainACPWrapper

class LangChainAnalyst(LangChainACPWrapper):
    def __init__(self):
        super().__init__(
            agent_name="langchain-analyst",
            capabilities=["data-analysis", "reasoning"]
        )
        self.chain = create_analysis_chain()
    
    async def execute(self, input_data):
        result = await self.chain.arun(input_data)
        return self.format_acp_response(result)
```

### AutoGen 그룹 ACP 연동
```python
from acp_bridge import AutoGenACPWrapper

class AutoGenReviewGroup(AutoGenACPWrapper):
    def __init__(self):
        super().__init__(
            agent_name="autogen-reviewers",
            capabilities=["peer-review", "consensus"]
        )
        self.group_chat = GroupChat([
            critic_agent, advisor_agent, synthesizer_agent
        ])
    
    async def execute(self, input_data):
        discussion = await self.group_chat.run(input_data)
        return self.synthesize_consensus(discussion)
```

---

## 🎯 연합 학습 메커니즘

### 지식 공유 패턴
- **피드백 루프**: 에이전트 간 성과 평가 및 개선
- **모델 앙상블**: 여러 에이전트의 결과 결합
- **점진적 학습**: 시간에 따른 성능 향상 추적

### 협업 학습 시나리오
```
Round 1: 각 에이전트가 독립적으로 작업 수행
Round 2: 결과를 공유하고 피어 리뷰 실시
Round 3: 피드백을 반영하여 개선된 결과 생성
Round N: 수렴할 때까지 반복
```

### 성능 메트릭
- **개별 성능**: 각 에이전트의 정확도, 속도
- **협업 효과**: 단독 vs 협업 시 성능 차이
- **학습 속도**: 피드백을 통한 개선 속도

---

## 🔍 오프라인 발견 시스템

### 패키지 메타데이터 예시
```json
{
  "name": "financial-advisor-agent",
  "version": "2.1.0",
  "acp_info": {
    "capabilities": [
      "portfolio-analysis",
      "risk-assessment",
      "market-prediction"
    ],
    "endpoints": {
      "run": "/agents/financial-advisor/runs",
      "status": "/agents/financial-advisor/status",
      "health": "/agents/financial-advisor/health"
    },
    "requirements": {
      "python": ">=3.9",
      "memory": "2GB",
      "cpu": "2 cores"
    }
  }
}
```

### 로컬 카탈로그 관리
```bash
# 에이전트 카탈로그 업데이트
acp-cli catalog update

# 로컬 에이전트 검색
acp-cli search --capability data-analysis

# 오프라인 에이전트 목록
acp-cli list --offline
```

---

## 📈 성능 및 사용성 비교

### 개발 복잡성
| 측면 | IBM ACP | AGNTCY ACP |
|:---:|:---:|:---:|
| **설정 시간** | 5분 | 30분 |
| **API 학습** | 1시간 | 3시간 |
| **첫 에이전트 등록** | 10분 | 45분 |
| **프레임워크 통합** | 쉬움 | 복잡함 |

### 운영 특성
| 측면 | IBM ACP | AGNTCY ACP |
|:---:|:---:|:---:|
| **네트워크 의존성** | 높음 | 낮음 |
| **확장성** | 제한적 | 우수함 |
| **장애 내성** | SPOF 위험 | 분산 복원력 |
| **보안 격리** | 중앙 관리 | 분산 관리 |

---

## 🛠️ 개발 환경 및 도구

### IBM ACP 스택
- **FastAPI**: RESTful 서버 구현
- **SQLAlchemy**: 에이전트 메타데이터 저장
- **Redis**: 세션 및 캐시 관리
- **IBM Watson**: AI 모델 통합

### AGNTCY ACP 스택
- **LangChain**: 체인 기반 에이전트
- **AutoGen**: 멀티에이전트 시스템
- **aiohttp**: 비동기 HTTP 클라이언트
- **YAML**: 설정 파일 관리

### 공통 도구
- **curl**: API 테스트 및 상호작용
- **jq**: JSON 데이터 처리
- **Postman**: API 문서화 및 테스트

---

## 🎯 학습 목표별 평가 기준

### 1. ACP 프로토콜 이해 (25%)
- **두 변형 차이**: IBM vs AGNTCY ACP 명확한 구분
- **RESTful 설계**: 표준 HTTP 패턴 준수
- **curl 활용**: SDK 없이 완전한 기능 사용

### 2. 연합 학습 구현 (25%)
- **협업 메커니즘**: 에이전트 간 효과적 지식 공유
- **성능 향상**: 협업을 통한 실제 품질 개선
- **학습 측정**: 정량적 개선 지표 제시

### 3. 시스템 통합 (20%)
- **프레임워크 브릿지**: LangChain, AutoGen 성공적 연동
- **오프라인 발견**: 네트워크 없는 환경에서 작동
- **호환성**: 기존 시스템과의 원활한 통합

### 4. 사용성 및 단순성 (20%)
- **개발자 경험**: 직관적이고 쉬운 API
- **문서화**: 완전한 사용 가이드
- **오류 처리**: 친화적인 에러 메시지

### 5. 비교 분석 (10%)
- **객관적 평가**: 두 ACP 변형의 장단점 분석
- **실무 관점**: 실제 적용 시나리오별 추천
- **미래 전망**: 발전 방향 제시

---

## 🔮 실무 적용 시나리오

### 스타트업 환경
- **빠른 프로토타이핑**: 최소한의 설정으로 즉시 시작
- **비용 효율성**: 복잡한 인프라 없이 운영
- **학습 곡선**: 개발자 온보딩 시간 단축

### 엔터프라이즈 환경
- **레거시 통합**: 기존 시스템과의 점진적 통합
- **거버넌스**: 오픈소스 vs 상용 라이선스 고려
- **보안 요구사항**: 격리된 네트워크 환경 지원

### 연구 기관
- **실험적 접근**: 다양한 AI 모델 조합 실험
- **재현 가능성**: 실험 결과의 일관된 재현
- **협업 연구**: 기관 간 에이전트 공유

---

## 📝 주간 과제 및 평가

### Week 11 과제
1. **IBM ACP 시스템** 완전 구현
2. **curl 기반 사용 가이드** 작성
3. **BeeAI 통합** 테스트

### Week 12 과제
1. **AGNTCY ACP 브릿지** 구현
2. **오프라인 발견 시스템** 테스트
3. **두 ACP 비교 분석** 리포트

### 최종 평가 (Week 12 금요일)
- **시스템 데모** (35%): 두 ACP 완전 동작
- **curl 시연** (25%): SDK 없는 완전한 기능 사용
- **비교 분석 발표** (25%): 객관적 장단점 분석
- **연합 학습 성과** (15%): 협업을 통한 개선 효과

---

## 💡 확장 아이디어

### 하이브리드 ACP
- **두 접근법 결합**: IBM의 중앙화 + AGNTCY의 분산화
- **상황별 전환**: 네트워크 상황에 따른 자동 모드 변경
- **점진적 마이그레이션**: 한 방식에서 다른 방식으로 전환

### 고급 연합 학습
- **차등 프라이버시**: 개인정보 보호하며 학습
- **연합 강화학습**: 에이전트 간 정책 공유
- **메타 학습**: 학습 자체를 학습하는 에이전트

### 커뮤니티 생태계
- **에이전트 마켓플레이스**: 공개 에이전트 저장소
- **평가 시스템**: 커뮤니티 기반 에이전트 평점
- **기여 인센티브**: 오픈소스 기여 보상 체계

---

## 🔚 2부 실습 총정리

### 4가지 프로토콜 실습 완료
1. **MCP (Week 5-6)**: LLM 도구 통합의 표준
2. **A2A (Week 7-8)**: 에이전트 협업의 미래
3. **AGP (Week 9-10)**: 엔터프라이즈 성능의 정점
4. **ACP (Week 11-12)**: 단순함의 힘

### 다음 주 예고: 고급 주제
**Week 13-16: 3부 고급 주제 및 프로젝트**
- 성능 벤치마킹 및 비교
- 보안 및 신뢰성 분석
- 프로토콜 상호 운용성
- 최종 개인 프로젝트

**실습의 대장정이 끝나갑니다! 이제 종합적인 분석과 개인 프로젝트가 남았습니다! 🎓** 