# Week 13: 성능 벤치마킹

## 🎯 학습 목표
- 4가지 프로토콜의 성능 특성을 정량적으로 비교
- 실제 벤치마킹 도구를 활용한 성능 측정 방법 습득
- 병목 지점 식별 및 최적화 전략 수립

## 📊 벤치마킹 시나리오

### 시나리오 1: 단순 요청-응답 테스트
- **목적**: 기본 통신 지연시간 측정
- **메트릭**: 응답 시간, 처리량 (RPS)
- **테스트 케이스**: 1KB, 10KB, 100KB 메시지

### 시나리오 2: 동시 연결 부하 테스트
- **목적**: 확장성 한계 측정
- **메트릭**: 동시 연결 수, 메모리 사용량
- **테스트 케이스**: 10, 100, 1000, 10000 동시 연결

### 시나리오 3: 복잡한 워크플로우 테스트
- **목적**: 실제 사용 시나리오에서의 성능
- **메트릭**: End-to-End 지연시간, 에러율
- **테스트 케이스**: 멀티스텝 에이전트 협업

## 🛠️ 벤치마킹 도구

### 1. Apache Bench (ab)
```bash
# MCP HTTP 서버 테스트
ab -n 1000 -c 10 http://localhost:3000/mcp/

# 결과 분석
# - Requests per second
# - Time per request 
# - Transfer rate
```

### 2. wrk (고성능 HTTP 벤치마킹)
```bash
# A2A REST API 테스트
wrk -t12 -c400 -d30s --script=a2a_test.lua http://localhost:8000/agents/

# Lua 스크립트로 복잡한 시나리오 테스트
```

### 3. gRPC 전용 도구 (ghz)
```bash
# AGP gRPC 서비스 테스트
ghz --insecure \
    --proto agp.proto \
    --call agp.Gateway/SendMessage \
    -d '{"message":"test"}' \
    -c 50 -n 10000 \
    localhost:50051
```

### 4. Custom Python 벤치마킹 스크립트
```python
# benchmark_suite.py - 통합 벤치마킹 도구
import asyncio
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

class ProtocolBenchmark:
    def __init__(self, protocol_name, endpoint):
        self.protocol_name = protocol_name
        self.endpoint = endpoint
        self.results = []
    
    async def run_benchmark(self, num_requests=1000, concurrency=10):
        """벤치마크 실행"""
        # 구현...
```

## 📈 성능 비교 결과 (예상)

| 프로토콜 | 평균 지연시간 | 최대 RPS | 메모리 사용량 | CPU 사용률 |
|---------|-------------|----------|-------------|-----------|
| MCP | 15ms | 2,000 | 50MB | 25% |
| A2A | 25ms | 1,500 | 75MB | 35% |
| AGP | 5ms | 8,000 | 30MB | 15% |
| ACP | 20ms | 1,800 | 60MB | 30% |

## 🔧 실습 과제

### 과제 1: 기본 벤치마킹
1. 각 프로토콜 서버를 로컬에서 실행
2. 제공된 벤치마킹 스크립트로 성능 측정
3. 결과를 표로 정리하고 분석

### 과제 2: 병목 지점 분석
1. 프로파일링 도구로 성능 병목 식별
2. 메모리 누수, CPU 스파이크 원인 분석
3. 최적화 방안 제시

### 과제 3: 커스텀 벤치마크 작성
1. 특정 사용 사례에 맞는 벤치마크 시나리오 설계
2. 자동화된 성능 회귀 테스트 구축
3. CI/CD 파이프라인에 통합

## 📚 참고 자료
- [Apache Bench 가이드](https://httpd.apache.org/docs/2.4/programs/ab.html)
- [wrk 벤치마킹 도구](https://github.com/wg/wrk)
- [gRPC 성능 최적화](https://grpc.io/docs/guides/performance/)
- [Python 성능 프로파일링](https://docs.python.org/3/library/profile.html) 