
class Member:
    def __init__(self, User_Id=None, User_Pw=None, User_Name=None, User_Email=None, User_Phone=None):
        self.User_Id = User_Id
        self.User_Pw = User_Pw
        self.User_Name = User_Name
        self.User_Email = User_Email
        self.User_Phone = User_Phone



    # def __str__(self):
    #     return 'Id: '+self.User_Id+', Pw: '+self.User_Pw+', Name: '+self.User_Name+', Email: '+self.User_Email+', Phone: '+self.User_Phone