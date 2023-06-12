import streamlit as st
from streamlit_chat import message
from . import chatbot as bot

def chat():

    '''
    st.text_input('input : ', key='input_texts')
    if st.session_state.input_texts:
        res_obj = bot.ChatbotMessageSender()
        res = res_obj.req_message_send(st.session_state.input_texts)

        if(res.status_code == 200):
            #print(res.text)
            dict_res = res.json()
            message(dict_res['bubbles'][0]['data']['description'])
    '''
    if 'past' not in st.session_state:  # 내 입력채팅값 저장할 리스트
        st.session_state['past'] = []

    if 'generated' not in st.session_state:  # 챗봇채팅값 저장할 리스트
        st.session_state['generated'] = []

    placeholder = st.empty()
    # 채팅 입력창을 아래위치로 내려주기위해 빈 부분을 하나 만듬

    with st.form('form', clear_on_submit=True):  # 채팅 입력창 생성
        user_input = st.text_input('당신: ', '')  # 입력부분
        submitted = st.form_submit_button('전송')  # 전송 버튼

    if submitted and user_input:
        user_input1 = user_input.strip()  # 채팅 입력값 및 여백제거

        res = bot.ChatbotMessageSender().req_message_send(user_input1)
        print('대화입력-----')
        print(res.json())

        res_type= res.json()['bubbles'][0]['type']





        chatbot_output1 = res.json()['bubbles'][0]['data']['description']
        #chatbot_output1 = res.json()['bubbles'][0]
        st.session_state.past.append(user_input1)
        # 입력값을 past 에 append -> 채팅 로그값 저장을 위해

        st.session_state.generated.append(chatbot_output1)

    with placeholder.container():
        # 리스트에 append된 채팅입력과 로봇출력을 리스트에서 꺼내서 메세지로 출력
        for i in range(len(st.session_state['past'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            if len(st.session_state['generated']) > i:
                message(st.session_state['generated'][i], key=str(i) + '_bot')