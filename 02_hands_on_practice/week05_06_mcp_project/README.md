# 5-6주차: MCP 실습 프로젝트

## 📋 프로젝트 개요
**"통합 개발 환경 확장 시스템"**

실제 MCP(Model Context Protocol)를 활용하여 다양한 외부 데이터 소스와 도구를 LLM에 연결하는 통합 시스템을 구축합니다.

## 🎯 학습 목표
- MCP의 5가지 핵심 프리미티브 실습 (Resources, Tools, Prompts, Roots, Sampling)
- Client-Server 아키텍처 이해
- 실제 MCP 서버 구현 및 Claude Desktop 연동
- JSON-RPC 2.0 통신 프로토콜 경험

## 🛠️ 구현할 MCP 서버들

### 1. 파일 시스템 MCP 서버
- **Resources**: 프로젝트 파일 및 디렉토리 구조 제공
- **Tools**: 파일 읽기/쓰기/검색 도구
- **Roots**: 프로젝트 루트 디렉토리 설정

### 2. 데이터베이스 MCP 서버
- **Resources**: 테이블 스키마 및 메타데이터
- **Tools**: SQL 쿼리 실행, 데이터 조회/수정
- **Prompts**: 일반적인 SQL 작업 템플릿

### 3. API 통합 MCP 서버
- **Tools**: GitHub API, Slack API 연동
- **Sampling**: LLM 체이닝을 통한 복합 작업

### 4. 문서 관리 MCP 서버
- **Resources**: Markdown, PDF 문서
- **Tools**: 문서 검색, 요약 생성
- **Prompts**: 문서 분석 템플릿

## 📁 프로젝트 구조

```
week05_06_mcp_project/
├── servers/
│   ├── filesystem_server/
│   │   ├── server.py
│   │   ├── config.json
│   │   └── README.md
│   ├── database_server/
│   │   ├── server.py
│   │   ├── schema.sql
│   │   └── README.md
│   ├── api_server/
│   │   ├── server.py
│   │   ├── integrations/
│   │   └── README.md
│   └── document_server/
│       ├── server.py
│       ├── documents/
│       └── README.md
├── client/
│   ├── mcp_client.py
│   ├── demo.py
│   └── claude_integration.md
├── tests/
│   ├── test_filesystem.py
│   ├── test_database.py
│   └── test_integration.py
├── config/
│   ├── claude_desktop_config.json
│   └── server_configs.json
└── docs/
    ├── setup_guide.md
    ├── architecture.md
    └── troubleshooting.md
```

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
cd 02_hands_on_practice/week05_06_mcp_project
pip install -r requirements.txt
npm install  # TypeScript MCP SDK 사용시
```

### 2. MCP 서버 실행
```bash
# 파일 시스템 서버
python servers/filesystem_server/server.py

# 데이터베이스 서버
python servers/database_server/server.py

# API 서버
python servers/api_server/server.py

# 문서 서버
python servers/document_server/server.py
```

### 3. Claude Desktop 연동
```bash
# Claude Desktop 설정 파일 복사
cp config/claude_desktop_config.json ~/.config/claude-desktop/
```

### 4. 클라이언트 테스트
```bash
# 통합 데모 실행
python client/demo.py

# 개별 서버 테스트
python tests/test_filesystem.py
```

## 📝 실습 단계

### Week 5: MCP 서버 구현

#### Day 1-2: 파일 시스템 MCP 서버
- Resources를 통한 파일/디렉토리 구조 노출
- Tools를 통한 파일 조작 기능 구현
- Roots를 통한 접근 권한 제어

#### Day 3-4: 데이터베이스 MCP 서버
- 데이터베이스 스키마를 Resources로 제공
- SQL 쿼리 실행 Tools 구현
- 일반적인 쿼리 Prompts 제공

#### Day 5: API 통합 서버
- 외부 API (GitHub, Slack) Tools 구현
- 인증 및 권한 관리
- 에러 처리 및 재시도 로직

### Week 6: 고급 기능 및 통합

#### Day 1-2: 문서 관리 서버
- 다양한 형식 문서 Resources 제공
- 문서 검색 및 분석 Tools
- 문서 처리 Prompts 및 Sampling

#### Day 3-4: Claude Desktop 연동
- Claude Desktop 설정 및 연동
- 실제 대화를 통한 MCP 서버 테스트
- 사용자 경험 개선

#### Day 5: 성능 최적화 및 모니터링
- 서버 성능 측정 및 최적화
- 로깅 및 오류 처리 개선
- 보안 고려사항 적용

## 🧪 주요 실습 예제

### MCP 파일 시스템 서버 예제
```python
from mcp import Server, ListResourcesResult, ReadResourceResult
from mcp.types import Resource, Tool

server = Server("filesystem-server")

@server.list_resources()
async def list_resources() -> ListResourcesResult:
    return ListResourcesResult(
        resources=[
            Resource(
                uri="file:///project",
                name="Project Files",
                mimeType="application/vnd.directory"
            )
        ]
    )

@server.read_resource()
async def read_resource(uri: str) -> ReadResourceResult:
    # 파일 내용 읽기 구현
    pass

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_files":
        # 파일 검색 구현
        pass
```

### Claude Desktop과 MCP 연동 설정
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["servers/filesystem_server/server.py"],
      "env": {
        "PROJECT_ROOT": "/path/to/project"
      }
    },
    "database": {
      "command": "python", 
      "args": ["servers/database_server/server.py"],
      "env": {
        "DB_URL": "postgresql://localhost/demo"
      }
    }
  }
}
```

## 📊 평가 기준

### 기술적 구현 (40%)
- MCP 프리미티브 올바른 사용
- JSON-RPC 2.0 통신 구현
- 에러 처리 및 예외 상황 대응

### 기능 완성도 (30%)
- 요구된 모든 MCP 서버 구현
- Claude Desktop 연동 성공
- 실제 사용 가능한 수준의 완성도

### 코드 품질 (20%)
- 코드 구조화 및 모듈화
- 테스트 코드 작성
- 문서화 및 주석

### 창의성 및 확장성 (10%)
- 추가 기능 구현
- 독창적인 MCP 서버 아이디어
- 성능 최적화 시도

## 📚 참고 자료
- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Anthropic MCP 가이드](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop 설정 가이드](docs/claude_integration.md)

## 🎁 보너스 과제
- 커스텀 MCP 서버 개발 (Notion, Google Drive 등)
- MCP Inspector를 활용한 디버깅
- 성능 벤치마킹 및 최적화
- 다른 MCP 클라이언트 (Zed, Replit) 연동 시도 