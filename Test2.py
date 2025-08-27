# -----------------------------
# 퀴즈 단계
# -----------------------------
elif st.session_state.step == "퀴즈":
    if st.session_state.level == "쉬움":
        words = easy_words
    elif st.session_state.level == "중간":
        words = medium_words
    else:
        words = hard_words

    # 퀴즈 단어 셔플 (처음 한 번만)
    if "quiz_words" not in st.session_state:
        st.session_state.quiz_words = random.sample(words, len(words))
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0

    # 현재 문제
    eng, kor = st.session_state.quiz_words[st.session_state.quiz_index]

    st.subheader("❓ 퀴즈 시작!")
    st.write(f"'{eng}' 의 뜻은 무엇일까요?")

    # 문제 번호 기반 key → 입력창 자동 초기화
    answer = st.text_input("정답 입력:", key=f"quiz_input_{st.session_state.quiz_index}")

    if st.button("확인"):
        if answer.strip() == kor:
            st.success("✅ 정답!")
            st.session_state.quiz_score += 1
        else:
            st.error(f"❌ 오답! 정답은 {kor}")

        st.session_state.quiz_index += 1

        if st.session_state.quiz_index >= len(st.session_state.quiz_words):
            st.success(f"🎉 퀴즈 완료! 점수: {st.session_state.quiz_score} / {len(st.session_state.quiz_words)}")
            del st.session_state.quiz_words  # 초기화
        else:
            st.experimental_rerun()

    st.write(f"진행 상황: {st.session_state.quiz_index + 1} / {len(st.session_state.quiz_words)}")
    st.write(f"현재 점수: {st.session_state.quiz_score}")
