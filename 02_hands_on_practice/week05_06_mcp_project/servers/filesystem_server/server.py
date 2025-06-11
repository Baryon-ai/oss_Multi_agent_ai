"""
MCP 파일 시스템 서버

이 서버는 파일 시스템에 대한 안전한 접근을 제공하는 MCP 서버입니다.
- Resources: 파일 및 디렉토리 구조 노출
- Tools: 파일 읽기/쓰기/검색 도구
- Roots: 접근 권한이 있는 루트 디렉토리 설정
"""

import asyncio
import json
import os
import sys
import mimetypes
import glob
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 관련 임포트 (실제 구현에서는 mcp 패키지 사용)
class MCPServer:
    """간단한 MCP 서버 구현"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.capabilities = {
            "resources": {"subscribe": True, "listChanged": True},
            "tools": {},
            "prompts": {},
            "roots": {"listChanged": True}
        }
        self.roots: List[str] = []
        
    def add_root(self, path: str):
        """루트 디렉토리 추가"""
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path) and os.path.isdir(abs_path):
            self.roots.append(abs_path)
            logger.info(f"루트 디렉토리 추가: {abs_path}")
        else:
            logger.error(f"유효하지 않은 루트 디렉토리: {abs_path}")

class FileSystemMCPServer:
    """파일 시스템 MCP 서버"""
    
    def __init__(self, project_root: str = None):
        self.server = MCPServer("filesystem-server")
        self.project_root = project_root or os.getcwd()
        self.server.add_root(self.project_root)
        
        # 허용된 파일 확장자 (보안상 제한)
        self.allowed_extensions = {
            '.txt', '.md', '.py', '.js', '.ts', '.json', '.yaml', '.yml', 
            '.html', '.css', '.sql', '.sh', '.bash', '.conf', '.cfg',
            '.log', '.csv', '.xml', '.ini', '.toml', '.rst'
        }
        
        # 제외할 디렉토리
        self.excluded_dirs = {
            '.git', '.svn', '__pycache__', 'node_modules', '.venv', 
            'venv', '.pytest_cache', '.mypy_cache', 'dist', 'build'
        }
    
    def is_path_allowed(self, path: str) -> bool:
        """경로가 허용되는지 확인"""
        abs_path = os.path.abspath(path)
        
        # 루트 디렉토리 내부인지 확인
        for root in self.server.roots:
            if abs_path.startswith(root):
                return True
        return False
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """파일 정보 반환"""
        try:
            stat = os.stat(file_path)
            return {
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_directory": os.path.isdir(file_path),
                "mime_type": mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            }
        except Exception as e:
            logger.error(f"파일 정보 조회 오류: {e}")
            return {}
    
    async def list_resources(self) -> Dict[str, Any]:
        """MCP Resources 목록 반환"""
        resources = []
        
        for root in self.server.roots:
            # 루트 디렉토리 자체를 리소스로 추가
            resources.append({
                "uri": f"file://{root}",
                "name": f"프로젝트 루트 ({os.path.basename(root)})",
                "mimeType": "application/vnd.directory",
                "description": f"프로젝트 루트 디렉토리: {root}"
            })
            
            # 주요 파일들을 리소스로 추가
            for file_path in self._scan_important_files(root):
                rel_path = os.path.relpath(file_path, root)
                file_info = self.get_file_info(file_path)
                
                if file_info:
                    resources.append({
                        "uri": f"file://{file_path}",
                        "name": rel_path,
                        "mimeType": file_info["mime_type"],
                        "description": f"파일 크기: {file_info['size']} bytes"
                    })
        
        return {
            "resources": resources
        }
    
    def _scan_important_files(self, root_dir: str, max_files: int = 50) -> List[str]:
        """중요한 파일들 스캔"""
        important_files = []
        
        # 우선순위가 높은 파일들
        priority_files = [
            'README.md', 'README.txt', 'requirements.txt', 'package.json',
            'setup.py', 'Dockerfile', 'docker-compose.yml', '.env.example',
            'config.py', 'settings.py', 'main.py', 'app.py', 'index.js'
        ]
        
        # 루트 레벨의 우선순위 파일들 먼저 추가
        for filename in priority_files:
            file_path = os.path.join(root_dir, filename)
            if os.path.isfile(file_path):
                important_files.append(file_path)
        
        # 나머지 파일들 추가 (제한된 수량)
        try:
            for root, dirs, files in os.walk(root_dir):
                # 제외 디렉토리 스킵
                dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
                
                for file in files:
                    if len(important_files) >= max_files:
                        break
                        
                    file_path = os.path.join(root, file)
                    ext = os.path.splitext(file)[1].lower()
                    
                    if ext in self.allowed_extensions and file_path not in important_files:
                        important_files.append(file_path)
                
                if len(important_files) >= max_files:
                    break
                    
        except Exception as e:
            logger.error(f"파일 스캔 오류: {e}")
        
        return important_files
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """리소스 읽기"""
        try:
            # URI에서 파일 경로 추출
            if not uri.startswith("file://"):
                raise ValueError("지원하지 않는 URI 스키마")
            
            file_path = uri[7:]  # "file://" 제거
            
            if not self.is_path_allowed(file_path):
                raise PermissionError("접근 권한이 없습니다")
            
            if os.path.isdir(file_path):
                # 디렉토리인 경우 목록 반환
                contents = []
                try:
                    for item in os.listdir(file_path):
                        item_path = os.path.join(file_path, item)
                        if item not in self.excluded_dirs:
                            contents.append(self.get_file_info(item_path))
                except PermissionError:
                    contents = [{"error": "디렉토리 읽기 권한이 없습니다"}]
                
                return {
                    "contents": [{
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(contents, indent=2, ensure_ascii=False)
                    }]
                }
            
            else:
                # 파일인 경우 내용 읽기
                if os.path.splitext(file_path)[1].lower() not in self.allowed_extensions:
                    raise ValueError("허용되지 않는 파일 형식입니다")
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                mime_type = mimetypes.guess_type(file_path)[0] or "text/plain"
                
                return {
                    "contents": [{
                        "uri": uri,
                        "mimeType": mime_type,
                        "text": content
                    }]
                }
                
        except Exception as e:
            logger.error(f"리소스 읽기 오류: {e}")
            return {
                "contents": [{
                    "uri": uri,
                    "mimeType": "text/plain",
                    "text": f"오류: {str(e)}"
                }]
            }
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """도구 호출"""
        try:
            if name == "search_files":
                return await self._search_files(arguments)
            elif name == "read_file":
                return await self._read_file(arguments)
            elif name == "write_file":
                return await self._write_file(arguments)
            elif name == "list_directory":
                return await self._list_directory(arguments)
            elif name == "file_stats":
                return await self._file_stats(arguments)
            else:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"알 수 없는 도구: {name}"
                    }]
                }
        except Exception as e:
            logger.error(f"도구 호출 오류: {e}")
            return {
                "content": [{
                    "type": "text", 
                    "text": f"오류: {str(e)}"
                }]
            }
    
    async def _search_files(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """파일 검색"""
        pattern = arguments.get("pattern", "")
        search_in_content = arguments.get("search_in_content", False)
        max_results = arguments.get("max_results", 20)
        
        results = []
        
        for root in self.server.roots:
            try:
                # 파일명 기반 검색
                for file_path in glob.glob(os.path.join(root, "**", f"*{pattern}*"), recursive=True):
                    if len(results) >= max_results:
                        break
                    
                    if self.is_path_allowed(file_path) and os.path.isfile(file_path):
                        ext = os.path.splitext(file_path)[1].lower()
                        if ext in self.allowed_extensions:
                            results.append({
                                "path": file_path,
                                "match_type": "filename",
                                "info": self.get_file_info(file_path)
                            })
                
                # 내용 기반 검색
                if search_in_content and len(results) < max_results:
                    for file_path in self._scan_important_files(root):
                        if len(results) >= max_results:
                            break
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if pattern.lower() in content.lower():
                                    results.append({
                                        "path": file_path,
                                        "match_type": "content",
                                        "info": self.get_file_info(file_path)
                                    })
                        except Exception:
                            continue
                            
            except Exception as e:
                logger.error(f"검색 오류: {e}")
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "pattern": pattern,
                    "results_count": len(results),
                    "results": results
                }, indent=2, ensure_ascii=False)
            }]
        }
    
    async def _read_file(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """파일 읽기"""
        file_path = arguments.get("path")
        
        if not file_path:
            raise ValueError("파일 경로가 필요합니다")
        
        if not self.is_path_allowed(file_path):
            raise PermissionError("접근 권한이 없습니다")
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.allowed_extensions:
            raise ValueError("허용되지 않는 파일 형식입니다")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return {
            "content": [{
                "type": "text",
                "text": f"파일: {file_path}\n{'='*50}\n{content}"
            }]
        }
    
    async def _write_file(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """파일 쓰기"""
        file_path = arguments.get("path")
        content = arguments.get("content", "")
        
        if not file_path:
            raise ValueError("파일 경로가 필요합니다")
        
        if not self.is_path_allowed(file_path):
            raise PermissionError("접근 권한이 없습니다")
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.allowed_extensions:
            raise ValueError("허용되지 않는 파일 형식입니다")
        
        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "content": [{
                "type": "text",
                "text": f"파일이 성공적으로 저장되었습니다: {file_path}"
            }]
        }
    
    async def _list_directory(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """디렉토리 목록"""
        dir_path = arguments.get("path", self.project_root)
        
        if not self.is_path_allowed(dir_path):
            raise PermissionError("접근 권한이 없습니다")
        
        if not os.path.isdir(dir_path):
            raise ValueError("유효한 디렉토리가 아닙니다")
        
        items = []
        for item in sorted(os.listdir(dir_path)):
            if item not in self.excluded_dirs:
                item_path = os.path.join(dir_path, item)
                items.append(self.get_file_info(item_path))
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "directory": dir_path,
                    "items": items
                }, indent=2, ensure_ascii=False)
            }]
        }
    
    async def _file_stats(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """파일 통계"""
        path = arguments.get("path", self.project_root)
        
        if not self.is_path_allowed(path):
            raise PermissionError("접근 권한이 없습니다")
        
        stats = {
            "total_files": 0,
            "total_directories": 0, 
            "total_size": 0,
            "file_types": {},
            "largest_files": []
        }
        
        file_sizes = []
        
        try:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
                stats["total_directories"] += len(dirs)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        ext = os.path.splitext(file)[1].lower() or "no_extension"
                        
                        stats["total_files"] += 1
                        stats["total_size"] += size
                        stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                        
                        file_sizes.append((file_path, size))
                        
                    except OSError:
                        continue
            
            # 가장 큰 파일들 (상위 10개)
            file_sizes.sort(key=lambda x: x[1], reverse=True)
            stats["largest_files"] = [
                {"path": path, "size": size} 
                for path, size in file_sizes[:10]
            ]
            
        except Exception as e:
            logger.error(f"통계 생성 오류: {e}")
        
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(stats, indent=2, ensure_ascii=False)
            }]
        }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록"""
        return [
            {
                "name": "search_files",
                "description": "파일명이나 내용으로 파일 검색",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string", "description": "검색할 패턴"},
                        "search_in_content": {"type": "boolean", "description": "파일 내용에서도 검색할지 여부"},
                        "max_results": {"type": "integer", "description": "최대 결과 수", "default": 20}
                    },
                    "required": ["pattern"]
                }
            },
            {
                "name": "read_file", 
                "description": "파일 내용 읽기",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "읽을 파일 경로"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "파일에 내용 쓰기",
                "inputSchema": {
                    "type": "object", 
                    "properties": {
                        "path": {"type": "string", "description": "쓸 파일 경로"},
                        "content": {"type": "string", "description": "파일 내용"}
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "list_directory",
                "description": "디렉토리 내용 목록",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "목록을 볼 디렉토리 경로"}
                    }
                }
            },
            {
                "name": "file_stats", 
                "description": "파일 시스템 통계",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "통계를 생성할 경로"}
                    }
                }
            }
        ]

# JSON-RPC 2.0 메시지 처리
async def handle_jsonrpc_message(server: FileSystemMCPServer, message: Dict[str, Any]) -> Dict[str, Any]:
    """JSON-RPC 2.0 메시지 처리"""
    
    method = message.get("method")
    params = message.get("params", {})
    message_id = message.get("id")
    
    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": server.server.capabilities,
                    "serverInfo": {
                        "name": server.server.name,
                        "version": server.server.version
                    }
                }
            }
        
        elif method == "resources/list":
            result = await server.list_resources()
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": result
            }
        
        elif method == "resources/read":
            uri = params.get("uri")
            result = await server.read_resource(uri)
            return {
                "jsonrpc": "2.0", 
                "id": message_id,
                "result": result
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "tools": server.get_tools()
                }
            }
        
        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            result = await server.call_tool(name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": result
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "error": {
                    "code": -32601,
                    "message": f"알 수 없는 메서드: {method}"
                }
            }
            
    except Exception as e:
        logger.error(f"메시지 처리 오류: {e}")
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "error": {
                "code": -32603,
                "message": f"내부 오류: {str(e)}"
            }
        }

async def main():
    """메인 서버 실행"""
    # 환경 변수에서 프로젝트 루트 가져오기
    project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
    
    server = FileSystemMCPServer(project_root)
    logger.info(f"파일 시스템 MCP 서버 시작됨")
    logger.info(f"프로젝트 루트: {project_root}")
    
    print("MCP 파일 시스템 서버가 준비되었습니다.")
    print(f"프로젝트 루트: {project_root}")

if __name__ == "__main__":
    asyncio.run(main()) 