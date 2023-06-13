import decimal
import math
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import tensorflow as tf
from keras.utils import img_to_array
# from keras.preprocessing.image import load_img
from member.service import MemberService
from pet.petsv import PetService
import datetime
from MedicalCharts.chart_db import ChartDao
import io
import plotly.graph_objects as go
import plotly.express as px
from keras.layers import Dense, Dropout
from keras.applications.resnet_v2 import ResNet50V2
from keras.applications.densenet import DenseNet121, preprocess_input
from keras import Sequential


class Diagnosing_eye_page:

    def __init__(self):
        self.service=MemberService()
        self.petsv=PetService()
        self.chartdb=ChartDao()


    # 입력받은 이미지를 입력받은 이미지분류를 적용하여 예측하는 함수
    def classification(self,img,weights_file):
        # 모델 로드
        model = tf.keras.models.load_model(weights_file)
        # 이미지 로드 및 전처리
        image = img.resize((224, 224))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = tf.expand_dims(image, axis=0)
        # 이미지 정규화
        image = image / 255.0
        # 예측
        prediction = model.predict(image)[0][0]
        # 클래스 라벨 정의
        class_labels = ['유', '무']
        # 분류의 임계값 설정 (e.g., 0.5)
        threshold = 0.5
        # 예측 클래스 레이블 결정
        predicted_class_label = class_labels[int(prediction >= threshold)] # 0.5 미만 : 유 / 0.5 이상 : 무
        prediction=1-prediction # 0.5 미만 : 무 / 0.5 이상 :유
        decimal_prediction = decimal.Decimal(prediction)
        prediction = (decimal_prediction * 10000).quantize(decimal.Decimal('0.00')) / 100
        # 예측된 클래스 라벨, 예측값 리턴
        return predicted_class_label,prediction


    # grad_cam
    def grad_cam_image(self, model_path,myimage_path, type='resnet'):
        import numpy as np
        import tensorflow as tf
        from tensorflow import keras
        # from keras.applications import resnet50, ResNet50
        from keras.preprocessing import image
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm

        # 사전 학습된 신경망 모델을 불러오고 구조 확인
        model = tf.keras.models.load_model(model_path)

        # 지정된 영상을 불러와 크기 조정하고 화면에 디스플레이
        image_path = myimage_path
        # img = load_img(image_path, target_size=(224, 224))
        img = Image.open(image_path)
        img = img.resize((224, 224))

        # 영상을 신경망 형태로 변환
        # img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        x = preprocess_input(img_array)

        if type=='resnet':
            # 인식을 시도하고 top-5결과를 출력
            model.predict(x)
            # 신경망 모델의 특 징 추출 부분에서 마지막 층을 지정
            # 특징 추출 부분만으로 구성된 model_1만들기
            last_conv_layer = model.get_layer('resnet50').get_layer('conv5_block3_out')
            model_1 = keras.Model(model.get_layer('resnet50').inputs, last_conv_layer.output)
            # 분류 (전역평균풀링 또는 완전연결층) 부분만으로 구성된 model__2만들기
            input_2 = keras.Input(shape=last_conv_layer.output.shape[1:])
            x_2 = model.get_layer('resnet50').get_layer("avg_pool")(input_2)
            x_2 = model.get_layer('dense')(x_2)
            model_2 = keras.Model(input_2, x_2)
        elif type=='resnet50v2':
            # 인식을 시도하고 top-5결과를 출력
            model.predict(x)
            # 신경망 모델의 특 징 추출 부분에서 마지막 층을 지정
            # 특징 추출 부분만으로 구성된 model_1만들기
            last_conv_layer = model.get_layer('resnet50v2').get_layer('conv5_block3_out')
            model_1 = keras.Model(model.get_layer('resnet50v2').inputs, last_conv_layer.output)
            # 분류 (전역평균풀링 또는 완전연결층) 부분만으로 구성된 model__2만들기
            input_2 = keras.Input(shape=last_conv_layer.output.shape[1:])
            x_2 = model.get_layer('resnet50v2').get_layer("avg_pool")(input_2)
            x_2 = model.get_layer('dense')(x_2)
            model_2 = keras.Model(input_2, x_2)
        elif type=='densenet':
            # 인식을 시도하고 top-5결과를 출력
            model.predict(x)
            last_conv_layer = model.get_layer('densenet121').get_layer("conv5_block16_concat")
            model_1 = keras.Model(model.get_layer('densenet121').inputs, last_conv_layer.output)
            # 분류 (전역평균풀링 또는 완전연결층) 부분만으로 구성된 model__2만들기
            input_2 = keras.Input(shape=last_conv_layer.output.shape[1:])
            x_2 = model.get_layer('densenet121').get_layer("avg_pool")(input_2)
            x_2 = model.get_layer('dense')(x_2)
            model_2 = keras.Model(input_2, x_2)
        # GradientTape함수를 이용한 그레디언트 계산
        with tf.GradientTape() as tape:
            output_1 = model_1(x)
            tape.watch(output_1)  # 마지막 층으로 미분하기 위한 준비
            preds = model_2(output_1)
            class_id = tf.argmax(preds[0])
            output_2 = preds[:, class_id]

        grads = tape.gradient(output_2, output_1)  # 그레디언트 계산
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))  # 식5 적용

        output_1 = output_1.numpy()[0]
        pooled_grads = pooled_grads.numpy()
        for i in range(pooled_grads.shape[-1]):
            output_1[:, :, i] *= pooled_grads[i]
        heatmap = np.mean(output_1, axis=-1)
        heatmap = np.maximum(heatmap, 0) / np.max(heatmap)  # 정규화

        # 열지도를 입력 영상에 씌움
        img = Image.open(image_path)
        # img = img.resize((224, 224))
        # img = image.load_img(image_path)  # 입력 영상을 다시 받음

        img = img_to_array(img)
        heatmap = np.uint8(255 * heatmap)  # [0,255]로 변환

        jet = cm.get_cmap("jet")  # jet 컬러맵으로 표시
        color = jet(np.arange(256))[:, :3]
        color_heatmap = color[heatmap]

        color_heatmap = keras.preprocessing.image.array_to_img(color_heatmap)
        color_heatmap = color_heatmap.resize((img.shape[1], img.shape[0]))
        color_heatmap = keras.preprocessing.image.img_to_array(color_heatmap)

        overlay_img = color_heatmap * 0.4 + img  # 덧씌움
        overlay_img = keras.preprocessing.image.array_to_img(overlay_img)
        return overlay_img
        # plt.matshow(overlay_img)
        # plt.gca().set_axis_off()
        # plt.matshow(overlay_img)
        # plt.xticks([]), plt.yticks([])
        # plt.savefig('', bbox_inches='tight', pad_inches=0)  # 이미지 파일로 저장


    def diagnosing_eye_page(self):
        # 안구질환 진단 페이지

        # 로그인된 사용자의 등록된 고양이가 있는지 검색
        self.petsv.printMyCat(print2=False,print1=False)
        # 로그인된 사용자의 현재 지정된 고양이 이름
        mycat = PetService.loginCatName

        # 탭 스타일변경 및 탭 설정
        font_css = """
                            <style>
                            button[data-baseweb="tab"]   {
                              background: #EAEAEA55;
                            }
                            </style>
                            """
        st.write(font_css, unsafe_allow_html=True)
        if mycat:
            tabname = f"{mycat}의 진단 기록📋"
        else:
            tabname="진단 기록📋"
        listtabs = ["안구질환 진단:eye:",tabname]
        whitespace = 30
        tabs = st.tabs([s.center(whitespace, "\u2001") for s in listtabs])

        # 안구질환 진단 탭
        with tabs[0]:
            # 로그인된 사용자만 가능
            if MemberService.loginId=="":
                st.error('로그인 먼저 하세요', icon="🚨")
            # 등록된 고양이가 없으면 에러메세지 출력
            elif mycat == "":
                st.error('마이페이지에서 반려묘를 등록해주세요')
            # 정상
            else:
                # 고양이의 정보와 오늘 날짜
                cat_info = self.petsv.printCatInfo(MemberService.loginId, mycat)
                now = datetime.datetime.now()
                year = int(now.strftime('%Y'))
                month = int(now.strftime('%m'))
                day = int(now.strftime('%d'))
                today = datetime.date(year, month, day)

                # 레이아웃 설정
                col1, col, col2 = st.columns([3, 0.5, 2])
                # 왼쪽은 서비스 및 이용 설명
                with col1:
                    st.markdown('''
                    고양이의 안구질환은 조기에 치료하지 않으면 큰 질병까지 이어질 수 있습니다.
                    이 서비스를 이용하여 안구상태를 주기적으로 체크하세요. 
                  
                    ###### [서비스 이용방법]
                    1. 고양이의 눈만 보이도록 사진을 찍습니다.
                    2. 사진을 업로드하면 진단이 진행됩니다.
                    3. 결과와 질환에 대한 통계를 확인합니다.''')
                    st.caption('AI챗봇에 질환에 대해 물어보면 더 많은 정보를 얻을 수 있습니다.')
                    with st.expander('📸 예시 사진보기'):
                        imgcol1,imgcol2,imgcol3=st.columns(3)
                        imgcol1.image('image/crop_C7_3e00fdab-60a5-11ec-8402-0a7404972c70.jpg', caption='손으로 눈을 벌리고 사진을 찍습니다.', width=150)
                        imgcol2.image('image/crop_C1_3e075e5a-60a5-11ec-8402-0a7404972c70.jpg', caption='눈 부위를 밝게 찍습니다.', width=150)
                        imgcol3.image('image/crop_C42_3e00a570-60a5-11ec-8402-0a7404972c70.jpg', caption='눈동자에 비치는 것이 없도록 찍습니다.', width=150)
                    with st.expander('📌 읽어보세요!!'):
                        st.markdown('- 사진의 각도에 따라서 결과가 다르게 나올 수 있습니다.')
                        st.markdown('- 여러번 시도 해보세요')
                        st.markdown('- 해당 서비스는 참고용으로만 사용해주세요')

                # 사진 업로드 기능(하단)
                uploaded_image = st.file_uploader("이미지를 업로드하세요.", type=["jpg"],label_visibility='collapsed')

                # 오른쪽에는 업로드한 사진 보기
                with col2:
                    st.markdown('###### 업로드 사진 보기')
                    if uploaded_image is not None:
                        image = Image.open(uploaded_image)
                        st.image(image, caption='Uploaded Image.', width=300)

                # 사진을 업로드하면 이미지분류모델 적용
                if uploaded_image is not None:
                    st.write('')
                    class_list = ['안검염', '비궤양성각막염', '결막염', '각막부골편', '각막궤양']
                    type_list=['densenet','resnet','resnet','densenet','resnet50v2']
                    model_list=['model/Blepharitis.h5','model/Deep_keratitis.h5','model/Conjunctivitis.h5','model/Conael_sequestrum.h5','model/Corneal_ulcer.h5']

                    predicted_class_list=[] # 유,무 리스트
                    prediction_list=[] # 예측값 리스트
                    gradimglist=[]
                    # 진행될 경우
                    with st.spinner('처리중입니다...(1분30초 이내)'):

                        for i,model in enumerate(model_list):
                            predicted_class_label,prediction = self.classification(image, model)
                            img=self.grad_cam_image(model_list[i], uploaded_image, type=type_list[i])
                            predicted_class_list.append(predicted_class_label)
                            prediction_list.append(str(prediction))
                            image_bytes=io.BytesIO()
                            img.save(image_bytes,format='JPEG')
                            image_bytes.seek(0)
                            image_data = image_bytes.read()
                            gradimglist.append(image_data)
                        print('끝')
                    # 예측라벨이 '유'인 질병명,예측값만 저장
                    yes_class=[] # 유 질병명 리스트
                    yes_pred=[] # 유 예측값 리스트

                    for i, pcl in enumerate(predicted_class_list):
                        if pcl=='유':
                            yes_class.append(class_list[i])
                            yes_pred.append(prediction_list[i])
                    # 결과 출력
                    total=''
                    for i in range(len(yes_class)):
                        total=total+yes_class[i]+'('+yes_pred[i]+'%)'+', '
                    newtotal=total.rstrip(', ')
                    if '유' in predicted_class_list :
                        st.success(f'해당 사진은 **{newtotal}** 이 예상됩니다. \n\n 가까운 병원에 가셔서 정확한 진단을 받아보세요', icon='😿')
                    else:
                        st.success('해당 사진에는 보이는 질환이 없습니다. 건강합니다.',icon='😸')

                    st.write('🔍자세히 살펴보기')
                    if predicted_class_list[0]=='무' and predicted_class_list[1]=='무'and predicted_class_list[2]=='무' and predicted_class_list[3]=='무' and predicted_class_list[4]=='무':
                        imagecol1, imagecol2, imagecol3, imagecol4, imagecol5 = st.columns(5)
                        colist = [imagecol1, imagecol2, imagecol3, imagecol4, imagecol5]
                        yes_grad = []
                        yes_class2 = []
                        for i in ['Blepharitis', 'Deep_keratitis', 'Conjunctivitis', 'Conael_sequestrum', 'Corneal_ulcer']:
                            if i == 'Blepharitis':
                                if predicted_class_list[0] == '유':
                                    yes_grad.append(gradimglist[0])
                                    yes_class2.append('안검염')
                            elif i == 'Deep_keratitis':
                                if predicted_class_list[1] == '유':
                                    yes_grad.append(gradimglist[1])
                                    yes_class2.append('비궤양성각막염')
                            elif i == 'Conjunctivitis':
                                if predicted_class_list[2] == '유':
                                    yes_grad.append(gradimglist[2])
                                    yes_class2.append('결막염')
                            elif i == 'Conael_sequestrum':
                                if predicted_class_list[3] == '유':
                                    yes_grad.append(gradimglist[3])
                                    yes_class2.append('각막부골편')
                            elif i == 'Corneal_ulcer':
                                if predicted_class_list[4] == '유':
                                    yes_grad.append(gradimglist[4])
                                    yes_class2.append('각막궤양')
                        for i, img in enumerate(yes_grad):
                            colist[i].image(Image.open(io.BytesIO(img)), caption=yes_class2[i], width=100)



                    # db 저장
                    image_name = now
                    self.chartdb.upload_image1(cat_info[3],today,
                                               image_name,uploaded_image,
                                               predicted_class_list[0], prediction_list[0],
                                               predicted_class_list[1], prediction_list[1],
                                               predicted_class_list[2], prediction_list[2],
                                               predicted_class_list[3], prediction_list[3],
                                               predicted_class_list[4], prediction_list[4],
                                               gradimglist[0],gradimglist[1],gradimglist[2],
                                               gradimglist[3],gradimglist[4]
                                               )

        # 진단 기록 탭
        with tabs[1]:
            # 로그인 사용자만 이용 가능
            if MemberService.loginId == "":
                st.error('로그인 먼저 하세요', icon="🚨")
            # 등록된 고양이가 있을 경우만 사용가능
            elif mycat == "":
                st.error('마이페이지에서 반려묘를 등록해주세요')
            # 정상
            else:
                # 로그인된 사용자가 지정한 고양이의 정보 출력
                cat_info = self.petsv.printCatInfo(MemberService.loginId, mycat)
                # 지정된 고양이가 진단 받은 날짜 불러오기
                Dates = self.chartdb.findDate(cat_info[3])

                # 진단 받은 날짜가 있는 경우
                if Dates:
                    # 날짜마다 확장탭 설정
                    for Date in Dates:
                        with st.expander(label=f' {Date}'):
                            # 지정된 고양이와 날짜에 맞는 정보 불러오기
                            images = self.chartdb.select1(cat_info[3], Date)
                            # 탭 안에 진단 받은 결과 출력
                            for name, img, Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis, Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent,grad_Blepharitis, grad_Deep_keratitis, grad_Conjunctivitis, grad_Conael_sequestrum, grad_Corneal_ulcer in images:
                                # 레이아웃 설정
                                col1, col2,col3 = st.columns([1,1,2])
                                # 왼쪽: 업로드한 사진
                                col1.write('##### 🖼️업로드한 사진')
                                col1.image(Image.open(io.BytesIO(img)), caption=name, width=200)
                                # 중앙: 예측라벨이 '유'인 질병명
                                col2.write('##### 📃의심되는 질병')
                                if Blepharitis=='유':
                                    col2.write('안검염')
                                if Deep_keratitis =='유':
                                    col2.write('비궤양성각막염')
                                if Conjunctivitis == '유':
                                    col2.write('결막염')
                                if Conael_sequestrum == '유':
                                    col2.write('각막부골편')
                                if Corneal_ulcer == '유':
                                    col2.write('각막궤양')
                                if Blepharitis=='무' and Deep_keratitis=='무'and Conjunctivitis=='무' and Conael_sequestrum=='무' and Corneal_ulcer=='무':
                                    col2.write('의심되는 질병이 없습니다.')
                                # 오른쪽: 예측명,예측값을 나타내는 시각화
                                with col3:
                                    data={'col':['안검염', '비궤양성각막염', '결막염', '각막부골편', '각막궤양'],
                                          'value':[float(Blepharitis_percent) ,
                                                   float(Deep_keratitis_percent) ,
                                                   float(Conjunctivitis_percent) ,
                                                   float(Conael_sequestrum_percent) ,
                                                   float(Corneal_ulcer_percent) ]}
                                    df=pd.DataFrame(data=data)
                                    # 예측값을 막대그래프로 표현
                                    fig1 = px.bar( x=df['col'], y=df['value'], text=df['value'],
                                                  color_discrete_sequence=['#FFC19E'])
                                    fig1.update_traces(textposition='auto')
                                    # 예측값이 50인 선그래프 표현 (유/무의 기준선)
                                    fig1.add_trace(px.line(x=df['col'], y=[50] * len(df),
                                                           color_discrete_sequence=['#FF5E00']).data[0])
                                    fig1.update_layout(
                                        xaxis=dict(title=''),
                                        yaxis=dict(title='질병일 확률',range=[0,100]),
                                        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                                        width=400,height=300
                                    )
                                    # 그래프 출력
                                    st.plotly_chart(fig1)

                                if Blepharitis=='유' or Deep_keratitis=='유' or Conjunctivitis=='유' or Conael_sequestrum=='유' or Corneal_ulcer=='유':
                                    st.write('🔍자세히 살펴보기')
                                    imagecol1,imagecol2,imagecol3,imagecol4,imagecol5=st.columns(5)
                                    colist=[imagecol1,imagecol2,imagecol3,imagecol4,imagecol5]
                                    yes_grad = []
                                    yes_class2=[]
                                    for i in ['Blepharitis','Deep_keratitis','Conjunctivitis','Conael_sequestrum','Corneal_ulcer']:
                                        if i == 'Blepharitis':
                                            if Blepharitis == '유':
                                                yes_grad.append(grad_Blepharitis)
                                                yes_class2.append('안검염')
                                        elif i == 'Deep_keratitis':
                                            if Deep_keratitis == '유':
                                                yes_grad.append(grad_Deep_keratitis)
                                                yes_class2.append('비궤양성각막염')
                                        elif i == 'Conjunctivitis':
                                            if Conjunctivitis == '유':
                                                yes_grad.append(grad_Conjunctivitis)
                                                yes_class2.append('결막염')
                                        elif i == 'Conael_sequestrum':
                                            if Conael_sequestrum == '유':
                                                yes_grad.append(grad_Conael_sequestrum)
                                                yes_class2.append('각막부골편')
                                        elif i == 'Corneal_ulcer':
                                            if Corneal_ulcer == '유':
                                                yes_grad.append(grad_Corneal_ulcer)
                                                yes_class2.append('각막궤양')
                                    for i,img in enumerate(yes_grad):
                                        colist[i].image(Image.open(io.BytesIO(img)), caption=yes_class2[i], width=100)



                                st.markdown("---")
                # 진단 받은 날짜가 없는 경우
                else:
                    st.error('안구질환 진단한 기록이 없습니다!')


if __name__ == '__main__':
    m = Diagnosing_eye_page()
    m.diagnosing_eye_page()

