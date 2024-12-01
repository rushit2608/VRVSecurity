from rest_framework import serializers
from .models import Users,Role,Permission
from rest_framework_simplejwt.tokens import RefreshToken 



class UserSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(read_only=True)
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
   
    class Meta:
        model=Users
        fields=['id','_id','username','email','name','isAdmin','role']
    
    def get_name(self,obj):
        firstname=obj.first_name
        lastname=obj.last_name
        name=firstname+' '+lastname
        if name=='':
            name=obj.email[:5]
            return name
        return name
    
    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


    
class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Users
        fields=['id','_id','username','email','name','isAdmin','token','role']
    
    def get_token(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)
    
    def get_role(self,obj):
        role = obj.role.name
        return str(role)