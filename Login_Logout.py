import streamlit as st
from member.service import MemberService

class login_page:
    # 로그인 페이지
    def __init__(self):
        self.service=MemberService()

    def run(self):
        # 레이아웃 설정
        col1, col2, col3 = st.columns([2, 1, 2])
        col2.subheader('로그인 🐱')
        # 레이아웃 설정 : 입력부분
        col4, col5, col6 = st.columns([1, 2, 1])
        # 로그인 기능
        with col5:
            if self.service.login_user(print1=False,print2=False)=='':
                login_id = st.text_input('아이디', placeholder='아이디를 입력하세요')
                login_pw = st.text_input('패스워드',placeholder='패스워드를 입력하세요', type='password')
                login_btn = st.button('로그인하기')
                if login_btn:
                    self.service.login(login_id, login_pw)
            else:
                self.service.logout()

if __name__ == '__main__':
    m = login_page()
    m.run()