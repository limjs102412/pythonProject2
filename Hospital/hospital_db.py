import streamlit as st
import sqlite3
import pandas as pd
from Hospital.hospital import hospital

class HosptialDao:
    # Hospital 테이블 생성 : 한번만 실행
    con=sqlite3.connect('mydb.db')
    cur=con.execute("""
    create table if not exists Hospital(
    Hospital_Name char(20),
    Hospital_Address char(50) primary key,
    Opening_Hour char(50),
    Hospital_Phone char(20),
    Latitude float,
    Longitude float,
    Hospital_Si char(10),
    Hospital_Gu char(10)
    )
    """)

    # Hospital 테이블에 동물병원 csv 데이터 삽입
    # con = sqlite3.connect('mydb.db')
    # hospital = pd.read_csv("data/동물병원_크롤링.csv", encoding='cp949')
    # hospital.to_sql('Hospital',con, if_exists='append', index=False)
    # con.commit()
    # con.close()

    # Hospital 테이블에 전체의 unique한 si 검색하는 메서드
    def select_si(self):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        cur.execute(f'SELECT distinct Hospital_Si from Hospital Order By Hospital_Si asc')
        row = [item[0] for item in cur.fetchall()]
        con.commit()
        con.close()
        return row
    # Hospital 테이블에 입력받은 si에 해당하는 unique한 gu 검색하는 메서드
    def select_gu(self,si):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        cur.execute(f'SELECT distinct Hospital_Gu from Hospital Where Hospital_Si="{si}" Order By  Hospital_Gu asc')
        row = [item[0] for item in cur.fetchall()]
        con.commit()
        con.close()
        return row


    # Hospital 테이블에서 입력받은 si, gu에 해당하는 입력받은 컬럼의 평균을 검색하는 메서드
    # 위도,경도 평균을 찾을 때 사용
    def find_avg(self,col_name,si,gu):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        cur.execute(
            f'SELECT avg({col_name}) from Hospital where Hospital_Si="{si}" and Hospital_Gu="{gu}"'
        )
        result = cur.fetchone()[0]
        cur.close()
        return result

    # Hospital 테이블에서 입력받은 si,gu에 해당하는 인스턴스를 검색하는 메서드
    def allinfo(self,si,gu):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        cur.execute(f'select * from Hospital where Hospital_Si="{si}" and Hospital_Gu="{gu}"')
        row_data = cur.fetchall()
        return row_data


