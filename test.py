import streamlit as st
import requests
from datetime import datetime

# 🌤️ 날씨 가져오기 함수
def get_weather(city):
    api_key = "YOUR_API_KEY"  # weatherapi.com에서 무료 발급
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=ko"
    response = requests.get(url)
    data = response.json()
    return data

# 👔 코디 추천 함수
def recommend_outfit(temp, condition):
    if "rain" in condition.lower() or "비" in condition:
        return "☔ 우산 챙기세요! 가벼운 방수 자켓 추천"
    elif temp < 5:
        return "🧥 두꺼운 패딩과 목도리 추천"
    elif temp < 15:
        return "🧥 가벼운 코트나 니트 추천"
    elif temp < 25:
        return "👕 반팔 + 가벼운 겉옷 추천"
    else:
        return "🩳 시원한 반팔, 반바지 추천"

# 🎨 Streamlit UI
st.title("👗 날씨 기반 코디 추천 앱")

city = st.text_input("도시 이름을 입력하세요 (예: Seoul, Tokyo, New York)", "Seoul")

if st.button("오늘 날씨 확인하기"):
    weather = get_weather(city)
    
    if "error" in weather:
        st.error("도시 이름을 확인해주세요 ❌")
    else:
        temp = weather["current"]["temp_c"]
        condition = weather["current"]["condition"]["text"]
        icon = weather["current"]["condition"]["icon"]

        st.subheader(f"🌤️ {city}의 현재 날씨")
        st.image(f"http:{icon}", width=80)
        st.write(f"🌡️ 온도: {temp}°C")
        st.write(f"☁️ 상태: {condition}")

        # 옷차림 추천
        outfit = recommend_outfit(temp, condition)
        st.success(outfit)
