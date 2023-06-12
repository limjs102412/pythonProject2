import streamlit as st
import sqlite3
from daylist.dayinfo import Daylist


class DaylistDao:

    con=sqlite3.connect('mydb.db')
    cur=con.execute("""
    create table if not exists Daylist(
    DaylistIdx INTEGER PRIMARY KEY AUTOINCREMENT,
    Cat_Num char(20),
    Date date ,
    Weight Int default 0,
    Breakfast_Food Int default 0,
    Lunch_Food Int default 0,
    Dinner_Food Int default 0,
    Breakfast_Water Int default 0,
    Lunch_Water Int default 0,
    Dinner_Water Int default 0,
    Playtime Int default 0,
    Check1 Int default 0 ,
    Check2 Int default 0 ,
    Check3 Int default 0 ,
    Check4 Int default 0 ,
    Check5 Int default 0 ,
    Check6 Int default 0,
    Check7 Int default 0,
    Check8 Int default 0,
    Check9 Int default 0,
    Check10 Int default 0,
    memo char(200) default "",
    FOREIGN KEY('Cat_Num') REFERENCES 'Cat'('Cat_Num') ON DELETE CASCADE)
    """)




    # Daylist테이블에 입력받은 정보를 삽입하는 메서드
    def insert(self, a:Daylist):
        con=sqlite3.connect('mydb.db')
        cur=con.cursor()
        cur.execute(f'INSERT INTO Daylist(Cat_Num, Date, Weight, Breakfast_Food, Lunch_Food,Dinner_Food, Breakfast_Water, Lunch_Water,Dinner_Water, Playtime, Check1, Check2, Check3,Check4,Check5, Check6,Check7, Check8, Check9, Check10, memo) VALUES("{a.Cat_Num}","{a.Date}","{a.Weight}","{a.Breakfast_Food}","{a.Lunch_Food}","{a.Dinner_Food}","{a.Breakfast_Water}","{a.Lunch_Water}","{a.Dinner_Water}","{a.Playtime}","{a.Check1}","{a.Check2}","{a.Check3}","{a.Check4}","{a.Check5}","{a.Check6}","{a.Check7}","{a.Check8}","{a.Check9}","{a.Check10}","{a.memo}")')
        con.commit()
        cur.close()
        con.close()

    # Daylist테이블에 입력받은 Cat_Num, Date 에 해당하는 인스턴스를 검색하는 메서드
    def select(self, Cat_Num,Date):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'select * from Daylist where Cat_Num="{Cat_Num}" and Date="{Date}"')
            day_info = cur.fetchone()
            if day_info:
                return Daylist(day_info[1],day_info[2],day_info[3],day_info[4],day_info[5],day_info[6],day_info[7],day_info[8],day_info[9],day_info[10],day_info[11],day_info[12],day_info[13],day_info[14],day_info[15],day_info[16],day_info[17],day_info[18],day_info[19],day_info[20],day_info[21])
            else:
                return
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

    # Daylist테이블에 입력받은 Cat_Num, Date에 해당하는 인스턴스 삭제하는 메서드
    def delete(self, Cat_Num,Date):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'delete from Daylist where Cat_Num="{Cat_Num}" and Date="{Date}"')
            con.commit()
            return st.write('삭제가 완료되었습니다.')
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

    # Daylist 테이블에 입력받은 정보로 수정하는 메서드
    def update(self,a:Daylist):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        try:
            cur.execute(f'update Daylist set Weight="{a.Weight}", Breakfast_Food="{a.Breakfast_Food}", Lunch_Food="{a.Lunch_Food}", Dinner_Food="{a.Dinner_Food}", Breakfast_Water="{a.Breakfast_Water}", Lunch_Water="{a.Lunch_Water}",Dinner_Water="{a.Dinner_Water}", Playtime="{a.Playtime}", Check1="{a.Check1}", Check2="{a.Check2}", Check3="{a.Check3}",Check4="{a.Check4}",  Check5="{a.Check5}", Check6="{a.Check6}",Check7="{a.Check7}", Check8="{a.Check8}", Check9="{a.Check9}",Check10="{a.Check10}", memo="{a.memo}" Where Cat_Num="{a.Cat_Num}" and Date="{a.Date}"')
            con.commit()
            return st.write('수정 완료되었습니다.', icon="✅")
        except Exception as e:
            st.write(e)
        finally:
            cur.close()
            con.close()

    # Daylist테이블에 입력받은 Cat_Num에 해당하는 인스턴스중 입력받은 startday 이후의 인스턴스를 검색하는 메서드
    def selectbydate(self,startday,Cat_Num):
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        cur.execute(f'select * from Daylist where Date >  "{startday}" and Cat_Num={Cat_Num} ORDER BY Date DESC;')
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        cur.close()
        con.close()
        return rows,columns