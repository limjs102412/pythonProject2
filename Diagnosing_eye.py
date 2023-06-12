import decimal
import math

import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import tensorflow as tf
from member.service import MemberService
from pet.petsv import PetService
import datetime
from MedicalCharts.chart_db import ChartDao
import io
import plotly.graph_objects as go
import plotly.express as px
from keras.layers import Dense, Dropout
from keras.applications.resnet_v2 import ResNet50V2
from keras.applications.densenet import DenseNet121
from keras import Sequential


class Diagnosing_eye_page:

    def __init__(self):
        self.service=MemberService()
        self.petsv=PetService()
        self.chartdb=ChartDao()



    # def classification(self, img, i):
    #     # 모델 아키텍처 정의
    #     if i == 0:
    #         model = self.Blepharitis_model()
    #     elif i == 1:
    #         model = self.Deep_keratitis_model()
    #     elif i == 2:
    #         model = self.Conjunctivitis_model()
    #     elif i == 3:
    #         model = self.Conael_sequestrum_model()
    #     elif i == 4:
    #         model = self.Corneal_ulcer_model()
    #
    #     load_weights_list = ['model/Blepharitis_weight.h5', 'model/Deep_keratitis_weight.h5', 'model/Conjunctivitis_weight.h5',
    #                          'model/Conael_sequestrum_weight.h5', 'model/Corneal_ulcer_weight.h5']
    #     # 저장된 가중치 로드
    #     model.load_weights(load_weights_list[i])
    #     # 이미지 전처리
    #     if isinstance(img, str):
    #         image = Image.open(img)
    #     elif isinstance(img, Image.Image):
    #         image = img
    #     else:
    #         raise ValueError("Invalid image format. `img` should be a file path or a PIL image object.")
    #
    #     image = image.resize((224, 224))
    #     image_array = np.array(image)
    #     # 이미지의 채널 축을 모델과 일치하도록 변경
    #     if image_array.shape[-1] == 4:
    #         image_array = image_array[..., :3]
    #     image_array = image_array / 255.0  # 이미지 정규화
    #     # 이미지를 모델의 입력 형식에 맞게 변환
    #     input_image = tf.convert_to_tensor(image_array, dtype=tf.float32)
    #     input_image = tf.expand_dims(input_image, axis=0)
    #     # 예측 수행
    #     prediction = model.predict(input_image)[0][0]
    #     # 클래스 라벨 정의
    #     class_labels = ['유', '무']  # 실제 클래스 라벨로 변경
    #     # 분류 임계값 설정 (예: 0.5)
    #     threshold = 0.5
    #     # 예측된 클래스 레이블 결정
    #     predicted_class_label = class_labels[int(prediction >= threshold)]
    #     prediction = 1 - prediction
    #     prediction = round(prediction * 100, 2)
    #     print(predicted_class_label, prediction)
    #     # 예측된 클래스 라벨, 예측 값 반환
    #     return predicted_class_label, prediction




    # 모델 아키텍처 생성 함수
    # 안검염
    def Blepharitis_model(self):
        model = Sequential()
        model.add(DenseNet121(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg'))
        model.add(Dense(2048, activation='relu'))
        model.add(Dense(2, activation='sigmoid'))
        model.summary()
        return model

    # 비궤양성각막염
    def Deep_keratitis_model(self):
        model = Sequential()
        model.add(ResNet50V2(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                             pooling='avg'))
        model.add(Dense(2048, activation='relu'))
        model.add(Dense(2, activation='sigmoid'))
        model.summary()
        return model

    # 결막염
    def Conjunctivitis_model(self):
        model = Sequential()
        model.add(ResNet50V2(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                             pooling='avg'))
        model.add(Dense(2048, activation='relu'))
        model.add(Dense(2, activation='sigmoid'))
        model.summary()
        return model

    # 각막부골편
    def Conael_sequestrum_model(self):
        model = Sequential()
        model.add(DenseNet121(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                              pooling='avg'))
        model.add(Dense(1024, activation='relu'))
        model.add(Dense(2, activation='sigmoid'))
        model.summary()
        return model

    # 각막궤양
    def Corneal_ulcer_model(self):
        model = Sequential()
        model.add(ResNet50V2(include_top=False, weights='imagenet', input_tensor=None, input_shape=(224, 224, 3),
                             pooling='avg'))
        model.add(Dense(2048, activation='relu'))
        model.add(Dense(2, activation='sigmoid'))
        model.summary()
        return model


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
    # def grad_cam_image(self, model_path,myimage_path,type='resnet'):
    #     import numpy as np
    #     import tensorflow as tf
    #     from tensorflow import keras
    #     from tensorflow.keras.applications import resnet50, ResNet50
    #     from tensorflow.keras.preprocessing import image
    #     import matplotlib.pyplot as plt
    #     import matplotlib.cm as cm
    #
    #     # 사전 학습된 신경망 모델을 불러오고 구조 확인
    #     model = load_model(model_path)
    #
    #     # 지정된 영상을 불러와 크기 조정하고 화면에 디스플레이
    #     image_path = myimage_path
    #     img = image.load_img(image_path, target_size=(224, 224))
    #
    #     # 영상을 신경망 형태로 변환
    #     img = load_img(image_path, target_size=(224, 224))
    #     img_array = img_to_array(img)
    #     img_array = np.expand_dims(img_array, axis=0)
    #     x = preprocess_input(img_array)
    #
    #     # 인식을 시도하고 top-5결과를 출력
    #     model.predict(x)
    #     last_conv_layer = model.get_layer('densenet121').get_layer("conv5_block16_concat")
    #
    #     model_1 = keras.Model(model.get_layer('densenet121').inputs, last_conv_layer.output)
    #
    #     # 분류 (전역평균풀링 또는 완전연결층) 부분만으로 구성된 model__2만들기
    #     input_2 = keras.Input(shape=last_conv_layer.output.shape[1:])
    #     x_2 = model.get_layer('densenet121').get_layer("avg_pool")(input_2)
    #     x_2 = model.get_layer('dense')(x_2)
    #     model_2 = keras.Model(input_2, x_2)
    #
    #     # GradientTape함수를 이용한 그레디언트 계산
    #     with tf.GradientTape() as tape:
    #         output_1 = model_1(x)
    #         tape.watch(output_1)  # 마지막 층으로 미분하기 위한 준비
    #         preds = model_2(output_1)
    #         class_id = tf.argmax(preds[0])
    #         output_2 = preds[:, class_id]
    #
    #     grads = tape.gradient(output_2, output_1)  # 그레디언트 계산
    #     pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))  # 식5 적용
    #
    #     output_1 = output_1.numpy()[0]
    #     pooled_grads = pooled_grads.numpy()
    #     for i in range(pooled_grads.shape[-1]):
    #         output_1[:, :, i] *= pooled_grads[i]
    #     heatmap = np.mean(output_1, axis=-1)
    #
    #     heatmap = np.maximum(heatmap, 0) / np.max(heatmap)  # 정규화
    #
    #     # 열지도를 입력 영상에 씌움
    #     img = image.load_img(image_path)  # 입력 영상을 다시 받음
    #
    #     img = image.img_to_array(img)
    #     heatmap = np.uint8(255 * heatmap)  # [0,255]로 변환
    #
    #     jet = cm.get_cmap("jet")  # jet 컬러맵으로 표시
    #     color = jet(np.arange(256))[:, :3]
    #     color_heatmap = color[heatmap]
    #
    #     color_heatmap = keras.preprocessing.image.array_to_img(color_heatmap)
    #     color_heatmap = color_heatmap.resize((img.shape[1], img.shape[0]))
    #     color_heatmap = keras.preprocessing.image.img_to_array(color_heatmap)
    #
    #     overlay_img = color_heatmap * 0.4 + img  # 덧씌움
    #     overlay_img = keras.preprocessing.image.array_to_img(overlay_img)
    #     # plt.matshow(overlay_img)
    #     plt.gca().set_axis_off()
    #     plt.matshow(overlay_img)
    #     plt.xticks([]), plt.yticks([])
    #     plt.savefig('', bbox_inches='tight', pad_inches=0)  # 이미지 파일로 저장


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
                    model_list=['model/Blepharitis.h5','model/Deep_keratitis.h5','model/Conjunctivitis.h5','model/Conael_sequestrum.h5','model/Corneal_ulcer.h5']
                    predicted_class_list=[] # 유,무 리스트
                    prediction_list=[] # 예측값 리스트
                    # 진행될 경우
                    with st.spinner('처리중입니다...(20초 이내)'):
                        for i,model in enumerate(model_list):
                            predicted_class_label,prediction = self.classification(image, model)
                            # predicted_class_label,prediction=self.classification(image,i)
                            predicted_class_list.append(predicted_class_label)
                            prediction_list.append(str(prediction))
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

                    # db 저장
                    image_name = now
                    self.chartdb.upload_image1(cat_info[3],today,
                                               image_name,uploaded_image,
                                               predicted_class_list[0], prediction_list[0],
                                               predicted_class_list[1], prediction_list[1],
                                               predicted_class_list[2], prediction_list[2],
                                               predicted_class_list[3], prediction_list[3],
                                               predicted_class_list[4], prediction_list[4]
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
                            for name, img, Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis, Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent in images:
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
                                st.markdown("---")

                # 진단 받은 날짜가 없는 경우
                else:
                    st.error('안구질환 진단한 기록이 없습니다!')


if __name__ == '__main__':
    m = Diagnosing_eye_page()
    m.diagnosing_eye_page()

