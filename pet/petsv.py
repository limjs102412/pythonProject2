from pet.cat import Pet
from pet.pet_db import PetDao
from member.service import MemberService
import streamlit as st

class PetService:
    loginCatName=''
    def __init__(self):
        self.dao=PetDao()
        self.service = MemberService()

    # 입력받은 정보를 db에 추가하는 기능
    def addCat(self,User_Id,Cat_Name,Cat_Age,Cat_Num,Cat_Kind,Cat_Gender,Cat_State,Cat_Eatkcal):
        a=Pet(User_Id=User_Id,Cat_Name=Cat_Name,Cat_Age=Cat_Age,Cat_Num=Cat_Num,Cat_Kind=Cat_Kind,Cat_Gender=Cat_Gender,Cat_State=Cat_State,Cat_Eatkcal=Cat_Eatkcal)
        self.dao.insert(a)

    # 입력받은 User_Id,Cat_Name에 해당하는 정보를 리턴하는 기능
    def printCatInfo(self,User_Id,Cat_Name):
        if Cat_Name :
            a = self.dao.cat_selectbyname(User_Id, Cat_Name)

            return [a.User_Id, a.Cat_Name, a.Cat_Age, a.Cat_Num, a.Cat_Kind, a.Cat_Gender, a.Cat_State,a.Cat_Eatkcal]
        else:
            return

    # 입력받은 User_Id, Cat_Name에 해당하는 정보를 삭제하는 기능
    def delete_Cat(self,User_Id,cat_name):
        if MemberService.loginId !='':
            self.dao.delete(User_Id=User_Id, cat_name=cat_name)
            MemberService.loginId = ''
            return

    # 로그인 중인 사용자가 반려묘를 선택하는 기능
    def printMyCat(self,print1=True,print2=True):
        if MemberService.loginId=='':
            if print1:
                st.error('로그인 먼저 하세요',icon="🚨")
                return
            else:
                return
        else:
            if print2:
                row=self.dao.findmycat(MemberService.loginId)
                option = st.selectbox("반려묘 선택", row)
                if option is None:
                    st.write('등록된 고양이가 없습니다')
                else:
                    PetService.loginCatName=option
                    return option
            else:
                return

    # 입력받은 정보로 수정하는 기능
    def UpdateCat(self,User_Id, Cat_Num, input_catage, input_catname, input_catkind, input_catgender,input_catstate,input_cateatkcal):
        self.dao.update(Pet(User_Id=User_Id, Cat_Name=input_catname, Cat_Age=input_catage, Cat_Num=Cat_Num, Cat_Kind=input_catkind, Cat_Gender=input_catgender,Cat_State=input_catstate,Cat_Eatkcal=input_cateatkcal))



