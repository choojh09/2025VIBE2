import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", layout="centered")
st.title("✊ ✋ ✌ 🦎 🖖 가위바위보도마뱀스포크 게임")

st.markdown("""
가위, 바위, 보, 도마뱀, 스포크 중 하나를 선택하세요!  
컴퓨터와의 대결에서 이겨보세요!

**규칙 요약:**
- 가위는 보, 도마뱀을 이김
- 바위는 가위, 도마뱀을 이김
- 보자는 바위, 스포크를 이김
- 도마뱀은 보, 스포크를 이김
- 스포크는 가위, 바위를 이김
""")

choices = ["가위", "바위", "보", "도마뱀", "스포크"]
user_choice = st.radio("당신의 선택은?", choices)

# 상태 초기화
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "total" not in st.session_state:
    st.session_state.total = 0

# 승리 규칙 정의
win_rules = {
    "가위": ["보", "도마뱀"],
    "바위": ["가위", "도마뱀"],
    "보": ["바위", "스포크"],
    "도마뱀": ["보", "스포크"],
    "스포크": ["가위", "바위"]
}

if st.button("결과 보기"):
    computer_choice = random.choice(choices)
    st.write(f"컴퓨터의 선택: **{computer_choice}**")

    if user_choice == computer_choice:
        result = "무승부입니다! 😐"
        st.session_state.draws += 1
    elif computer_choice in win_rules.get(user_choice, []):
        result = "당신이 이겼습니다! 🎉"
        st.session_state.wins += 1
    else:
        result = "컴퓨터가 이겼습니다! 😢"
        st.session_state.losses += 1

    st.session_state.total += 1
    st.subheader(result)

    st.markdown("---")
    st.markdown(f"**총 게임 수:** {st.session_state.total}")
    st.markdown(f"✅ 승리: {st.session_state.wins}  \n❌ 패배: {st.session_state.losses}  \n➖ 무승부: {st.session_state.draws}")

