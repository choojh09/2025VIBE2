import streamlit as st
import random

st.set_page_config(page_title="Streamlit 솔리테어", layout="wide")
st.title("🃏 Streamlit 솔리테어 (룰 구현 완료)")

st.markdown("""
텍스트 기반 솔리테어입니다. 각 열에서 맨 아래 카드만 움직일 수 있으며, 
동일한 무늬의 A부터 K까지 순서대로 파운데이션에 쌓을 수 있습니다.
카드는 --- 카드 --- 형식으로 표시됩니다.
""")

# 카드 문자열 포맷
suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = [f"{suit}{rank}" for suit in suits for rank in ranks]

# 상태 초기화
if "columns" not in st.session_state:
    random.shuffle(deck)
    st.session_state.columns = [deck[i*7:(i+1)*7] for i in range(4)]
    st.session_state.foundation = {suit: [] for suit in suits}

# 카드 옮기기
selected_column = st.selectbox("열에서 카드를 옮기세요:", list(range(1, 5)))
move = st.button("파운데이션으로 이동")

if move:
    col_idx = selected_column - 1
    if st.session_state.columns[col_idx]:
        card = st.session_state.columns[col_idx][-1]
        suit, rank = card[0], card[1:]
        foundation = st.session_state.foundation[suit]
        expected = ranks[len(foundation)]
        if rank == expected:
            st.session_state.foundation[suit].append(card)
            st.session_state.columns[col_idx].pop()
            st.success(f"{card} 이동 성공!")
        else:
            st.warning(f"{card}는 현재 이동할 수 없습니다. 다음은 {suit}{expected} 이어야 합니다.")
    else:
        st.warning("선택한 열에 카드가 없습니다.")

# 테이블 출력
st.markdown("---")
st.subheader("📍 테이블")
table_display = ""
for row in zip(*[col + ["   "] * (7 - len(col)) for col in st.session_state.columns]):
    line = "  ".join([f"---{card}---" if card.strip() else "         " for card in row])
    table_display += line + "\n"
st.text(table_display)

# 파운데이션 출력
st.markdown("---")
st.subheader("✅ 파운데이션")
foundation_display = "  ".join([
    f"{suit}: " + (" → ".join(st.session_state.foundation[suit]) if st.session_state.foundation[suit] else "(비어있음)")
    for suit in suits
])
st.markdown(f"```\n{foundation_display}\n```")

if st.button("🔄 초기화"):
    random.shuffle(deck)
    st.session_state.columns = [deck[i*7:(i+1)*7] for i in range(4)]
    st.session_state.foundation = {suit: [] for suit in suits}
    st.experimental_rerun()
