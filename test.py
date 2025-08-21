import streamlit as st
import random
import pandas as pd

st.title("🃏 영어 단어 플래시카드")

# CSV 업로드
uploaded_file = st.file_uploader("📂 단어장이 담긴 CSV 파일을 업로드하세요 (영어, 뜻)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    words = list(zip(df["영어"], df["뜻"]))

    # 세션 상태 초기화
    if "index" not in st.session_state:
        st.session_state.index = 0
        st.session_state.unknown = []

    eng, kor = words[st.session_state.index]

    st.subheader("📖 플래시카드")
    st.markdown(f"**단어:** {eng}")

    if st.button("뜻 보기"):
        st.markdown(f"👉 **뜻:** {kor}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("알아요 ✅"):
            st.session_state.index = (st.session_state.index + 1) % len(words)

    with col2:
        if st.button("몰라요 ❌"):
            st.session_state.unknown.append((eng, kor))
            st.session_state.index = (st.session_state.index + 1) % len(words)

    st.markdown("---")
    if st.session_state.unknown:
        st.subheader("❌ 아직 모르는 단어")
        for e, k in st.session_state.unknown:
            st.write(f"{e} - {k}")

else:
    st.info("CSV 파일을 업로드하면 플래시카드를 시작할 수 있어요.")
