import streamlit as st

# 🌟 페이지 기본 설정
st.set_page_config(page_title="MBTI 직업 추천", page_icon="💼", layout="centered")

# 🌟 상단 제목
st.markdown("<h1 style='text-align:center; color:#FF69B4;'>💼 MBTI 기반 직업 추천 🌟</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>당신의 MBTI에 딱 맞는 직업을 찾아드립니다! 🚀</p>", unsafe_allow_html=True)

# 📋 MBTI 목록
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 📌 MBTI별 직업 추천
job_recommendations = {
    "ISTJ": ["📊 회계사", "⚖️ 변호사", "📋 관리자", "🏛️ 공무원"],
    "ISFJ": ["💉 간호사", "📚 교사", "🤝 사회복지사"],
    "INFJ": ["🧠 심리상담가", "✍️ 작가", "🌍 인권운동가"],
    "INTJ": ["📈 데이터 분석가", "🔬 연구원", "🗂️ 전략기획자"],
    "ISTP": ["🔧 엔지니어", "🛫 파일럿", "🔨 수리공"],
    "ISFP": ["🎨 디자이너", "📷 사진작가", "🎵 음악가"],
    "INFP": ["📖 작가", "🗨️ 상담사", "🌱 사회운동가"],
    "INTP": ["💻 프로그래머", "🔭 과학자", "💡 발명가"],
    "ESTP": ["💼 영업직", "🚀 기업가", "⚽ 스포츠 코치"],
    "ESFP": ["🎭 배우", "🎉 이벤트 기획자", "🧳 여행 가이드"],
    "ENFP": ["📢 광고기획자", "🎤 강연가", "🚀 창업가"],
    "ENTP": ["🏢 스타트업 창업자", "📋 기획자", "📊 마케터"],
    "ESTJ": ["👔 경영자", "🪖 군인", "📅 프로젝트 매니저"],
    "ESFJ": ["💉 간호사", "📚 교사", "💬 상담가"],
    "ENFJ": ["🤝 HR 매니저", "🧑‍🏫 코치", "🎓 강사"],
    "ENTJ": ["👑 CEO", "⚖️ 변호사", "📊 전략기획자"]
}

# 🎯 MBTI 선택 박스
selected_mbti = st.selectbox("💡 나의 MBTI 선택하기", mbti_types, index=2)

# 결과 출력
if selected_mbti:
    st.markdown(f"<h2 style='color:#FFD700;'>🔍 {selected_mbti} 유형 추천 직업</h2>", unsafe_allow_html=True)
    jobs = job_recommendations.get(selected_mbti, [])
    
    # 💖 직업 카드 스타일
    for job in jobs:
        st.markdown(
            f"""
            <div style='background-color:#fce4ec; padding:10px; border-radius:12px; margin-bottom:10px;'>
                <span style='font-size:18px;'>{job}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 추가 설명
    descriptions = {
        "INFJ": "INFJ는 이상주의적이며 깊은 사고를 하는 성향이 있어 🌱 사람들의 성장을 돕는 직업에서 강점을 보입니다.",
        "ENTP": "ENTP는 창의적이고 도전적인 성향을 가져 🚀 새로운 아이디어를 현실로 만드는 직업에 적합합니다.",
        "ISFP": "ISFP는 예술적 감각과 따뜻한 마음을 가진 유형으로 🎨 창의적인 분야에서 빛을 발합니다."
    }
    if selected_mbti in descriptions:
        st.info(descriptions[selected_mbti])

# 하단
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>💖 Created with Streamlit | Made for Career Education 🎓</p>", unsafe_allow_html=True)
