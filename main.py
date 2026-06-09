import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="산행 MBTI | 등산 유형 추천",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CSS Design
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(150, 210, 180, 0.28), transparent 28%),
        radial-gradient(circle at top right, rgba(120, 180, 230, 0.22), transparent 30%),
        linear-gradient(180deg, #f5fbf7 0%, #eef6f2 45%, #f8faf6 100%);
}

.hero {
    border-radius: 32px;
    padding: 42px 38px;
    background: linear-gradient(135deg, rgba(16, 83, 65, .94), rgba(47, 119, 96, .90)),
                url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    color: white;
    box-shadow: 0 22px 55px rgba(31, 78, 63, .25);
    margin-bottom: 24px;
}

.hero h1 {
    font-size: 3.0rem;
    line-height: 1.12;
    margin: 0 0 12px 0;
    font-weight: 800;
}

.hero p {
    font-size: 1.1rem;
    opacity: .94;
    max-width: 850px;
}

.badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.30);
    margin-bottom: 14px;
    font-weight: 700;
}

.card {
    padding: 24px;
    border-radius: 26px;
    background: rgba(255,255,255,.72);
    border: 1px solid rgba(47, 119, 96, .13);
    box-shadow: 0 12px 30px rgba(58, 91, 74, .10);
    margin-bottom: 16px;
}

.question-card {
    padding: 22px 24px 16px 24px;
    border-radius: 24px;
    background: rgba(255,255,255,.82);
    border: 1px solid rgba(38, 101, 79, .13);
    box-shadow: 0 8px 22px rgba(42, 84, 68, .08);
    margin: 18px 0;
}

.result-card {
    padding: 30px;
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(255,255,255,.92), rgba(235,247,239,.92));
    border: 1px solid rgba(36, 98, 77, .14);
    box-shadow: 0 18px 45px rgba(33, 78, 61, .14);
}

.type-title {
    font-size: 2.1rem;
    font-weight: 800;
    margin: 6px 0 8px 0;
    color: #174f3e;
}

.soft-title {
    color: #245f4b;
    font-weight: 800;
    margin-top: 8px;
}

.pill {
    display: inline-block;
    padding: 8px 12px;
    margin: 4px 6px 4px 0;
    border-radius: 999px;
    background: #e8f5ec;
    color: #1f5d48;
    border: 1px solid #cfe8d8;
    font-weight: 700;
}

.trail-img {
    min-height: 240px;
    border-radius: 28px;
    background: linear-gradient(160deg, rgba(20,80,62,.16), rgba(255,255,255,.55)),
                url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80');
    background-size: cover;
    background-position: center;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.35), 0 16px 36px rgba(42, 84, 68, .14);
}

.small-note {
    color: #557166;
    font-size: .92rem;
}

[data-testid="stMetricValue"] {
    color: #1e5f49;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eef8f1 0%, #f7faf5 100%);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Data
# -----------------------------
questions = [
    {
        "axis": "EI", "left": "I", "right": "E",
        "q": "산행 전날, 마음이 더 가까운 쪽은?",
        "left_text": "혼자 조용히 코스와 장비를 점검한다",
        "right_text": "함께 갈 사람들과 기대감을 나누며 준비한다"
    },
    {
        "axis": "EI", "left": "I", "right": "E",
        "q": "처음 만난 사람들과 함께 걷게 되었을 때 나는?",
        "left_text": "천천히 분위기를 보며 편안한 거리를 유지한다",
        "right_text": "먼저 말을 걸고 산행 분위기를 풀어 본다"
    },
    {
        "axis": "EI", "left": "I", "right": "E",
        "q": "정상에 올랐을 때 더 하고 싶은 것은?",
        "left_text": "잠시 조용히 풍경을 바라보며 쉰다",
        "right_text": "사진을 찍고 사람들과 감탄을 나눈다"
    },
    {
        "axis": "SN", "left": "S", "right": "N",
        "q": "등산 코스를 고를 때 더 끌리는 기준은?",
        "left_text": "거리, 고도, 난이도, 교통 같은 구체적 정보",
        "right_text": "능선 분위기, 계절감, 새로운 경험의 가능성"
    },
    {
        "axis": "SN", "left": "S", "right": "N",
        "q": "산길에서 더 자주 눈에 들어오는 것은?",
        "left_text": "길 상태, 이정표, 바위, 나무, 발 디딜 곳",
        "right_text": "산의 흐름, 풍경의 변화, 머릿속에 떠오르는 생각"
    },
    {
        "axis": "SN", "left": "S", "right": "N",
        "q": "새로운 산을 알게 되었을 때 나는?",
        "left_text": "후기와 지도, 예상 시간을 먼저 확인한다",
        "right_text": "그 산에서 어떤 장면을 만날지 먼저 상상한다"
    },
    {
        "axis": "TF", "left": "T", "right": "F",
        "q": "일행 중 한 명이 힘들어할 때 나는?",
        "left_text": "속도, 거리, 하산 시간을 계산해 방법을 정한다",
        "right_text": "먼저 괜찮은지 묻고 마음을 편하게 해 준다"
    },
    {
        "axis": "TF", "left": "T", "right": "F",
        "q": "코스 선택에서 의견이 갈리면?",
        "left_text": "위험도와 시간표를 기준으로 합리적으로 정한다",
        "right_text": "모두가 납득하고 편안한 방향을 찾는다"
    },
    {
        "axis": "TF", "left": "T", "right": "F",
        "q": "산행 후 가장 만족스러운 순간은?",
        "left_text": "계획한 코스를 안전하게 완주했을 때",
        "right_text": "함께한 사람들과 좋은 추억이 생겼을 때"
    },
    {
        "axis": "JP", "left": "J", "right": "P",
        "q": "산행 계획을 세울 때 나는?",
        "left_text": "출발 시간, 휴식 지점, 하산 시간을 미리 잡는다",
        "right_text": "큰 방향만 정하고 현장에서 유연하게 움직인다"
    },
    {
        "axis": "JP", "left": "J", "right": "P",
        "q": "예상치 못한 갈림길이 나오면?",
        "left_text": "원래 계획과 안전 정보를 확인한 뒤 결정한다",
        "right_text": "상황이 괜찮다면 새로운 길도 시도해 본다"
    },
    {
        "axis": "JP", "left": "J", "right": "P",
        "q": "등산 가방을 챙기는 방식은?",
        "left_text": "체크리스트로 빠뜨린 물건이 없는지 확인한다",
        "right_text": "필수품 위주로 챙기고 나머지는 상황에 맡긴다"
    },
]

hiker_types = {
    "ISTJ": {"name": "정석 루트 마스터", "emoji": "🧭", "tagline": "지도, 시간, 안전을 믿고 차분히 완주하는 산행가", "style": "정해진 코스를 안정적으로 걷는 종주형·정규 탐방로 산행", "mountain": "북한산 둘레길, 소백산 비로봉, 지리산 노고단", "tips": ["출발 전 기상과 탐방로 통제 여부 확인", "체크리스트 기반 장비 준비", "동행자에게 예상 하산 시간 공유"], "color": "#2F6F5E"},
    "ISFJ": {"name": "따뜻한 페이스메이커", "emoji": "🍵", "tagline": "일행의 컨디션을 살피며 오래 기억될 산행을 만드는 사람", "style": "무리 없는 속도의 힐링 산행·숲길·둘레길", "mountain": "오대산 선재길, 축령산 잣나무숲, 청계산", "tips": ["간식과 따뜻한 음료 준비", "일행의 체력 차이를 고려한 코스 선택", "휴식 지점을 미리 정하기"], "color": "#4E8B6F"},
    "INFJ": {"name": "고요한 능선 사색가", "emoji": "🌙", "tagline": "산길에서 생각을 정리하고 의미를 발견하는 타입", "style": "풍경이 깊고 조용한 능선 산행·일출 산행", "mountain": "덕유산 향적봉, 설악산 권금성, 가야산 소리길", "tips": ["혼자 갈 때는 위치 공유 필수", "해 뜨기 전 산행은 보온과 랜턴 준비", "기록용 작은 노트나 카메라 추천"], "color": "#596B9A"},
    "INTJ": {"name": "전략적 종주 설계자", "emoji": "♟️", "tagline": "코스의 구조와 변수를 읽고 산행을 설계하는 사람", "style": "장거리 종주·고도 차가 있는 계획형 산행", "mountain": "지리산 성중종주, 덕유산 대종주, 한라산 성판악", "tips": ["구간별 탈출로 확인", "체력 배분표 만들기", "비상 시나리오를 2개 이상 준비"], "color": "#324B63"},
    "ISTP": {"name": "바위길 해결사", "emoji": "🪨", "tagline": "현장에서 길을 읽고 몸으로 문제를 해결하는 실전형", "style": "암릉·릿지 느낌의 기술적 산행 단, 안전장비 필수", "mountain": "도봉산 신선대, 관악산 연주대, 월출산", "tips": ["위험 구간에서는 속도보다 접지력", "장갑과 접지 좋은 등산화 준비", "비 오는 날 암릉 산행 피하기"], "color": "#6A6D54"},
    "ISFP": {"name": "계절 감성 트레커", "emoji": "🍂", "tagline": "꽃, 숲, 바람, 햇빛을 온몸으로 느끼는 산행가", "style": "봄꽃·단풍·계곡·숲길 중심의 감성 산행", "mountain": "내장산, 변산반도, 유명산 계곡길", "tips": ["사진 명소보다 안전한 보행 우선", "계절별 방수·방풍 준비", "여유로운 하산 시간을 확보"], "color": "#C08457"},
    "INFP": {"name": "숲속 몽상가", "emoji": "🌿", "tagline": "사람이 적은 길에서 자기만의 이야기를 발견하는 타입", "style": "조용한 숲길·문학적 감성이 있는 길·사찰길", "mountain": "선운산, 내변산, 오대산 월정사 전나무숲", "tips": ["너무 외진 길은 피하고 통신 상태 확인", "감성 기록용 사진·메모 추천", "무리한 야간 산행은 피하기"], "color": "#7A9B76"},
    "INTP": {"name": "코스 분석 탐험가", "emoji": "🔍", "tagline": "지도와 고도표를 보며 최적의 길을 궁리하는 타입", "style": "새 코스 분석·GPS 기록·지형 이해형 산행", "mountain": "속리산 문장대, 치악산, 팔공산", "tips": ["GPS 앱과 보조배터리 준비", "지도만 보느라 주변 안전을 놓치지 않기", "산행 후 기록 정리 추천"], "color": "#4B778D"},
    "ESTP": {"name": "스릴 능선 러너", "emoji": "⚡", "tagline": "역동적이고 생생한 산행에서 에너지를 얻는 타입", "style": "전망 좋은 암릉·빠른 템포의 활동적 산행", "mountain": "불암산, 수락산, 도봉산, 월출산", "tips": ["무리한 추월 금지", "보호 장비와 수분 보충 필수", "날씨 나쁜 날 스릴 코스 피하기"], "color": "#D97745"},
    "ESFP": {"name": "정상 인증 분위기 메이커", "emoji": "📸", "tagline": "사람들과 웃고 찍고 나누며 산행을 즐기는 타입", "style": "전망대·인증샷 명소·맛집 연계 산행", "mountain": "아차산, 인왕산, 남산, 대둔산", "tips": ["사진 촬영 시 낭떠러지 접근 금지", "대중교통 접근성 좋은 코스 추천", "하산 후 식사 장소까지 코스로 설계"], "color": "#E19A3B"},
    "ENFP": {"name": "즉흥 숲길 크리에이터", "emoji": "🎒", "tagline": "새로운 길과 사람, 예상 밖의 풍경을 좋아하는 타입", "style": "테마 산행·계절 이벤트·새로운 코스 탐방", "mountain": "강화 마니산, 제천 월악산, 가평 운악산", "tips": ["즉흥 변경 전 하산 시간 확인", "동행자와 체력 기대치 맞추기", "흥미로운 코스일수록 안전정보 먼저 확인"], "color": "#E07A5F"},
    "ENTP": {"name": "루트 개척 아이디어뱅크", "emoji": "🗺️", "tagline": "남들이 잘 안 가는 조합과 새로운 산행 방식을 찾는 타입", "style": "연계산행·테마산행·색다른 루트 기획", "mountain": "불수사도북 일부 구간, 관악산 연계길, 영남알프스", "tips": ["비공식 샛길은 피하기", "아이디어보다 안전 기준 우선", "동행자에게 코스 난이도를 정확히 안내"], "color": "#8A5AAB"},
    "ESTJ": {"name": "대장형 리더 산악인", "emoji": "🚩", "tagline": "일정과 속도를 관리하며 팀을 목적지까지 이끄는 타입", "style": "단체 산행·종주·시간 관리가 중요한 코스", "mountain": "설악산 대청봉, 한라산, 지리산 바래봉", "tips": ["리더일수록 후미 확인", "일정표와 비상연락망 준비", "팀원의 체력 차이를 계획에 반영"], "color": "#A94F3D"},
    "ESFJ": {"name": "모두의 산행 코디네이터", "emoji": "🥾", "tagline": "사람들이 편안하게 즐기도록 챙기는 산행 운영자", "style": "친목 산행·초보자 동행 산행·도시 근교 산행", "mountain": "청계산, 광교산, 무등산 증심사 코스", "tips": ["초보자 기준의 난이도 안내", "간식·휴식·화장실 위치 확인", "하산 후 일정까지 부드럽게 연결"], "color": "#5C9E7B"},
    "ENFJ": {"name": "동행 성장 가이드", "emoji": "🌄", "tagline": "함께 걷는 사람에게 자신감과 의미를 주는 타입", "style": "초보자 리딩·교육형 산행·목표 달성형 산행", "mountain": "북한산 백운대 초보 리딩, 소요산, 계룡산", "tips": ["격려와 안전 안내를 함께 하기", "무리한 목표보다 완주 경험 중시", "산행 전후 피드백 나누기"], "color": "#3B8E8C"},
    "ENTJ": {"name": "원정대 플래너", "emoji": "🏔️", "tagline": "큰 목표를 세우고 팀을 조직해 도전하는 타입", "style": "원정 산행·장거리 코스·체계적 목표 산행", "mountain": "설악산 공룡능선, 지리산 종주, 영남알프스 9봉", "tips": ["도전 목표와 안전 기준을 분리", "체력 훈련 계획 세우기", "기상 악화 시 철수 기준 명확히 하기"], "color": "#284B63"},
}

axis_names = {
    "EI": ("고요한 충전", "함께하는 활력"),
    "SN": ("현실 감각", "풍경 상상력"),
    "TF": ("판단과 안전", "공감과 동행"),
    "JP": ("계획적 완주", "유연한 탐험")
}

# -----------------------------
# Helper functions
# -----------------------------
def score_to_letter(axis, left_letter, right_letter, value, scores):
    # value: -2, -1, 0, 1, 2
    if value < 0:
        scores[left_letter] += abs(value)
    elif value > 0:
        scores[right_letter] += value
    else:
        scores[left_letter] += 0.5
        scores[right_letter] += 0.5


def calculate_mbti(responses):
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for q, value in responses:
        score_to_letter(q["axis"], q["left"], q["right"], value, scores)
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"
    return mbti, scores


def confidence(a, b):
    total = a + b
    if total == 0:
        return 50
    return round(max(a, b) / total * 100)


def axis_progress(label1, label2, score1, score2):
    c = confidence(score1, score2)
    winner = label1 if score1 >= score2 else label2
    st.progress(c / 100, text=f"{winner} 성향 {c}%")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("### ⛰️ 산행 MBTI")
    st.write("부드러운 상황 질문으로 등산 성향을 추정합니다.")
    st.markdown("---")
    st.markdown("**활용 예시**")
    st.write("• 산악회 신입 회원 유형 파악")
    st.write("• 등산 동아리 아이스브레이킹")
    st.write("• 산행 코스 추천 활동")
    st.markdown("---")
    st.caption("공식 MBTI 검사가 아니라 산행 성향을 이해하기 위한 참고용 웹앱입니다.")

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="badge">Mountain Personality Finder</div>
    <h1>나는 어떤 등산객일까?</h1>
    <p>MBTI를 직접 묻지 않고, 산행 상황에서의 선택을 통해 나의 등산 스타일을 찾아봅니다. 결과는 등산 유형, 어울리는 산행 방식, 추천 코스, 안전 팁으로 이어집니다.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.15, .85], gap="large")
with left:
    st.markdown("<div class='card'><h3 class='soft-title'>🌲 진단 방법</h3><p>각 질문에서 내 모습에 더 가까운 방향을 선택하세요. 완전히 한쪽이 아니어도 괜찮습니다. 산에서는 사람마다 다른 속도와 방식이 있으니까요.</p></div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='trail-img'></div>", unsafe_allow_html=True)

# -----------------------------
# Form
# -----------------------------
with st.form("hiker_form"):
    st.markdown("### 🧑‍🦯 산행자 정보")
    c1, c2, c3 = st.columns(3)
    with c1:
        nickname = st.text_input("닉네임", placeholder="예: 능선러버")
    with c2:
        hiking_level = st.selectbox("등산 경험", ["입문", "초보", "보통", "숙련", "고수"])
    with c3:
        preferred = st.selectbox("선호 산행", ["가벼운 숲길", "정상 인증", "장거리 종주", "계곡·숲", "암릉·능선", "아직 모르겠음"])

    st.markdown("### 🌿 산길에서의 나를 떠올려 보세요")
    st.caption("가운데는 ‘둘 다 비슷함’입니다. 왼쪽 또는 오른쪽으로 갈수록 해당 문장에 더 가깝습니다.")

    responses = []
    slider_labels = {
        -2: "왼쪽에 매우 가까움",
        -1: "왼쪽에 조금 가까움",
        0: "둘 다 비슷함",
        1: "오른쪽에 조금 가까움",
        2: "오른쪽에 매우 가까움"
    }

    for idx, q in enumerate(questions, start=1):
        st.markdown(f"""
        <div class="question-card">
            <b>{idx}. {q['q']}</b><br><br>
            <span class="small-note">← {q['left_text']}</span><br>
            <span class="small-note">→ {q['right_text']}</span>
        </div>
        """, unsafe_allow_html=True)
        value = st.select_slider(
            "나의 선택",
            options=[-2, -1, 0, 1, 2],
            value=0,
            format_func=lambda x: slider_labels[x],
            key=f"q_{idx}",
            label_visibility="collapsed"
        )
        responses.append((q, value))

    submitted = st.form_submit_button("⛰️ 나의 등산 유형 보기", use_container_width=True)

# -----------------------------
# Result
# -----------------------------
if submitted:
    mbti, scores = calculate_mbti(responses)
    result = hiker_types[mbti]

    st.balloons()
    st.markdown("---")

    r1, r2 = st.columns([1.05, .95], gap="large")
    with r1:
        st.markdown(f"""
        <div class="result-card">
            <div style="font-size:3.4rem">{result['emoji']}</div>
            <div class="small-note">추정 산행 MBTI: <b>{mbti}</b></div>
            <div class="type-title">{result['name']}</div>
            <p style="font-size:1.08rem; color:#34584b;">{result['tagline']}</p>
            <span class="pill">{hiking_level} 등산객</span>
            <span class="pill">선호: {preferred}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🥾 어울리는 산행 스타일")
        st.success(result["style"])

        st.markdown("### 🗺️ 추천 산행지 예시")
        st.write(result["mountain"])

    with r2:
        st.markdown("### 📊 성향 지도")
        axis_progress(axis_names["EI"][0], axis_names["EI"][1], scores["I"], scores["E"])
        axis_progress(axis_names["SN"][0], axis_names["SN"][1], scores["S"], scores["N"])
        axis_progress(axis_names["TF"][0], axis_names["TF"][1], scores["T"], scores["F"])
        axis_progress(axis_names["JP"][0], axis_names["JP"][1], scores["J"], scores["P"])

        st.markdown("### 🎒 안전하고 즐거운 산행 팁")
        for tip in result["tips"]:
            st.write(f"- {tip}")

    st.markdown("### 🧩 함께 가면 좋은 등산 파트너")
    partner_cols = st.columns(4)
    partner_texts = [
        ("🧭 계획형", "일정과 안전을 챙겨주는 사람"),
        ("🌿 감성형", "풍경과 분위기를 함께 즐기는 사람"),
        ("⚡ 활동형", "산행에 활력을 더해주는 사람"),
        ("🍵 배려형", "속도와 컨디션을 맞춰주는 사람"),
    ]
    for col, (title, desc) in zip(partner_cols, partner_texts):
        with col:
            st.markdown(f"<div class='card'><h4>{title}</h4><p>{desc}</p></div>", unsafe_allow_html=True)

    result_df = pd.DataFrame([{
        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "닉네임": nickname,
        "등산경험": hiking_level,
        "선호산행": preferred,
        "산행MBTI": mbti,
        "등산유형": result["name"],
        "추천스타일": result["style"],
        "추천산행지": result["mountain"],
        "E": scores["E"], "I": scores["I"],
        "S": scores["S"], "N": scores["N"],
        "T": scores["T"], "F": scores["F"],
        "J": scores["J"], "P": scores["P"],
    }])

    st.download_button(
        "📥 결과 CSV 다운로드",
        data=result_df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"hiker_mbti_result_{nickname if nickname else 'guest'}.csv",
        mime="text/csv",
        use_container_width=True
    )

    with st.expander("교사용·모임 운영자용 활용 아이디어"):
        st.write("1. 산악회 신입 회원의 선호 산행 스타일 파악")
        st.write("2. 산행 조 편성 시 계획형·배려형·활동형을 균형 있게 배치")
        st.write("3. 결과 CSV를 모아 다음 산행 코스 선정 자료로 활용")
        st.write("4. 단, 결과는 성격을 고정하는 검사가 아니라 대화와 안전 계획을 위한 참고 자료로 활용")
