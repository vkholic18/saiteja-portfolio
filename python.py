from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
def home(request):
    return render(request,'home.html')

def editor(request):
    return render(request,'editor.html')


@api_view(["GET","POST"])
def display_roles_prvileges(request):
    try:
        roles=RoleMaster.objects.filter(status=StatusChoices.ACTIVE)
        print(roles)
        roles_data={}
        for each_role in roles:
            for each_privilege in each_role.get_privileges():
                print(each_privilege.id)

                
    except:
        print("errror")
    return Response({"msg":"success"})



from django.db import models

# Create your models here.
from django.db import models

# Assume StatusChoices is defined somewhere in your application
class StatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    # Add other status choices as needed

class PrivilegeMaster(models.Model):
    privilege_name = models.CharField(max_length=255)
    privilege_description = models.CharField(max_length=255)
    action_base = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "privilege_master"
    
    def __str__(self):
        return self.privilege_name

class RoleMaster(models.Model):
    role_name = models.CharField(max_length=255)
    role_description = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    created_by = models.CharField(max_length=255)  # You might want to link this to a User model instead
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    usertype = models.IntegerField()
    privileges = models.ManyToManyField(
        PrivilegeMaster, 
        through='RolePrivilege',
        related_name='role_privileges'
    )

    class Meta:
        db_table = "role_master"

    def get_privileges(self):
        return self.privileges.all()

    def __str__(self):
        return self.role_name

class RolePrivilege(models.Model):
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE, related_name="role_details")
    privilege = models.ForeignKey(PrivilegeMaster, on_delete=models.CASCADE, related_name="privilege_details")

    class Meta:
        unique_together = ('role', 'privilege')
        db_table = "role_privilege"

    def __str__(self):
        return f"{self.role.role_name} - {self.privilege.privilege_name}"

