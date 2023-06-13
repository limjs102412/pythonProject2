class Chart:
    def __init__(self,Cat_Num=None,Date=None,name=None,data=None,
                 Blepharitis=None,Blepharitis_percent=None,Deep_keratitis=None,
                 Deep_keratitis_percent=None,Conjunctivitis=None,
                 Conjunctivitis_percent=None,Conael_sequestrum=None,
                 Conael_sequestrum_percent=None,Corneal_ulcer=None,
                 Corneal_ulcer_percent=None,grad_Blepharitis=None,
                 grad_Deep_keratitis=None,grad_Conjunctivitis=None,
                 grad_Conael_sequestrum=None, grad_Corneal_ulcer=None):
        self.Cat_Num = Cat_Num
        self.Date = Date
        self.name=name
        self.data = data
        self.Blepharitis = Blepharitis
        self.Blepharitis_percent = Blepharitis_percent
        self.Deep_keratitis = Deep_keratitis
        self.Deep_keratitis_percent = Deep_keratitis_percent
        self.Conjunctivitis = Conjunctivitis
        self.Conjunctivitis_percent = Conjunctivitis_percent
        self.Conael_sequestrum = Conael_sequestrum
        self.Conael_sequestrum_percent = Conael_sequestrum_percent
        self.Corneal_ulcer = Corneal_ulcer
        self.Corneal_ulcer_percent = Corneal_ulcer_percent
        self.grad_Blepharitis=grad_Blepharitis
        self.grad_Deep_keratitis=grad_Deep_keratitis
        self.grad_Conjunctivitis=grad_Conjunctivitis
        self.grad_Conael_sequestrum=grad_Conael_sequestrum
        self.grad_Corneal_ulcer=grad_Corneal_ulcer