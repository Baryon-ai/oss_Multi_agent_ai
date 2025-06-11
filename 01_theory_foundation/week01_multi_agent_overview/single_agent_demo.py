"""
1주차 실습 1: 단일 에이전트 시스템 데모

이 파일은 단일 에이전트의 기본 구조와 동작 방식을 보여줍니다.
에이전트는 환경을 감지하고, 의사결정을 내리며, 행동을 수행하는 기본 사이클을 가집니다.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentState(Enum):
    """에이전트의 상태를 정의하는 열거형"""
    IDLE = "idle"
    SENSING = "sensing"
    THINKING = "thinking"
    ACTING = "acting"
    ERROR = "error"

@dataclass
class Sensor:
    """센서 데이터를 나타내는 데이터 클래스"""
    name: str
    value: Any
    timestamp: datetime
    unit: str = ""

@dataclass
class Action:
    """에이전트가 수행할 행동을 나타내는 데이터 클래스"""
    type: str
    parameters: Dict[str, Any]
    priority: int = 1
    estimated_duration: float = 1.0

class Environment:
    """에이전트가 상호작용하는 환경 시뮬레이터"""
    
    def __init__(self):
        self.temperature = 25.0
        self.humidity = 60.0
        self.light_level = 300.0
        self.occupancy = False
        
    def get_sensor_data(self) -> List[Sensor]:
        """환경 센서 데이터를 반환"""
        import random
        
        # 센서 값을 약간 변화시켜 실시간 시뮬레이션
        self.temperature += random.uniform(-0.5, 0.5)
        self.humidity += random.uniform(-1.0, 1.0)
        self.light_level += random.uniform(-10, 10)
        self.occupancy = random.choice([True, False])
        
        return [
            Sensor("temperature", round(self.temperature, 1), datetime.now(), "°C"),
            Sensor("humidity", round(self.humidity, 1), datetime.now(), "%"),
            Sensor("light_level", round(self.light_level, 1), datetime.now(), "lux"),
            Sensor("occupancy", self.occupancy, datetime.now(), "boolean")
        ]
    
    def execute_action(self, action: Action) -> bool:
        """에이전트의 행동을 환경에 적용"""
        try:
            if action.type == "adjust_temperature":
                target_temp = action.parameters.get("target", 25.0)
                self.temperature += (target_temp - self.temperature) * 0.1
                logger.info(f"온도를 {target_temp}°C로 조정 중 (현재: {self.temperature:.1f}°C)")
                
            elif action.type == "adjust_lighting":
                target_light = action.parameters.get("target", 300.0)
                self.light_level += (target_light - self.light_level) * 0.2
                logger.info(f"조명을 {target_light} lux로 조정 중 (현재: {self.light_level:.1f} lux)")
                
            elif action.type == "alert":
                message = action.parameters.get("message", "알림")
                logger.warning(f"🚨 알림: {message}")
                
            return True
            
        except Exception as e:
            logger.error(f"행동 실행 실패: {e}")
            return False

class SimpleAgent:
    """간단한 단일 에이전트 구현"""
    
    def __init__(self, name: str, environment: Environment):
        self.name = name
        self.environment = environment
        self.state = AgentState.IDLE
        self.sensor_data: List[Sensor] = []
        self.knowledge_base: Dict[str, Any] = {
            "comfort_temp_range": (22.0, 26.0),
            "comfort_humidity_range": (40.0, 70.0),
            "min_light_level": 200.0,
            "max_temp_change": 2.0
        }
        self.action_history: List[Action] = []
        
    async def sense(self) -> List[Sensor]:
        """환경을 감지하는 단계"""
        self.state = AgentState.SENSING
        logger.info(f"[{self.name}] 🔍 환경 감지 중...")
        
        await asyncio.sleep(0.5)  # 센싱 시간 시뮬레이션
        self.sensor_data = self.environment.get_sensor_data()
        
        for sensor in self.sensor_data:
            logger.info(f"  📊 {sensor.name}: {sensor.value} {sensor.unit}")
            
        return self.sensor_data
    
    async def think(self) -> List[Action]:
        """수집된 데이터를 바탕으로 의사결정을 내리는 단계"""
        self.state = AgentState.THINKING
        logger.info(f"[{self.name}] 🤔 데이터 분석 및 의사결정 중...")
        
        await asyncio.sleep(1.0)  # 사고 시간 시뮬레이션
        actions = []
        
        # 온도 제어 로직
        temp_sensor = next((s for s in self.sensor_data if s.name == "temperature"), None)
        if temp_sensor:
            comfort_min, comfort_max = self.knowledge_base["comfort_temp_range"]
            if temp_sensor.value < comfort_min:
                actions.append(Action(
                    type="adjust_temperature",
                    parameters={"target": comfort_min + 1.0},
                    priority=2
                ))
            elif temp_sensor.value > comfort_max:
                actions.append(Action(
                    type="adjust_temperature", 
                    parameters={"target": comfort_max - 1.0},
                    priority=2
                ))
        
        # 조명 제어 로직
        light_sensor = next((s for s in self.sensor_data if s.name == "light_level"), None)
        occupancy_sensor = next((s for s in self.sensor_data if s.name == "occupancy"), None)
        
        if light_sensor and occupancy_sensor:
            if occupancy_sensor.value and light_sensor.value < self.knowledge_base["min_light_level"]:
                actions.append(Action(
                    type="adjust_lighting",
                    parameters={"target": 400.0},
                    priority=1
                ))
            elif not occupancy_sensor.value and light_sensor.value > 100.0:
                actions.append(Action(
                    type="adjust_lighting",
                    parameters={"target": 50.0},
                    priority=1
                ))
        
        # 습도 경고 로직
        humidity_sensor = next((s for s in self.sensor_data if s.name == "humidity"), None)
        if humidity_sensor:
            comfort_min, comfort_max = self.knowledge_base["comfort_humidity_range"]
            if humidity_sensor.value < comfort_min:
                actions.append(Action(
                    type="alert",
                    parameters={"message": f"습도가 낮습니다 ({humidity_sensor.value}%)"},
                    priority=3
                ))
            elif humidity_sensor.value > comfort_max:
                actions.append(Action(
                    type="alert",
                    parameters={"message": f"습도가 높습니다 ({humidity_sensor.value}%)"},
                    priority=3
                ))
        
        # 우선순위별 정렬
        actions.sort(key=lambda x: x.priority, reverse=True)
        
        if actions:
            logger.info(f"  💡 {len(actions)}개의 행동을 계획했습니다")
            for i, action in enumerate(actions):
                logger.info(f"    {i+1}. {action.type} (우선순위: {action.priority})")
        else:
            logger.info("  ✅ 모든 것이 정상입니다. 행동이 필요하지 않습니다")
            
        return actions
    
    async def act(self, actions: List[Action]) -> None:
        """계획된 행동을 실행하는 단계"""
        if not actions:
            return
            
        self.state = AgentState.ACTING
        logger.info(f"[{self.name}] 🎯 행동 실행 중...")
        
        for action in actions:
            logger.info(f"  ⚡ {action.type} 실행 중...")
            success = self.environment.execute_action(action)
            
            if success:
                self.action_history.append(action)
                await asyncio.sleep(action.estimated_duration)
                logger.info(f"  ✅ {action.type} 완료")
            else:
                logger.error(f"  ❌ {action.type} 실패")
                self.state = AgentState.ERROR
                break
    
    async def run_cycle(self) -> None:
        """에이전트의 한 번의 전체 실행 사이클"""
        try:
            # 감지 → 사고 → 행동 사이클
            sensor_data = await self.sense()
            actions = await self.think()
            await self.act(actions)
            
            self.state = AgentState.IDLE
            
        except Exception as e:
            logger.error(f"[{self.name}] 실행 사이클 오류: {e}")
            self.state = AgentState.ERROR
    
    def get_status(self) -> Dict[str, Any]:
        """에이전트의 현재 상태 정보를 반환"""
        latest_sensors = {s.name: s.value for s in self.sensor_data}
        
        return {
            "name": self.name,
            "state": self.state.value,
            "latest_sensors": latest_sensors,
            "total_actions": len(self.action_history),
            "knowledge_base": self.knowledge_base
        }

async def main():
    """메인 실행 함수"""
    print("🤖 단일 에이전트 시스템 데모를 시작합니다")
    print("=" * 60)
    
    # 환경과 에이전트 생성
    environment = Environment()
    agent = SimpleAgent("스마트홈 제어 에이전트", environment)
    
    # 5번의 실행 사이클 시뮬레이션
    for cycle in range(1, 6):
        print(f"\n🔄 실행 사이클 {cycle}/5")
        print("-" * 40)
        
        await agent.run_cycle()
        
        # 상태 정보 출력
        status = agent.get_status()
        print(f"\n📋 에이전트 상태: {status['state']}")
        print(f"📊 총 실행한 행동 수: {status['total_actions']}")
        
        # 다음 사이클까지 대기
        if cycle < 5:
            await asyncio.sleep(2)
    
    print("\n" + "=" * 60)
    print("✅ 단일 에이전트 데모가 완료되었습니다")
    print(f"📈 총 {len(agent.action_history)}개의 행동을 실행했습니다")
    
    # 실행된 행동 요약
    if agent.action_history:
        print("\n📋 실행된 행동 요약:")
        action_counts = {}
        for action in agent.action_history:
            action_counts[action.type] = action_counts.get(action.type, 0) + 1
        
        for action_type, count in action_counts.items():
            print(f"  • {action_type}: {count}회")

if __name__ == "__main__":
    asyncio.run(main()) 