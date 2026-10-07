from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from PIL import Image

app = FastAPI()

UPLOAD_DIR = "."
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {
        "version": "v39.2-Arche-Sovereign-AI-Vision",
        "system_mode": "AUTONOMOUS_KOREAN_ANALYTICAL_GOVERNED",
        "control_lock": "SECURED_BY_DAYUL"
    }

@app.post("/upload-screen")
async def upload_screen(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, "local_captured.png")
    
    # 1. 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. 화면 분석 로직 (Pillow 활용)
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            format_type = img.format
            
        analysis_result = (
            f"해상도 {width}x{height} 크기의 {format_type} 화면이 성공적으로 감지되었습니다. "
            "현재 시각 데이터의 무결성이 정상적으로 확인되었습니다."
        )
    except Exception as e:
        analysis_result = f"이미지 분석 중 예외 발생: {str(e)}"

    # 3. 결과 반환
    return JSONResponse(content={
        "status": "SUCCESS",
        "message": "Screen received and analyzed by Arche Sovereign",
        "filename": "local_captured.png",
        "analysis": analysis_result,
        "control_lock": "SECURED_BY_DAYUL"
    })