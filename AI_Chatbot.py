import streamlit as st
from utils.chatbot_desc import chat
from member.service import MemberService
class AI_Chatbot_page():
    # AI 챗봇 페이지
    # 설명 부분
    def __init__(self):
        self.service=MemberService()
    def run(self):
        if MemberService.loginId=="":
            st.error('로그인 먼저 하세요', icon="🚨")
        else:
            st.subheader('냥박사와 채팅하기')
            st.info("""안녕하세요! 안냥의 든든한 AI 챗봇 냥박사입니다! 저와 같이 대화해요!""")
            expander = st.expander("어떤 질문을 할 수 있나요? : 냥박사 질문 가이드")
            expander.write("""🐾 먼저 '안녕'으로 대화를 시작해보세요!
                       \n   냥박사와 대화를 하면서 다양한 정보를 알아볼 수 있답니다. \n
                            
                       \n👉 고양이 질환을 알고 싶다면 : "고양이 질환 알려줘"로 검색해보세요! \n 
                       \n👉 고양이 건강 상식을 알고 싶다면 : "고양이 건강 상식 알려줘"로 검색해보세요! \n 
                       \n👉 고양이 묘종 사전을 알고 싶다면 : "묘종사전 알려줘"로 검색해보세요! \n
                            
                       \n👉 그 외 친화력 좋은 묘종, 고양이 언어 등을 알 수 있습니다! \n
                       \n '친화력 좋은 묘종을 알려줘' '고양이가 골골거렸어' 등등 다양한 말을 건네보세요!\n  """)

if __name__=='__main__':
    m=AI_Chatbot_page()
    m.run()
