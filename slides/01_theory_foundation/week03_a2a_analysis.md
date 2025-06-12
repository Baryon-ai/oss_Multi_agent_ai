---
marp: true
theme: default
paginate: true
header: '**멀티에이전트 프로토콜 학습 과정**'
footer: 'Week 3: A2A (Agent to Agent Protocol) 분석'
style: |
  section {
    font-size: 22px;
  }
  h1 {
    color: #4285f4;
  }
  h2 {
    color: #1a73e8;
  }
  .highlight {
    background-color: #e8f0fe;
    padding: 15px;
    border-left: 4px solid #4285f4;
  }
---

# Week 3: A2A (Agent to Agent Protocol) 분석

## 🤝 Google의 에이전트 협업 혁신

---

## 🎯 학습 목표

- **A2A 프로토콜**의 에이전트 간 협업 철학 이해
- **Agent Card 시스템**과 서비스 발견 메커니즘 학습
- **Task 중심 아키텍처**와 라이프사이클 관리 파악
- **50+ 파트너 생태계**와 실제 적용 사례 분석

---

## 🚀 A2A란 무엇인가?

### Google의 비전
> **"Agent to Agent Protocol: 전문화된 에이전트들이 협업하여 복잡한 작업을 효율적으로 해결"**

### 핵심 철학
- 🤝 **에이전트 협업**: 각자의 전문성을 살린 분업
- 🔍 **동적 발견**: 필요에 따라 적절한 에이전트 찾기
- 🔒 **안전한 협업**: DID 기반 신뢰 메커니즘
- 🌐 **생태계 확장**: 다양한 프레임워크 간 상호 운용성

---

## 🏗️ A2A 아키텍처 개요

```
[Client Agent] ←→ [Remote Agent]
      ↑               ↑
      ↓               ↓
[Agent Card]    [Agent Card]
      ↑               ↑
      ↓               ↓
[Service Discovery] ←→ [DID Auth]
```

### 구성요소
- **Agent Card**: 에이전트 메타데이터 (JSON 형식)
- **Service Discovery**: 동적 에이전트 발견
- **DID Authentication**: 분산 신원 확인
- **Task Lifecycle**: 작업 생성 → 실행 → 완료

---

## 📋 Agent Card 시스템

### Agent Card 구조
```json
{
  "agent_id": "data-analyst",
  "display_name": "Data Analysis Agent",
  "description": "Performs statistical analysis",
  "capabilities": ["data-analysis", "visualization"],
  "endpoint": "https://my-agent.example.com",
  "supported_modalities": ["text", "json", "csv"],
  "authentication": {
    "method": "DID",
    "public_key": "..."
  }
}
```

### Agent Card의 역할
- 🏷️ **신원 증명**: 에이전트의 정체성 명시
- 🛠️ **능력 공개**: 제공 가능한 서비스 목록
- 🔗 **연결 정보**: 접근 방법 및 인증 정보

---

## 🔍 서비스 발견 메커니즘

### 동적 발견 과정
1. **요구사항 분석**: 필요한 능력(capability) 정의
2. **에이전트 검색**: Registry에서 적합한 에이전트 탐색
3. **신뢰성 검증**: DID를 통한 신원 확인
4. **연결 설정**: 실제 통신 채널 구축

### 검색 기준
- **Capability Matching**: 필요한 기능 보유 여부
- **Modality Support**: 지원하는 데이터 형식
- **Performance Metrics**: 응답 시간, 신뢰도
- **Geographic Location**: 지역적 제약사항

---

## 🔐 DID 기반 인증 시스템

### DID (Decentralized Identifiers)란?
- **분산 신원 확인**: 중앙 기관 없이 신원 증명
- **자기 주권 신원**: 에이전트가 자신의 신원 관리
- **상호 운용성**: 다양한 플랫폼 간 신뢰 구축

### A2A에서의 DID 활용
```
Agent A ←→ DID Registry ←→ Agent B
  ↓                              ↓
[인증서 제출]              [인증서 검증]
  ↓                              ↓
[신뢰 구축] ←→ [안전한 통신] ←→ [협업 시작]
```

---

## 📊 Task 중심 아키텍처

### Task 라이프사이클
1. **Task 생성**: 클라이언트가 작업 요청
2. **Agent 할당**: 적절한 에이전트 선택
3. **실행 모니터링**: 진행 상황 추적
4. **결과 반환**: 완료된 작업 결과 전달
5. **정리**: 리소스 해제 및 세션 종료

### Task 관리 특징
- **비동기 처리**: 장시간 작업 지원
- **진행 상황 추적**: 실시간 상태 업데이트
- **오류 처리**: 실패 시 복구 메커니즘
- **스트리밍**: Server-Sent Events 지원

---

## 🌐 통신 프로토콜

### JSON-RPC 2.0 over HTTP(S)
```json
{
  "jsonrpc": "2.0",
  "method": "execute_task",
  "params": {
    "task_type": "data_analysis",
    "data": {...},
    "options": {...}
  },
  "id": "task_123"
}
```

### 지원하는 통신 패턴
- **동기 호출**: 즉시 응답이 필요한 작업
- **비동기 처리**: 장시간 실행되는 작업
- **스트리밍**: 실시간 데이터 전송
- **푸시 알림**: 작업 완료 시 자동 알림

---

## 🤖 Opaque Agent 개념

### Opaque Agent의 특징
- **블랙박스 모델**: 내부 구현 숨김
- **인터페이스 중심**: 입력/출력만 공개
- **보안 강화**: 내부 상태 노출 방지
- **유연성 증대**: 구현 변경 시 호환성 유지

### 장점
- 🔒 **보안**: 내부 로직 보호
- 🔧 **유지보수**: 독립적 업데이트 가능
- 🤝 **협업**: 표준 인터페이스로 통신
- 📈 **확장성**: 내부 최적화 자유

---

## 🏢 50+ 파트너 생태계

### 기술 파트너 (Technology Partners)
- **Salesforce**: CRM 데이터 연동
- **Atlassian**: 프로젝트 관리 도구
- **MongoDB**: 데이터베이스 서비스
- **Box**: 클라우드 스토리지
- **Cohere**: AI 언어 모델
- **Intuit**: 금융 소프트웨어
- **PayPal**: 결제 서비스

### 서비스 파트너 (Service Partners)
- **Big 4 컨설팅**: Accenture, Deloitte, KPMG, PwC
- **McKinsey & Company**: 전략 컨설팅
- **BCG**: 비즈니스 혁신
- **Capgemini**: 디지털 변환

---

## 🛠️ 프레임워크 통합

### 지원하는 AI 프레임워크
- **LangChain**: 체인 기반 워크플로우
- **AutoGen**: Microsoft의 멀티에이전트 시스템
- **LlamaIndex**: 문서 검색 및 분석

### 통합 방식
```
LangChain Agent ←→ A2A Protocol ←→ AutoGen Agent
       ↑                                  ↑
   [Chain 실행]                      [그룹 토론]
       ↓                                  ↓
   [결과 공유] ←→ [A2A 메시징] ←→ [작업 분배]
```

---

## 📱 실제 적용 사례

### 1. 자동차 수리점 시나리오 (공식 예제)
```
고객 문의 → [접수 에이전트] → [진단 에이전트]
                ↓                      ↓
          [견적 에이전트] ← → [부품 조달 에이전트]
                ↓                      ↓
          [일정 관리 에이전트] → [알림 에이전트]
```

### 2. 마케팅 캠페인 관리
- **데이터 분석 에이전트**: 고객 세분화
- **콘텐츠 생성 에이전트**: 개인화된 메시지
- **채널 관리 에이전트**: 다중 채널 배포
- **성과 측정 에이전트**: ROI 분석

### 3. 고객 서비스 자동화
- **문의 분류 에이전트**: 자동 티켓 분류
- **지식 검색 에이전트**: FAQ 및 매뉴얼 검색
- **에스컬레이션 에이전트**: 복잡한 문의 전달

---

## 🎮 A2A 실습 시나리오

### 크로스 플랫폼 에이전트 마켓플레이스
1. **Agent Card 생성**: 자신의 전문 에이전트 정의
2. **서비스 등록**: Registry에 에이전트 등록
3. **동적 발견**: 다른 에이전트 검색 및 연결
4. **협업 실행**: 실제 작업 위임 및 결과 수신

### 실습 목표
- Agent Card 설계 및 구현
- DID 기반 인증 체험
- Task 라이프사이클 관리
- 스트리밍 통신 구현

---

## 🔄 A2A vs MCP 비교

| 특징 | A2A | MCP |
|:---:|:---:|:---:|
| **목적** | 에이전트 간 협업 | LLM 컨텍스트 제공 |
| **구조** | P2P 네트워크 | Client-Server |
| **발견** | 동적 서비스 발견 | 정적 서버 등록 |
| **인증** | DID 기반 | 토큰/키 기반 |
| **통신** | JSON-RPC over HTTP | JSON-RPC (다양한 전송) |

### 상호 보완 관계
- **A2A + MCP**: 에이전트가 MCP 서버를 통해 도구 접근
- **협업 시나리오**: A2A로 에이전트 발견, MCP로 도구 활용

---

## 📈 Google Cloud Next 2025 발표

### 주요 발표 내용 (2025년 4월)
- **50+ 파트너 확정**: 기술 및 서비스 파트너십
- **프로덕션 준비**: 엔터프라이즈급 안정성 확보
- **관찰 가능성**: 내장된 모니터링 및 로깅
- **글로벌 확산**: 다국가 지원 계획

### 향후 로드맵
- **성능 최적화**: 지연 시간 단축
- **보안 강화**: 양자 안전 암호화 지원
- **AI 통합**: Google Gemini와의 네이티브 연동
- **오픈소스**: 핵심 구성요소 오픈소스화

---

## 🌟 A2A의 독특한 장점

### 1. 전문화와 협업의 조화
- **단일 에이전트**: 모든 기능을 구현해야 함
- **A2A 에이전트**: 전문 분야에 집중, 필요시 협업

### 2. 동적 생태계
- **정적 통합**: 미리 정의된 연결만 가능
- **A2A 발견**: 런타임에 최적의 파트너 찾기

### 3. 확장성과 유연성
- **수직 확장**: 단일 에이전트 성능 향상
- **수평 확장**: 새로운 전문 에이전트 추가

---

## 🔮 다음 주 예고: AGP & ACP

### Agent Gateway Protocol (AGP)
- **Cisco의 고성능 접근**: gRPC + HTTP/2
- **게이트웨이 중심**: 중앙화된 메시지 라우팅
- **엔터프라이즈 보안**: mTLS, RBAC

### Agent Communication Protocol (ACP)
- **두 가지 변형**: IBM ACP vs AGNTCY ACP
- **RESTful 단순성**: SDK 없는 curl 친화적 API
- **오픈소스 거버넌스**: Linux Foundation vs Cisco

---

## 📝 이번 주 정리

### 핵심 개념
1. **A2A = 에이전트 협업 플랫폼**: 전문화된 에이전트들의 동적 협업
2. **Agent Card**: JSON 기반 에이전트 메타데이터
3. **DID 인증**: 분산 신원 확인 시스템
4. **Task 라이프사이클**: 생성 → 실행 → 완료

### 실무 적용 포인트
- **마이크로서비스 아키텍처**와 유사한 에이전트 분해
- **API 게이트웨이** 패턴의 에이전트 버전
- **서비스 메시** 개념의 AI 에이전트 적용

---

## 🎯 과제 안내

### 주간 과제: 에이전트 협업 시나리오 설계
1. **실제 비즈니스 문제** 선정 (예: 고객 서비스, 마케팅)
2. **에이전트 역할 분해**: 3-5개 전문 에이전트 정의
3. **Agent Card 설계**: 각 에이전트의 메타데이터 작성
4. **협업 워크플로우**: 에이전트 간 상호작용 시나리오
5. **A4 4페이지** 분량으로 작성

### 제출 기한
**다음 주 수업 시작 전까지**

---

## 💭 토론 주제

### 생각해볼 질문들
- 🤔 A2A가 기존 마이크로서비스와 다른 점은?
- 🤔 에이전트 간 신뢰를 어떻게 구축할 수 있을까?
- 🤔 50+ 파트너 생태계의 진짜 의미는?
- 🤔 Opaque Agent의 한계는 무엇일까?

### 다음 수업 준비
- Cisco AGP 및 IBM/AGNTCY ACP 문서 조사
- gRPC vs RESTful API 차이점 복습

**감사합니다! 🙏** 