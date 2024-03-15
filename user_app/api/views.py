
from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status 


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.user.is_authenticated:
        # Only delete the auth_token if the user is authenticated
        request.user.auth_token.delete()

    # Your logout logic goes here (e.g., clearing session, etc.)

    return Response({'detail': 'Successfully logged out'})





@api_view(['POST'])
def registration_view(request):
    
    if request.method == 'POST':
        serializer =RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data ['response'] = "Registration successful"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account)
            
        
        else:
            data = serializer.errors
        
        return data
        