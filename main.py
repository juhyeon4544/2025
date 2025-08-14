import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 직업 추천", page_icon="💼", layout="centered")

st.title("💼 MBTI 기반 직업 추천")
st.write("당신의 MBTI를 선택하면, 어울리는 직업을 추천해드립니다!")

# MBTI 리스트
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# MBTI별 직업 추천 데이터
job_recommendations = {
    "ISTJ": ["회계사", "변호사", "관리자", "공무원"],
    "ISFJ": ["간호사", "교사", "사회복지사"],
    "INFJ": ["심리상담가", "작가", "인권운동가"],
    "INTJ": ["데이터 분석가", "연구원", "전략기획자"],
    "ISTP": ["엔지니어", "파일럿", "수리공"],
    "ISFP": ["디자이너", "사진작가", "음악가"],
    "INFP": ["작가", "상담사", "사회운동가"],
    "INTP": ["프로그래머", "과학자", "발명가"],
    "ESTP": ["영업직", "기업가", "스포츠 코치"],
    "ESFP": ["배우", "이벤트 기획자", "여행 가이드"],
    "ENFP": ["광고기획자", "강연가", "창업가"],
    "ENTP": ["스타트업 창업자", "기획자", "마케터"],
    "ESTJ": ["경영자", "군인", "프로젝트 매니저"],
    "ESFJ": ["간호사", "교사", "상담가"],
    "ENFJ": ["HR 매니저", "코치", "강사"],
    "ENTJ": ["CEO", "변호사", "전략기획자"]
}

# MBTI 선택
selected_mbti = st.selectbox("MBTI를 선택하세요", mbti_types)

# 직업 추천 출력
if selected_mbti:
    st.subheader(f"🔍 {selected_mbti} 유형 추천 직업")
    for job in job_recommendations.get(selected_mbti, []):
        st.write(f"- {job}")

# (선택) 추천 직업에 대한 추가 설명
if selected_mbti == "INFJ":
    st.info("INFJ는 이상주의적이고 깊은 사고를 하는 성향이 있어 사람들의 성장을 돕는 직업에서 강점을 보입니다.")

