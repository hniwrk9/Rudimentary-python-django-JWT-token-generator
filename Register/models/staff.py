from django.db import models
from .role import Role

class Staff(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    active = models.BooleanField()
    csid = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Role, default=4, on_delete=models.SET_DEFAULT)


    def __str__(self):
        return self.csid

    @staticmethod
    def updateStatus(csid):
        Staff.objects.filter(csid = csid).update(active = 0)



    @staticmethod
    def get_staff_by_csid(csid):
        try:
            return Staff.objects.get(csid = csid)
        except:
            return False
    
    @staticmethod
    def get_staff_by_email(email):
        try:
            return Staff.objects.get(email = email)
        except:
            return False
        



