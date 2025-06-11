# 7-8주차: A2A 실습 프로젝트

## 📋 프로젝트 개요
**"크로스 플랫폼 에이전트 마켓플레이스"**

Google의 A2A(Agent to Agent Protocol)를 활용하여 다양한 프레임워크의 에이전트들이 서로 협업할 수 있는 마켓플레이스를 구축합니다.

## 🎯 학습 목표
- A2A의 Agent Card 기반 서비스 발견 메커니즘 이해
- JSON-RPC 2.0 over HTTP(S) 통신 방식 경험
- Task 중심 아키텍처 구현
- Opaque Agent 개념을 통한 안전한 에이전트 협업
- 동기/비동기, 스트리밍, 푸시 알림 패턴 실습

## 🛠️ 구현할 에이전트들

### 1. 데이터 분석 에이전트
- **Capability**: data-analysis, visualization, statistics
- **입력**: CSV, JSON 데이터
- **출력**: 분석 리포트, 차트, 통계

### 2. 자연어 처리 에이전트  
- **Capability**: nlp, sentiment-analysis, summarization
- **입력**: 텍스트 문서
- **출력**: 감정 분석, 요약, 키워드 추출

### 3. 이미지 처리 에이전트
- **Capability**: image-processing, ocr, classification
- **입력**: 이미지 파일
- **출력**: 텍스트 추출, 분류 결과

### 4. 워크플로우 오케스트레이터 에이전트
- **Capability**: workflow, orchestration, task-management
- **기능**: 다른 에이전트들을 조합하여 복합 작업 수행

## 📁 프로젝트 구조

```
week07_08_a2a_project/
├── agents/
│   ├── data_analyst/
│   │   ├── agent.py
│   │   ├── agent_card.json
│   │   └── requirements.txt
│   ├── nlp_agent/
│   │   ├── agent.py
│   │   ├── agent_card.json
│   │   └── requirements.txt
│   ├── image_processor/
│   │   ├── agent.py
│   │   ├── agent_card.json
│   │   └── requirements.txt
│   └── orchestrator/
│       ├── agent.py
│       ├── agent_card.json
│       └── workflows/
├── marketplace/
│   ├── discovery_service.py
│   ├── registry.py
│   └── web_ui/
├── client/
│   ├── a2a_client.py
│   ├── task_manager.py
│   └── streaming_client.py
├── tests/
│   ├── test_agents.py
│   ├── test_discovery.py
│   └── test_workflows.py
├── examples/
│   ├── simple_collaboration.py
│   ├── workflow_example.py
│   └── streaming_demo.py
└── docs/
    ├── agent_development.md
    ├── api_reference.md
    └── deployment_guide.md
```

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
cd 02_hands_on_practice/week07_08_a2a_project
pip install -r requirements.txt
```

### 2. 에이전트 실행
```bash
# 각 에이전트를 별도 터미널에서 실행
python agents/data_analyst/agent.py --port 8001
python agents/nlp_agent/agent.py --port 8002  
python agents/image_processor/agent.py --port 8003
python agents/orchestrator/agent.py --port 8004
```

### 3. 마켓플레이스 실행
```bash
# 서비스 발견 및 레지스트리 서비스
python marketplace/discovery_service.py --port 8000
```

### 4. 클라이언트 테스트
```bash
# 에이전트 발견 및 협업 테스트
python examples/simple_collaboration.py

# 워크플로우 실행
python examples/workflow_example.py

# 스트리밍 데모
python examples/streaming_demo.py
```

## 📝 실습 단계

### Week 7: A2A 에이전트 구현

#### Day 1-2: 데이터 분석 에이전트
- Agent Card 정의 및 서비스 등록
- CSV/JSON 데이터 분석 기능 구현
- 결과 시각화 및 리포트 생성

#### Day 3-4: 자연어 처리 에이전트  
- 텍스트 분석 파이프라인 구현
- 감정 분석, 요약, 키워드 추출
- 다국어 지원 및 성능 최적화

#### Day 5: 이미지 처리 에이전트
- OCR 및 이미지 분류 기능
- 멀티모달 데이터 처리
- 결과 검증 및 신뢰도 측정

### Week 8: 고급 협업 및 워크플로우

#### Day 1-2: 마켓플레이스 구축
- 서비스 발견 메커니즘 구현
- 에이전트 레지스트리 및 상태 관리
- 웹 UI를 통한 시각적 모니터링

#### Day 3-4: 워크플로우 오케스트레이터
- 복합 작업 정의 및 실행
- 에이전트 간 데이터 파이프라인
- 오류 처리 및 재시도 로직

#### Day 5: 스트리밍 및 실시간 협업
- Server-Sent Events (SSE) 구현
- 실시간 작업 상태 업데이트
- 푸시 알림 시스템

## 🧪 주요 실습 예제

### A2A Agent Card 정의
```json
{
  "agent_id": "data-analyst-v1",
  "display_name": "Data Analysis Agent",
  "description": "Performs statistical analysis and visualization of datasets",
  "version": "1.0.0",
  "capabilities": [
    "data-analysis",
    "visualization", 
    "statistics",
    "csv-processing",
    "json-processing"
  ],
  "endpoint": "http://localhost:8001",
  "supported_modalities": ["text", "application/json", "text/csv"],
  "authentication": {
    "type": "api_key",
    "required": false
  },
  "rate_limits": {
    "requests_per_minute": 60,
    "concurrent_tasks": 5
  },
  "metadata": {
    "framework": "custom",
    "language": "python",
    "contact": "team@example.com"
  }
}
```

### A2A 클라이언트 사용 예제
```python
import asyncio
from a2a_client import A2AClient

async def analyze_data_workflow():
    client = A2AClient(discovery_url="http://localhost:8000")
    
    # 1. 데이터 분석 에이전트 발견
    analysts = await client.discover_agents(capability="data-analysis")
    if not analysts:
        raise Exception("데이터 분석 에이전트를 찾을 수 없습니다")
    
    analyst = analysts[0]
    
    # 2. 분석 작업 생성
    task = await client.create_task(
        agent_id=analyst["agent_id"],
        task_data={
            "operation": "analyze",
            "data_source": "sales_data.csv",
            "analysis_type": "trend_analysis"
        }
    )
    
    # 3. 스트리밍으로 진행 상황 모니터링
    async for update in client.stream_task_updates(task.id):
        print(f"진행 상황: {update.status} - {update.message}")
        
        if update.status == "completed":
            result = update.result
            print(f"분석 완료: {result}")
            break
        elif update.status == "failed":
            print(f"분석 실패: {update.error}")
            break
    
    return result

# 실행
result = asyncio.run(analyze_data_workflow())
```

### 워크플로우 오케스트레이션 예제
```python
class DataProcessingWorkflow:
    def __init__(self, client: A2AClient):
        self.client = client
    
    async def execute(self, document_url: str):
        """문서 → OCR → NLP → 분석 파이프라인"""
        
        # 1. 이미지 처리 에이전트로 OCR
        image_agents = await self.client.discover_agents(capability="ocr")
        ocr_task = await self.client.create_task(
            agent_id=image_agents[0]["agent_id"],
            task_data={"image_url": document_url, "operation": "extract_text"}
        )
        
        text_result = await self.client.wait_for_completion(ocr_task.id)
        extracted_text = text_result["text"]
        
        # 2. NLP 에이전트로 텍스트 분석
        nlp_agents = await self.client.discover_agents(capability="nlp")
        nlp_task = await self.client.create_task(
            agent_id=nlp_agents[0]["agent_id"],
            task_data={
                "text": extracted_text,
                "operations": ["sentiment", "summarize", "keywords"]
            }
        )
        
        nlp_result = await self.client.wait_for_completion(nlp_task.id)
        
        # 3. 데이터 분석 에이전트로 최종 리포트
        analyst_agents = await self.client.discover_agents(capability="data-analysis")
        report_task = await self.client.create_task(
            agent_id=analyst_agents[0]["agent_id"],
            task_data={
                "operation": "generate_report",
                "nlp_results": nlp_result,
                "source_document": document_url
            }
        )
        
        final_report = await self.client.wait_for_completion(report_task.id)
        return final_report
```

## 📊 평가 기준

### 기술적 구현 (40%)
- A2A 프로토콜 올바른 구현
- Agent Card 및 서비스 발견 기능
- Task 라이프사이클 관리
- JSON-RPC 2.0 통신

### 에이전트 품질 (30%)
- 각 에이전트의 기능 완성도
- 에러 처리 및 복원력
- 성능 및 확장성
- 모달리티 지원

### 협업 및 워크플로우 (20%)
- 에이전트 간 효과적인 협업
- 복합 워크플로우 설계
- 실시간 스트리밍 구현
- 상태 동기화

### 사용자 경험 (10%)
- 마켓플레이스 UI/UX
- 모니터링 및 디버깅 도구
- 문서화 품질
- 데모 시나리오

## 📚 참고 자료
- [A2A 공식 문서](https://goo.gle/a2a)
- [Google A2A GitHub](https://github.com/google-a2a/A2A)
- [JSON-RPC 2.0 사양](https://www.jsonrpc.org/specification)
- [Agent Card 표준](docs/agent_development.md)

## 🎁 보너스 과제
- LangChain/AutoGen 에이전트와의 상호 운용성
- 복잡한 다단계 워크플로우 구현
- A2A 에이전트 마켓플레이스 확장
- 성능 벤치마킹 및 최적화
- 보안 강화 (인증, 권한 관리) 