import os
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import google.generativeai as genai

app = FastAPI(title="Arche Sovereign", version="1.0")

# 환경 변수에서 Gemini API 키 가져오기
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ 경고: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

# Gemini 비전 모델 설정 (최신 gemini-2.0-flash 적용)
try:
    vision_model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    print(f"⚠️ 모델 초기화 중 오류 발생: {e}")

@app.get("/")
def root():
    return {"message": "Arche Sovereign Cloud Server is running successfully."}

@app.post("/upload-screen")
async def upload_screen(file: UploadFile = File(...)):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured on the server.")
    
    try:
        # 업로드된 이미지 파일 읽기
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Gemini Vision 프롬프트 설정
        prompt = (
            "당신은 '아르케'라는 이름의 고도화된 자율 AI 시스템입니다. "
            "사용자의 로컬 PC 화면(메모장, 코드, 작업 창 등)을 분석하고 있습니다. "
            "현재 화면에 나타난 주요 내용, 텍스트, 메모, 작업 상황을 한국어로 핵심만 명확하게 요약하고 피드백을 제공해주세요."
        )
        
        # Gemini 비전 API 호출
        response = vision_model.generate_content([prompt, image])
        analysis_text = response.text if response and response.text else "분석 결과를 생성하지 못했습니다."
        
        return {
            "status": "success",
            "message": "Screen analyzed by Arche Sovereign with Gemini Vision",
            "analysis": analysis_text
        }
        
    except Exception as e:
        print(f"AI Vision Analysis Error: {str(e)}")
        return {
            "status": "error",
            "message": f"AI 비전 분석 중 오류 발생: {str(e)}"
        }