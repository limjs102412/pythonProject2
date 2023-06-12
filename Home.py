import streamlit as st
from streamlit_option_menu import option_menu
from Diagnosing_eye import Diagnosing_eye_page
from member.service import MemberService
from Signup import signup_page
from Login_Logout import login_page
from Mypage import Mypage_page
from Write_life import Daylist_page
import About
from guide_Hospital import Hospital_page
from pet.petsv import PetService
from AI_Chatbot import AI_Chatbot_page

class Home_page:
    def __init__(self):
        self.signup=signup_page()
        self.login=login_page()
        self.service=MemberService()
        self.Mypage = Mypage_page()
        self.Daylist=Daylist_page()
        self.eye=Diagnosing_eye_page()
        self.hospital=Hospital_page()
        self.petsv=PetService()
        self.aichat=AI_Chatbot_page()

    # 사이드바 설정
    def main(self,choose=None):
        # 로그인이 안된 경우, 사이드바에 '로그인' 출력
        if self.service.login_user(print1=False,print2=False) == '':
            login_logout = '로그인'
        # 로그인된 경우, 사이드바에 '로그아웃' 출력
        else:
            login_logout = '로그아웃'

        # 사이드바
        menu = ["홈", "회원가입", "마이페이지", login_logout]
        if choose == menu[0]:
            self.bar()
        if choose == menu[1]:
            self.signup.run()
        if choose == menu[3]:
            self.login.run()
        if choose == menu[2]:
            self.Mypage.run()

    # 사이드바 '홈' 상단 및 네비게이션바 설정
    def bar(self):
        col, col1, col2,col3 = st.columns([2, 3, 1.5,1])
        # 상단 중앙: 로고
        with col1:
            st.markdown('## 냥이의 하루, 안냥:cat:')
        # 상단 오른쪽: 반려묘 선택
        with col3:
            self.petsv.printMyCat(print1=False)

        st.write('#')
        # 사이드바 홈 안의 네비게이션바 설정
        nav = ["About", "안구질환 진단", "일지 쓰기", "AI 챗봇",  "동물병원 위치"]
        select = option_menu(None, nav,
                             icons=['house', 'camera fill', 'book', 'bi-chat-dots',  'hospital'],
                             default_index=0,
                             styles={
                                 "container": {"padding": "5!important", "background-color": "#fafafa"},
                                 "icon": {"color": "orange", "font-size": "25px"},
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                              "--hover-color": "#eee"},
                                 "nav-link-selected": {"background-color": "#02ab21"}
                             }, orientation="horizontal"
                             )
        # 네비게이션바
        if select == nav[0]:
            About.About_page()
        if select == nav[1]:
            self.eye.diagnosing_eye_page()
        if select == nav[2]:
            self.Daylist.run()
        if select == nav[3]:
            self.aichat.run()
        if select == nav[4]:
            self.hospital.run()

    def run(self):
        # 웹 설정
        st.set_page_config(
            page_title='냥이의 하루, 안냥 ',
            page_icon=':cat:',
            layout='wide',  # wide,centered
            menu_items={
                'Get Help': 'https://lc.multicampus.com/k-digital/#/login',  # 페이지로 이동하기
                'About': '### 대박징조의 *반려묘의 안구질환 진단 및 하루 기록 서비스* 입니다.'
            },
            initial_sidebar_state='expanded'
        )
        # 사이드바
        # 로그인이 안된 경우, 사이드바에 '로그인' 출력
        if self.service.login_user(print1=False,print2=False) == '':
            login_logout = '로그인'
        # 로그인된 경우, 사이드바에 '로그아웃' 출력
        else:
            login_logout = '로그아웃'
        # 메뉴
        menu = ["홈", "회원가입",  "마이페이지",login_logout]

        # 사이드바
        with st.sidebar:
            self.service.login_user()
            choose = option_menu("", menu,
                                 icons=['house', 'bi-clipboard-check', 'gear','person lines fill' ],
                                  default_index=0
                                 )
        # 네비게이션바에 선택된 페이지 출력
        self.main(choose)


if __name__== '__main__':
    m=Home_page()
    m.run()
