from rest_framework.views import exception_handler

from django.http import Http404

from rest_framework import exceptions

from userauth.models import User


def custom_exception_handler(exc, context):
    request = context['request']

    response = exception_handler(exc, context)

    if isinstance(exc, exceptions.NotFound): 
        user    = User.objects.get(email__iexact = request.data['email'])  
        
        custom_response_data = { 
            'user_id': user.id
        }
        response.data = custom_response_data 

    
    if isinstance(exc, exceptions.PermissionDenied):  
        try:
            user    = User.objects.get(email__iexact = request.data['email'])   
            
            custom_response_data = { 
                'user_id': user.id, 
                'profile_id': user.profile.id 
            }
            response.data = custom_response_data 
        except:
            pass
            


    return response
