import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 한글 폰트 이용 관련
import platform
st.set_option('deprecation.showPyplotGlobalUse', False)
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':  # 맥OS
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # 윈도우
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system...  sorry~~~')
fontprop = fm.FontProperties(fname="font/NanumGothic.ttf")



def About_page():
# 주요서비스 설명 부분(상단)
    st.subheader('About:house:')
    st.write(' ')
    st.markdown('''
            ##### 냥이의 하루,안냥 

            고양이들의 하루가 어제보다 더 건강하고 즐거울 수 있도록  
            사진으로 간편하게 반려묘의 안구질환을 진단하고 반려묘의 하루를 매일 기록할 수 있는 서비스 입니다. 

            #
            ###### [주요 서비스]
            * 📸 안구진단 : 안구사진을 업로드하면 의심스러운 질병을 진단해보세요.              
            * 📝 하루기록 : 반려묘의 하루를 기록하고 통계를 통해서 반려묘의 건강을 체크해보세요.
            * 🏥 동물병원    :    지역 선택을 통해 병원의 위치와 간단한 정보를 확인해보세요. 
            * 💬 챗봇    :    고양이에 대해 궁금한점을 챗봇과 이야기 해보세요.

            #
            ''')

    st.image(image='image/20230327_1642222721.png', use_column_width=True)

# 고양이 질병 통계 시각화 부분(하단)
    st.markdown('''###### [고양이 질병 통계]''')

    # 파일 업로드
    df = pd.read_csv('data/고양이안구.csv')
    df1 = pd.read_csv('data/각막궤양.csv')
    df2 = pd.read_csv('data/각막부골편.csv')
    df3 = pd.read_csv('data/결막염.csv')
    df4 = pd.read_csv('data/비궤양성각막염.csv')
    df5 = pd.read_csv('data/안검염.csv')

    dataframes = {
        '각막궤양': df1,
        '각막부골편': df2,
        '결막염': df3,
        '비궤양성각막염': df4,
        '안검염': df5
    }

    # 질병 분포 비율 그래프
    st.subheader('질병 분포 비율')
    fig_disease, ax_disease = plt.subplots(figsize=(12, 8))
    disease_counts = df['label_disease_nm'].value_counts()
    colors = ['#F4E3C1', '#D9B996', '#B78E69', '#A46C42', '#8C4D23']
    wedgeprops = {'width': 0.55, 'edgecolor': 'w', 'linewidth': 3}
    explode = [0.03, 0.03, 0.03, 0.03, 0.03]
    wedges, labels, _ = ax_disease.pie(disease_counts, colors=colors, autopct='%1.2f%%',
                                       startangle=90, explode=explode, wedgeprops=wedgeprops,
                                       textprops={'fontsize': 20}, shadow=True, pctdistance=0.7)
    ax_disease.set_aspect('equal')
    legend_labels = ['안검염', '비궤양성각막염', '각막부골편', '결막염', '각막궤양']
    ax_disease.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.95, 0.8), fontsize=20)
    plt.tight_layout()
    fig_disease.savefig("disease_pie_chart.png", dpi=200)# 해상도 조정
    st.image("disease_pie_chart.png")

    # 각 질병에 해당하는 selectbox 박스 생성
    selected_disease = st.selectbox('질병 선택', list(dataframes.keys()))
    selected_data = dataframes[selected_disease]

    # 탭 생성
    tabs = st.tabs(['질병(나이) 그래프', '질병(성별) 그래프', '질병(종/안구+평균나이) 그래프'])

    # 선택한 질병에 대한 연령대(age) 그래프
    with tabs[0]:
        fig_age, ax_age = plt.subplots(figsize=(10, 6))
        sns.countplot(x='age', data=selected_data, palette='YlOrBr_r', order=selected_data['age'].value_counts().index,
                      ax=ax_age, linewidth=1, edgecolor='black')
        ax_age.set_xlabel('연령[살]')
        ax_age.set_ylabel('개체[마리]', rotation=0, ha='right')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig_age)

    # 선택한 질병에 대한 성별(gender) 그래프
    with tabs[1]:
        fig_gender, ax_gender = plt.subplots(figsize=(6, 2))
        gender_counts = selected_data['gender'].value_counts()
        colors = ['#8B4513', '#F5DEB3']
        wedges, labels, _ = ax_gender.pie(gender_counts, colors=colors, autopct='%1.1f%%',
                                          startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2.5},
                                          textprops={'fontsize': 5}, shadow=True)
        ax_gender.set_aspect('equal')
        legend_labels = ['Male', 'Female']
        ax_gender.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.9, 0.8), fontsize=5)
        plt.tight_layout()
        st.pyplot(fig_gender)

    #  선택한 질병에 대한 '종'별 평균 나이 히트맵 그래프
    with tabs[2]:
        fig_breed, ax_breed = plt.subplots(figsize=(10, 6))
        breed_age_mean = selected_data.pivot_table(index='breed', columns='eye_position', values='age_mean')
        breed_age_mean = breed_age_mean.sort_values(by=['오른쪽눈', '왼쪽눈'], ascending=False)
        heatmap = sns.heatmap(breed_age_mean, cmap='YlOrBr', annot=True, fmt='.2f', cbar=False, linecolor='black',
                              annot_kws={'fontsize': 8, 'fontweight': 'bold'})
        ax_breed.set_xlabel('고양이 안구', rotation=0, ha='right')
        ax_breed.set_ylabel('고양이 종', rotation=0, ha='right')
        plt.xticks(rotation=45)
        st.pyplot(fig_breed)