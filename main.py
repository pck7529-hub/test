import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="MBTI 기반 진로 추천",
    page_icon="🧭",
    layout="centered"
)

st.title("🧭 MBTI 성향 기반 진로 추천 웹앱")
st.caption("상황형 질문을 통해 학생의 성향을 자연스럽게 파악하고, 어울리는 진로를 추천합니다.")

st.info(
    "※ 이 검사는 공식 MBTI 검사가 아니라 진로 탐색을 위한 참고용 활동입니다. "
    "결과는 학생 상담이나 진로 대화의 출발점으로 활용하세요."
)

# -----------------------------
# 질문 데이터
# -----------------------------
questions = [
    {
        "axis": "EI",
        "left": "E",
        "right": "I",
        "question": "새로운 모둠 활동이 시작되었을 때 나는?",
        "left_text": "먼저 말을 걸고 역할을 나누는 편이다",
        "right_text": "분위기를 살핀 뒤 필요한 말을 하는 편이다"
    },
    {
        "axis": "EI",
        "left": "E",
        "right": "I",
        "question": "발표나 토론 시간이 주어지면 나는?",
        "left_text": "말하면서 생각이 정리되는 편이다",
        "right_text": "생각을 정리한 뒤 말하는 편이다"
    },
    {
        "axis": "SN",
        "left": "S",
        "right": "N",
        "question": "문제를 해결할 때 나는?",
        "left_text": "구체적인 자료와 실제 사례를 먼저 본다",
        "right_text": "전체 흐름과 가능성을 먼저 생각한다"
    },
    {
        "axis": "SN",
        "left": "S",
        "right": "N",
        "question": "새로운 지식을 배울 때 더 흥미로운 것은?",
        "left_text": "실험, 관찰, 실제 적용",
        "right_text": "아이디어, 상상, 미래 가능성"
    },
    {
        "axis": "TF",
        "left": "T",
        "right": "F",
        "question": "친구가 고민을 말했을 때 나는?",
        "left_text": "문제의 원인과 해결 방법을 함께 찾는다",
        "right_text": "친구의 감정을 먼저 공감해 준다"
    },
    {
        "axis": "TF",
        "left": "T",
        "right": "F",
        "question": "중요한 결정을 할 때 나는?",
        "left_text": "논리와 기준에 맞는 선택을 하려 한다",
        "right_text": "사람들의 마음과 관계를 고려한다"
    },
    {
        "axis": "JP",
        "left": "J",
        "right": "P",
        "question": "과제가 주어졌을 때 나는?",
        "left_text": "계획을 세우고 미리 끝내려 한다",
        "right_text": "상황에 맞게 유연하게 진행한다"
    },
    {
        "axis": "JP",
        "left": "J",
        "right": "P",
        "question": "여행이나 체험활동을 준비할 때 나는?",
        "left_text": "일정과 준비물을 미리 정리한다",
        "right_text": "큰 방향만 정하고 즉흥적으로 움직인다"
    }
]

career_map = {
    "INTJ": ["연구원", "데이터 분석가", "공학자", "전략기획자", "소프트웨어 개발자"],
    "INTP": ["과학자", "프로그래머", "수학자", "AI 연구원", "철학·논리 분야"],
    "ENTJ": ["경영자", "기획자", "프로젝트 매니저", "변호사", "창업가"],
    "ENTP": ["창업가", "마케터", "발명가", "콘텐츠 기획자", "토론·정책 분야"],
    "INFJ": ["상담가", "교사", "작가", "심리학자", "사회문제 해결 분야"],
    "INFP": ["작가", "디자이너", "상담가", "예술가", "NGO 활동가"],
    "ENFJ": ["교사", "상담가", "교육기획자", "인사 담당자", "사회복지사"],
    "ENFP": ["콘텐츠 크리에이터", "광고기획자", "방송·문화 분야", "진로코치", "창의기획자"],
    "ISTJ": ["공무원", "회계사", "품질관리자", "법무·행정 분야", "데이터 관리자"],
    "ISFJ": ["간호사", "교사", "사회복지사", "행정직", "보건·복지 분야"],
    "ESTJ": ["관리자", "경찰·군인", "경영지원", "행정가", "생산관리자"],
    "ESFJ": ["교사", "간호사", "서비스 관리자", "상담·복지 분야", "홍보 담당자"],
    "ISTP": ["엔지니어", "정비사", "응급구조사", "기술직", "스포츠·장비 분야"],
    "ISFP": ["디자이너", "예술가", "뷰티·패션 분야", "동물·자연 관련 직업", "치료·재활 분야"],
    "ESTP": ["영업 전문가", "스포츠 지도자", "경찰·소방", "이벤트 기획자", "창업가"],
    "ESFP": ["배우·방송인", "이벤트 기획자", "관광·서비스 분야", "유아교육", "공연예술 분야"]
}

strength_map = {
    "E": "사람들과의 상호작용 속에서 에너지를 얻고 표현력이 좋은 편입니다.",
    "I": "깊이 생각하고 집중하며 혼자 정리하는 시간이 중요한 편입니다.",
    "S": "구체적 사실, 경험, 실제 사례를 바탕으로 판단하는 편입니다.",
    "N": "가능성, 아이디어, 미래 방향을 상상하는 데 강점이 있습니다.",
    "T": "논리적 기준과 객관적 근거를 바탕으로 판단하는 편입니다.",
    "F": "사람의 감정, 관계, 가치의 조화를 중요하게 여기는 편입니다.",
    "J": "계획적이고 체계적으로 일을 진행하는 데 강점이 있습니다.",
    "P": "상황 변화에 유연하게 대응하고 다양한 선택지를 열어두는 편입니다."
}

# -----------------------------
# 입력 폼
# -----------------------------
with st.form("mbti_form"):
    name = st.text_input("이름 또는 별명", placeholder="예: 김민준")
    grade = st.selectbox("학년", ["중1", "중2", "중3", "고1", "고2", "고3", "기타"])

    st.divider()
    st.subheader("상황형 질문")

    answers = []

    for i, q in enumerate(questions):
        st.write(f"**{i+1}. {q['question']}**")
        choice = st.radio(
            label="선택",
            options=[
                q["left_text"],
                "둘 다 비슷하다",
                q["right_text"]
            ],
            key=f"q{i}",
            horizontal=False,
            label_visibility="collapsed"
        )

        if choice == q["left_text"]:
            answers.append((q["axis"], q["left"]))
        elif choice == q["right_text"]:
            answers.append((q["axis"], q["right"]))
        else:
            answers.append((q["axis"], "M"))

    submitted = st.form_submit_button("결과 보기")

# Streamlit의 form은 입력값을 한 번에 제출하게 해 앱이 불필요하게 계속 다시 실행되는 것을 줄이는 데 유용합니다. :contentReference[oaicite:2]{index=2}

# -----------------------------
# 결과 계산
# -----------------------------
if submitted:
    scores = {
        "E": 0, "I": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }

    for axis, result in answers:
        if result != "M":
            scores[result] += 1
        else:
            # 중립 선택은 양쪽에 0.5점
            if axis == "EI":
                scores["E"] += 0.5
                scores["I"] += 0.5
            elif axis == "SN":
                scores["S"] += 0.5
                scores["N"] += 0.5
            elif axis == "TF":
                scores["T"] += 0.5
                scores["F"] += 0.5
            elif axis == "JP":
                scores["J"] += 0.5
                scores["P"] += 0.5

    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"

    careers = career_map.get(mbti, [])

    st.divider()
    st.header("📌 진로 추천 결과")

    if name:
        st.write(f"**{name} 학생의 추정 성향은 `{mbti}` 입니다.**")
    else:
        st.write(f"**추정 성향은 `{mbti}` 입니다.**")

    st.subheader("성향 해석")
    for letter in mbti:
        st.write(f"- **{letter}**: {strength_map[letter]}")

    st.subheader("추천 진로")
    cols = st.columns(2)
    for idx, career in enumerate(careers):
        with cols[idx % 2]:
            st.success(career)

    st.subheader("진로 탐색 질문")
    st.write(
        f"""
        `{mbti}` 성향의 학생은 위 직업들을 참고하되, 다음 질문을 함께 생각해 보면 좋습니다.

        1. 내가 오래 집중해도 지치지 않는 활동은 무엇인가?
        2. 사람, 자료, 도구, 아이디어 중 무엇을 다룰 때 흥미가 큰가?
        3. 추천 직업 중 실제로 체험해 보고 싶은 분야는 무엇인가?
        4. 관련 동아리, 과목, 독서, 탐구 주제로 연결할 수 있는 것은 무엇인가?
        """
    )

    # 결과 저장용 데이터프레임
    result_df = pd.DataFrame([{
        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "이름": name,
        "학년": grade,
        "MBTI": mbti,
        "추천진로": ", ".join(careers),
        "E": scores["E"],
        "I": scores["I"],
        "S": scores["S"],
        "N": scores["N"],
        "T": scores["T"],
        "F": scores["F"],
        "J": scores["J"],
        "P": scores["P"]
    }])

    csv = result_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 결과 CSV 다운로드",
        data=csv,
        file_name=f"mbti_career_result_{name if name else 'student'}.csv",
        mime="text/csv"
    )

    st.caption("교사는 다운로드한 CSV 파일을 모아 학급 진로 상담 자료로 활용할 수 있습니다.")
