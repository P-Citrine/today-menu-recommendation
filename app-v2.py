import streamlit as st

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="오늘의 메뉴 결정 도우미",
    page_icon="🍽️",
    layout="centered"
)

# 세션 상태 초기화 (다시 검사하기 및 결과 확인 버튼 상태 관리)
if "run_id" not in st.session_state:
    st.session_state.run_id = 0
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "submitted_answers" not in st.session_state:
    st.session_state.submitted_answers = None
if "just_submitted" not in st.session_state:
    st.session_state.just_submitted = False

# ==========================================
# 2. 식당 메뉴판 느낌의 커스텀 스타일(CSS)
# ==========================================
st.markdown("""
<style>
    /* 전체 배경을 따뜻한 미색 종이 느낌으로 설정 */
    .stApp {
        background-color: #FDF9F1;
    }
    /* 상단 식당 간판/차림표 헤더 디자인 */
    .menu-header {
        background-color: #C84B31;
        color: #FFFDF7;
        padding: 24px 20px;
        border-radius: 12px;
        text-align: center;
        border: 3px double #FFFDF7;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .menu-header h1 {
        margin: 0;
        font-size: 2rem;
        color: #FFFDF7 !important;
        letter-spacing: 2px;
    }
    .menu-header p {
        margin: 8px 0 0 0;
        font-size: 0.95rem;
        opacity: 0.95;
    }
    /* 질문 카드: 식당 주문서 느낌의 점선 테두리 */
    .order-card {
        background-color: #FFFFFF;
        border: 2px dashed #D9C5B2;
        border-radius: 10px;
        padding: 14px 18px 4px 18px;
        margin-bottom: 12px;
    }
    .question-title {
        font-weight: 700;
        color: #4A3525;
        font-size: 1.05rem;
        margin-bottom: 4px;
    }
    /* 결과 메뉴판 박스 */
    .result-board {
        background-color: #FFFDF9;
        border: 3px solid #C84B31;
        border-radius: 14px;
        padding: 28px 20px;
        text-align: center;
        margin-top: 16px;
        box-shadow: 0 6px 14px rgba(200, 75, 49, 0.12);
    }
    .badge {
        display: inline-block;
        background-color: #C84B31;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .menu-name {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2D1E12;
        margin: 10px 0 6px 0;
    }
    .menu-desc {
        color: #5C4738;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 14px;
    }
    .side-tip {
        background-color: #F7EFE2;
        border-radius: 8px;
        padding: 10px 14px;
        display: inline-block;
        color: #4A3525;
        font-size: 0.92rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. 총 14가지 메뉴별 귀여운 일러스트(SVG) 및 정보 데이터
# ==========================================
MENU_DATA = {
    "얼큰 돼지김치찌개 & 솥밥": {
        "tag": "든든한 한식 대표주자",
        "desc": "보글보글 끓는 얼큰한 국물에 푹 익은 김치와 두툼한 돼지고기! 지친 속과 마음을 확실하게 채워주는 한국인의 소울푸드입니다.",
        "side": "추천 곁들임: 계란말이 또는 김 가루 듬뿍",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFF0E6"/>
            <path d="M75 45 Q70 30 80 20" stroke="#FF8A65" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M100 42 Q95 27 105 17" stroke="#FF8A65" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M125 45 Q120 30 130 20" stroke="#FF8A65" stroke-width="5" fill="none" stroke-linecap="round"/>
            <ellipse cx="100" cy="95" rx="68" ry="26" fill="#3E3E3E"/>
            <path d="M32 95 Q38 158 100 158 Q162 158 168 95 Z" fill="#2C2C2C"/>
            <rect x="18" y="88" width="18" height="12" rx="6" fill="#2C2C2C"/>
            <rect x="164" y="88" width="18" height="12" rx="6" fill="#2C2C2C"/>
            <ellipse cx="100" cy="95" rx="60" ry="20" fill="#E64A19"/>
            <rect x="72" y="84" width="22" height="14" rx="3" fill="#FFF9C4" transform="rotate(-10 83 91)"/>
            <circle cx="118" cy="94" r="9" fill="#FFCCBC"/>
            <circle cx="95" cy="99" r="5" fill="#66BB6A"/>
            <circle cx="84" cy="128" r="4.5" fill="#FFFFFF"/>
            <circle cx="116" cy="128" r="4.5" fill="#FFFFFF"/>
            <path d="M93 135 Q100 143 107 135" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "뜨끈하고 진한 돼지국밥": {
        "tag": "속부터 든든한 영혼의 국밥",
        "desc": "뽀얗고 진하게 우러난 사골 육수에 야들야들한 수육이 한가득! 부추무침과 다대기를 취향껏 풀어 한 숟갈 뜨면 피로가 사르르 녹습니다.",
        "side": "추천 곁들임: 잘 익은 깍두기 & 부추무침 듬뿍",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#F5EFE6"/>
            <path d="M80 46 Q75 30 85 22" stroke="#BCAAA4" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M120 46 Q115 30 125 22" stroke="#BCAAA4" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M30 96 Q36 160 100 160 Q164 160 170 96 Z" fill="#373737"/>
            <ellipse cx="100" cy="96" rx="70" ry="24" fill="#4E4E4E"/>
            <ellipse cx="100" cy="96" rx="62" ry="18" fill="#FFFDF7"/>
            <rect x="64" y="88" width="22" height="12" rx="4" fill="#D7CCC8" transform="rotate(-8 75 94)"/>
            <rect x="112" y="89" width="22" height="12" rx="4" fill="#D7CCC8" transform="rotate(10 123 95)"/>
            <circle cx="100" cy="94" r="9" fill="#D84315"/>
            <path d="M85 102 L115 100" stroke="#43A047" stroke-width="4" stroke-linecap="round"/>
            <circle cx="84" cy="130" r="4.5" fill="#FFFFFF"/>
            <circle cx="116" cy="130" r="4.5" fill="#FFFFFF"/>
            <path d="M93 137 Q100 144 107 137" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "내 맘대로 골라 담는 마라탕": {
        "tag": "얼얼하고 중독적인 마라 수혈",
        "desc": "고소한 땅콩소스와 얼얼한 마라 향신료의 환상 조합! 청경채, 분모자, 푸주, 소고기까지 내가 좋아하는 재료만 골라 먹는 재미가 있습니다.",
        "side": "추천 곁들임: 쫀득 바삭 꿔바로우 미니 사이즈",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFEBEE"/>
            <path d="M32 98 Q42 158 100 158 Q158 158 168 98 Z" fill="#FFF8E1" stroke="#FFCDD2" stroke-width="4"/>
            <ellipse cx="100" cy="98" rx="68" ry="24" fill="#D32F2F"/>
            <ellipse cx="75" cy="94" rx="14" ry="8" fill="#66BB6A" transform="rotate(-20 75 94)"/>
            <rect x="96" y="85" width="26" height="11" rx="5.5" fill="#FFFDE7" transform="rotate(12 109 90)"/>
            <circle cx="128" cy="98" r="8" fill="#FFCC80"/>
            <circle cx="86" cy="103" r="6" fill="#B71C1C"/>
            <circle cx="85" cy="130" r="4.5" fill="#4E342E"/>
            <circle cx="115" cy="130" r="4.5" fill="#4E342E"/>
            <ellipse cx="74" cy="135" rx="5" ry="3" fill="#FF8A80"/>
            <ellipse cx="126" cy="135" rx="5" ry="3" fill="#FF8A80"/>
            <path d="M94 136 Q100 143 106 136" stroke="#4E342E" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "진한 육수의 돈코츠 라멘": {
        "tag": "깊고 진한 일식 면 요리",
        "desc": "진하게 우려낸 돈코츠 육수에 꼬들꼬들한 생면, 불향 입힌 차슈와 촉촉한 반숙 아지타마고(맛달걀)까지 완벽하게 어우러진 한 그릇입니다.",
        "side": "추천 곁들임: 육즙 가득 교자 만두 3피스",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFF8E1"/>
            <rect x="115" y="54" width="60" height="5" rx="2.5" fill="#8D6E63" transform="rotate(-12 145 56)"/>
            <rect x="115" y="64" width="60" height="5" rx="2.5" fill="#8D6E63" transform="rotate(-6 145 66)"/>
            <path d="M34 102 Q44 158 100 158 Q156 158 166 102 Z" fill="#C62828"/>
            <ellipse cx="100" cy="102" rx="66" ry="22" fill="#FFE0B2"/>
            <rect x="122" y="76" width="22" height="24" rx="3" fill="#263238" transform="rotate(14 133 88)"/>
            <ellipse cx="74" cy="96" rx="13" ry="10" fill="#FFFFFF"/>
            <circle cx="74" cy="96" r="6" fill="#FF8F00"/>
            <circle cx="104" cy="98" r="12" fill="#D7CCC8" stroke="#8D6E63" stroke-width="3"/>
            <circle cx="86" cy="132" r="4" fill="#FFFFFF"/>
            <circle cx="114" cy="132" r="4" fill="#FFFFFF"/>
            <path d="M94 138 Q100 144 106 138" stroke="#FFFFFF" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "바삭 꾸덕 반반 치킨": {
        "tag": "국민 힐링 메뉴 후라이드&양념",
        "desc": "고민할 필요 없이 바삭한 후라이드와 매콤달콤 양념을 한 번에! 한 입 베어 물면 오늘 하루 쌓인 스트레스가 바삭하게 부서집니다.",
        "side": "추천 곁들임: 아삭한 치킨무 & 시원한 탄산음료",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFF3E0"/>
            <path d="M44 110 L56 158 L144 158 L156 110 Z" fill="#E53935"/>
            <rect x="68" y="110" width="16" height="48" fill="#FFFFFF"/>
            <rect x="116" y="110" width="16" height="48" fill="#FFFFFF"/>
            <circle cx="74" cy="95" r="24" fill="#FFB300"/>
            <circle cx="98" cy="88" r="25" fill="#FFA000"/>
            <circle cx="124" cy="96" r="23" fill="#D84315"/>
            <circle cx="120" cy="88" r="3" fill="#FFF8E1"/>
            <circle cx="130" cy="93" r="3" fill="#FFF8E1"/>
            <circle cx="86" cy="130" r="4.5" fill="#2D1E12"/>
            <circle cx="114" cy="130" r="4.5" fill="#2D1E12"/>
            <path d="M94 138 Q100 145 106 138" stroke="#2D1E12" stroke-width="4" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "고슬고슬 중화 새우볶음밥": {
        "tag": "불향 입힌 황금빛 고소함",
        "desc": "센 불에서 빠르게 볶아내 밥알 하나하나가 고슬고슬 살아있는 계란 새우볶음밥! 짜장 소스에 쓱쓱 비벼 먹으면 남녀노소 호불호 없는 맛입니다.",
        "side": "추천 곁들임: 얼큰한 짬뽕 국물 & 단무지",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFFDE7"/>
            <ellipse cx="100" cy="126" rx="74" ry="30" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="4"/>
            <path d="M48 124 Q100 98 148 124 Q130 144 90 142 Z" fill="#4E342E"/>
            <path d="M52 122 Q56 64 100 64 Q144 64 148 122 Z" fill="#FFD54F"/>
            <path d="M92 60 Q106 48 112 64" stroke="#FF7043" stroke-width="8" fill="none" stroke-linecap="round"/>
            <circle cx="76" cy="92" r="4" fill="#66BB6A"/>
            <circle cx="122" cy="96" r="4" fill="#66BB6A"/>
            <circle cx="88" cy="102" r="4" fill="#4E342E"/>
            <circle cx="112" cy="102" r="4" fill="#4E342E"/>
            <path d="M95 109 Q100 115 105 109" stroke="#4E342E" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "통통 에그 베이컨 샌드위치": {
        "tag": "신선하고 간편한 브런치 정석",
        "desc": "노릇하게 구운 식빵 사이에 부드러운 에그마요, 짭조름한 베이컨, 아삭한 양상추와 토마토가 꽉 찬 샌드위치! 손에 들고 가볍게 즐기기 최고입니다.",
        "side": "추천 곁들임: 아이스 아메리카노 또는 생과일주스",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#F1F8E9"/>
            <polygon points="42,135 100,55 158,135" fill="#F5DEB3" stroke="#D2995B" stroke-width="6" stroke-linejoin="round"/>
            <path d="M52 130 Q75 122 100 130 Q125 138 148 130" stroke="#66BB6A" stroke-width="7" fill="none" stroke-linecap="round"/>
            <line x1="56" y1="122" x2="144" y2="122" stroke="#EF5350" stroke-width="6" stroke-linecap="round"/>
            <line x1="60" y1="114" x2="140" y2="114" stroke="#FFD54F" stroke-width="7" stroke-linecap="round"/>
            <circle cx="88" cy="96" r="4" fill="#5D4037"/>
            <circle cx="112" cy="96" r="4" fill="#5D4037"/>
            <path d="M95 103 Q100 108 105 103" stroke="#5D4037" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "로제 떡볶이 & 모둠튀김": {
        "tag": "매콤 꾸덕 도파민 충전",
        "desc": "매콤함과 부드러운 크림의 황금 비율! 쫄깃한 떡에 소스를 듬뿍 찍어 바삭한 튀김과 함께 먹으면 스트레스가 단번에 날아갑니다.",
        "side": "추천 곁들임: 김말이 튀김 & 쿨피스",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFEAE5"/>
            <path d="M35 100 Q45 155 100 155 Q155 155 165 100 Z" fill="#FFB74D"/>
            <ellipse cx="100" cy="100" rx="65" ry="22" fill="#FF7043"/>
            <rect x="65" y="86" width="32" height="14" rx="7" fill="#FFF8E1" transform="rotate(-18 81 93)"/>
            <rect x="102" y="88" width="32" height="14" rx="7" fill="#FFF8E1" transform="rotate(15 118 95)"/>
            <rect x="82" y="97" width="32" height="14" rx="7" fill="#FFF8E1" transform="rotate(4 98 104)"/>
            <circle cx="122" cy="83" r="10" fill="#FFFDE7"/>
            <circle cx="122" cy="83" r="5" fill="#FFD54F"/>
            <circle cx="86" cy="128" r="4" fill="#4E342E"/>
            <circle cx="114" cy="128" r="4" fill="#4E342E"/>
            <ellipse cx="75" cy="133" rx="5" ry="3" fill="#FF8A80"/>
            <ellipse cx="125" cy="133" rx="5" ry="3" fill="#FF8A80"/>
            <path d="M95 132 Q100 139 105 132" stroke="#4E342E" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "바삭 등심 수제 돈가스": {
        "tag": "실패 없는 겉바속촉 정석",
        "desc": "한 입 베어 물면 경쾌하게 바삭! 육즙 가득한 두툼한 등심 돈가스에 달콤짭짤한 소스와 양배추 샐러드의 조화는 언제나 옳습니다.",
        "side": "추천 곁들임: 따뜻한 미니 우동",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFF8E1"/>
            <ellipse cx="100" cy="112" rx="74" ry="44" fill="#FFFFFF" stroke="#E0CFA9" stroke-width="5"/>
            <circle cx="58" cy="95" r="16" fill="#AED581"/>
            <circle cx="70" cy="88" r="13" fill="#C5E1A5"/>
            <ellipse cx="112" cy="114" rx="48" ry="26" fill="#F59E0B"/>
            <line x1="88" y1="90" x2="82" y2="138" stroke="#FFF8E1" stroke-width="3"/>
            <line x1="106" y1="88" x2="100" y2="140" stroke="#FFF8E1" stroke-width="3"/>
            <line x1="124" y1="90" x2="118" y2="138" stroke="#FFF8E1" stroke-width="3"/>
            <path d="M78 110 Q95 102 112 114 Q128 124 144 110" stroke="#6D4C41" stroke-width="6" fill="none" stroke-linecap="round"/>
            <circle cx="96" cy="60" r="4" fill="#5D4037"/>
            <circle cx="118" cy="60" r="4" fill="#5D4037"/>
            <path d="M102 67 Q107 73 112 67" stroke="#5D4037" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "쉬림프 알리오올리오 & 파스타": {
        "tag": "기분 전환 캐주얼 양식",
        "desc": "고소한 마늘 향과 탱글탱글한 새우가 어우러진 파스타! 평범한 하루에 작은 여유와 맛있는 설렘을 더해줄 메뉴입니다.",
        "side": "추천 곁들임: 따끈한 마늘빵 & 수제 피클",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFFDE7"/>
            <ellipse cx="100" cy="118" rx="72" ry="38" fill="#FFFFFF" stroke="#CFD8DC" stroke-width="5"/>
            <ellipse cx="100" cy="112" rx="50" ry="25" fill="#FFE082"/>
            <path d="M65 112 Q100 85 135 112" stroke="#FFB300" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M70 120 Q100 98 130 120" stroke="#FFA000" stroke-width="5" fill="none" stroke-linecap="round"/>
            <circle cx="80" cy="98" r="9" fill="#FF8A65"/>
            <circle cx="120" cy="102" r="9" fill="#FF8A65"/>
            <ellipse cx="100" cy="92" rx="10" ry="5" fill="#66BB6A" transform="rotate(-20 100 92)"/>
            <circle cx="88" cy="115" r="4" fill="#4E342E"/>
            <circle cx="112" cy="115" r="4" fill="#4E342E"/>
            <path d="M95 122 Q100 128 105 122" stroke="#4E342E" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "더블 치즈 수제버거 세트": {
        "tag": "빠르고 확실한 행복 충전",
        "desc": "폭신한 브리오슈 번 사이에 육즙 가득 패티와 사르르 녹은 체다치즈! 바쁜 일정 속에서도 확실한 만족감을 주는 메뉴입니다.",
        "side": "추천 곁들임: 바삭한 감자튀김 & 제로콜라",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FFF3E0"/>
            <path d="M48 92 Q48 48 100 48 Q152 48 152 92 Z" fill="#F59E0B"/>
            <ellipse cx="82" cy="65" rx="4" ry="2" fill="#FFF8E1"/>
            <ellipse cx="102" cy="60" rx="4" ry="2" fill="#FFF8E1"/>
            <ellipse cx="120" cy="67" rx="4" ry="2" fill="#FFF8E1"/>
            <path d="M44 96 Q60 104 75 96 Q90 88 105 96 Q120 104 135 96 Q148 90 156 96" stroke="#66BB6A" stroke-width="8" fill="none" stroke-linecap="round"/>
            <polygon points="50,104 150,104 105,120" fill="#FFD54F"/>
            <rect x="48" y="106" width="104" height="18" rx="9" fill="#6D4C41"/>
            <rect x="50" y="126" width="100" height="22" rx="10" fill="#F59E0B"/>
            <circle cx="86" cy="79" r="4.5" fill="#4E342E"/>
            <circle cx="114" cy="79" r="4.5" fill="#4E342E"/>
            <path d="M95 85 Q100 90 105 85" stroke="#4E342E" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "연어 아보카도 포케 볼": {
        "tag": "가볍고 산뜻한 건강 한 끼",
        "desc": "신선한 연어와 부드러운 아보카도, 아삭한 채소에 고소한 소스를 곁들인 포케! 식곤증 없이 오후에도 가뿐한 컨디션을 지켜줍니다.",
        "side": "추천 곁들임: 단호박 수프 또는 아이스 아메리카노",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#E8F5E9"/>
            <path d="M36 102 Q45 158 100 158 Q155 158 164 102 Z" fill="#81C784"/>
            <ellipse cx="100" cy="102" rx="64" ry="22" fill="#FFFDF7"/>
            <rect x="62" y="88" width="22" height="18" rx="5" fill="#FF8A65"/>
            <rect x="86" y="92" width="20" height="16" rx="5" fill="#FF7043"/>
            <path d="M112 86 Q135 84 138 104 Q120 110 112 86 Z" fill="#9CCC65"/>
            <circle cx="72" cy="105" r="7" fill="#FFD54F"/>
            <circle cx="86" cy="130" r="4" fill="#2E7D32"/>
            <circle cx="114" cy="130" r="4" fill="#2E7D32"/>
            <path d="M94 136 Q100 142 106 136" stroke="#2E7D32" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "숯불 직화 제육덮밥": {
        "tag": "불향 가득 단짠매콤 밥도둑",
        "desc": "은은한 불향이 입혀진 매콤달콤 제육볶음 위에 반숙 계란후라이 톡! 숟가락으로 쓱쓱 비벼 마지막 한 톨까지 맛있게 비우게 됩니다.",
        "side": "추천 곁들임: 시원한 콩나물국 & 상추쌈",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#FBE9E7"/>
            <path d="M36 105 Q46 158 100 158 Q154 158 164 105 Z" fill="#5D4037"/>
            <ellipse cx="100" cy="104" rx="64" ry="22" fill="#D84315"/>
            <ellipse cx="100" cy="98" rx="30" ry="16" fill="#FFFFFF"/>
            <circle cx="100" cy="96" r="10" fill="#FFB300"/>
            <circle cx="72" cy="104" r="4" fill="#81C784"/>
            <circle cx="130" cy="102" r="4" fill="#81C784"/>
            <circle cx="85" cy="132" r="4" fill="#FFF8E1"/>
            <circle cx="115" cy="132" r="4" fill="#FFF8E1"/>
            <path d="M94 139 Q100 145 106 139" stroke="#FFF8E1" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        </svg>
        """
    },
    "시원한 냉모밀 & 초밥 세트": {
        "tag": "깔끔하고 정갈한 일식 한 상",
        "desc": "살얼음 동동 띄운 쯔유 육수에 쫄깃한 메밀면, 그리고 한 입에 쏙 들어가는 신선한 초밥까지! 깔끔하고 기분 좋게 배부른 메뉴입니다.",
        "side": "추천 곁들임: 바삭한 새우튀김 1피스",
        "svg": """
        <svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="90" fill="#E3F2FD"/>
            <rect x="34" y="88" width="76" height="54" rx="14" fill="#37474F"/>
            <ellipse cx="72" cy="92" rx="34" ry="12" fill="#6D4C41"/>
            <path d="M54 92 Q72 82 90 92" stroke="#D7CCC8" stroke-width="4" fill="none"/>
            <rect x="120" y="102" width="46" height="24" rx="10" fill="#FFFFFF" stroke="#ECEFF1" stroke-width="2"/>
            <rect x="118" y="94" width="50" height="13" rx="6" fill="#FF7043"/>
            <rect x="137" y="93" width="10" height="33" fill="#263238"/>
            <circle cx="62" cy="116" r="3.5" fill="#FFFFFF"/>
            <circle cx="82" cy="116" r="3.5" fill="#FFFFFF"/>
            <path d="M68 122 Q72 126 76 122" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round"/>
        </svg>
        """
    }
}


# ==========================================
# 4. 10개의 질문 및 14가지 메뉴 가중치 구성
# (각 질문당 선택지 최대 3개 유지)
# ==========================================
QUESTIONS = [
    {
        "q": "1. 지금 배고픔 정도는 어느 정도인가요?",
        "options": [
            ("꼬르륵 폭발 직전! 든든하게 채울래요", {
                "얼큰 돼지김치찌개 & 솥밥": 3, "뜨끈하고 진한 돼지국밥": 3,
                "숯불 직화 제육덮밥": 3, "바삭 등심 수제 돈가스": 2, "고슬고슬 중화 새우볶음밥": 2
            }),
            ("적당히 출출한 기분 좋은 상태예요", {
                "진한 육수의 돈코츠 라멘": 3, "내 맘대로 골라 담는 마라탕": 2,
                "쉬림프 알리오올리오 & 파스타": 2, "더블 치즈 수제버거 세트": 2, "바삭 꾸덕 반반 치킨": 2
            }),
            ("배는 덜 고픈데 맛있는 게 당겨요", {
                "통통 에그 베이컨 샌드위치": 3, "연어 아보카도 포케 볼": 3,
                "로제 떡볶이 & 모둠튀김": 2, "시원한 냉모밀 & 초밥 세트": 2
            })
        ]
    },
    {
        "q": "2. 오늘 국물이 필요한 날인가요?",
        "options": [
            ("뜨끈하고 진한 국물이 꼭 있어야 해요", {
                "얼큰 돼지김치찌개 & 솥밥": 3, "뜨끈하고 진한 돼지국밥": 4,
                "내 맘대로 골라 담는 마라탕": 3, "진한 육수의 돈코츠 라멘": 3
            }),
            ("시원한 육수나 꾸덕·자작한 소스가 좋아요", {
                "시원한 냉모밀 & 초밥 세트": 3, "로제 떡볶이 & 모둠튀김": 3,
                "쉬림프 알리오올리오 & 파스타": 2, "고슬고슬 중화 새우볶음밥": 2
            }),
            ("국물 없이 깔끔하거나 바삭한 메뉴가 좋아요", {
                "바삭 꾸덕 반반 치킨": 3, "통통 에그 베이컨 샌드위치": 3,
                "바삭 등심 수제 돈가스": 2, "더블 치즈 수제버거 세트": 2,
                "연어 아보카도 포케 볼": 2, "숯불 직화 제육덮밥": 2
            })
        ]
    },
    {
        "q": "3. 매운맛은 얼마나 당기시나요?",
        "options": [
            ("스트레스 풀리는 얼큰·매콤·얼얼한 맛!", {
                "내 맘대로 골라 담는 마라탕": 4, "얼큰 돼지김치찌개 & 솥밥": 3,
                "로제 떡볶이 & 모둠튀김": 3, "숯불 직화 제육덮밥": 3
            }),
            ("매콤달콤하거나 감칠맛 나는 적당한 자극", {
                "바삭 꾸덕 반반 치킨": 3, "쉬림프 알리오올리오 & 파스타": 2,
                "진한 육수의 돈코츠 라멘": 2, "뜨끈하고 진한 돼지국밥": 2
            }),
            ("안 맵고 고소하거나 담백·깔끔한 맛", {
                "고슬고슬 중화 새우볶음밥": 3, "통통 에그 베이컨 샌드위치": 3,
                "바삭 등심 수제 돈가스": 3, "연어 아보카도 포케 볼": 2, "시원한 냉모밀 & 초밥 세트": 2
            })
        ]
    },
    {
        "q": "4. 오늘 가장 당기는 주재료(탄수화물/메인)는?",
        "options": [
            ("한국인은 역시 든든한 밥심!", {
                "얼큰 돼지김치찌개 & 솥밥": 3, "뜨끈하고 진한 돼지국밥": 3,
                "숯불 직화 제육덮밥": 3, "고슬고슬 중화 새우볶음밥": 4, "연어 아보카도 포케 볼": 1
            }),
            ("후루룩 넘어가는 면이나 쫄깃한 떡·당면", {
                "진한 육수의 돈코츠 라멘": 4, "내 맘대로 골라 담는 마라탕": 3,
                "쉬림프 알리오올리오 & 파스타": 3, "로제 떡볶이 & 모둠튀김": 3, "시원한 냉모밀 & 초밥 세트": 3
            }),
            ("폭신한 빵이나 고기·튀김 위주!", {
                "통통 에그 베이컨 샌드위치": 4, "더블 치즈 수제버거 세트": 3,
                "바삭 꾸덕 반반 치킨": 4, "바삭 등심 수제 돈가스": 2
            })
        ]
    },
    {
        "q": "5. 생각 중인 한 끼 예산은 어느 정도인가요?",
        "options": [
            ("1만 원 이하~안팎으로 가성비 좋게!", {
                "통통 에그 베이컨 샌드위치": 3, "뜨끈하고 진한 돼지국밥": 3,
                "고슬고슬 중화 새우볶음밥": 3, "숯불 직화 제육덮밥": 2, "얼큰 돼지김치찌개 & 솥밥": 2
            }),
            ("1만 원대 초중반의 만족스러운 식사", {
                "진한 육수의 돈코츠 라멘": 3, "내 맘대로 골라 담는 마라탕": 3,
                "바삭 등심 수제 돈가스": 2, "더블 치즈 수제버거 세트": 2, "연어 아보카도 포케 볼": 2
            }),
            ("오늘은 기분 내며 조금 넉넉하게!", {
                "바삭 꾸덕 반반 치킨": 4, "쉬림프 알리오올리오 & 파스타": 3,
                "시원한 냉모밀 & 초밥 세트": 3, "로제 떡볶이 & 모둠튀김": 2
            })
        ]
    },
    {
        "q": "6. 누구와 함께 식사하시나요?",
        "options": [
            ("내 페이스대로 편하게 혼밥!", {
                "뜨끈하고 진한 돼지국밥": 2, "진한 육수의 돈코츠 라멘": 3,
                "고슬고슬 중화 새우볶음밥": 3, "통통 에그 베이컨 샌드위치": 3,
                "연어 아보카도 포케 볼": 2, "숯불 직화 제육덮밥": 2
            }),
            ("친한 친구·동기와 수다 떨며 나눠 먹기", {
                "바삭 꾸덕 반반 치킨": 4, "로제 떡볶이 & 모둠튀김": 3,
                "내 맘대로 골라 담는 마라탕": 3, "얼큰 돼지김치찌개 & 솥밥": 2
            }),
            ("깔끔하고 기분 내기 좋은 약속 자리", {
                "쉬림프 알리오올리오 & 파스타": 3, "시원한 냉모밀 & 초밥 세트": 3,
                "바삭 등심 수제 돈가스": 2, "더블 치즈 수제버거 세트": 2
            })
        ]
    },
    {
        "q": "7. 식사 후 원하는 컨디션은?",
        "options": [
            ("배 두드리며 묵직하고 확실한 포만감!", {
                "뜨끈하고 진한 돼지국밥": 3, "바삭 꾸덕 반반 치킨": 3,
                "얼큰 돼지김치찌개 & 솥밥": 2, "숯불 직화 제육덮밥": 2, "더블 치즈 수제버거 세트": 2
            }),
            ("기분 좋을 만큼 적당히 든든하게", {
                "고슬고슬 중화 새우볶음밥": 3, "진한 육수의 돈코츠 라멘": 2,
                "바삭 등심 수제 돈가스": 2, "내 맘대로 골라 담는 마라탕": 2, "쉬림프 알리오올리오 & 파스타": 2
            }),
            ("식곤증 없이 가볍고 산뜻하게!", {
                "통통 에그 베이컨 샌드위치": 4, "연어 아보카도 포케 볼": 4,
                "시원한 냉모밀 & 초밥 세트": 2
            })
        ]
    },
    {
        "q": "8. 지금 입안에서 원하는 식감은?",
        "options": [
            ("바삭바삭한 튀김이나 불향 입힌 식감!", {
                "바삭 꾸덕 반반 치킨": 4, "바삭 등심 수제 돈가스": 4,
                "고슬고슬 중화 새우볶음밥": 2, "숯불 직화 제육덮밥": 2
            }),
            ("쫄깃탱글하거나 진하게 감기는 식감", {
                "내 맘대로 골라 담는 마라탕": 3, "진한 육수의 돈코츠 라멘": 3,
                "로제 떡볶이 & 모둠튀김": 3, "뜨끈하고 진한 돼지국밥": 2
            }),
            ("아삭아삭 신선하고 폭신한 식감", {
                "통통 에그 베이컨 샌드위치": 3, "연어 아보카도 포케 볼": 3,
                "시원한 냉모밀 & 초밥 세트": 2, "더블 치즈 수제버거 세트": 2
            })
        ]
    },
    {
        "q": "9. 식사 시간 여유는 얼마나 있나요?",
        "options": [
            ("바쁘다 바빠! 빠르고 간편하게 먹을래요", {
                "통통 에그 베이컨 샌드위치": 4, "고슬고슬 중화 새우볶음밥": 3,
                "더블 치즈 수제버거 세트": 3, "뜨끈하고 진한 돼지국밥": 2
            }),
            ("보통의 식사 시간 (30~40분 정도)", {
                "진한 육수의 돈코츠 라멘": 2, "얼큰 돼지김치찌개 & 솥밥": 2,
                "숯불 직화 제육덮밥": 2, "바삭 등심 수제 돈가스": 2, "연어 아보카도 포케 볼": 2
            }),
            ("여유롭게 이야기 나누며 천천히 즐길래요", {
                "바삭 꾸덕 반반 치킨": 4, "쉬림프 알리오올리오 & 파스타": 3,
                "내 맘대로 골라 담는 마라탕": 2, "로제 떡볶이 & 모둠튀김": 2
            })
        ]
    },
    {
        "q": "10. 오늘 내 기분에 가장 가까운 단어는?",
        "options": [
            ("위로가 필요한 날, 익숙하고 푸근한 맛", {
                "뜨끈하고 진한 돼지국밥": 3, "얼큰 돼지김치찌개 & 솥밥": 3,
                "고슬고슬 중화 새우볶음밥": 2, "숯불 직화 제육덮밥": 2
            }),
            ("도파민 충전! 스트레스 날리는 강렬한 맛", {
                "내 맘대로 골라 담는 마라탕": 3, "바삭 꾸덕 반반 치킨": 3,
                "로제 떡볶이 & 모둠튀김": 3, "더블 치즈 수제버거 세트": 2
            }),
            ("리프레시! 깔끔하고 기분 전환되는 맛", {
                "통통 에그 베이컨 샌드위치": 2, "연어 아보카도 포케 볼": 3,
                "쉬림프 알리오올리오 & 파스타": 3, "시원한 냉모밀 & 초밥 세트": 3, "진한 육수의 돈코츠 라멘": 2
            })
        ]
    }
]


# ==========================================
# 5. 메인 화면 구성 (헤더 및 진행률)
# ==========================================
st.markdown("""
<div class="menu-header">
    <h1>🍽️ 오늘의 차림표 결정소</h1>
    <p>10가지 주문서 항목에 체크해 주시면, 14가지 인기 메뉴 중 딱 맞는 한 끼를 내어드립니다!</p>
</div>
""", unsafe_allow_html=True)

# 진행률 표시를 위한 상단 공간 예약
progress_container = st.container()

st.markdown("### 📝 손님 주문서 작성")
st.caption("각 질문마다 가장 마음에 드는 보기를 하나씩 골라주세요.")

# 사용자의 선택 결과를 저장할 리스트
user_answers = []

# 10개의 질문을 식당 주문서 카드 형태로 출력
for idx, item in enumerate(QUESTIONS):
    st.markdown(f'<div class="order-card"><div class="question-title">{item["q"]}</div></div>', unsafe_allow_html=True)
    option_labels = [opt[0] for opt in item["options"]]

    # index=None 으로 설정해 처음에는 아무것도 선택되지 않게 함
    choice = st.radio(
        label=item["q"],
        options=option_labels,
        index=None,
        key=f"q_{idx}_{st.session_state.run_id}",
        label_visibility="collapsed"
    )
    user_answers.append(choice)
    st.write("")  # 질문 사이 여백

# ==========================================
# 6. 전체 응답 진행률 실시간 계산 및 표시
# ==========================================
answered_count = sum(1 for ans in user_answers if ans is not None)
total_questions = len(QUESTIONS)
progress_ratio = answered_count / total_questions

with progress_container:
    st.markdown(f"**📋 주문서 작성 진행률: {answered_count} / {total_questions} 완료 ({int(progress_ratio * 100)}%)**")
    st.progress(progress_ratio)
    st.divider()


# ==========================================
# 7. 결과 확인 버튼 및 추천 메뉴 출력
# ==========================================
st.divider()

# 결과 확인 후 답변을 다시 변경한 경우, 다시 '결과 확인' 버튼을 누르도록 초기화
if st.session_state.show_result and user_answers != st.session_state.submitted_answers:
    st.session_state.show_result = False

if answered_count < total_questions:
    # 아직 모든 질문에 답하지 않은 경우: 안내 문구 + 비활성화된 결과 확인 버튼 표시
    st.session_state.show_result = False
    st.info(f"👆 아직 선택하지 않은 항목이 **{total_questions - answered_count}개** 남아 있어요. 모든 항목을 선택한 뒤 아래 결과 확인 버튼을 눌러주세요!")
    st.button(
        "🍽️ 결과 확인하기 (모든 질문을 먼저 선택해 주세요)",
        disabled=True,
        use_container_width=True
    )
else:
    # 모든 질문에 답한 경우: 결과 확인 버튼 활성화
    if not st.session_state.show_result:
        st.success("✅ 10가지 주문서 항목을 모두 선택하셨습니다! 아래 버튼을 눌러 추천 메뉴를 확인해 보세요.")
        if st.button("🍽️ 결과 확인하기", use_container_width=True, type="primary"):
            st.session_state.show_result = True
            st.session_state.submitted_answers = list(user_answers)
            st.session_state.just_submitted = True
            st.rerun()

# '결과 확인하기' 버튼을 눌렀을 때만 결과 화면 표시
if st.session_state.show_result and answered_count == total_questions:
    # 모든 메뉴 점수를 0점으로 초기화
    scores = {menu: 0 for menu in MENU_DATA.keys()}

    # 선택한 답변에 따라 메뉴별 가중치 점수 합산
    for idx, selected_label in enumerate(user_answers):
        for opt_label, weights in QUESTIONS[idx]["options"]:
            if opt_label == selected_label:
                for menu_name, point in weights.items():
                    scores[menu_name] += point

    # 점수가 높은 순서대로 정렬
    sorted_menus = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_menu_name, best_score = sorted_menus[0]
    best_menu_info = MENU_DATA[best_menu_name]

    # 버튼을 방금 눌렀을 때만 풍선 애니메이션 실행
    if st.session_state.just_submitted:
        st.balloons()
        st.session_state.just_submitted = False

    st.subheader("🔔 주문하신 추천 메뉴 나왔습니다!")

    # 대표 추천 메뉴 + 귀여운 SVG 그림 카드 출력
    st.markdown(f"""
    <div class="result-board">
        <div class="badge">{best_menu_info['tag']}</div>
        <div>{best_menu_info['svg']}</div>
        <div class="menu-name">“ {best_menu_name} ”</div>
        <div class="menu-desc">{best_menu_info['desc']}</div>
        <div class="side-tip">🥢 {best_menu_info['side']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # 차선책 메뉴 (2위, 3위) 및 상위 5개 점수 비교 표시
    with st.expander("📖 혹시 이 메뉴가 안 당기시나요? (차선책 차림표 보기)"):
        second_menu, _ = sorted_menus[1]
        third_menu, _ = sorted_menus[2]
        st.write(f"**🥈 2순위 추천:** {second_menu} — *{MENU_DATA[second_menu]['tag']}*")
        st.write(f"**🥉 3순위 추천:** {third_menu} — *{MENU_DATA[third_menu]['tag']}*")
        st.caption("내 취향 적합도 상위 5개 메뉴 점수 비교")
        chart_data = {name: score for name, score in sorted_menus[:5]}
        st.bar_chart(chart_data)

    st.write("")

    # ==========================================
    # 8. 다시 검사하기(주문서 새로 쓰기) 버튼
    # ==========================================
    if st.button("🔄 주문서 새로 쓰기 (다시 검사하기)", use_container_width=True, type="primary"):
        st.session_state.run_id += 1
        st.session_state.show_result = False
        st.session_state.submitted_answers = None
        st.session_state.just_submitted = False
        st.rerun()
