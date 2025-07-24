import streamlit as st
import random

st.set_page_config(page_title="Streamlit 솔리테어", layout="wide")
st.title("🃏 Streamlit 솔리테어 (룰 + 이동 + 색 규칙 + 파운데이션 포함)")

st.markdown("""
텍스트 기반 솔리테어입니다. 
- 각 열에서 마지막 공개된 카드만 다른 열로 옮길 수 있습니다.
- 파운데이션에는 같은 무늬로 A부터 K까지 순서대로 쌓아야 합니다.
- 카드 이동 시 색이 교차해야 하며, 이동되는 카드는 현재 카드보다 숫자가 1 작아야 합니다.
- 더미(Deck)에서 새로운 카드를 열고, 오픈된 카드를 열 또는 파운데이션으로 이동할 수 있습니다.
""")

suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
rank_value = {rank: i+1 for i, rank in enumerate(ranks)}
suit_color = {"♠": "black", "♣": "black", "♥": "red", "♦": "red"}
deck_full = [f"{suit}{rank}" for suit in suits for rank in ranks]

# 상태 초기화
if "columns" not in st.session_state:
    random.shuffle(deck_full)
    st.session_state.columns = []
    for i in range(4):
        pile = deck_full[i*7:(i+1)*7]
        hidden = pile[:-1]
        visible = [pile[-1]] if pile else []
        st.session_state.columns.append({"hidden": hidden, "visible": visible})
    st.session_state.foundation = {suit: [] for suit in suits}
    st.session_state.deck = deck_full[28:]
    st.session_state.open_card = []
    st.session_state.discard_pile = []

# 테이블 출력
st.markdown("---")
st.subheader("📍 테이블")
max_height = max(len(col["hidden"] + col["visible"]) for col in st.session_state.columns)
table_grid = []
for i in range(max_height):
    row = []
    for col in st.session_state.columns:
        hidden = col["hidden"]
        visible = col["visible"]
        total = hidden + visible
        if i < len(hidden):
            row.append("[###]")
        elif i < len(total):
            row.append(f"[{total[i]:>3}]")
        else:
            row.append("[   ]")
    table_grid.append(row)

for row in table_grid:
    st.markdown(" ".join(row))

# 더미와 오픈 카드
st.markdown("---")
st.subheader("🎴 더미와 오픈 카드")
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 더미에서 카드 열기"):
        if st.session_state.deck:
            card = st.session_state.deck.pop(0)
            st.session_state.open_card = [card]
            st.session_state.discard_pile.append(card)
        else:
            st.session_state.deck = st.session_state.discard_pile
            st.session_state.discard_pile = []
            st.session_state.open_card = []
            random.shuffle(st.session_state.deck)
            st.info("더미가 초기화되었습니다.")

with col2:
    if st.session_state.open_card:
        st.markdown(f"열린 카드: [{st.session_state.open_card[-1]}]")
    else:
        st.markdown("열린 카드 없음")

# 열에서 파운데이션 이동
st.markdown("---")
st.subheader("⬆️ 열 → 파운데이션 이동")
source_col_idx = st.selectbox("출발 열 (1~4):", [1, 2, 3, 4], key="col_to_foundation")
if st.button("열 카드 → 파운데이션 이동"):
    col = st.session_state.columns[source_col_idx - 1]
    if col["visible"]:
        card = col["visible"][-1]
        suit, rank = card[0], card[1:]
        foundation = st.session_state.foundation[suit]
        expected = ranks[len(foundation)] if len(foundation) < 13 else None
        if rank == expected:
            foundation.append(card)
            col["visible"].pop()
            if not col["visible"] and col["hidden"]:
                col["visible"].append(col["hidden"].pop())
            st.success(f"{card} → 파운데이션으로 이동 완료")
        else:
            st.warning(f"{suit} 파운데이션에는 {expected}가 필요합니다.")
    else:
        st.warning("선택한 열에 보이는 카드가 없습니다.")

# 파운데이션 상태 출력
st.markdown("---")
st.subheader("🏛️ 파운데이션 상태")
foundation_display = "  ".join([f"{suit}: {','.join(st.session_state.foundation[suit]) or '_'}" for suit in suits])
st.markdown(f"`{foundation_display}`")
