from django.db import models
from .staff import Staff

class User(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=500)
    ran = models.CharField(unique=True, max_length=50, default='')
    

    def register(self):
        self.save()
    
    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email = email)
        except:
            return False
        
    @staticmethod
    def get_user_by_ran(ran):
        try:
            return User.objects.get(ran = ran)
        except:
            return False






    