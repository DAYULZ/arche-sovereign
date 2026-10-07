import os
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from pydantic import BaseModel

app = FastAPI(
    title="Arche Sovereign Core",
    version="v39.1-Arche-Sovereign-Korean-Brief-Worker",
)

# 업로드된 이미지를 저장할 폴더 (서버 내부 임시 저장용)
UPLOAD_DIR = "received_screens"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SECRET_KEY = "SECURED_BY_DAYUL"


@app.get("/")
def read_root():
  return {
      "version": "v39.1-Arche-Sovereign-Korean-Brief-Worker",
      "system_mode": "AUTONOMOUS_KOREAN_ANALYTICAL_GOVERNED",
      "override_fuse_active": False,
      "anchor_hash": (
          "ab1982b9a22c1d33c1a060b06a1ed31e3e18a5db97d8398a75c8c697e33e9fd7"
      ),
      "control_lock": "SECURED_BY_DAYUL",
  }


# 슬래시 유무에 상관없이 모두 수신할 수 있도록 복수 경로 지정
@app.post("/upload-screen")
@app.post("/upload-screen/")
async def upload_screen(
    file: UploadFile = File(...), x_control_lock: str = Header(None)
):
  # 보안 검증: 다율 님의 통제권(Control Lock) 확인
  if x_control_lock != SECRET_KEY:
    raise HTTPException(status_code=403, detail="ACCESS DENIED: SECURED_BY_DAYUL")

  # 파일 저장 경로 설정
  file_path = os.path.join(UPLOAD_DIR, file.filename)

  # 이미지 파일 저장
  with open(file_path, "wb") as buffer:
    content = await file.read()
    buffer.write(content)

  return {
      "status": "SUCCESS",
      "message": "Screen received successfully by Arche Sovereign",
      "filename": file.filename,
      "control_lock": "SECURED_BY_DAYUL",
  }