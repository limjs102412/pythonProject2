import datetime
from member.service import MemberService
from pet.petsv import PetService
from daylist.daylistsv import DaylistService
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
class Daylist_page:
    # 일지쓰기 페이지
    def __init__(self):
        self.service=MemberService()
        self.petsv=PetService()
        self.daylistsv=DaylistService()

    def check(daylistinfo):
        if daylistinfo == 'False' or False:
            return 0
        else:
            return 1

    # 고양이정보와 몸무게, 사료칼로리를 이용하여 권장량 계산하는 함수
    def recommend(self,info,weight,kcal):
        # 활동지수
        activity_score=0
        if info=='0':
            activity_score=1.0
        elif info=='1':
            activity_score = 0.9
        elif info=='2':
            activity_score = 1.0
        elif info=='3':
            activity_score = 1.2
        elif info=='4':
            activity_score = 1.4
        elif info=='5':
            activity_score = 2.5
        elif info=='6':
            activity_score = 4
        elif info=='7':
            activity_score = 2.5
        # 기초대사량 2kg미만: rer=70*(weight*0.75)
        # 2kg이상 : rer=30*weight +70
        if weight<2:
            rer=70*(weight*0.75)
        else:
            rer=30*weight+70
        # 하루 필요 칼로리: rer*activity_score
        mer=rer * activity_score
        # 하루 급여량(g)=mer *1000/사료칼로리(kcal/kg)
        recommend=mer * 1000 / kcal
        return recommend


    def run(self):
        # 시각화 한글사용
        plt.rcParams['axes.unicode_minus'] = False
        if platform.system() == 'Darwin':  # 맥OS
            rc('font', family='AppleGothic')
        elif platform.system() == 'Windows':  # 윈도우
            path = "c:/Windows/Fonts/malgun.ttf"
            font_name = font_manager.FontProperties(fname=path).get_name()
            rc('font', family=font_name)
        else:
            print('Unknown system...  sorry~~~')

        # 로그인한 사용자의 고양이 등록확인
        self.petsv.printMyCat(print2=False)
        # 로그인한 사용자가 지정한 고양이 이름 불러오기
        mycat=PetService.loginCatName
        # 로그인되어 있지 않은 경우
        if MemberService.loginId=="":
            return
        # 등록한 고양이가 없는 경우
        elif mycat=="":
            st.error('마이페이지에서 반려묘를 등록해주세요')
        # 정상
        else:
            st.subheader(f'{mycat}의 일지 📝')
            # 탭 스타일변경 및 설정
            font_css = """
            <style>
            button[data-baseweb="tab"]   {
              background: #EAEAEA55;
            }
            </style>
            """
            st.write(font_css, unsafe_allow_html=True)
            listtabs=["오늘의 일지 작성","일지 보기","통계보기"]
            whitespace = 15
            tabs = st.tabs([s.center(whitespace, "\u2001") for s in listtabs])

            # 오늘의 일지 작성 탭
            with tabs[0]:
                # 사용자가 지정한 고양이의 정보 불러오기
                cat_info = self.petsv.printCatInfo(MemberService.loginId, mycat)
                # 오늘의 날짜 불러오기
                now = datetime.datetime.now()
                year = int(now.strftime('%Y'))
                month = int(now.strftime('%m'))
                day = int(now.strftime('%d'))
                today = datetime.date(year, month, day)

                #레이아웃 설정
                layout1,layout2,layout3=st.columns([1,5,1])
                # 중앙
                with layout2:
                    # 레이아웃 설정
                    col1,col2,col3=st.columns([1.4,1,1])
                    col2.subheader(today)
                    st.info('다음 양식을 작성하고, 저장하기 버튼을 클릭해주세요')

                    # 지정된 고양이의 오늘의 일지 정보 불러오기
                    daylistinfo = self.daylistsv.printDaylistInfo(cat_info[3], today)
                    # 정보가 있는 경우
                    if daylistinfo:
                        breakfast_food = daylistinfo[2]
                        lunch_food = daylistinfo[3]
                        dinner_food = daylistinfo[4]
                        breakfast_water = daylistinfo[5]
                        lunch_water = daylistinfo[6]
                        dinner_water = daylistinfo[7]
                        weight = daylistinfo[1]
                        playtime = daylistinfo[8]
                        check1 = Daylist_page.check(daylistinfo[9])
                        check2 = Daylist_page.check(daylistinfo[10])
                        check3 = Daylist_page.check(daylistinfo[11])
                        check4 = Daylist_page.check(daylistinfo[12])
                        check5 = Daylist_page.check(daylistinfo[13])
                        check6 = Daylist_page.check(daylistinfo[14])
                        check7 = Daylist_page.check(daylistinfo[15])
                        check8 = Daylist_page.check(daylistinfo[16])
                        check9 = Daylist_page.check(daylistinfo[17])
                        check10 = Daylist_page.check(daylistinfo[18])
                        memo = daylistinfo[19]
                    # 정보가 업는 경우
                    else:
                        breakfast_food = 0
                        lunch_food = 0
                        dinner_food = 0
                        breakfast_water = 0
                        lunch_water = 0
                        dinner_water = 0
                        weight = 0
                        playtime = 0
                        check1 = 0
                        check2 = 0
                        check3 = 0
                        check4 = 0
                        check5 = 0
                        check6 = 0
                        check7 = 0
                        check8 = 0
                        check9 = 0
                        check10 = 0
                        memo = ""

                    # 확장탭 : 몸무게
                    with st.expander('몸무게'):
                        subcol13, subcol14, subcol15 = st.columns([1, 1, 3])
                        input_weight = subcol13.number_input('몸무게', value=int(weight), min_value=0, step=1,label_visibility='collapsed')
                        subcol14.write('')
                        subcol14.write('')
                        subcol14.write('')
                        subcol14.write('kg')
                    # 확장탭 : 놀이시간
                    with st.expander('놀이시간'):
                        subcol13, subcol14, subcol15 = st.columns([1, 1, 3])
                        input_playtime = subcol13.number_input('놀이시간', value=playtime, min_value=0, step=1,label_visibility='collapsed')
                        subcol14.write('')
                        subcol14.write('')
                        subcol14.write('')
                        subcol14.write('hour')
                    # 확장탭 : 사료량
                    with st.expander('사료량'):
                        c_col1, c_col2, c_col3, c_col4, c_col5, c_col6 = st.columns(6)
                        input_breakfast_food = c_col1.number_input('아침사료급여량', value=breakfast_food, min_value=0, step=10)
                        c_col2.write('')
                        c_col2.write('')
                        c_col2.write('')
                        c_col2.write('gram')
                        input_lunch_food = c_col3.number_input('점심사료급여량', value=lunch_food, min_value=0, step=10)
                        c_col4.write('')
                        c_col4.write('')
                        c_col4.write('')
                        c_col4.write('gram')
                        input_dinner_food = c_col5.number_input('저녁사료급여량', value=dinner_food, min_value=0, step=10)
                        c_col6.write('')
                        c_col6.write('')
                        c_col6.write('')
                        c_col6.write('gram')
                    # 확장탭 : 음수량
                    with st.expander('음수량'):
                        c_col1, c_col2, c_col3, c_col4, c_col5, c_col6 = st.columns(6)
                        input_breakfast_water = c_col1.number_input('아침음수량', value=breakfast_water, min_value=0, step=1)
                        c_col2.write('')
                        c_col2.write('')
                        c_col2.write('')
                        c_col2.write('ml')
                        input_lunch_water = c_col3.number_input('점심음수량', value=lunch_water, min_value=0, step=1)
                        c_col4.write('')
                        c_col4.write('')
                        c_col4.write('')
                        c_col4.write('ml')
                        input_dinner_water = c_col5.number_input('저녁음수량', value=dinner_water, min_value=0, step=1)
                        c_col6.write('')
                        c_col6.write('')
                        c_col6.write('')
                        c_col6.write('ml')
                        st.write("")
                    # 확장탭 : 오늘의 특이사항
                    with st.expander('오늘의 특이사항'):
                        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
                        input_ckeck1 = c_col1.checkbox(label="출혈:drop_of_blood:", value=bool(check1))
                        input_ckeck2 = c_col2.checkbox(label="무기력🪫", value=bool(check2))
                        input_ckeck3 = c_col3.checkbox(label="투약💊", value=bool(check3))
                        input_ckeck4 = c_col4.checkbox(label="열🌡", value=bool(check4))
                        input_ckeck5 = c_col5.checkbox(label="목욕🛁", value=bool(check5))
                        st.write("")
                        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
                        input_ckeck6 = c_col1.checkbox(label="귀청소👂", value=bool(check6))
                        input_ckeck7 = c_col2.checkbox(label="병원🩺", value=bool(check7))
                        input_ckeck8 = c_col3.checkbox(label="기분 나쁨😿", value=bool(check8))
                        input_ckeck9 = c_col4.checkbox(label="기분 보통😺", value=bool(check9))
                        input_ckeck10 = c_col5.checkbox(label="기분 좋음😸", value=bool(check10))
                        st.write("")
                        st.write('메모')
                        input_memo = st.text_area('input memo', value=memo, label_visibility="collapsed")
                    savebtn = st.button('저장하기')

                    # 저장하기 버튼 클릭한 경우
                    if savebtn:
                        # 이미 저장된 정보가 있는 경우
                        if self.daylistsv.printDaylistInfo(cat_info[3], today):
                            # 수정
                            self.daylistsv.modifyDaylist(cat_info[3], today, input_weight, input_breakfast_food,
                                                         input_lunch_food, input_dinner_food, input_breakfast_water,
                                                         input_lunch_water, input_dinner_water, input_playtime,
                                                         input_ckeck1, input_ckeck2, input_ckeck3, input_ckeck4,
                                                         input_ckeck5, input_ckeck6, input_ckeck7, input_ckeck8,
                                                         input_ckeck9, input_ckeck10, input_memo)
                        # 저장된 정보가 없는 경우
                        else:
                            # 등록
                            self.daylistsv.addDaylist(cat_info[3], today, input_weight, input_breakfast_food,
                                                      input_lunch_food, input_dinner_food, input_breakfast_water,
                                                      input_lunch_water, input_dinner_water, input_playtime, input_ckeck1,
                                                      input_ckeck2, input_ckeck3, input_ckeck4, input_ckeck5, input_ckeck6,
                                                      input_ckeck7, input_ckeck8, input_ckeck9, input_ckeck10, input_memo)
                            st.success(f'{today}, {mycat}의 일지를 저장합니다.', icon="✅")

            # 일지 보기 탭
            with tabs[1]:
                # 레이아웃 설정
                col1, col2 = st.columns([1, 2], gap='large')
                # 왼쪽 : 날짜선택
                with col1:
                    st.markdown('###### 👇날짜 선택')
                    choose_date = st.date_input('👇날짜 선택', today, label_visibility='collapsed')
                    daylistinfo = self.daylistsv.printDaylistInfo(cat_info[3], choose_date)
                    st.caption('변경시 날짜를 다시 선택해주세요')
                # 오른쪽 : 선택한 날짜에 맞는 정보 출력
                with col2:
                    st.markdown('###### 👇기록 확인')
                    # 선택한 날짜에 맞는 정보가 있는 경우
                    if daylistinfo:
                        breakfast_food_cd = daylistinfo[2]
                        lunch_food_cd = daylistinfo[3]
                        dinner_food_cd = daylistinfo[4]
                        breakfast_water_cd = daylistinfo[5]
                        lunch_water_cd = daylistinfo[6]
                        dinner_water_cd = daylistinfo[7]
                        weight_cd = daylistinfo[1]
                        playtime_cd = daylistinfo[8]
                        check1_cd = Daylist_page.check(daylistinfo[9])
                        check2_cd = Daylist_page.check(daylistinfo[10])
                        check3_cd = Daylist_page.check(daylistinfo[11])
                        check4_cd = Daylist_page.check(daylistinfo[12])
                        check5_cd = Daylist_page.check(daylistinfo[13])
                        check6_cd = Daylist_page.check(daylistinfo[14])
                        check7_cd = Daylist_page.check(daylistinfo[15])
                        check8_cd = Daylist_page.check(daylistinfo[16])
                        check9_cd = Daylist_page.check(daylistinfo[17])
                        check10_cd = Daylist_page.check(daylistinfo[18])
                        memo_cd = daylistinfo[19]

                        with st.expander(f'{choose_date}의 기록'):
                            # 몸무게
                            st.write('---')
                            subcol13, subcol14, subcol15 = st.columns([1, 1, 3])
                            subcol13.markdown('###### ▪️ 몸무게')
                            subcol14.text_input('몸무게', value=str(weight_cd) + 'kg', disabled=True,label_visibility='collapsed')
                            # 놀이시간
                            st.write('---')
                            subcol13, subcol14, subcol15 = st.columns([1, 1, 3])
                            subcol13.markdown('###### ▪️ 놀이시간')
                            hour = 'hour'
                            subcol14.text_input('놀이시간', value=str(playtime_cd) + hour, disabled=True,label_visibility='collapsed')
                            # 사료급여량
                            st.write('---')
                            st.markdown('###### ▪️ 사료급여량')
                            gram = 'gram'
                            subcol1, subcol2, subcol3, subcol4, subcol5, subcol6 = st.columns([1, 2, 1, 2, 1, 2],gap='medium')
                            subcol1.write('아침')
                            subcol2.text_input('아침사료량', value=str(breakfast_food_cd) + gram, disabled=True,label_visibility='collapsed')
                            subcol3.write('점심')
                            subcol4.text_input('점심사료량', value=str(lunch_food_cd) + gram, disabled=True,label_visibility='collapsed')
                            subcol5.write('저녁')
                            subcol6.text_input('저녁사료량', value=str(dinner_food_cd) + gram, disabled=True,label_visibility='collapsed')
                            # 음수량
                            st.write('---')
                            st.markdown('###### ▪️ 음수량')
                            ml = 'ml'
                            subcol1, subcol2, subcol3, subcol4, subcol5, subcol6 = st.columns([1, 2, 1, 2, 1, 2],gap='medium')
                            subcol1.write('아침')
                            subcol2.text_input('아침음수량', value=str(breakfast_water_cd) + ml, disabled=True,label_visibility='collapsed')
                            subcol3.write('점심')
                            subcol4.text_input('점심음수량', value=str(lunch_water_cd) + ml, disabled=True,label_visibility='collapsed')
                            subcol5.write('저녁')
                            subcol6.text_input('저녁음수량', value=str(dinner_water_cd) + ml, disabled=True,label_visibility='collapsed')
                            # 특이사항
                            st.write('---')
                            st.markdown('###### ▪️ 오늘의 특이사항')
                            c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
                            c_col1.checkbox(label=":drop_of_blood:", value=bool(check1_cd), disabled=True)
                            c_col2.checkbox(label="🪫", value=bool(check2_cd), disabled=True)
                            c_col3.checkbox(label="💊", value=bool(check3_cd), disabled=True)
                            c_col4.checkbox(label="🌡", value=bool(check4_cd), disabled=True)
                            c_col5.checkbox(label="🛁", value=bool(check5_cd), disabled=True)
                            st.write("")
                            c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
                            c_col1.checkbox(label="👂", value=bool(check6_cd), disabled=True)
                            c_col2.checkbox(label="🩺", value=bool(check7_cd), disabled=True)
                            c_col3.checkbox(label="😿", value=bool(check8_cd), disabled=True)
                            c_col4.checkbox(label="😺", value=bool(check9_cd), disabled=True)
                            c_col5.checkbox(label="😸", value=bool(check10_cd), disabled=True)
                            st.markdown('###### ▪️ 메모')
                            st.text_area('memo', value=memo_cd, disabled=True, label_visibility="collapsed")
                    # 날짜에 맞는 정보가 없는 경우
                    else:
                        st.info("기록이 없는 날입니다. 오늘이라면 추가해주세요", icon="✍🏼")

            # 통계보기 탭
            with tabs[2]:
                st.write("")
                st.subheader('통계보기 📊')
                col1,col2,col3=st.columns([1,1,2])
                period=col1.selectbox("기간",("1주일","1개월","6개월","1년"),label_visibility="collapsed")
                # 날짜에 맞게 불러오기
                if period=='1주일':
                    days=7
                elif period=='1개월':
                    days=30
                elif period=='6개월':
                    days=183
                elif period=='1년':
                    days=365
                # 기간에 맞는 데이터로 새로운 데이터프레임 생성
                startday=(now-datetime.timedelta(days=days)).strftime('%Y-%m-%d')
                df=self.daylistsv.makedf(startday,cat_info[3])
                st.caption(f'{startday} ~ {today}')
                st.write("")
                # 데이터가 있는 경우
                if df is not None:
                    # 기간을 인덱스로 설정
                    df.set_index('Date',inplace=True,drop=True)
                    col1, col2, col3 = st.columns([1, 1, 1])

                    # col1: 몸무게 변화 그래프
                    with col1:
                        st.markdown('###### ✔️ 몸무게 변화')
                        fig=go.Figure()
                        # 선 그래프 생성
                        fig.add_trace(px.line(df,x=df.index, y='Weight',text='Weight',color_discrete_sequence=['#FF5E00']).update_traces(textposition='top center').data[0])
                        fig.update_layout(
                            xaxis=dict(title='Date'),
                            yaxis=dict(title='Weight'),
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                            width=400)
                        st.plotly_chart(fig)

                    # col2: 하루 평균 사료량 그래프
                    df['total_food']=(df['Breakfast_Food']+df['Lunch_Food']+df['Dinner_Food'])
                    df['Recommendfood'] = round(df['Weight'].apply(lambda x: self.recommend(cat_info[6], x, cat_info[7])),2)
                    df['total_water'] = (df['Breakfast_Water'] + df['Lunch_Water'] + df['Dinner_Water'])
                    df['Recommendwater']= df['Weight']*50
                    with col2:
                        st.markdown('###### ✔️ 하루 섭취량 및 권장 사료량')
                        # 막대 그래프 생성
                        fig1 = px.bar(df, x=df.index, y='total_food', text='total_food',color_discrete_sequence=['#FFC19E'])
                        fig1.update_traces(textposition='auto')
                        # 선 그래프 생성
                        fig1.add_trace(px.line(df, x=df.index, y='Recommendfood', text='Recommendfood',color_discrete_sequence=['#FF5E00']).update_traces(
                            textposition='top center').data[0])
                        fig1.update_layout(
                            xaxis=dict(title='Date'),
                            yaxis=dict(title='Food'),
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                            width=400)
                        st.plotly_chart(fig1)

                    # col3: 하루 평균 음수량 그래프
                    with col3:
                        st.markdown('###### ✔️ 하루 음수량 및 권장 음수량')
                        # 막대 그래프 생성
                        fig2 = px.bar(df, x=df.index, y='total_water', text='total_water',color_discrete_sequence=['#FFC19E'])
                        fig2.update_traces(textposition='auto')
                        # 선 그래프 생성
                        fig2.add_trace(px.line(df, x=df.index, y='Recommendwater', text='Recommendwater',color_discrete_sequence=['#FF5E00']).update_traces(
                            textposition='top center').data[0])
                        fig2.update_layout(
                            xaxis=dict(title='Date'),
                            yaxis=dict(title='Water'),
                            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                            width=400)
                        st.plotly_chart(fig2)

                    # 권장 사료량 안내 표시
                    df['Recommendfood-totalfood'] = df['Recommendfood'] - df['total_food']
                    negative_count_food = (df['Recommendfood-totalfood'] < 0).sum()
                    st.info(f'💡 {period}동안 하루 섭취량이 권장 사료량보다 많은 날의 수는 {negative_count_food}일 입니다.')
                    # 권장 사료량보다 많이 섭취한 날(좋지 않은 습관)이 기간의 절반보다 많은 경우
                    if days/2 < negative_count_food:
                        st.write('➕ 권장 사료량보다 많이 섭취한 날이 기간의 절반보다 많습니다. 관심이 필요합니다!')
                    # 기간동안의 평균 권장 사료량보다 기간동안의 평균 섭취량이 더 많은 경우
                    if (sum(df['Recommendfood'])/days - sum(df['total_food'])/days) < 0:
                        st.write(f'➕ {period}기간동안 평균 권장 사료량보다 {period}기간동안 평균 섭취량이 더 많습니다. 하루 사료량을 줄일 필요가 있습니다.')
                    # 권장 음수량 안내 표시
                    df['totalwater-Recommendwater'] = df['total_water'] - df['Recommendwater']
                    positive_count = (df['totalwater-Recommendwater'] < 0).sum()
                    st.info(f'💡 {period}동안 하루 음수량이 권장 음수량보다 적은 날의 수는 {positive_count}일 입니다.')
                    # 권장 음수량보다 적게 섭취한 날(좋지 않은 습관)이 기간의 절반보다 많은 경우
                    if days/2 < positive_count:
                        st.write('➕ 권장 음수량보다 적게 섭취한 날이 기간의 절반보다 적습니다. 관심이 필요합니다!')
                    # 기간동안 평균 권장 음수량보다 기간동안의 평균 음수량이 더 적은 경우
                    if (sum(df['Recommendwater'])/days - sum(df['total_water'])/days) > 0:
                        st.write(f'➕ {period}기간동안 평균 권장 음수량보다 {period}기간동안 평균 음수량이 더 적습니다. 하루 음수량을 늘릴 필요가 있습니다.')

                    # 권장 사료량 확인방법
                    with st.expander('❕권장 사료량 확인방법'):
                        col4,col5,col6=st.columns([1,2,1])
                        with col5:
                            st.markdown('''######  1️⃣ 기초대사랑 구하기 (RER: Resting Energy Requirement)''')
                            st.markdown('''- 몸무게가 2kg 미만일 경우''')
                            st.latex(r'''RER(kcal) = 70 \times ( 체중(kg) \times 0.75)''')
                            st.markdown('''- 몸무게가 2kg 이상일 경우''')
                            st.latex(r'''RER(kcal) = 30 \times 체중(kg) + 70 ''')
                            st.write('')
                            st.markdown('''###### 2️⃣ 하루에 필요한 칼로리 구하기 (MER : Maintenance Energy requriement)''')
                            st.latex(r'''MER = 기초대사량 \times 활동수치''')
                            st.markdown('''- 활동 수치 확인 (참고 : 미국 수의 영양학 협의체)''')
                            data={'해당 사항':['집중 치료중/병원 입원중','저체중/비만','과체중 경향/활동성이 적은','중성화를 했으며, 보통 활동량','중성화를 하지 않았으며, 보통 활동량','임신중','수유중','새끼 강아지/고양이'],
                                  '활동 수치':['1.0','0.9','1.0','1.2','1.4','2.5','4','2.5']}
                            df = pd.DataFrame(data)
                            st.dataframe(df)
                            st.markdown('''
                            ###### 3️⃣ 하루 급여량 구하기''')
                            st.latex(r'''하루 급여량(g) = 하루에 필요한 열량(MER) \times 1000 / 사료 칼로리(kcal/kg) ''')
                    # 권장 음수량 확인방법
                    with st.expander('❕권장 음수량 확인방법'):
                        col4, col5, col6 = st.columns([1, 2, 1])
                        with col5:
                            st.latex(r'''하루 권장 음수량(ml) = 체중(kg) \times 50 ''')
                # 데이터가 없는 경우
                else:
                    st.error('정보가 없습니다')

if __name__ == '__main__':
    m = Daylist_page()
    m.run()


