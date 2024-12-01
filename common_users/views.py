from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializer import UserSerializerWithToken
from .models import Users,Role
from rest_framework.permissions import AllowAny

from rest_framework.response import Response 
from rest_framework.decorators import api_view,permission_classes   
from rest_framework import status

from .roledecorator import role_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("validating token")
        data = super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        print("validating token")
        for k,v in serializer.items():
            data[k]=v       
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    print("validating token")
    serializer_class=MyTokenObtainPairSerializer

    
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    
    try:
        name = request.data.get('username') 
        email = request.data.get('email')
        password = request.data.get('password')
        role_name = request.data.get('role', 'User')

        print("sssss", name, email, password, role_name)

        try:
            user = Users.objects.create_user(name=name, email=email, password=password)

            role_instance,_ = Role.objects.get_or_create(name=role_name)
            user.role = role_instance
            user.save()

            return Response({"message": "User created successfully"}, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            print("Role not found")
            return Response({"error": f"Role '{role_name}' not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"error": "Invalid request method"}, status=status.HTTP_401_UNAUTHORIZED)
    




@login_required
@role_required(['Admin'])
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@role_required(['Moderator'])
def moderator_dashboard(request):
    return render(request, 'moderator_dashboard.html')

@login_required
@role_required(['User', 'Admin'])
def user_dashboard(request):
    return render(request, 'user_dashboard.html')
