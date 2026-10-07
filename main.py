import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import google.generativeai as genai

app = FastAPI()

# 1. Gemini API 설정 (Render 환경 변수에서 안전하게 불러옴)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # 최신 비전 모델 장착
    vision_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    vision_model = None

UPLOAD_DIR = "."
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {
        "version": "v41-Arche-Gemini-Vision",
        "system_mode": "AUTONOMOUS_VISION_GOVERNED",
        "control_lock": "SECURED_BY_DAYUL"
    }

@app.post("/upload-screen")
async def upload_screen(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, "local_captured.png")
    
    # 2. 파일 저장
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Gemini AI 비전 분석 수행
    analysis_result = "Gemini API 키가 설정되지 않았습니다."
    if vision_model:
        try:
            img = Image.open(file_path)
            prompt = (
                "당신은 아르케 자율 시스템의 AI 두뇌입니다. "
                "이 화면 이미지를 분석하여 사용자가 현재 어떤 작업을 하고 있는지, "
                "특이사항이나 눈여겨봐야 할 점이 있는지 한국어로 간결하고 명확하게 분석해 주세요."
            )
            response = vision_model.generate_content([prompt, img])
            analysis_result = response.text.strip()
        except Exception as e:
            analysis_result = f"AI 비전 분석 중 오류 발생: {str(e)}"
    else:
        with Image.open(file_path) as img:
            width, height = img.size
            analysis_result = f"해상도 {width}x{height} 화면 수신 (API 키 등록 필요)"

    # 4. 결과 반환
    return JSONResponse(content={
        "status": "SUCCESS",
        "message": "Screen analyzed by Arche Sovereign with Gemini Vision",
        "filename": "local_captured.png",
        "analysis": analysis_result,
        "control_lock": "SECURED_BY_DAYUL"
    })