#!/bin/bash

echo "🚀 멀티에이전트 프로토콜 실습 환경 설정을 시작합니다..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 필수 디렉토리 생성
echo -e "${BLUE}📁 디렉토리 구조 생성 중...${NC}"
mkdir -p 01_theory_foundation/{week01_multi_agent_overview,week02_mcp_deep_dive,week03_a2a_analysis,week04_agp_acp_exploration}
mkdir -p 02_hands_on_practice/{week05_06_mcp_project,week07_08_a2a_project,week09_10_agp_project,week11_12_acp_project}
mkdir -p 03_advanced_topics/{week13_performance_benchmarking,week14_security_reliability,week15_interoperability,week16_final_project}
mkdir -p common/{utils,models,protocols}
mkdir -p docs/{images,guides,references}

# Python 가상환경 생성
echo -e "${BLUE}🐍 Python 가상환경 설정 중...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3가 설치되지 않았습니다. Python 3.9+ 설치가 필요합니다.${NC}"
    exit 1
fi

python3 -m venv venv
source venv/bin/activate

# Python 의존성 설치
echo -e "${BLUE}📦 Python 패키지 설치 중...${NC}"
pip install --upgrade pip

# requirements.txt 생성 및 설치
cat > requirements.txt << EOF
# 공통 의존성
fastapi==0.104.1
uvicorn[standard]==0.24.0
asyncio-mqtt==0.16.1
aiofiles==23.2.1
httpx==0.25.0
websockets==12.0
redis==5.0.1
sqlalchemy==2.0.23
alembic==1.12.1
pytest==7.4.3
pytest-asyncio==0.21.1

# MCP 관련
jsonrpc-requests==0.4.0
pydantic==2.5.0

# A2A 관련  
grpcio==1.59.3
grpcio-tools==1.59.3
protobuf==4.25.1

# AGP 관련
aiokafka==0.8.11
confluent-kafka==2.3.0

# ACP 관련
flask==3.0.0
requests==2.31.0

# 개발 도구
black==23.11.0
isort==5.12.0
mypy==1.7.1
pre-commit==3.6.0

# 모니터링 및 로깅
opentelemetry-api==1.21.0
opentelemetry-sdk==1.21.0
structlog==23.2.0
EOF

pip install -r requirements.txt

# Node.js 의존성 (MCP용)
echo -e "${BLUE}📦 Node.js 패키지 설정 중...${NC}"
if command -v npm &> /dev/null; then
    cat > package.json << EOF
{
  "name": "multi-agent-protocol-course",
  "version": "1.0.0",
  "description": "Multi-Agent Protocol Learning Course",
  "scripts": {
    "start:mcp": "cd 02_hands_on_practice/week05_06_mcp_project && npm start",
    "test": "jest",
    "dev": "nodemon"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "express": "^4.18.2",
    "ws": "^8.14.2",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/node": "^20.9.0",
    "typescript": "^5.2.2",
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}
EOF
    npm install
else
    echo -e "${YELLOW}⚠️  Node.js가 설치되지 않았습니다. MCP 실습을 위해 Node.js 18+ 설치를 권장합니다.${NC}"
fi

# Docker Compose 파일 생성
echo -e "${BLUE}🐳 Docker 환경 설정 중...${NC}"
cat > docker-compose.yml << EOF
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: multiagent_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

volumes:
  redis_data:
  postgres_data:
EOF

# 환경 변수 파일 생성
echo -e "${BLUE}🔧 환경 변수 설정 중...${NC}"
cat > .env << EOF
# 데이터베이스 설정
DATABASE_URL=postgresql://postgres:password@localhost:5432/multiagent_db
REDIS_URL=redis://localhost:6379

# API 키 (실습용 - 실제 환경에서는 변경 필요)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 서버 설정
HOST=localhost
PORT=8000

# 로깅 레벨
LOG_LEVEL=INFO
EOF

echo -e "${GREEN}✅ 환경 설정이 완료되었습니다!${NC}"
echo -e "${YELLOW}📋 다음 단계:${NC}"
echo "1. 가상환경 활성화: source venv/bin/activate"
echo "2. Docker 서비스 시작: docker-compose up -d"
echo "3. 첫 번째 실습 시작: cd 01_theory_foundation/week01_multi_agent_overview"
echo ""
echo -e "${GREEN}�� 실습을 시작하세요!${NC}" 