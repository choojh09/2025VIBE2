import streamlit as st
import html

# --- 질문지 구성 ---
QUESTIONS = [
    ("사교적인 편이다.", "E"),
    ("혼자 있는 시간이 필요하다.", "I"),
    ("사실과 현실을 중요시한다.", "S"),
    ("아이디어나 가능성에 끌린다.", "N"),
    ("논리와 분석으로 결정을 내린다.", "T"),
    ("감정과 공감을 중시한다.", "F"),
    ("계획을 세우고 실천하는 것을 선호한다.", "J"),
    ("유연하고 즉흥적인 걸 선호한다.", "P"),
    # 총 60문항 중 반복될 유형별 예시, 아래에서 반복
]

# 각 유형을 7개씩 추가하여 총 60개 구성
types = ["E", "I", "S", "N", "T", "F", "J", "P"]
repeated = (60 - len(QUESTIONS)) // len(types)
for t in types:
    for i in range(repeated):
        QUESTIONS.append((f"[{t}] 유형에 대한 질문 예시 {i+1}", t))

# --- MBTI 계산 로직 ---
if "scores" not in st.session_state:
    st.session_state.scores = {t: 0 for t in types}

st.set_page_config(page_title="MBTI 직업 추천", layout="wide")
st.title("🔍 MBTI 기반 진로 추천 웹사이트")
st.markdown("60개의 문항에 답변하여 본인의 성향을 파악하고, 적절한 직업을 추천받을 수 있습니다.")

with st.form("mbti_form"):
    for idx, (question, t) in enumerate(QUESTIONS):
        choice = st.radio(f"{idx+1}. {question}", ("그렇다", "아니다"), key=f"q{idx}")
        if choice == "그렇다":
            st.session_state.scores[t] += 1
    submitted = st.form_submit_button("결과 보기")

# --- MBTI 유형 결정 및 직업 추천 ---
if submitted:
    mbti = ""
    mbti += "E" if st.session_state.scores["E"] >= st.session_state.scores["I"] else "I"
    mbti += "S" if st.session_state.scores["S"] >= st.session_state.scores["N"] else "N"
    mbti += "T" if st.session_state.scores["T"] >= st.session_state.scores["F"] else "F"
    mbti += "J" if st.session_state.scores["J"] >= st.session_state.scores["P"] else "P"

    st.subheader(f"🧠 당신의 MBTI는: {mbti}")

    MBTI_JOBS = {
        "ISTJ": ["회계사", "공무원", "군인"],
        "ISFJ": ["간호사", "사회복지사", "초등교사"],
        "INFJ": ["심리상담사", "기획자", "인권활동가"],
        "INTJ": ["개발자", "전략기획가", "연구원"],
        "ISTP": ["기술자", "파일럿", "경찰관"],
        "ISFP": ["예술가", "치료사", "인테리어디자이너"],
        "INFP": ["작가", "심리상담가", "NGO활동가"],
        "INTP": ["과학자", "데이터분석가", "이론가"],
        "ESTP": ["소방관", "기업 영업", "스포츠 트레이너"],
        "ESFP": ["연예인", "이벤트기획자", "메이크업아티스트"],
        "ENFP": ["마케터", "작가", "교육 콘텐츠 기획자"],
        "ENTP": ["창업가", "광고기획자", "변호사"],
        "ESTJ": ["경영자", "군 간부", "프로젝트매니저"],
        "ESFJ": ["영양사", "간호사", "교사"],
        "ENFJ": ["진로상담가", "홍보담당자", "리더십 코치"],
        "ENTJ": ["CEO", "전략컨설턴트", "정치가"]
    }

    st.markdown("### 🔎 추천 직업군:")
    for job in MBTI_JOBS.get(mbti, []):
        st.markdown(f"- {job}")

    st.markdown("---")
    st.caption("이 결과는 참고용이며, 자기 탐색의 방향을 제시합니다.")
