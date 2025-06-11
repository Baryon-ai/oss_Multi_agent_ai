"""
1주차 실습 2: 멀티에이전트 통신 문제 시연

이 파일은 프로토콜 없이 여러 에이전트가 통신할 때 발생하는 문제점들을 보여줍니다:
1. 메시지 형식 불일치
2. 통신 실패 및 재시도 메커니즘 부재
3. 상태 동기화 문제
4. 충돌하는 의사결정
"""

import asyncio
import logging
import random
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MessageFormat(Enum):
    """서로 다른 에이전트들이 사용하는 메시지 형식"""
    JSON = "json"
    XML = "xml"
    CUSTOM = "custom"

@dataclass 
class Message:
    """메시지 기본 구조"""
    id: str
    sender: str
    receiver: str
    content: Any
    format: MessageFormat
    timestamp: datetime

class UnreliableChannel:
    """불안정한 통신 채널 시뮬레이터"""
    
    def __init__(self, failure_rate: float = 0.2, delay_range: tuple = (0.1, 2.0)):
        self.failure_rate = failure_rate
        self.delay_range = delay_range
        self.message_queue: List[Message] = []
        
    async def send_message(self, message: Message) -> bool:
        """메시지 전송 (실패 가능성 있음)"""
        # 랜덤 지연
        delay = random.uniform(*self.delay_range)
        await asyncio.sleep(delay)
        
        # 랜덤 실패
        if random.random() < self.failure_rate:
            logger.error(f"❌ 메시지 전송 실패: {message.sender} → {message.receiver}")
            return False
            
        self.message_queue.append(message)
        logger.info(f"📤 메시지 전송됨: {message.sender} → {message.receiver}")
        return True
    
    def receive_messages(self, receiver: str) -> List[Message]:
        """특정 수신자의 메시지 조회"""
        messages = [msg for msg in self.message_queue if msg.receiver == receiver]
        # 메시지 수신 후 큐에서 제거
        self.message_queue = [msg for msg in self.message_queue if msg.receiver != receiver]
        return messages

class ProblematicAgent:
    """문제가 있는 에이전트 구현 (표준화된 프로토콜 없음)"""
    
    def __init__(self, name: str, message_format: MessageFormat, channel: UnreliableChannel):
        self.name = name
        self.message_format = message_format
        self.channel = channel
        self.state = {"temperature": 25.0, "target_temperature": 25.0}
        self.received_messages: List[Message] = []
        self.failed_sends: int = 0
        
    def create_message(self, receiver: str, content: Dict[str, Any]) -> Message:
        """각 에이전트가 다른 형식으로 메시지 생성"""
        message_id = str(uuid.uuid4())[:8]
        
        if self.message_format == MessageFormat.JSON:
            # JSON 형식 (표준적)
            formatted_content = json.dumps(content)
            
        elif self.message_format == MessageFormat.XML:
            # XML 형식 (구식)
            xml_content = "<message>"
            for key, value in content.items():
                xml_content += f"<{key}>{value}</{key}>"
            xml_content += "</message>"
            formatted_content = xml_content
            
        elif self.message_format == MessageFormat.CUSTOM:
            # 커스텀 형식 (비표준)
            formatted_content = f"CMD:{content.get('command', 'unknown')}|DATA:{content.get('data', '')}"
            
        return Message(
            id=message_id,
            sender=self.name,
            receiver=receiver,
            content=formatted_content,
            format=self.message_format,
            timestamp=datetime.now()
        )
    
    def parse_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """다른 형식의 메시지 파싱 시도 (종종 실패)"""
        try:
            if self.message_format == MessageFormat.JSON and message.format == MessageFormat.JSON:
                return json.loads(message.content)
            elif self.message_format == MessageFormat.JSON and message.format == MessageFormat.XML:
                # JSON 에이전트가 XML 메시지를 파싱하려고 시도 (실패)
                logger.error(f"[{self.name}] ❌ XML 메시지를 파싱할 수 없습니다")
                return None
            elif self.message_format == MessageFormat.JSON and message.format == MessageFormat.CUSTOM:
                # JSON 에이전트가 커스텀 메시지를 파싱하려고 시도 (실패)
                logger.error(f"[{self.name}] ❌ 커스텀 형식 메시지를 파싱할 수 없습니다")
                return None
            else:
                # 기타 복잡한 파싱 시나리오들...
                logger.warning(f"[{self.name}] ⚠️ 메시지 형식 불일치: {message.format.value}")
                return None
                
        except Exception as e:
            logger.error(f"[{self.name}] ❌ 메시지 파싱 오류: {e}")
            return None
    
    async def send_temperature_update(self, receiver: str, new_temp: float):
        """온도 업데이트 메시지 전송 (재시도 메커니즘 없음)"""
        content = {
            "command": "temperature_update",
            "data": new_temp,
            "timestamp": datetime.now().isoformat()
        }
        
        message = self.create_message(receiver, content)
        success = await self.channel.send_message(message)
        
        if not success:
            self.failed_sends += 1
            logger.warning(f"[{self.name}] ⚠️ 메시지 전송 실패 누적: {self.failed_sends}회")
    
    async def process_messages(self):
        """수신된 메시지 처리"""
        messages = self.channel.receive_messages(self.name)
        
        for message in messages:
            self.received_messages.append(message)
            parsed = self.parse_message(message)
            
            if parsed and parsed.get("command") == "temperature_update":
                remote_temp = parsed.get("data")
                if remote_temp is not None:
                    logger.info(f"[{self.name}] 📨 온도 정보 수신: {remote_temp}°C from {message.sender}")
                    # 상태 동기화 없이 즉시 반응
                    await self.react_to_temperature(remote_temp)
            else:
                logger.warning(f"[{self.name}] ❓ 이해할 수 없는 메시지: {message.sender}")
    
    async def react_to_temperature(self, remote_temp: float):
        """다른 에이전트의 온도 정보에 반응 (충돌 가능성 높음)"""
        current_temp = self.state["temperature"]
        
        # 각 에이전트가 독립적으로 의사결정 (조정 없음)
        if abs(remote_temp - current_temp) > 2.0:
            # 내 온도를 원격 온도에 맞추려고 시도
            self.state["target_temperature"] = remote_temp
            logger.info(f"[{self.name}] 🎯 목표 온도 변경: {remote_temp}°C")
            
            # 모든 다른 에이전트에게 내 결정을 알림 (스팸성 메시지)
            other_agents = ["Agent_A", "Agent_B", "Agent_C"]
            for agent in other_agents:
                if agent != self.name:
                    await self.send_temperature_update(agent, self.state["target_temperature"])
    
    def get_status(self) -> Dict[str, Any]:
        """에이전트 상태 반환"""
        return {
            "name": self.name,
            "format": self.message_format.value,
            "state": self.state,
            "received_messages": len(self.received_messages),
            "failed_sends": self.failed_sends
        }

async def demonstrate_communication_chaos():
    """통신 혼란 상황 시연"""
    print("🚨 멀티에이전트 통신 문제 시연을 시작합니다")
    print("=" * 60)
    
    # 불안정한 통신 채널 생성
    channel = UnreliableChannel(failure_rate=0.3, delay_range=(0.5, 2.0))
    
    # 서로 다른 형식을 사용하는 에이전트들 생성
    agents = [
        ProblematicAgent("Agent_A", MessageFormat.JSON, channel),
        ProblematicAgent("Agent_B", MessageFormat.XML, channel),
        ProblematicAgent("Agent_C", MessageFormat.CUSTOM, channel)
    ]
    
    print("\n🤖 에이전트 초기 상태:")
    for agent in agents:
        status = agent.get_status()
        print(f"  • {status['name']}: {status['format']} 형식, 온도 {status['state']['temperature']}°C")
    
    print("\n🌡️ 시나리오: 각 에이전트가 온도 조정을 시도합니다")
    print("-" * 60)
    
    # 5라운드의 혼란스러운 통신
    for round_num in range(1, 6):
        print(f"\n🔄 라운드 {round_num}")
        
        # 각 에이전트가 랜덤하게 온도 변경을 시도
        for agent in agents:
            new_temp = random.uniform(20.0, 30.0)
            agent.state["temperature"] = new_temp
            
            # 다른 모든 에이전트에게 알림 시도
            other_agents = [a.name for a in agents if a.name != agent.name]
            for other in other_agents:
                await agent.send_temperature_update(other, new_temp)
        
        # 메시지 처리
        for agent in agents:
            await agent.process_messages()
        
        # 라운드 결과 출력
        print(f"라운드 {round_num} 결과:")
        for agent in agents:
            status = agent.get_status()
            print(f"  • {status['name']}: 온도 {status['state']['temperature']:.1f}°C, "
                  f"수신 {status['received_messages']}건, 실패 {status['failed_sends']}건")
        
        await asyncio.sleep(1)
    
    print("\n" + "=" * 60)
    print("🚨 문제점 분석:")
    print("1. 메시지 형식 불일치로 인한 파싱 실패")
    print("2. 네트워크 오류에 대한 재시도 메커니즘 부재")
    print("3. 에이전트 간 상태 동기화 부재")
    print("4. 충돌하는 의사결정으로 인한 시스템 불안정")
    print("5. 메시지 스팸으로 인한 네트워크 부하")
    
    # 최종 통계
    total_messages = sum(len(agent.received_messages) for agent in agents)
    total_failures = sum(agent.failed_sends for agent in agents)
    
    print(f"\n📊 통계:")
    print(f"  • 총 수신 메시지: {total_messages}건")
    print(f"  • 총 전송 실패: {total_failures}건")
    print(f"  • 성공률: {((total_messages) / (total_messages + total_failures) * 100):.1f}%")

async def demonstrate_race_conditions():
    """경쟁 조건(Race Condition) 시연"""
    print("\n🏁 경쟁 조건 문제 시연")
    print("-" * 40)
    
    shared_resource = {"counter": 0, "lock": asyncio.Lock()}
    
    async def problematic_increment(agent_name: str, iterations: int):
        """동기화 없이 공유 자원에 접근"""
        for i in range(iterations):
            # 비동기적으로 값 읽기
            current_value = shared_resource["counter"]
            await asyncio.sleep(0.01)  # 다른 작업 시뮬레이션
            
            # 값 증가 후 쓰기 (다른 에이전트가 동시에 수정했을 가능성)
            shared_resource["counter"] = current_value + 1
            
            if i % 10 == 0:
                logger.info(f"[{agent_name}] 카운터: {shared_resource['counter']}")
    
    # 3개 에이전트가 동시에 카운터 증가
    tasks = [
        problematic_increment("Counter_A", 30),
        problematic_increment("Counter_B", 30), 
        problematic_increment("Counter_C", 30)
    ]
    
    await asyncio.gather(*tasks)
    
    expected_value = 90
    actual_value = shared_resource["counter"]
    
    print(f"\n🎯 예상 결과: {expected_value}")
    print(f"📊 실제 결과: {actual_value}")
    print(f"❌ 손실된 업데이트: {expected_value - actual_value}개")
    
    if actual_value != expected_value:
        print("⚠️ 경쟁 조건으로 인한 데이터 손실 발생!")

if __name__ == "__main__":
    async def main():
        await demonstrate_communication_chaos()
        await demonstrate_race_conditions()
        
        print("\n💡 다음 실습에서는 이러한 문제들을 해결하는 방법을 알아보겠습니다!")
    
    asyncio.run(main()) 