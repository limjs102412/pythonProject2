import streamlit as st
import sqlite3
from pet.cat import Pet


class PetDao:
    # Cat 테이블 생성 : 한번만 실행
    con=sqlite3.connect('mydb.db')
    cur=con.execute("""
    create table if not exists Cat(
    User_Id char(15),
    Cat_Name char(45),
    Cat_Age int,
    Cat_Num char(20) primary key,
    Cat_Kind char(20),
    Cat_Gender char(5),
    Cat_State char(20),
    Cat_Eatkcal int,
    FOREIGN KEY('User_Id') REFERENCES 'User'('User_Id') ON DELETE CASCADE)
    """)

    # Cat테이블에서 입력받은 정보를 삽입하는 메서드
    def insert(self, a:Pet):
        con=sqlite3.connect('mydb.db')
        cur=con.cursor()
        cur.execute(f'INSERT INTO Cat (User_Id,Cat_Name,Cat_Age,Cat_Num,Cat_Kind,Cat_Gender,Cat_State,Cat_Eatkcal) VALUES("{a.User_Id}","{a.Cat_Name}","{a.Cat_Age}","{a.Cat_Num}","{a.Cat_Kind}","{a.Cat_Gender}","{a.Cat_State}","{a.Cat_Eatkcal}")')
        con.commit()
        cur.close()
        con.close()

    # Cat테이블에서 입력받은 User_Id, Cat_Name 해당하는 인스턴스를 검색하는 메서드
    def cat_selectbyname(self, User_Id, Cat_Name):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'select * from Cat where User_Id="{User_Id}" and Cat_Name="{Cat_Name}"')
            cat_info = cur.fetchone()
            if cat_info:
                return Pet(cat_info[0],cat_info[1],cat_info[2],cat_info[3],cat_info[4],cat_info[5],cat_info[6],cat_info[7])
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

    # Cat테이블에서 입력받은 User_Id, Cat_Num에 해당하는 인스턴스를 검색하는 메서드
    def cat_selectbynum(self, User_Id,Cat_Num):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'select * from Cat where User_Id="{User_Id}" and Cat_Num="{Cat_Num}"')
            cat_info = cur.fetchone()
            if cat_info:
                return Pet(cat_info[0],cat_info[1],cat_info[2],cat_info[3],cat_info[4],cat_info[5],cat_info[6],cat_info[7])
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

    # Cat테이블에서 입력받은 User_Id에 해당하는 인스턴스의 Cat_Name을 검색하는 메서드
    def findmycat(self,User_Id):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'select Cat_Name from Cat where User_Id="{User_Id}"')
            row = [item[0] for item in cur.fetchall()]
            con.commit()
            return row
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

    # Cat테이블에서 입력받은 User_Id, Cat_name에 해당하는 인스턴스를 삭제하는 메서드
    def delete(self, User_Id:str, cat_name:str):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'delete from Cat where User_Id="{User_Id}" and Cat_Name="{cat_name}"')
            con.commit()
            return st.write('삭제가 완료되었습니다.', icon="✅")
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

     # Cat테이블에서 입력받은 정보로 수정하는 메서드
    def update(self,a:Pet):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'update Cat set Cat_Name="{a.Cat_Name}", Cat_Age="{a.Cat_Age}", Cat_Kind="{a.Cat_Kind}",Cat_Gender="{a.Cat_Gender}",Cat_State="{a.Cat_State}",Cat_Eatkcal="{a.Cat_Eatkcal}" Where User_Id="{a.User_Id}" and Cat_Num="{a.Cat_Num}"')
            con.commit()
            return st.write('수정 완료되었습니다.', icon="✅")
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

