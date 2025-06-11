# 멀티에이전트 프로토콜 비교 학습 실습 과정

## 📚 과정 개요
4가지 주요 멀티에이전트 프로토콜(MCP, A2A, AGP, ACP)을 이론과 실습을 통해 학습하는 16주 과정입니다.

## 🛠️ 실습 환경 설정

### 필수 요구사항
- Python 3.9+
- Node.js 18+ (MCP 실습용)
- Docker & Docker Compose
- Git

### 설치 스크립트 실행
```bash
# 프로젝트 클론
git clone <repository-url>
cd multi_agent_protocol_course

# 의존성 설치
chmod +x setup.sh
./setup.sh
```

## 📁 폴더 구조

```
multi_agent_protocol_course/
├── 01_theory_foundation/        # 이론 기초 (1-4주)
├── 02_hands_on_practice/        # 실습 및 비교 (5-12주)
├── 03_advanced_topics/          # 고급 주제 (13-16주)
├── common/                      # 공통 라이브러리 및 유틸리티
├── docs/                        # 문서 및 가이드
└── setup.sh                     # 환경 설정 스크립트
```

## 🎯 주차별 학습 가이드

### 1부: 이론 기초 (1-4주)
- **1주차**: 멀티에이전트 시스템 개요
- **2주차**: MCP (Model Context Protocol) 심화
- **3주차**: A2A (Agent to Agent Protocol) 분석  
- **4주차**: AGP & ACP 프로토콜 탐구

### 2부: 실습 및 비교 (5-12주)
- **5-6주차**: MCP 실습 프로젝트
- **7-8주차**: A2A 실습 프로젝트
- **9-10주차**: AGP 실습 프로젝트
- **11-12주차**: ACP 실습 프로젝트

### 3부: 고급 주제 (13-16주)
- **13주차**: 성능 벤치마킹
- **14주차**: 보안 및 신뢰성 분석
- **15주차**: 프로토콜 상호 운용성
- **16주차**: 최종 프로젝트 발표

## 🚀 빠른 시작

1. **환경 설정**
   ```bash
   cd 01_theory_foundation/week01_multi_agent_overview
   python run_demo.py
   ```

2. **각 프로토콜 테스트**
   ```bash
   # MCP 테스트
   cd 02_hands_on_practice/week05_06_mcp_project
   npm run start

   # A2A 테스트  
   cd 02_hands_on_practice/week07_08_a2a_project
   python main.py

   # AGP 테스트
   cd 02_hands_on_practice/week09_10_agp_project
   cargo run

   # ACP 테스트
   cd 02_hands_on_practice/week11_12_acp_project
   python server.py
   ```

## 📖 추가 리소스
- [강의 자료](multi_agent_protocol_course.md)
- [공식 문서 링크](docs/official_resources.md)
- [FAQ](docs/faq.md)

## 💬 문의사항
실습 과정에서 문의사항이 있으시면 Issues를 통해 질문해 주세요. 

https://claude.ai/chat/6e2e35d6-c87d-4880-b53a-95c15da2881a

https://www.linkedin.com/feed/update/urn:li:activity:7338344450508603392/