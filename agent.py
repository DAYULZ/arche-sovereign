import io
import time
import pyautogui
import requests

# Render에 배포된 아르케 서버 주소
SERVER_URL = "https://arche-sovereign.onrender.com/upload-screen"
SECRET_KEY = "SECURED_BY_DAYUL"


def capture_and_send():
  try:
    print("🖥️️ 화면을 캡처하는 중...")
    # 전체 화면 캡처
    screenshot = pyautogui.screenshot()

    # 이미지를 메모리 상에서 바이트로 변환
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()

    # 클라우드 아르케 서버로 전송
    files = {"file": ("screen.png", img_byte_arr, "image/png")}
    headers = {"X-Control-Lock": SECRET_KEY}

    print("🚀 클라우드 아르케에게 화면 전송 중...")
    response = requests.post(SERVER_URL, files=files, headers=headers)

    if response.status_code == 200:
      print(f"✅ 전송 성공! 응답: {response.json()}")
    else:
      print(f"❌ 전송 실패 (상태 코드: {response.status_code})")
      print(response.text)

  except Exception as e:
    print(f"❌ 에러 발생: {e}")


if __name__ == "__main__":
  print("🛡️ 다율 님 전용 로컬 에이전트 대기 중...")
  print("화면을 캡처하여 서버로 보내려면 엔터키를 누르세요.")
  while True:
    input()
    capture_and_send()
    print("\n다시 캡처하려면 엔터를 누르세요.")