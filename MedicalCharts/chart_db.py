import streamlit as st
import sqlite3
from MedicalCharts.chart import Chart
from PIL import Image
import io

class ChartDao:
    # image 테이블 생성
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS image
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           Cat_Num char(20),
                          Date date,
                          name TEXT, 
                          image BLOB,
                          Blepharitis Int default 0,
                          Blepharitis_percent char(10),
                          Deep_keratitis Int default 0,
                           Deep_keratitis_percent char(10),
                            Conjunctivitis Int default 0,
                            Conjunctivitis_percent char(10),
                            Conael_sequestrum Int default 0,
                            Conael_sequestrum_percent char(10),
                            Corneal_ulcer Int default 0,
                            Corneal_ulcer_percent char(10)
                            )''')


    # image테이블에서 입력받은 Cat_Num에 해당하는 unique한 날짜를 검색하는 메서드
    def findDate(self,Cat_Num):
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        c.execute(f"SELECT DISTINCT Date FROM image WHERE Cat_Num={Cat_Num} ORDER BY Date DESC")
        row = [item[0] for item in c.fetchall()]
        return row

    # image테이블에서 입력받은 Cat_Num, Date에 해당하는 인스턴스의 정보를 검색하는 메서드
    def select1(self,Cat_Num,Date):
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        c.execute(f"SELECT name, image,Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis,Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent FROM image WHERE Cat_Num='{Cat_Num}' and Date='{Date}'")
        images = c.fetchall()

        return images

    # image테이블에서 입력받은 정보를 삽입하는 메서드
    def upload_image1(self,Cat_Num,Date,image_name,uploaded_image,Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis,Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent):
        image = Image.open(uploaded_image)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_data = image_bytes.getvalue()
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        c.execute("INSERT INTO image (Cat_Num, Date, name, image,Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis,Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent) VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?)",
                  (Cat_Num,Date, image_name, image_data,Blepharitis, Blepharitis_percent, Deep_keratitis, Deep_keratitis_percent, Conjunctivitis,Conjunctivitis_percent, Conael_sequestrum, Conael_sequestrum_percent, Corneal_ulcer, Corneal_ulcer_percent))
        conn.commit()
        st.success("이미지가 저장되었습니다. 진단 기록 탭에서 확인하세요")