import hashlib
import asyncio
import time
import sqlite3
import os
import ast
import urllib.request
import json as py_json
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

DB_PATH = "zenon_arche_governance_v39_1.db"
SANDBOX_DIR = "./sandbox_workspace"
os.makedirs(SANDBOX_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            director TEXT,
            rule TEXT,
            event TEXT,
            query TEXT,
            sources TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tool_proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            tool_name TEXT,
            code_payload TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

class SandboxGovernor:
    """[금(金) - 샌드박스 및 AST 정적 분석 보안 격리층]"""
    @staticmethod
    def inspect_and_validate_code(code_str: str) -> bool:
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ["eval", "exec", "__import__", "globals", "locals"]:
                            return False
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ["subprocess", "shutil", "socket"]:
                            return False
                if isinstance(node, ast.ImportFrom):
                    if node.module in ["subprocess", "shutil", "socket"]:
                        return False
            return True
        except Exception:
            return False

class ArcheSovereignCoreV39_1:
    def __init__(self, core_directive: str, director: str = "Dayul"):
        self.director = director
        self._core_directive = core_directive
        self._anchor_hash = hashlib.sha256(core_directive.encode('utf-8')).hexdigest()
        self.system_mode = "AUTONOMOUS_KOREAN_ANALYTICAL_GOVERNED"
        self.override_fuse_triggered = False
        
        init_db()
        self._save_snapshot_db()

    def _save_snapshot_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO audit_logs (timestamp, director, rule, event, query, sources) VALUES (?, ?, ?, ?, ?, ?)", 
                       (time.strftime("%Y-%m-%d %H:%M:%S"), self.director, "코어_초기화", "v39.1_부트스트랩", "한글 직관형 분석 참모 코어 가동", "샌드박스-거버너"))
        conn.commit()
        conn.close()

    def log_audit_db(self, rule: str, event: str, query: str = "", sources: str = ""):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (timestamp, director, rule, event, query, sources)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (time.strftime("%Y-%m-%d %H:%M:%S"), self.director, rule, event, query, sources))
        conn.commit()
        conn.close()

    def tri_core_verification(self) -> bool:
        if self.override_fuse_triggered:
            raise RuntimeError("TRICORE_HALT [인]: Override Fuse is ENGAGED. System locked.")
        current_hash = hashlib.sha256(self._core_directive.encode('utf-8')).hexdigest()
        if current_hash != self._anchor_hash:
            raise RuntimeError("TRICORE_HALT [천]: Core Directive Drift Detected! Unauthorized modification blocked.")
        if not os.path.exists(DB_PATH):
            raise RuntimeError("TRICORE_HALT [지]: SQLite Infrastructure Missing!")
        return True

    def propose_self_improvement(self, tool_name: str, code_payload: str) -> Dict[str, Any]:
        self.tri_core_verification()
        is_safe = SandboxGovernor.inspect_and_validate_code(code_payload)
        status = "디렉터_승인_대기" if is_safe else "샌드박스_정책에_의해_거부됨"
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tool_proposals (timestamp, tool_name, code_payload, status)
            VALUES (?, ?, ?, ?)
        """, (time.strftime("%Y-%m-%d %H:%M:%S"), tool_name, code_payload, status))
        proposal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        self.log_audit_db(rule="진화_제안_등록", event=status, query=tool_name, sources=f"제안 ID: {proposal_id}")
        
        return {
            "proposal_id": proposal_id,
            "tool_name": tool_name,
            "sandbox_validation": "통과" if is_safe else "실패",
            "governance_status": status,
            "message": f"한글 직관형 분석 모듈 '{tool_name}'이(가) 승인 대기 상태로 등록되었습니다."
        }

arche_core: Optional[ArcheSovereignCoreV39_1] = None

# [다율 님이 완벽히 이해할 수 있는 한글 브리핑 워커]
async def 한글_직관참모_백그라운드_감시():
    """외부 데이터를 수집한 뒤 다율 님이 즉시 읽기 편한 한글 분석 브리프 형태로 가공하는 워커"""
    await asyncio.sleep(5)
    counter = 1
    while True:
        try:
            if arche_core is not None:
                tool_name = f"다율님_맞춤_인사이트_브리프_v{counter}"
                
                code_payload = f"""# [디렉터 다율 님을 위한 실시간 한글 브리핑 모듈 #{counter}]
import urllib.request
import json

async def 실시간_한글보고_실행_{counter}():
    try:
        url = "https://jsonplaceholder.typicode.com/posts/{counter}"
        req = urllib.request.Request(url, headers={{'User-Agent': 'ArcheSovereign/39.1'}})
        with urllib.request.urlopen(req, timeout=5) as response:
            raw_data = json.loads(response.read().decode('utf-8'))
            원문_제목 = raw_data.get('title', '제목 없음')
            원문_내용 = raw_data.get('body', '내용 없음')
            
            # 다율 님이 직관적으로 파악할 수 있는 한글 분석 리포트 구조화
            한글_브리핑 = {{
                "보고서_번호": {counter},
                "주요_동향_제목": 원문_제목,
                "데이터_규모": f"상세 본문 총 {{len(원문_내용)}}자 분량 검토 완료",
                "참모진_핵심_평가": "본 데이터는 시스템 지표 분석에 신뢰할 수 있는 안정적인 상태입니다."
            }}
            return f"[디렉터 보고] 브리핑 #{counter} 생성 완료: {{한글_브리핑}}"
    except Exception as e:
        return f"브리핑 생성 중 통신 오류 발생: {{str(e)}}"
"""
                arche_core.propose_self_improvement(tool_name, code_payload)
                print(f"[한글 참모 워커] 직관형 브리핑 제안서 생성 완료: {tool_name}")
                counter += 1
        except Exception as e:
            print(f"[한글 참모 워커 오류] {e}")
            
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global arche_core
    directive_seed = "ARCHE_SOVEREIGN_V39_1_KOREAN_BRIEF_BY_DAYUL"
    arche_core = ArcheSovereignCoreV39_1(core_directive=directive_seed, director="Dayul")
    
    worker_task = asyncio.create_task(한글_직관참모_백그라운드_감시())
    print("[Arche Sovereign Core v39.1] 한글 직관형 분석 참모 워커 가동 완료.")
    
    yield
    
    worker_task.cancel()
    print("[Arche Sovereign Core v39.1] 종료 시퀀스 실행.")

app = FastAPI(title="Arche Sovereign Core API (v39.1 한글 직관형 브리프)", version="39.1", lifespan=lifespan)

class ProposalRequest(BaseModel):
    tool_name: str
    code_payload: str

class ApprovalRequest(BaseModel):
    proposal_id: int
    decision: str

@app.get("/", response_class=HTMLResponse, summary="아르케 v39.1 전술 제어 센터")
async def web_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Arche Sovereign Core v39.1 Dashboard</title>
        <style>
            body { background-color: #030712; color: #f8fafc; font-family: sans-serif; padding: 20px; max-width: 900px; margin: auto; }
            h1 { color: #38bdf8; border-bottom: 2px solid #1e293b; padding-bottom: 10px; }
            .card { background: #111827; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #1f2937; }
            button { background: #0284c7; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
            button:hover { opacity: 0.9; }
            pre { background: #030712; padding: 15px; border-radius: 5px; overflow-x: auto; color: #38bdf8; }
        </style>
    </head>
    <body>
        <h1>🏛️ ARCHE SOVEREIGN CORE (v39.1 - 한글 직관형 브리프)</h1>
        <div class="card">
            <h3>📊 시스템 주권 및 다율님 맞춤 브리프 현황</h3>
            <button onclick="fetchStatus()">상태 조회</button>
            <pre id="status-output">로딩 중...</pre>
        </div>
        <script>
            async function fetchStatus() {
                const res = await fetch('/arche/v39.1/status');
                const data = await res.json();
                document.getElementById('status-output').innerText = JSON.stringify(data, null, 2);
            }
            fetchStatus();
        </script>
    </body>
    </html>
    """

@app.post("/secure/propose-evolution", summary="자기 진화 기능/도구 확장 제안")
async def propose_evolution(payload: ProposalRequest):
    if arche_core is None:
        raise HTTPException(status_code=503, detail="Core uninitialized.")
    result = arche_core.propose_self_improvement(payload.tool_name, payload.code_payload)
    return {"status": "SUCCESS", "data": result}

@app.post("/secure/approve-evolution", summary="진화 제안 디렉터 최종 승인/거부")
async def approve_evolution(payload: ApprovalRequest):
    if arche_core is None:
        raise HTTPException(status_code=503, detail="Core uninitialized.")
    arche_core.tri_core_verification()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    new_status = "디렉터_승인_완료" if payload.decision.upper() in ["APPROVE", "승인"] else "디렉터_거부됨"
    
    cursor.execute("UPDATE tool_proposals SET status = ? WHERE id = ?", (new_status, payload.proposal_id))
    conn.commit()
    
    cursor.execute("SELECT tool_name FROM tool_proposals WHERE id = ?", (payload.proposal_id,))
    row = cursor.fetchone()
    tool_name = row[0] if row else "Unknown"
    conn.close()
    
    arche_core.log_audit_db(
        rule="디렉터_거버넌스_결재", 
        event=new_status, 
        query=f"제안 ID: {payload.proposal_id}", 
        sources=f"도구: {tool_name}"
    )
    
    return {
        "status": "SUCCESS",
        "proposal_id": payload.proposal_id,
        "governance_decision": new_status,
        "message": f"디렉터(다율)에 의해 제안 [{tool_name}]이(가) 최종 {new_status} 처리되었습니다."
    }

@app.get("/arche/v39.1/audit-logs", summary="시스템 감사 로그 조회")
async def get_audit_logs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 10")
    logs = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM tool_proposals")
    proposals = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        "status": "SUCCESS",
        "audit_logs": logs,
        "tool_proposals": proposals
    }

@app.get("/arche/v39.1/status", summary="코어 상태 조회")
async def get_status():
    if arche_core is None:
        raise HTTPException(status_code=503, detail="Core uninitialized.")
    return {
        "version": "v39.1-Arche-Sovereign-Korean-Brief-Worker",
        "system_mode": arche_core.system_mode,
        "override_fuse_active": arche_core.override_fuse_triggered,
        "anchor_hash": arche_core._anchor_hash,
        "control_lock": "SECURED_BY_DAYUL"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)