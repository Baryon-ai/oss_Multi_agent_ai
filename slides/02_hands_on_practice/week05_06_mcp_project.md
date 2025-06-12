---
marp: true
theme: default
paginate: true
header: '**멀티에이전트 프로토콜 학습 과정**'
footer: 'Week 5-6: MCP 실습 프로젝트 - 통합 개발 환경 확장'
style: |
  section {
    font-size: 22px;
  }
  h1 {
    color: #e74c3c;
  }
  h2 {
    color: #c0392b;
  }
  .project-box {
    background-color: #fff3cd;
    padding: 20px;
    border-left: 5px solid #ffc107;
    margin: 15px 0;
  }
---

# Week 5-6: MCP 실습 프로젝트

## 🔌 "통합 개발 환경 확장 시스템" 구현

---

## 🎯 프로젝트 개요

### 프로젝트 목표
> **"LLM이 개발자의 일상 도구들과 자연스럽게 연동되는 통합 환경 구축"**

### 핵심 아이디어
- **GitHub**: 코드 리포지토리 접근 및 분석
- **Google Drive**: 문서 및 디자인 파일 관리
- **Slack**: 팀 커뮤니케이션 자동화
- **PostgreSQL**: 프로젝트 데이터베이스 조회
- **Claude Desktop**: 실제 MCP 연동 체험

---

## 🎪 MCP 5가지 프리미티브 활용 계획

### 1. 📄 Resources (리소스)
- **GitHub 파일**: README.md, 코드 파일, 이슈 목록
- **Google Drive 문서**: 프로젝트 명세서, 회의록
- **데이터베이스 스키마**: 테이블 구조, 관계 정보

### 2. 🛠️ Tools (도구)
- **GitHub API**: 이슈 생성, PR 분석, 커밋 히스토리
- **Slack API**: 메시지 발송, 채널 관리
- **SQL 실행**: 데이터 조회, 분석 쿼리

### 3. 💬 Prompts (프롬프트)
- **코드 리뷰 템플릿**: 표준화된 리뷰 가이드라인
- **문서 작성 가이드**: API 문서, 사용자 매뉴얼 템플릿
- **회의 요약 형식**: 액션 아이템 추출 템플릿

---

## 📋 Week 5: 설계 및 기초 구현

### Day 1-2: 아키텍처 설계
- **MCP 서버 구조** 설계
- **서비스별 인터페이스** 정의
- **보안 모델** 수립

### Day 3-4: GitHub 서버 구현
- **Repository Resources**: 파일 목록, 내용 접근
- **Issue Tools**: 이슈 생성, 검색, 업데이트
- **Webhook 처리**: 실시간 이벤트 수신

### Day 5: Google Drive 연동
- **Document Resources**: 문서 읽기, 메타데이터
- **File Tools**: 업로드, 다운로드, 공유 설정

---

## 📋 Week 6: 통합 및 고도화

### Day 1-2: Slack 통합
- **Messaging Tools**: 자동 알림, 팀 업데이트
- **Channel Resources**: 대화 히스토리, 멤버 정보

### Day 3-4: PostgreSQL 연동
- **Schema Resources**: 테이블 구조, 관계 정보
- **Query Tools**: 데이터 조회, 분석 실행

### Day 5: Claude Desktop 연동
- **실제 MCP 클라이언트** 연결
- **종합 테스트** 및 데모 준비

---

## 🏗️ 시스템 아키텍처

```
    Claude Desktop (Host)
           ↓
      MCP Client
           ↓ (JSON-RPC 2.0)
    ┌─────────────────┐
    │   MCP Gateway   │
    └─────────────────┘
         ↓     ↓     ↓     ↓
    [GitHub] [Drive] [Slack] [PostgreSQL]
     Server   Server  Server   Server
```

### 각 서버의 역할
- **MCP Gateway**: 중앙 라우팅 및 인증 관리
- **서비스 서버들**: 각 외부 서비스와의 전용 연결
- **Claude Desktop**: 사용자 인터페이스 및 LLM 통합

---

## 🛡️ 보안 설계

### 인증 계층
1. **API 키 관리**: 각 서비스별 안전한 키 저장
2. **OAuth 2.0**: Google Drive, Slack 인증
3. **Personal Access Token**: GitHub 접근
4. **데이터베이스 연결**: 암호화된 연결 문자열

### 권한 제어
- **Read-Only 기본**: 읽기 전용으로 시작
- **명시적 Write 권한**: 쓰기 작업은 별도 승인
- **Scope 제한**: 최소 필요 권한만 요청
- **감사 로깅**: 모든 접근 기록 저장

---

## 🎮 실습 시나리오

### 시나리오 1: 프로젝트 상태 파악
```
사용자: "현재 프로젝트 진행 상황을 요약해줘"

Claude + MCP:
1. GitHub에서 최근 커밋, 오픈 이슈 조회
2. Google Drive에서 프로젝트 문서 확인
3. Slack에서 최근 팀 대화 분석
4. PostgreSQL에서 진행률 데이터 조회
5. 종합 리포트 생성
```

### 시나리오 2: 자동 코드 리뷰
```
GitHub Webhook → MCP Server → 코드 분석 → Slack 알림
```

### 시나리오 3: 문서 자동 업데이트
```
코드 변경 감지 → API 문서 생성 → Google Drive 업로드
```

---

## 📊 학습 목표별 평가 기준

### 1. MCP 프리미티브 이해 (25%)
- **Resources**: 적절한 리소스 정의 및 구현
- **Tools**: 실용적인 도구 기능 제공
- **Prompts**: 재사용 가능한 템플릿 설계

### 2. 시스템 통합 능력 (25%)
- **여러 서비스 연동**: 4개 서비스 성공적 통합
- **데이터 흐름**: 서비스 간 원활한 데이터 교환

### 3. 보안 구현 (20%)
- **인증 처리**: 안전한 API 키 관리
- **권한 제어**: 적절한 접근 제한

### 4. 사용자 경험 (20%)
- **직관적 인터페이스**: Claude Desktop에서 자연스러운 사용
- **오류 처리**: 친화적인 에러 메시지

### 5. 창의성 및 확장성 (10%)
- **독창적 기능**: 기본 요구사항을 넘어선 혁신
- **미래 확장**: 새로운 서비스 추가 용이성

---

## 🔧 개발 환경 및 도구

### 필수 기술 스택
- **Python 3.9+**: MCP 서버 구현
- **FastAPI**: HTTP 서버 프레임워크
- **asyncio**: 비동기 처리
- **SQLAlchemy**: 데이터베이스 ORM

### MCP SDK 및 라이브러리
- **@modelcontextprotocol/sdk**: TypeScript MCP SDK
- **mcp-python**: Python MCP 구현체
- **JSON-RPC 2.0**: 통신 프로토콜 라이브러리

### 외부 서비스 SDK
- **PyGithub**: GitHub API 클라이언트
- **google-api-python-client**: Google Drive API
- **slack-sdk**: Slack 클라이언트
- **psycopg2**: PostgreSQL 드라이버

---

## 📈 진행 단계별 체크포인트

### Week 5 중간 체크포인트 (수요일)
- [ ] MCP 서버 기본 구조 완성
- [ ] GitHub Resources 구현 완료
- [ ] 최소 1개 Tool 동작 확인

### Week 5 최종 체크포인트 (금요일)
- [ ] GitHub, Google Drive 서버 완성
- [ ] 기본 보안 모델 적용
- [ ] 통합 테스트 통과

### Week 6 중간 체크포인트 (수요일)
- [ ] Slack, PostgreSQL 서버 완성
- [ ] 모든 프리미티브 구현 완료

### Week 6 최종 데모 (금요일)
- [ ] Claude Desktop 연동 성공
- [ ] 3가지 시나리오 시연 완료
- [ ] 팀별 프레젠테이션

---

## 🎯 실무 연결점

### DevOps 자동화 관점
- **CI/CD 파이프라인**: GitHub Actions와 연동
- **모니터링**: 프로젝트 상태 자동 감시
- **알림 시스템**: 이상 상황 자동 보고

### 협업 도구 통합
- **지식 관리**: 문서와 코드의 일관성 유지
- **커뮤니케이션**: 개발 진행 상황 자동 공유
- **프로젝트 관리**: 이슈와 작업의 연결

### AI 어시스턴트 개발
- **컨텍스트 제공**: LLM에게 풍부한 프로젝트 정보
- **자동화 워크플로우**: 반복 작업의 지능적 처리
- **의사결정 지원**: 데이터 기반 개발 방향 제시

---

## 💡 확장 아이디어

### 추가 서비스 연동
- **Jira**: 프로젝트 관리 및 스프린트 추적
- **Figma**: 디자인 파일 및 프로토타입 접근
- **AWS/Azure**: 클라우드 리소스 모니터링
- **Docker Hub**: 컨테이너 이미지 관리

### 고급 기능
- **자연어 쿼리**: "지난 주 가장 많이 수정된 파일은?"
- **예측 분석**: "현재 속도로 언제 릴리스 가능할까?"
- **자동 문서화**: 코드 변경사항 자동 문서 업데이트
- **스마트 알림**: 중요도 기반 선택적 알림

---

## 📝 주간 과제 및 평가

### Week 5 과제
1. **개인 GitHub 리포지토리** MCP 서버 연결
2. **기본 Resources** 구현 (파일 목록, 내용 읽기)
3. **간단한 Tool** 구현 (이슈 생성)

### Week 6 과제
1. **4개 서비스 통합** 완료
2. **Claude Desktop 연동** 성공
3. **실제 사용 케이스** 시연

### 최종 평가 (Week 6 금요일)
- **개인 구현** (60%): 기능 완성도 및 코드 품질
- **팀 발표** (25%): 시연 및 설명
- **동료 평가** (15%): 팀워크 및 기여도

---

## 🔮 다음 주 예고: A2A 프로젝트

### Week 7-8: "크로스 플랫폼 에이전트 마켓플레이스"
- **Google A2A**: 50+ 파트너 생태계 체험
- **Agent Card**: 에이전트 메타데이터 설계
- **DID 인증**: 분산 신원 확인 실습
- **프레임워크 통합**: LangChain ↔ AutoGen 연동

### MCP vs A2A 비교 관점
- **MCP**: LLM ← → 도구 연결
- **A2A**: 에이전트 ← → 에이전트 협업

**준비물**: Google Cloud 계정, DID 지갑 설정

**실습의 시작! 이론을 실제로 만나는 시간입니다! 🚀** 