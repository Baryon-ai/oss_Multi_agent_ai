"""
A2A 데이터 분석 에이전트

이 에이전트는 A2A 프로토콜을 사용하여 데이터 분석 서비스를 제공합니다.
- CSV/JSON 데이터 분석
- 통계 분석 및 시각화
- 트렌드 분석 및 리포트 생성
"""

import asyncio
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
import logging
from datetime import datetime
import io
import base64
from pathlib import Path
import argparse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A2A 관련 모델
class AgentCard(BaseModel):
    agent_id: str
    display_name: str
    description: str
    version: str
    capabilities: List[str]
    endpoint: str
    supported_modalities: List[str]
    authentication: Dict[str, Any]
    rate_limits: Dict[str, int]
    metadata: Dict[str, Any]

class TaskRequest(BaseModel):
    task_id: str
    agent_id: str
    task_data: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str  # "accepted", "running", "completed", "failed"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: Optional[int] = None
    estimated_completion: Optional[str] = None

class TaskUpdate(BaseModel):
    task_id: str
    status: str
    message: str
    progress: int
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class DataAnalysisAgent:
    """A2A 데이터 분석 에이전트"""
    
    def __init__(self, agent_id: str = "data-analyst-v1", port: int = 8001):
        self.agent_id = agent_id
        self.port = port
        self.endpoint = f"http://localhost:{port}"
        
        # 실행 중인 작업들
        self.running_tasks: Dict[str, TaskUpdate] = {}
        
        # Agent Card 정의
        self.agent_card = AgentCard(
            agent_id=agent_id,
            display_name="Data Analysis Agent",
            description="Performs statistical analysis and visualization of datasets",
            version="1.0.0",
            capabilities=[
                "data-analysis",
                "visualization", 
                "statistics",
                "csv-processing",
                "json-processing",
                "trend-analysis",
                "descriptive-stats"
            ],
            endpoint=self.endpoint,
            supported_modalities=["text", "application/json", "text/csv"],
            authentication={
                "type": "api_key",
                "required": False
            },
            rate_limits={
                "requests_per_minute": 60,
                "concurrent_tasks": 5
            },
            metadata={
                "framework": "custom",
                "language": "python",
                "contact": "data-team@example.com",
                "created": datetime.now().isoformat()
            }
        )
        
        # FastAPI 앱 생성
        self.app = FastAPI(title="Data Analysis Agent", version="1.0.0")
        self._setup_routes()
    
    def _setup_routes(self):
        """API 엔드포인트 설정"""
        
        @self.app.get("/")
        async def root():
            return {"message": f"Data Analysis Agent ({self.agent_id}) is running"}
        
        @self.app.get("/agent-card")
        async def get_agent_card():
            """Agent Card 반환"""
            return self.agent_card.dict()
        
        @self.app.post("/tasks", response_model=TaskResponse)
        async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
            """새 작업 생성"""
            try:
                # 작업 상태 초기화
                task_update = TaskUpdate(
                    task_id=request.task_id,
                    status="accepted",
                    message="작업이 접수되었습니다",
                    progress=0
                )
                self.running_tasks[request.task_id] = task_update
                
                # 백그라운드에서 작업 실행
                background_tasks.add_task(
                    self._execute_task, request.task_id, request.task_data
                )
                
                return TaskResponse(
                    task_id=request.task_id,
                    status="accepted",
                    estimated_completion=self._estimate_completion_time(request.task_data)
                )
                
            except Exception as e:
                logger.error(f"작업 생성 오류: {e}")
                raise HTTPException(status_code=400, detail=str(e))
        
        @self.app.get("/tasks/{task_id}", response_model=TaskResponse)
        async def get_task_status(task_id: str):
            """작업 상태 조회"""
            if task_id not in self.running_tasks:
                raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
            
            task_update = self.running_tasks[task_id]
            
            return TaskResponse(
                task_id=task_id,
                status=task_update.status,
                result=task_update.result,
                error=task_update.error,
                progress=task_update.progress
            )
        
        @self.app.get("/tasks/{task_id}/stream")
        async def stream_task_updates(task_id: str):
            """Server-Sent Events로 작업 상태 스트리밍"""
            if task_id not in self.running_tasks:
                raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
            
            async def event_generator():
                last_status = None
                while True:
                    if task_id in self.running_tasks:
                        current_update = self.running_tasks[task_id]
                        
                        # 상태가 변경되었거나 진행률이 업데이트된 경우만 전송
                        if (last_status != current_update.status or 
                            current_update.status == "running"):
                            
                            yield f"data: {current_update.json()}\n\n"
                            last_status = current_update.status
                        
                        # 작업이 완료되었으면 스트리밍 종료
                        if current_update.status in ["completed", "failed"]:
                            break
                    
                    await asyncio.sleep(1)
            
            return StreamingResponse(
                event_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive"
                }
            )
        
        @self.app.delete("/tasks/{task_id}")
        async def cancel_task(task_id: str):
            """작업 취소"""
            if task_id not in self.running_tasks:
                raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
            
            task_update = self.running_tasks[task_id]
            if task_update.status in ["completed", "failed"]:
                raise HTTPException(status_code=400, detail="이미 완료된 작업입니다")
            
            task_update.status = "cancelled"
            task_update.message = "작업이 취소되었습니다"
            
            return {"message": "작업이 취소되었습니다"}
    
    def _estimate_completion_time(self, task_data: Dict[str, Any]) -> str:
        """작업 완료 예상 시간 계산"""
        operation = task_data.get("operation", "analyze")
        
        # 작업 유형별 예상 시간 (초)
        time_estimates = {
            "analyze": 30,
            "visualize": 45,
            "trend_analysis": 60,
            "descriptive_stats": 15,
            "correlation_analysis": 40
        }
        
        estimated_seconds = time_estimates.get(operation, 30)
        completion_time = datetime.now().timestamp() + estimated_seconds
        
        return datetime.fromtimestamp(completion_time).isoformat()
    
    async def _execute_task(self, task_id: str, task_data: Dict[str, Any]):
        """작업 실행"""
        try:
            # 작업 시작
            self.running_tasks[task_id].status = "running"
            self.running_tasks[task_id].message = "데이터 분석을 시작합니다"
            self.running_tasks[task_id].progress = 10
            
            operation = task_data.get("operation", "analyze")
            
            if operation == "analyze":
                result = await self._analyze_data(task_id, task_data)
            elif operation == "visualize":
                result = await self._create_visualization(task_id, task_data)
            elif operation == "trend_analysis":
                result = await self._trend_analysis(task_id, task_data)
            elif operation == "descriptive_stats":
                result = await self._descriptive_statistics(task_id, task_data)
            elif operation == "correlation_analysis":
                result = await self._correlation_analysis(task_id, task_data)
            else:
                raise ValueError(f"지원하지 않는 작업: {operation}")
            
            # 작업 완료
            self.running_tasks[task_id].status = "completed"
            self.running_tasks[task_id].message = "분석이 완료되었습니다"
            self.running_tasks[task_id].progress = 100
            self.running_tasks[task_id].result = result
            
        except Exception as e:
            logger.error(f"작업 실행 오류 ({task_id}): {e}")
            self.running_tasks[task_id].status = "failed"
            self.running_tasks[task_id].message = f"작업 실행 중 오류 발생: {str(e)}"
            self.running_tasks[task_id].error = str(e)
    
    async def _analyze_data(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """일반적인 데이터 분석"""
        data_source = task_data.get("data_source")
        analysis_type = task_data.get("analysis_type", "basic")
        
        # 진행률 업데이트
        self.running_tasks[task_id].progress = 20
        self.running_tasks[task_id].message = "데이터를 로드하는 중..."
        await asyncio.sleep(1)  # 시뮬레이션
        
        # 데이터 로드 (시뮬레이션)
        if data_source and data_source.endswith('.csv'):
            # 실제로는 파일을 로드하지만, 여기서는 시뮬레이션 데이터 생성
            df = self._generate_sample_data()
        else:
            # JSON 데이터 처리
            df = self._generate_sample_data()
        
        self.running_tasks[task_id].progress = 50
        self.running_tasks[task_id].message = "데이터 분석 중..."
        await asyncio.sleep(2)
        
        # 기본 통계 분석
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        stats = {}
        
        for col in numeric_cols:
            stats[col] = {
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "count": int(df[col].count())
            }
        
        self.running_tasks[task_id].progress = 80
        self.running_tasks[task_id].message = "결과를 생성하는 중..."
        await asyncio.sleep(1)
        
        return {
            "analysis_type": analysis_type,
            "data_source": data_source,
            "dataset_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "numeric_columns": len(numeric_cols)
            },
            "statistics": stats,
            "summary": f"{len(df)}개 행, {len(df.columns)}개 열의 데이터를 분석했습니다."
        }
    
    async def _create_visualization(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 시각화 생성"""
        self.running_tasks[task_id].progress = 30
        self.running_tasks[task_id].message = "차트를 생성하는 중..."
        
        # 시뮬레이션 데이터 생성
        df = self._generate_sample_data()
        
        # 시각화 생성 (Base64 인코딩된 이미지로 반환)
        plt.figure(figsize=(10, 6))
        
        chart_type = task_data.get("chart_type", "histogram")
        
        if chart_type == "histogram":
            plt.hist(df['value'], bins=20, alpha=0.7)
            plt.title("Value Distribution")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
        elif chart_type == "line":
            plt.plot(df.index, df['value'])
            plt.title("Value Trend")
            plt.xlabel("Index")
            plt.ylabel("Value")
        elif chart_type == "scatter":
            if 'category' in df.columns:
                plt.scatter(df.index, df['value'], c=df['category'].astype('category').cat.codes)
                plt.colorbar(label='Category')
            else:
                plt.scatter(df.index, df['value'])
            plt.title("Value Scatter Plot")
            plt.xlabel("Index")
            plt.ylabel("Value")
        
        # 이미지를 Base64로 인코딩
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        self.running_tasks[task_id].progress = 90
        await asyncio.sleep(1)
        
        return {
            "chart_type": chart_type,
            "image_data": image_base64,
            "format": "png",
            "description": f"{chart_type} 차트가 생성되었습니다"
        }
    
    async def _trend_analysis(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """트렌드 분석"""
        self.running_tasks[task_id].progress = 40
        self.running_tasks[task_id].message = "트렌드 패턴을 분석하는 중..."
        
        df = self._generate_time_series_data()
        
        # 이동평균 계산
        df['ma_7'] = df['value'].rolling(window=7).mean()
        df['ma_30'] = df['value'].rolling(window=30).mean()
        
        # 트렌드 방향 계산
        recent_trend = df['value'].tail(10).diff().mean()
        trend_direction = "상승" if recent_trend > 0 else "하락" if recent_trend < 0 else "보합"
        
        self.running_tasks[task_id].progress = 80
        await asyncio.sleep(2)
        
        return {
            "trend_direction": trend_direction,
            "recent_change": float(recent_trend),
            "volatility": float(df['value'].std()),
            "moving_averages": {
                "7_day": float(df['ma_7'].tail(1).iloc[0]) if not df['ma_7'].empty else None,
                "30_day": float(df['ma_30'].tail(1).iloc[0]) if not df['ma_30'].empty else None
            },
            "analysis_period": f"{len(df)} 일간의 데이터",
            "summary": f"최근 트렌드는 {trend_direction} 경향을 보이고 있습니다."
        }
    
    async def _descriptive_statistics(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """기술통계 분석"""
        self.running_tasks[task_id].progress = 50
        self.running_tasks[task_id].message = "기술통계를 계산하는 중..."
        
        df = self._generate_sample_data()
        
        await asyncio.sleep(1)
        
        return {
            "dataset_shape": {"rows": len(df), "columns": len(df.columns)},
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "descriptive_stats": df.describe().to_dict(),
            "summary": "기술통계 분석이 완료되었습니다."
        }
    
    async def _correlation_analysis(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """상관관계 분석"""
        self.running_tasks[task_id].progress = 60
        self.running_tasks[task_id].message = "상관관계를 분석하는 중..."
        
        df = self._generate_sample_data()
        
        # 수치형 컬럼만 선택
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            raise ValueError("상관관계 분석을 위해서는 최소 2개의 수치형 컬럼이 필요합니다")
        
        # 상관계수 계산
        correlation_matrix = numeric_df.corr()
        
        await asyncio.sleep(2)
        
        return {
            "correlation_matrix": correlation_matrix.to_dict(),
            "strong_correlations": self._find_strong_correlations(correlation_matrix),
            "summary": "상관관계 분석이 완료되었습니다."
        }
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """샘플 데이터 생성"""
        np.random.seed(42)
        
        data = {
            'value': np.random.normal(100, 15, 1000),
            'category': np.random.choice(['A', 'B', 'C'], 1000),
            'score': np.random.uniform(0, 100, 1000),
            'count': np.random.poisson(10, 1000)
        }
        
        return pd.DataFrame(data)
    
    def _generate_time_series_data(self) -> pd.DataFrame:
        """시계열 샘플 데이터 생성"""
        dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
        trend = np.linspace(100, 120, 365)
        noise = np.random.normal(0, 5, 365)
        seasonal = 10 * np.sin(2 * np.pi * np.arange(365) / 365)
        
        values = trend + seasonal + noise
        
        return pd.DataFrame({
            'date': dates,
            'value': values
        })
    
    def _find_strong_correlations(self, corr_matrix: pd.DataFrame) -> List[Dict[str, Any]]:
        """강한 상관관계 찾기"""
        strong_correlations = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:  # 강한 상관관계 기준
                    strong_correlations.append({
                        "variable1": corr_matrix.columns[i],
                        "variable2": corr_matrix.columns[j],
                        "correlation": float(corr_value),
                        "strength": "강함" if abs(corr_value) > 0.8 else "보통"
                    })
        
        return strong_correlations

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='A2A Data Analysis Agent')
    parser.add_argument('--port', type=int, default=8001, help='Port to run the agent on')
    parser.add_argument('--agent-id', type=str, default='data-analyst-v1', help='Agent ID')
    
    args = parser.parse_args()
    
    # 에이전트 생성
    agent = DataAnalysisAgent(agent_id=args.agent_id, port=args.port)
    
    # 서버 실행
    import uvicorn
    logger.info(f"데이터 분석 에이전트 시작: {agent.endpoint}")
    logger.info(f"Agent Card: {agent.endpoint}/agent-card")
    
    uvicorn.run(
        agent.app,
        host="0.0.0.0",
        port=args.port,
        log_level="info"
    )

if __name__ == "__main__":
    main() 