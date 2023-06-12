import streamlit as st
from member.service import MemberService
from pet.petsv import PetService
import sqlite3

class Mypage_page:
    # 마이페이지

    def __init__(self):
        self.service=MemberService()
        self.petsv=PetService()

    def run(self):
        # 레이아웃 설정
        col4, col5, col6 = st.columns([1, 2, 1])
        # 중앙
        with col5:
            st.title('냥이의 하루, 안냥:cat:')
        # 오른쪽: 로그인된 사용자의 닉네임 출력
        with col6:
            st.write('#')
            self.service.login_user(print2=False)

        # 레이아웃 설정
        col1, col2, col3 = st.columns([1, 3, 1])
        # 중앙
        with col2:
            # 탭 설정
            tab1, tab2, tab3 = st.tabs(['회원정보', '반려묘 등록', '반려묘 정보'])

            # 회원정보 탭
            with tab1:
                st.subheader('회원 정보')
                # 로그인된 사용자만 이용 가능
                if MemberService.loginId == '':
                    st.error('로그인하고 이용하세요')
                    return
                # 정상
                else:
                    con = sqlite3.connect('mydb.db')
                    cur = con.cursor()
                    cur.execute(f'select * from User where User_Id="{MemberService.loginId}"')
                    user_info = cur.fetchone()
                    st.text_input(label="아이디", value=user_info[0], max_chars=15, disabled=True, key=1)
                    st.text_input(label="비밀번호", value=user_info[1], max_chars=20, disabled=True, key=2)
                    input_name = st.text_input(label='닉네임',  value=user_info[2], max_chars=45, key=3)
                    input_email = st.text_input(label='이메일',  value=user_info[3], max_chars=100, key=4)
                    input_phone = st.text_input(label='전화번호',  value=user_info[4], max_chars=20, key=5)
                    modifybtn = st.button('수정')
                    if modifybtn:
                        con = sqlite3.connect('mydb.db')
                        cur = con.cursor()
                        sql = 'update User set User_Name=?, User_Email=?, User_Phone=? where User_Id=?'
                        d = (input_name,input_email,input_phone,MemberService.loginId)
                        cur.execute(sql,d)
                        con.commit()
                        cur.close()
                        con.close()
                        return st.success('수정 완료되었습니다.', icon="✅")
                    st.subheader('회원 탈퇴')
                    delbtn=st.button("탈퇴")

                    if delbtn:
                        self.service.delMember(MemberService.loginId)



            with tab2:
                st.subheader('반려묘 등록')
                st.info('다음 양식을 모두 입력 후 제출합니다.')
                input_Name = st.text_input('반려묘 이름', max_chars=45)
                input_Age = st.number_input('반려묘 나이', value=1, min_value=1, step=1)
                input_Num = st.text_input('반려묘 등록번호', max_chars=20)
                input_Kind = st.text_input('반려묘 종', max_chars=20)
                input_Gender = st.text_input('반려묘 성별', max_chars=5)
                state= st.radio(
                    "고양이의 현재 상태를 선택해주세요",
                    ('집중 치료중/병원 입원중', '저체중/비만', '과체중 경향/활동적은','중성화를 했으며, 보통활동량','중성화를 하지 않았으며, 보통활동량','임신중','수유중','새끼 고양이'))
                if state=='집중 치료중/병원 입원중':
                    input_State=0
                elif state=='저체중/비만':
                    input_State=1
                elif state=='과체중 경향/활동적은':
                    input_State=2
                elif state=='중성화를 했으며, 보통활동량':
                    input_State=3
                elif state=='중성화를 하지 않았으며, 보통활동량':
                    input_State=4
                elif state=='임신중':
                    input_State=5
                elif state=='수유중':
                    input_State=6
                elif state=='새끼 고양이':
                    input_State=7
                input_Eatkacl = st.number_input('먹이는 사료칼로리(kcal/kg)', value=1, min_value=1, step=1)
                submitted = st.button('반려묘 등록하기')
                if submitted:
                    if MemberService.loginId == '':
                        st.write('로그인하고 이용하세요')
                    else:
                        self.petsv.addCat(MemberService.loginId, input_Name, input_Age, input_Num, input_Kind, input_Gender,input_State,input_Eatkacl)
                        st.success(f'{input_Name} 등록되었습니다', icon="✅")

            with tab3:
                if MemberService.loginId == '':
                    st.write('로그인 먼저 하세요')
                    return
                else:
                    st.subheader('반려묘 정보')
                    mycat=self.petsv.printMyCat()
                    if mycat:
                        cat_info = self.petsv.printCatInfo(MemberService.loginId, mycat)
                        st.text_input(label="아이디", value=cat_info[0], max_chars=15, disabled=True)
                        st.text_input(label="반려묘 등록번호", value=cat_info[3], max_chars=15, disabled=True)
                        input_catname = st.text_input(label="반려묘 이름", value=cat_info[1], max_chars=45, key=6)
                        input_catage = st.number_input(label="반려묘 나이", value=cat_info[2], min_value=1, step=1, key=7)
                        input_catkind = st.text_input(label="반려묘 종", value=cat_info[4], max_chars=20, key=8)
                        input_catgender = st.text_input(label="반려묘 성별", value=cat_info[5], max_chars=5, key=9)
                        input_catstate=st.radio(label="고양이의 현재 상태를 선택해주세요",options=('집중 치료중/병원 입원중', '저체중/비만', '과체중 경향/활동적은','중성화를 했으며, 보통활동량','중성화를 하지 않았으며, 보통활동량','임신중','수유중','새끼 고양이'),
                                                index=int(cat_info[6]))

                        input_cateatkcal = st.number_input(label="먹이는 사료칼로리(kcal/kg)", value=cat_info[7], min_value=1, step=1, key=10)
                        editted = st.button('수정하기')
                        if editted:
                            self.petsv.UpdateCat(MemberService.loginId, cat_info[3], input_catage, input_catname, input_catkind, input_catgender,input_catstate,input_cateatkcal)
                        st.subheader('반려묘 삭제')
                        if st.button('삭제하기'):
                            self.petsv.delete_Cat(MemberService.loginId, mycat)
                    else:
                        st.error('반려묘 등록하세요')



if __name__ == '__main__':
    m = Mypage_page()
    m.run()
