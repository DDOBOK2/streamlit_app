import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import random
import re

# CSV 파일에서 데이터를 로드하고 분석하는 함수
def get_menu_message(file_path, today):
    df = pd.read_csv(file_path)
    menu_today = df[df['급식일자'] == int(today.strftime('%Y%m%d'))]['요리명'].values
    if len(menu_today) > 0:
        dishes = menu_today[0].split('<br/>')
        if len(dishes) > 2:
            selected_dish = random.choice(dishes[1:3]).strip()  # 두 번째와 세 번째 요리명에서 랜덤 선택
            selected_dish_cleaned = re.sub(r'\s*\(.*?\)\s*', '', selected_dish)
            return f"OOO 님 안녕하세요, {selected_dish_cleaned} 맛있게 드셨나요?"
        else:
            return "오늘의 두 번째 또는 세 번째 메뉴 정보를 찾을 수 없습니다."
    else:
        return "오늘의 메뉴 정보를 찾을 수 없습니다."
    
def get_timetable_message(file_path, today):
    df = pd.read_csv(file_path)
    timetable_today = df[df['시간표일자'] == int(today.strftime('%Y%m%d'))]
    if not timetable_today.empty:
        # '수업내용' 열에서만 랜덤하게 선택
        subjects = timetable_today['수업내용'].values
        selected_subject = random.choice(subjects).strip()
        return f" OOO 님, 오늘 {selected_subject} 수업은 어땠나요?"
    else:
        return "오늘의 시간표 정보를 찾을 수 없습니다."
    
# 캐릭터 이미지와 말풍선 표시를 위한 HTML 코드 생성
def get_img_with_hover_markdown(file_path, message):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    img_format = "image/png"
    html_code = f"""
    <style>
    .character-container {{
        position: fixed;
        bottom: 10vh;
        left: 10px;
        z-index: 10000;
        display: flex;
        align-items: flex-end;
    }}
    .character-container img {{
        width: 200px;
        cursor: pointer;
    }}
    .speech-bubble {{
        position: relative;
        background: white;
        border-radius: 0.4em;
        padding: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        margin-left: 10px;
        font-size: 1.2em;
        cursor: pointer;
    }}
    .speech-bubble:after {{
        content: '';
        position: absolute;
        bottom: 10px;
        left: -20px;
        width: 0;
        height: 0;
        border: 10px solid transparent;
        border-right-color: white;
        border-left: 0;
        border-bottom: 0;
        margin-top: -5px;
        margin-left: -10px;
    }}
    .menu {{
        display: none;
        position: absolute;
        top: -100px;
        left: 20px;
        background: white;
        border-radius: 0.4em;
        padding: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }}
    .menu a {{
        display: block;
        margin: 5px 0;
        color: black;
        text-decoration: none;
        font-size: 1em;
    }}
    .menu a:hover {{
        text-decoration: underline;
    }}
    </style>
    <div class="character-container">
        <img src="data:{img_format};base64,{encoded_string}" onclick="showMenu()">
        <div class="speech-bubble" onclick="showMenu()">
            <span id="message">{message}</span>
            <div id="menu" class="menu">
                <a href="#" onclick="selectMenu('문제은행')">문제은행</a>
                <a href="#" onclick="selectMenu('AI 출제')">AI 출제</a>
                <a href="#" onclick="selectMenu('학급관리')">학급관리</a>
                <a href="#" onclick="selectMenu('통계')">통계</a>
            </div>
        </div>
    </div>
    <script>
    function showMenu() {{
        var menu = document.getElementById("menu");
        if (menu.style.display === "none" || menu.style.display === "") {{
            menu.style.display = "block";
        }} else {{
            menu.style.display = "none";
        }}
    }}
    function selectMenu(menu) {{
        var message = document.getElementById("message");
        message.innerHTML = menu + "으로 이동합니다...";
        setTimeout(function() {{
            window.location.href = window.location.origin + window.location.pathname + "#" + menu;
        }}, 1000);
    }}
    </script>
    """
    return html_code

# 페이지 설정
st.set_page_config(layout="wide")

# 현재 날짜
today = datetime.now()

# CSV 파일 경로
food_file_path = 'food.csv'
timetable_file_path = 'timetable.csv'

# 랜덤으로 음식 메뉴 또는 시간표 메시지를 선택
if random.choice([True, False]):
    message = get_menu_message(food_file_path, today)
else:
    message = get_timetable_message(timetable_file_path, today)

# 캐릭터 이미지와 말풍선 표시
st.markdown(get_img_with_hover_markdown("IMG_1459.PNG", message), unsafe_allow_html=True)

# 상단 메뉴 생성
menu = ["문제은행", "AI 출제", "학급관리", "통계"]
choice = st.selectbox("메뉴 선택", menu, index=0)

# 각 메뉴에 대한 내용
if choice == "문제은행":
    st.header("문제은행")
    st.write("문제은행 화면의 내용")
    st.write("""
    - 문제 생성하기: 학년, 과목, 단원을 선택하고 문제 유형과 난이도를 설정합니다.
    - 문제 미리보기: 생성된 문제를 미리 보고 검토할 수 있습니다.
    - 문제 배포하기: 완성된 문제를 학급에 배포합니다. 온라인 배포 또는 종이 문서 인쇄 옵션이 있습니다.
    """)
    st.table({
        '학년/학기': ['6학년/1학기'],
        '과목': ['국어'],
        '출제범위': ['1. 대화와 공감\n2. 작품을 감상해요'],
        '출제 유형': ['선택형, 서답형'],
        '문제 수': ['25개'],
        '난이도': ['상: 20%, 중: 50%, 하: 30%']
    })
elif choice == "AI 출제":
    st.header("AI 출제")
    st.write("AI 출제 화면의 내용")
    st.write("""
    - AI 출제 기능: AI를 이용하여 자동으로 문제를 출제합니다. 학년, 과목, 단원을 선택하고 AI 출제 방식을 설정합니다.
    - AI 출제 미리보기: AI가 출제한 문제를 미리 보고 검토할 수 있습니다.
    - AI 문제 배포: AI가 출제한 문제를 학급에 배포합니다. 학생별 맞춤형 문제 제공이 가능합니다.
    """)
    st.bar_chart({
        '대화와 공감': [75],
        '작품을 감상해요': [65],
        '글을 요약해요': [80],
        '글쓰기의 과정': [70],
        '글쓴이의 주장': [90]
    })
elif choice == "학급관리":
    st.header("학급관리")
    st.write("학급관리 화면의 내용")
    st.write("""
    - 학급 정보 관리: 학급 정보를 관리합니다. 학년, 반, 학생 수 등을 설정하고 학생 목록을 관리합니다.
    - 학급 코드 생성: 학급 코드를 생성하여 학생들이 접속할 수 있도록 합니다.
    - 학생 추가/삭제: 학생을 추가하거나 삭제할 수 있습니다. 학급 코드와 번호를 입력하여 관리합니다.
    """)
    st.table({
        '학년': ['6학년'],
        '반': ['1반'],
        '학생 수': ['30명'],
        '학급 코드': ['a54321']
    })
elif choice == "통계":
    st.header("통계")
    st.write("통계 화면의 내용")
    st.write("""
    - 학급 통계: 학급 전체의 평가 결과를 통계적으로 분석합니다. 과목별 평균 점수와 평가 횟수를 확인할 수 있습니다.
    - 학생별 통계: 각 학생의 평가 결과를 통계적으로 분석합니다. 학생별 성적 추이를 확인할 수 있습니다.
    - AI 통계: AI 출제 문제의 결과를 분석합니다. 문제 유형별, 난이도별 정답률을 확인할 수 있습니다.
    """)
    st.line_chart({
        '평가 1': [85, 75],
        '평가 2': [80, 78],
        '평가 3': [78, 85],
        '평가 4': [88, 82],
        '평가 5': [90, 79]
    }, width=0, height=400)

