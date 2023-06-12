import streamlit as st
from member.service import MemberService


class signup_page:
    # 회원가입 페이지
    def __init__(self):
        self.servise=MemberService()

    def run(self):
        global check1
        # 레이아웃 설정
        col1,col2,col3=st.columns([2,1,2])
        # 중앙
        col2.subheader('회원가입 📝')

        # 레이아웃 설정
        col4, col5, col6 = st.columns([1, 2, 1])
        # 중앙: 입력란
        col5.info('다음 양식을 모두 입력 후 제출합니다.')
        input_id = col5.text_input('아이디', max_chars=15)
        input_pwd = col5.text_input('비밀번호', type='password')
        input_pwd2 = col5.text_input('비밀번호 확인', type='password')
        checkbtn = col5.button('확인')
        # 비밀번호, 비밀번호 확인이 일치한지 검사
        if checkbtn:
            if input_pwd != input_pwd2:
                col5.error('비밀번호가 다릅니다. 다시 입력해주세요', icon="🚨")
                check1 = 0
            elif input_pwd=='':
                col5.error('비밀번호를 입력하세요', icon="🚨")
                check1=0
            else:
                col5.success('확인되었습니다.', icon="✅")
                check1=1
        input_name = col5.text_input('닉네임', max_chars=45)
        input_email = col5.text_input('이메일', max_chars=100)
        input_phone = col5.text_input('전화번호', max_chars=20)
        submitted=col5.button('회원가입하기')
        # 회원가입하기 버튼 클릭시 회원가입 기능
        if submitted:
            # 비밀번호확인버튼 클릭한 경우
            if check1==1:
                self.servise.addMember(input_id,input_pwd,input_name,input_email,input_phone)
                col5.success(f'{input_id}님,환영합니다! 로그인해주세요.', icon="✅")
            # 비밀번호확인버튼 클릭하지 않은 경우
            elif check1==0:
                col5.error('비밀번호 확인버튼을 클릭해주세요', icon="🚨")
            else:
                col5.write('error')
if __name__=='__main__':
    m=signup_page()
    m.run()






